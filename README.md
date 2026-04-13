# 🌿 EcoMarket AI Support — Taller Práctico #1

Sistema de atención al cliente basado en **IA Generativa** para EcoMarket, una empresa de e-commerce sostenible.

## 📋 Descripción

Este repositorio implementa la solución propuesta en el Taller Práctico #1, demostrando cómo la ingeniería de prompts puede transformar la atención al cliente automatizando el 80% de consultas repetitivas mediante un modelo LLM open-source con contexto RAG simulado.

**Modelo utilizado:** `llama3-8b-8192` via [Groq API](https://groq.com) (gratuita)  
**Alternativa local:** Ollama con `mistral:7b-instruct` (sin internet)

---

## 🗂️ Estructura del Repositorio

```
ecomarket-ai-support/
├── README.md
├── requirements.txt
├── .env.example
│
├── fase1_modelo/
│   └── justificacion.md          # Justificación del modelo de IA seleccionado
│
├── fase2_evaluacion/
│   └── riesgos_fortalezas.md     # Fortalezas, limitaciones y riesgos éticos
│
├── fase3_prompts/
│   ├── config.py                 # Configuración centralizada
│   ├── data/
│   │   ├── orders_database.txt   # Base de datos de 10 pedidos de prueba
│   │   └── return_policy.txt     # Política de devoluciones de EcoMarket
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── system_prompts.py     # System prompts del agente EcoBot
│   │   ├── order_status.py       # Lógica y prompt de estado de pedido
│   │   └── return_request.py     # Lógica y prompt de devoluciones
│   └── main.py                   # Script principal de demostración
│
└── tests/
    ├── test_order_prompt.py      # Casos de prueba para pedidos
    └── test_return_prompt.py     # Casos de prueba para devoluciones
```

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/ecomarket-ai-support.git
cd ecomarket-ai-support
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` y agrega tu API key de Groq:

```
GROQ_API_KEY=gsk_tu_api_key_aqui
```

> 💡 **Obtener API Key gratuita de Groq:** Ve a [console.groq.com](https://console.groq.com), crea una cuenta gratuita y genera una API key. No requiere tarjeta de crédito.

---

## 🚀 Uso

### Demo interactiva (menú)

```bash
python fase3_prompts/main.py
```

### Consultar estado de un pedido

```bash
python fase3_prompts/main.py --mode order --tracking ECO-12345
python fase3_prompts/main.py --mode order --tracking ECO-12346   # Pedido retrasado
python fase3_prompts/main.py --mode order --tracking ECO-99999   # Pedido no encontrado
```

### Solicitar devolución de producto

```bash
# Devolución posible
python fase3_prompts/main.py --mode return --product "botella de acero inoxidable" --reason "llegó con golpe" --days 10

# Devolución NO posible (higiene)
python fase3_prompts/main.py --mode return --product "jabón orgánico abierto" --reason "no me gustó el olor" --days 5

# Devolución fuera de plazo
python fase3_prompts/main.py --mode return --product "set de cubiertos de bambú" --reason "cambié de opinión" --days 45
```

### Ejecutar todos los casos de prueba

```bash
python -m pytest tests/ -v
# O sin pytest:
python tests/test_order_prompt.py
python tests/test_return_prompt.py
```

---

## 🔄 Alternativa: Uso con Ollama (sin API key, 100% local)

```bash
# 1. Instalar Ollama desde https://ollama.com
# 2. Descargar el modelo
ollama pull mistral:7b-instruct

# 3. Cambiar en .env:
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral:7b-instruct
```

---

## 📊 Casos de prueba incluidos

| # | Escenario | Tipo | Resultado esperado |
|---|-----------|------|--------------------|
| 1 | Pedido ECO-12345 en tránsito | Estado | Info de entrega + tracking |
| 2 | Pedido ECO-12346 retrasado | Estado | Disculpa + nueva fecha |
| 3 | Pedido ECO-12347 entregado | Estado | Confirmación de entrega |
| 4 | Pedido ECO-12349 cancelado | Estado | Info del reembolso |
| 5 | Número de pedido inexistente | Estado | Redirección a soporte |
| 6 | Devolución de producto de hogar (OK) | Devolución | Instrucciones del proceso |
| 7 | Devolución de jabón abierto (NO) | Devolución | Negativa empática + alternativas |
| 8 | Devolución fuera de plazo 30 días | Devolución | Negativa + escalado a humano |
| 9 | Devolución por daño en envío | Devolución | Aprobación + compensación |
| 10 | Producto perecedero (alimento) | Devolución | Negativa empática + política |

---

## 🏗️ Arquitectura de la solución

```
Consulta del cliente
        │
        ▼
┌───────────────────┐
│  Clasificador     │ ──► simple (80%) ──► RAG + LLM ──► Respuesta automática
│  de intención     │
└───────────────────┘ ──► compleja (20%) ──► Asistente de agente humano
```

En este prototipo, el **RAG está simulado** mediante la carga directa de los archivos de texto en `fase3_prompts/data/`. En producción, estos datos serían recuperados dinámicamente desde las APIs de EcoMarket.

---

## 📚 Fases del taller

- [Fase 1 — Justificación del modelo](fase1_modelo/justificacion.md)
- [Fase 2 — Fortalezas, limitaciones y riesgos éticos](fase2_evaluacion/riesgos_fortalezas.md)
- Fase 3 — Ingeniería de prompts (este directorio)
