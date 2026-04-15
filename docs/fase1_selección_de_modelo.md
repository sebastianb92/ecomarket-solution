# Fase 1: Selección y Justificación del Modelo de IA

## 1. Contexto del Problema

**EcoMarket** es una empresa de e-commerce especializada en productos sostenibles que experimenta un crecimiento acelerado. Su departamento de soporte enfrenta un cuello de botella crítico:

| Métrica | Valor actual |
|---|---|
| Consultas diarias | Miles (multi-canal: chat, email, RRSS) |
| Consultas repetitivas | **80%** (estado de pedido, devoluciones, características de producto) |
| Consultas complejas | **20%** (quejas, problemas técnicos, sugerencias) |
| Tiempo de respuesta promedio | **24 horas** |
| Impacto | Deterioro de la satisfacción del cliente |

El desafío es doble: **(a)** responder con precisión factual a consultas sobre pedidos y productos (datos que cambian en tiempo real), y **(b)** mantener un tono empático y fluido en la comunicación con el cliente.

---

## 2. Modelo Seleccionado: Arquitectura Híbrida RAG con LLM

### 2.1 ¿Qué es RAG (Retrieval-Augmented Generation)?

RAG es un patrón arquitectónico que combina un modelo de lenguaje grande (LLM) con un sistema de recuperación de información. En lugar de depender exclusivamente del conocimiento almacenado en los pesos del modelo durante su entrenamiento, RAG **recupera información relevante de fuentes externas** (bases de datos, documentos) y la inyecta como contexto en el prompt antes de generar la respuesta.

### 2.2 Modelo Base Recomendado

Se propone utilizar **Llama 3.3 70B (llama-3.3-70b-versatile) vía Groq API** como LLM base en esta implementación, combinado con una capa de RAG que se conecta a las bases de datos de EcoMarket.

**¿Por qué un LLM de propósito general y no un modelo pequeño afinado (fine-tuned)?**

| Criterio | LLM + RAG | Fine-tuned SLM | Chatbot de reglas |
|---|---|---|---|
| Precisión con datos en tiempo real | ✅ Alta (consulta BD en cada petición) | ❌ Baja (datos congelados al momento del entrenamiento) | ✅ Alta (consulta BD directa) |
| Fluidez y naturalidad | ✅ Alta | ✅ Media-Alta | ❌ Baja (respuestas rígidas) |
| Capacidad de manejar consultas inesperadas | ✅ Alta | ⚠️ Limitada al dominio de entrenamiento | ❌ Nula |
| Costo de mantenimiento | ⚠️ Medio (API + infra de recuperación) | ❌ Alto (re-entrenamiento frecuente) | ✅ Bajo |
| Tiempo de implementación | ✅ Semanas | ❌ Meses | ✅ Semanas |
| Escalabilidad | ✅ Alta (horizontal via API) | ⚠️ Media | ⚠️ Media |
| Multilingüe | ✅ Nativo | ⚠️ Requiere datos en cada idioma | ❌ Requiere traducción manual |

**Conclusión:** El 80% de las consultas de EcoMarket requieren datos que cambian en tiempo real (estado de pedidos, inventario, fechas de envío). Un modelo fine-tuned tendría sus datos "congelados" y necesitaría re-entrenamiento constante. RAG resuelve este problema recuperando la información actualizada en cada consulta.

### 2.3 ¿Por qué no solo fine-tuning?

El fine-tuning es valioso cuando se necesita adaptar el *estilo* o *dominio* del modelo, pero presenta limitaciones críticas para el caso de EcoMarket:

1. **Datos dinámicos:** Los estados de pedidos, inventario y precios cambian constantemente. Un modelo fine-tuned no puede acceder a esta información actualizada sin re-entrenamiento.
2. **Costo de re-entrenamiento:** Cada actualización del catálogo o cambio en las políticas requeriría un nuevo ciclo de fine-tuning, lo cual es costoso tanto en tiempo como en recursos computacionales.
3. **Riesgo de alucinaciones:** Sin acceso a datos reales, un modelo fine-tuned podría inventar estados de pedidos o características de productos basándose en patrones estadísticos del entrenamiento.

**Sin embargo**, se recomienda un **enfoque híbrido**: utilizar fine-tuning *ligero* (ej: LoRA) para adaptar el tono y estilo de comunicación de EcoMarket al modelo base, y RAG para toda la información factual que cambia en tiempo real.

---

## 3. Arquitectura Propuesta

### 3.1 Diagrama de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CANALES DE ENTRADA                          │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│    │   Chat   │    │  Email   │    │   RRSS   │    │ WhatsApp │   │
│    └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘   │
│         └───────────────┼───────────────┼───────────────┘         │
│                         ▼                                         │
│              ┌─────────────────────┐                              │
│              │    API Gateway      │                              │
│              │  (Unifica canales)  │                              │
│              └─────────┬───────────┘                              │
│                        ▼                                          │
│         ┌──────────────────────────────┐                          │
│         │   CLASIFICADOR DE INTENCIÓN  │                          │
│         │   (¿Qué tipo de consulta?)   │                          │
│         └──────┬───────────────┬───────┘                          │
│                ▼               ▼                                  │
│    ┌───────────────┐  ┌────────────────┐                          │
│    │  80% Consultas│  │ 20% Consultas  │                          │
│    │  Repetitivas  │  │   Complejas    │                          │
│    └───────┬───────┘  └───────┬────────┘                          │
│            ▼                  ▼                                   │
│  ┌──────────────────┐  ┌──────────────┐                           │
│  │   Motor RAG      │  │   Agente     │                           │
│  │ ┌──────────────┐ │  │   Humano     │                           │
│  │ │ Recuperador   │ │  │ (con asist.  │                           │
│  │ │ de contexto   │ │  │  de IA)      │                           │
│  │ └──────┬───────┘ │  └──────────────┘                           │
│  │        ▼         │                                             │
│  │ ┌──────────────┐ │                                             │
│  │ │   LLM Base   │ │                                             │
│  │ │ (Llama 3.3)  │ │                                             │
│  │ └──────┬───────┘ │                                             │
│  └────────┼─────────┘                                             │
│           ▼                                                       │
│  ┌──────────────────┐                                             │
│  │  Validación de   │                                             │
│  │  Respuesta       │                                             │
│  │  (Confianza >    │                                             │
│  │   umbral?)       │                                             │
│  └────────┬─────────┘                                             │
│           ▼                                                       │
│  ┌──────────────────┐                                             │
│  │ RESPUESTA AL     │                                             │
│  │ CLIENTE          │                                             │
│  └──────────────────┘                                             │
│                                                                   │
│  ════════════════════════════════════════════════                  │
│           FUENTES DE DATOS (RAG)                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ BD       │  │ BD       │  │ BD       │  │ Histórico│         │
│  │ Pedidos  │  │ Catálogo │  │ Políticas│  │ de FAQ   │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Flujo de Procesamiento

1. **Recepción:** La consulta del cliente llega por cualquier canal y se unifica a través del API Gateway.
2. **Clasificación:** Un clasificador de intención (que puede ser el mismo LLM con un prompt específico, o un modelo más ligero) determina el tipo de consulta.
3. **Consultas repetitivas (80%):**
   - El sistema de RAG busca en las bases de datos relevantes (pedidos, catálogo, políticas de devolución) la información necesaria.
   - Esta información se inyecta como contexto en el prompt del LLM.
   - El LLM genera una respuesta fluida, empática y precisa basada en los datos reales.
4. **Consultas complejas (20%):**
   - Se escalan a un agente humano.
   - El agente recibe un **resumen generado por IA** del historial del cliente y la consulta, acelerando su tiempo de resolución.
5. **Validación:** Antes de enviar la respuesta automatizada, un módulo de validación verifica que la confianza sea superior a un umbral. Si no lo es, se escala a un humano.

### 3.3 Integración con las Bases de Datos de EcoMarket

El modelo **sí se integraría** con las bases de datos de EcoMarket, pero de manera controlada:

- **BD de Pedidos:** Consulta en tiempo real del estado, ubicación y fecha estimada de entrega. Acceso de solo lectura via API interna.
- **BD de Catálogo de Productos:** Consulta de características, disponibilidad, precios y especificaciones de productos sostenibles.
- **BD de Políticas:** Acceso a las políticas de devolución, garantía y envío vigentes. Estas se almacenan como documentos indexados para búsqueda semántica.
- **Histórico de FAQ:** Base de conocimiento construida a partir de las interacciones previas exitosas del equipo de soporte.

**Importante:** El LLM no tiene acceso directo a la base de datos. La capa de RAG actúa como intermediario, garantizando que solo se recupere información relevante y que no se expongan datos sensibles de otros clientes.

---

## 4. Justificación por Criterios

### 4.1 Costo

| Componente | Costo estimado mensual | Notas |
|---|---|---|
| API LLM (Groq + Llama 3.3 70B) | $500–$2,000 USD | Dependiendo del volumen y del uso por tokens. Modelos más ligeros o rutas de fallback pueden manejar el 80% de consultas simples |
| Infraestructura RAG | $200–$500 USD | Base de datos vectorial (Pinecone, Weaviate) + servidor de embeddings |
| API Gateway + Integraciones | $100–$300 USD | Cloud functions/containers |
| **Total estimado** | **$800–$2,800 USD/mes** | **vs. costo de 5-10 agentes adicionales a tiempo completo: $15,000–$30,000 USD/mes** |

El ROI es claro: la solución de IA cuesta entre un **5% y un 18%** de lo que costaría contratar personal adicional para cubrir la misma demanda, manteniendo la calidad del servicio.

### 4.2 Escalabilidad

- **Horizontal:** El modelo se consume vía API, lo que permite escalar automáticamente ante picos de demanda (ej: Black Friday, lanzamientos de productos).
- **Multi-canal:** La misma lógica de prompts y RAG sirve para chat, email, RRSS y WhatsApp.
- **Multi-idioma:** Los LLMs modernos soportan decenas de idiomas sin configuración adicional, algo crítico si EcoMarket expande operaciones internacionalmente.

### 4.3 Facilidad de Integración

- **APIs bien documentadas:** Groq ofrece una API compatible con OpenAI y SDKs fáciles de integrar en Python y JavaScript.
- **Sin cambios en la BD existente:** El RAG se conecta a las bases de datos actuales de EcoMarket via APIs de solo lectura. No requiere migración ni modificación de esquemas.
- **Implementación incremental:** Se puede comenzar con un solo canal (ej: chat web) y expandir gradualmente.

### 4.4 Calidad de Respuesta Esperada

- **Precisión factual:** Garantizada por RAG (datos reales, no inventados).
- **Tono y empatía:** Controlados mediante prompts de sistema cuidadosamente diseñados (ver `prompts/system_prompts.txt`).
- **Consistencia:** Las mismas políticas se aplican uniformemente a todos los clientes, sin variaciones por agente.
- **Tiempo de respuesta:** De **24 horas** a **segundos** para el 80% de las consultas.

---

## 5. Comparación con Alternativas Descartadas

### 5.1 Chatbot Basado en Reglas (Descartado)

**Ventajas:** Barato, predecible, fácil de implementar para flujos simples.

**Razones de descarte:**
- No maneja variaciones en el lenguaje del cliente ("¿dónde está mi paquete?", "quiero saber sobre mi envío", "¿ya salió mi pedido?").
- Requiere mantenimiento manual de cada flujo y cada posible pregunta.
- Experiencia de usuario frustrante cuando la consulta no coincide con un patrón predefinido.
- No escala a medida que el catálogo y las políticas de EcoMarket crecen.

### 5.2 LLM de Propósito General sin RAG (Descartado)

**Ventajas:** Fácil de implementar, buena fluidez conversacional.

**Razones de descarte:**
- **Alto riesgo de alucinaciones:** Sin acceso a datos reales, el modelo inventaría estados de pedidos, precios o políticas.
- No puede responder preguntas específicas sobre pedidos individuales.
- Respuestas genéricas que no reflejan las políticas específicas de EcoMarket.

### 5.3 Fine-tuning Exclusivo (Descartado como solución única)

**Ventajas:** Modelo especializado en el dominio de EcoMarket, respuestas muy naturales.

**Razones de descarte (como solución *única*):**
- Los datos de pedidos cambian en tiempo real; re-entrenar el modelo para cada cambio es inviable.
- Costo alto de entrenamiento y re-entrenamiento.
- Riesgo de memorizar datos de clientes específicos (problema de privacidad).
- **Sí se recomienda como complemento** del RAG para adaptar el tono y estilo de comunicación.

---

## 6. Conclusión

La arquitectura **RAG híbrida con LLM** es la solución más adecuada para EcoMarket porque:

1. **Resuelve el problema del 80%** de consultas repetitivas con respuestas instantáneas, precisas y empáticas.
2. **Mantiene la precisión factual** al conectarse a datos en tiempo real, eliminando el riesgo de información desactualizada.
3. **Escala naturalmente** con el crecimiento de EcoMarket sin requerir re-entrenamiento.
4. **Empodera a los agentes humanos** permitiéndoles enfocarse en el 20% de casos complejos que realmente requieren su expertise y empatía.
5. **Ofrece el mejor balance** entre costo, calidad y velocidad de implementación.

El resultado esperado es una **reducción del tiempo de respuesta de 24 horas a segundos** para la mayoría de consultas, con un **aumento significativo en la satisfacción del cliente** y una **reducción de costos operativos** del departamento de soporte.
