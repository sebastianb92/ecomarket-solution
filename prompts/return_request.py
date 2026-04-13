"""
return_request.py — Módulo de solicitud de devolución de producto

Implementa el prompt de devolución con capacidad de distinguir entre
productos devolvibles y no devolvibles, con respuestas empáticas en ambos casos.

DESAFÍO CLAVE: El modelo debe:
  - Identificar si el producto entra en una categoría prohibida
  - Verificar el plazo de 30 días
  - Detectar casos de excepción (daño en tránsito, primera devolución)
  - Comunicar tanto el "sí" como el "no" con empatía genuina
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fase3_prompts.config import load_return_policy
    from fase3_prompts.prompts.system_prompts import RETURN_SYSTEM_PROMPT
    from fase3_prompts.prompts.llm_client import LLMClient
except ImportError:
    from config import load_return_policy
    from prompts.system_prompts import RETURN_SYSTEM_PROMPT
    from prompts.llm_client import LLMClient


def build_return_user_prompt(
    product_name: str,
    reason: str,
    days_since_delivery: int,
    product_was_opened: bool = False,
    is_first_return: bool = False
) -> str:
    """
    Construye el prompt del usuario para una solicitud de devolución.

    TÉCNICAS DE PROMPT ENGINEERING APLICADAS:
    - Contexto de política inyectado (RAG simulado)
    - Variables de entrada claramente etiquetadas
    - Árbol de decisión explícito en el prompt
    - Instrucción de priorizar empatía antes que la negativa
    - Casos de excepción documentados
    - Restricción de no cerrar sin alternativa

    Args:
        product_name: Nombre del producto que el cliente quiere devolver.
        reason: Motivo de la devolución expresado por el cliente.
        days_since_delivery: Días transcurridos desde la entrega.
        product_was_opened: Si el producto ya fue abierto/usado.
        is_first_return: Si es la primera devolución del cliente.

    Returns:
        Prompt completo listo para enviar al LLM.
    """
    try:
        policy_context = load_return_policy()
    except FileNotFoundError:
        policy_context = "Política de devoluciones no disponible."

    opened_text = "Sí" if product_was_opened else "No especificado"
    first_return_text = "Sí (cliente nuevo o primera devolución)" if is_first_return else "No"

    return f"""--- POLÍTICA DE DEVOLUCIONES DE ECOMARKET (CONTEXTO RAG) ---
{policy_context}
--- FIN DE LA POLÍTICA ---

SOLICITUD DE DEVOLUCIÓN DEL CLIENTE:
  Producto: {product_name}
  Motivo indicado por el cliente: {reason}
  Días desde la entrega: {days_since_delivery} días
  ¿Producto abierto o usado?: {opened_text}
  ¿Es primera devolución del cliente?: {first_return_text}

ÁRBOL DE DECISIÓN — sigue estos pasos EN ORDEN:

PASO 1 — Verificar caso de excepción UNIVERSAL:
  ¿El motivo menciona daño durante el envío, defecto de fabricación o producto incorrecto?
  → Si SÍ: SIEMPRE aprueba la devolución (excepción universal, sin importar el tipo de producto).
     Ofrece reembolso completo O reenvío + menciona que EcoMarket cubre el envío de devolución.
  → Si NO: continúa al Paso 2.

PASO 2 — Verificar categoría del producto:
  ¿El producto es un alimento, bebida, planta, semilla, suplemento o similar perecedero?
  → Si SÍ: devolución NO posible por razones sanitarias. Ve al Paso 5 (negativa empática).

  ¿El producto es de higiene personal (jabón, champú, cepillo de dientes, cosmética, etc.)?
  → Si el embalaje fue ABIERTO: devolución NO posible. Ve al Paso 5.
  → Si el embalaje NO fue abierto: puede continuar. Ve al Paso 3.

  ¿El producto es personalizado o contenido digital?
  → Si SÍ: devolución NO posible. Ve al Paso 5.

  → Si ninguna de las anteriores aplica: el producto SÍ puede devolverse. Ve al Paso 3.

PASO 3 — Verificar plazo:
  ¿Han pasado más de 30 días desde la entrega?
  → Si SÍ: normalmente fuera de plazo.
     EXCEPCIÓN: ¿Es primera devolución del cliente o es cliente Premium?
       → Si es primera devolución: puede haber excepción hasta 45 días. Escala a agente humano.
       → Si no: devolución NO posible por plazo. Ve al Paso 5 con mención de escalar a humano.
  → Si NO (dentro de los 30 días): la devolución ES posible. Ve al Paso 4.

PASO 4 — RESPUESTA AFIRMATIVA (devolución aprobada):
  ✓ Confirma positivamente que la devolución ES posible
  ✓ Explica el proceso en 3 pasos numerados (ecomarket.com/devoluciones → etiqueta → envío)
  ✓ Menciona el plazo de reembolso (5-7 días hábiles)
  ✓ Ofrece la opción de crédito de tienda (+5% de bonificación)
  ✓ Si aplica: menciona que EcoMarket cubre el envío de devolución

PASO 5 — RESPUESTA DE NEGATIVA EMPÁTICA (devolución no aprobada):
  ① PRIMERO: Reconoce y valida la situación del cliente con empatía genuina.
     Ejemplo: "Entiendo perfectamente lo frustrante que puede ser esta situación..."
  ② SEGUNDO: Explica la razón de forma simple, sin sonar como un párrafo legal.
     Hazlo humano: "La razón es que productos como [X] no podemos reaceptarlos por..."
  ③ TERCERO: Ofrece SIEMPRE al menos UNA alternativa:
     - ¿Puede escalarse a un agente humano para revisión de excepción?
     - ¿Hay descuento o cupón de compensación disponible?
     - ¿Algún consejo útil para el producto (si aplica)?
  ④ NUNCA termines con un "no" definitivo y frío. Siempre hay algo más que ofrecer.

TONO: Cálido, humano, orientado a soluciones. Nunca defensivo ni corporativo."""


def request_return(
    product_name: str,
    reason: str,
    days_since_delivery: int,
    product_was_opened: bool = False,
    is_first_return: bool = False
) -> str:
    """
    Procesa una solicitud de devolución usando el LLM.

    Args:
        product_name: Nombre del producto a devolver.
        reason: Motivo de la devolución.
        days_since_delivery: Días desde la entrega.
        product_was_opened: Si fue abierto.
        is_first_return: Si es primera devolución.

    Returns:
        Respuesta generada por EcoBot.
    """
    user_prompt = build_return_user_prompt(
        product_name, reason, days_since_delivery,
        product_was_opened, is_first_return
    )

    client = LLMClient()
    response = client.chat(RETURN_SYSTEM_PROMPT, user_prompt)

    return response


if __name__ == "__main__":
    # Ejemplos de uso directo
    test_cases = [
        {
            "product_name": "Botella de acero inoxidable 750ml",
            "reason": "No me gusta el color, quiero cambiarlo",
            "days_since_delivery": 15,
            "product_was_opened": False,
            "label": "Devolución POSIBLE (producto de hogar, dentro de plazo)"
        },
        {
            "product_name": "Jabón orgánico artesanal",
            "reason": "No me gusta el olor",
            "days_since_delivery": 5,
            "product_was_opened": True,
            "label": "Devolución NO POSIBLE (higiene abierto)"
        },
        {
            "product_name": "Kit de bambú reutilizable",
            "reason": "El producto llegó roto, el embalaje estaba aplastado",
            "days_since_delivery": 3,
            "product_was_opened": True,
            "label": "Devolución POSIBLE (daño en tránsito — excepción universal)"
        },
        {
            "product_name": "Set de cubiertos de bambú",
            "reason": "Cambié de opinión",
            "days_since_delivery": 45,
            "product_was_opened": False,
            "label": "Devolución LÍMITE (fuera de plazo 30 días)"
        },
    ]

    for case in test_cases:
        print(f"\n{'='*65}")
        print(f"CASO: {case['label']}")
        print('='*65)
        response = request_return(
            product_name=case["product_name"],
            reason=case["reason"],
            days_since_delivery=case["days_since_delivery"],
            product_was_opened=case.get("product_was_opened", False),
            is_first_return=case.get("is_first_return", False)
        )
        print(response)
