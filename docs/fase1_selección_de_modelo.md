# Fase 1 — Selección y Justificación del Modelo de IA

## Contexto del problema

**EcoMarket** recibe miles de consultas diarias a través de chat, correo y redes sociales:
- **80%** son repetitivas: estado de pedido, devoluciones, características de producto.
- **20%** son complejas: quejas, problemas técnicos, solicitudes con empatía.
- Tiempo de respuesta actual: **24 horas** → Objetivo: **< 2 minutos** para el 80%.

---

## Análisis comparativo de opciones

| Opción | Descripción | Ventajas | Desventajas |
|--------|-------------|----------|-------------|
| **LLM de propósito general** (GPT-4o, Claude 3) | API externa, sin ajuste | Alta fluidez, fácil integración | Costo por token, datos salen de la empresa |
| **LLM afinado** (Fine-tuned) | Modelo base + datos propios | Precisión máxima en dominio | Costo alto de entrenamiento, mantenimiento |
| **SLM open-source** (Mistral 7B, LLaMA 3) | Modelo pequeño local | Sin costo de API, privacidad total | Menor razonamiento complejo |
| **RAG + LLM (seleccionado)** | **LLM + recuperación en tiempo real de BD** | **Precisión + fluidez + privacidad + escalable** | **Complejidad de implementación inicial** |

---

## Modelo seleccionado: Arquitectura Híbrida RAG + LLM

### Justificación

Un LLM sin contexto de datos reales tiene un problema crítico para EcoMarket: **las alucinaciones**. Si un cliente pregunta por el estado del pedido #ECO-12346, el modelo no tiene forma de saber la respuesta y podría inventarla. El módulo RAG resuelve esto al recuperar primero la información real de la base de datos y luego inyectarla en el prompt, garantizando que el modelo solo responda con datos verificados.

### ¿Por qué no un modelo fine-tuned?

El fine-tuning es un proceso computacionalmente costoso y requiere mantenimiento continuo cada vez que cambian los datos (nuevos productos, políticas actualizadas). Con RAG, los datos se actualizan en tiempo real sin necesidad de re-entrenar el modelo.

### ¿Por qué un modelo open-source y no GPT-4o?

- **Privacidad**: Los datos sensibles de los clientes (pedidos, direcciones) nunca salen del entorno de EcoMarket.
- **Costo**: Modelos como LLaMA 3.1 8B o Mistral 7B son 60–80% más baratos a escala.
- **Control**: EcoMarket controla las versiones, actualizaciones y el comportamiento del modelo.

---

## Arquitectura propuesta (dos niveles)

### Nivel 1 — Chatbot automatizado (80% de consultas)

**Componentes:**
1. **Clasificador de intención**: Determina si la consulta es sobre pedido, devolución, producto, etc.
2. **Módulo RAG**: Recupera el contexto relevante (datos del pedido, política de devolución) de la BD interna.
3. **LLM** (llama-3.3-70b-versatile): Genera la respuesta con el contexto inyectado.
4. **Capa de validación**: Verifica que los datos mencionados en la respuesta coincidan con los de la BD.

### Nivel 2 — Asistente de agente humano (20% de casos complejos)

**El sistema NO reemplaza al agente, lo empodera:**
1. Analiza la conversación y genera un resumen del problema.
2. Extrae el historial relevante del cliente.
3. Sugiere respuestas con tono empático según las políticas de la empresa.
4. El agente revisa, ajusta y envía → Tiempo de respuesta: de 24h a < 2h.

---

## Justificación multifactor

| Criterio | Evaluación | Puntuación |
|----------|-----------|-----------|
| **Costo** | Open-source elimina costo por token; infraestructura cloud predecible | ★★★★☆ 4/5 |
| **Escalabilidad** | Instancias horizontales según demanda, sin límites de terceros | ★★★★★ 5/5 |
| **Facilidad de integración** | APIs REST con CRM/helpdesk existentes (Zendesk, Freshdesk) | ★★★★☆ 4/5 |
| **Calidad de respuesta** | RAG garantiza precisión factual; LLM aporta fluidez y empatía | ★★★★★ 5/5 |
| **Privacidad de datos** | Datos nunca salen del entorno de EcoMarket | ★★★★★ 5/5 |
| **Precisión factual** | RAG elimina alucinaciones sobre datos críticos del negocio | ★★★★★ 5/5 |
