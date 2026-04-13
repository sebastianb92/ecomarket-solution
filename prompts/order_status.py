"""
order_status.py — Módulo de consulta de estado de pedido

Implementa el prompt de estado de pedido con contexto RAG simulado.
El módulo RAG está simulado cargando el archivo orders_database.txt,
que en producción sería reemplazado por una consulta a la BD real de EcoMarket.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fase3_prompts.config import load_orders_db
    from fase3_prompts.prompts.system_prompts import ORDER_SYSTEM_PROMPT
    from fase3_prompts.prompts.llm_client import LLMClient
except ImportError:
    from config import load_orders_db
    from prompts.system_prompts import ORDER_SYSTEM_PROMPT
    from prompts.llm_client import LLMClient


def build_order_user_prompt(tracking_number: str, orders_context: str) -> str:
    """
    Construye el prompt del usuario para una consulta de estado de pedido.

    El contexto de pedidos (orders_context) simula lo que el módulo RAG
    recuperaría dinámicamente de la base de datos de EcoMarket.

    TÉCNICAS DE PROMPT ENGINEERING APLICADAS:
    - Separación clara de contexto vs. instrucción con delimitadores ---
    - Rol del modelo ya definido en el system prompt
    - Instrucciones paso a paso numeradas
    - Manejo explícito de casos extremos (pedido no encontrado)
    - Formato de salida especificado
    - Restricción explícita de no inventar información

    Args:
        tracking_number: Número de seguimiento consultado por el cliente.
        orders_context: Texto con los datos de pedidos (simulación de RAG).

    Returns:
        Prompt completo listo para enviar al LLM.
    """
    return f"""--- BASE DE DATOS DE PEDIDOS (CONTEXTO RAG — usa ÚNICAMENTE esta información) ---
{orders_context}
--- FIN DEL CONTEXTO ---

CONSULTA DEL CLIENTE:
El cliente pregunta por el estado de su pedido con número de seguimiento: {tracking_number}

INSTRUCCIONES PARA TU RESPUESTA:

PASO 1 — Verificar existencia del pedido:
  Busca el número "{tracking_number}" en el contexto anterior.
  Considera variaciones: con y sin guión, en mayúsculas y minúsculas.

PASO 2a — Si el pedido EXISTE en el contexto:
  Proporciona al cliente:
  ✓ Estado actual del pedido con descripción clara y amigable
  ✓ Fecha estimada de entrega (o confirmación si ya fue entregado)
  ✓ Enlace de seguimiento (tracking_url) si está disponible
  ✓ Si está RETRASADO: disculpa sincera primero, luego nueva fecha y razón
  ✓ Si está CANCELADO: estado del reembolso y plazos
  ✓ Si está PENDIENTE DE PAGO: urgencia amable + enlace de pago
  ✓ Próximo paso que el cliente debe esperar

PASO 2b — Si el pedido NO APARECE en el contexto:
  ✓ Informa amablemente que no puedes encontrar ese número de pedido
  ✓ Sugiere verificar el número (a veces hay errores tipográficos)
  ✓ Proporciona alternativas: soporte@ecomarket.com o 900-ECO-MKT
  ✗ NUNCA inventes información sobre un pedido que no aparece

FORMATO DE RESPUESTA:
  - Saludo personalizado (usa el nombre del cliente si aparece en el contexto)
  - Información clara y estructurada
  - Cierre ofreciendo ayuda adicional
  - Tono: cálido y profesional, no robótico"""


def query_order_status(tracking_number: str) -> str:
    """
    Consulta el estado de un pedido usando el LLM con contexto RAG simulado.

    Args:
        tracking_number: Número de seguimiento del pedido.

    Returns:
        Respuesta generada por EcoBot.
    """
    # 1. Cargar contexto RAG (simulado desde archivo)
    try:
        orders_context = load_orders_db()
    except FileNotFoundError as e:
        return f"❌ Error al cargar la base de datos de pedidos: {e}"

    # 2. Construir el prompt de usuario con el contexto inyectado
    user_prompt = build_order_user_prompt(tracking_number, orders_context)

    # 3. Llamar al LLM
    client = LLMClient()
    response = client.chat(ORDER_SYSTEM_PROMPT, user_prompt)

    return response


if __name__ == "__main__":
    # Ejemplo de uso directo
    test_numbers = ["ECO-12345", "ECO-12346", "ECO-99999"]
    for number in test_numbers:
        print(f"\n{'='*60}")
        print(f"Consultando pedido: {number}")
        print('='*60)
        print(query_order_status(number))
