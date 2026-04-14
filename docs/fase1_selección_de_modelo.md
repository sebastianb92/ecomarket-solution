# Fase 1 — Selección y Justificación del Modelo de IA

## Contexto del problema

**EcoMarket** recibe miles de consultas diarias a través de chat, correo y redes sociales:
- **80%** son repetitivas: estado de pedido, devoluciones, características de producto.
- **20%** son complejas: quejas, problemas técnicos, solicitudes con empatía.
- Tiempo de respuesta actual: **24 horas** → Objetivo: **< 2 minutos** para el 80%.

---

## Análisis comparativo de opciones

| Tipo de modelo | Descripción | Ventajas | Desventajas | Casos de uso ideales | Consideraciones técnicas |
|--------|-------------|----------|-------------|----------------------|--------------------------|
| **LLM de propósito general** (GPT-4o, Claude 3) | Uso de modelos avanzados vía API externa sin personalización específica. Entrenados con grandes volúmenes de datos generales. | - Alta fluidez y calidad de texto<br>- Excelente comprensión contextual<br>- Fácil integración vía API<br>- No requiere infraestructura propia | - Costos por token<br>- Riesgo de exposición de datos<br>- No especializado en dominio<br>- Dependencia de terceros | - Chatbots generales<br>- Asistentes virtuales<br>- MVPs rápidos<br>- Generación de contenido | - Integración vía REST/API<br>- Control de costos (tokens)<br>- Latencia dependiente del proveedor<br>- Prompt engineering |
| **LLM afinado** (Fine-tuned) | Modelo base reentrenado con datos propios para mejorar desempeño en un dominio específico. | - Alta precisión en dominio<br>- Respuestas consistentes<br>- Mejor rendimiento en lenguaje técnico | - Alto costo de entrenamiento<br>- Requiere datos limpios<br>- Mantenimiento continuo<br>- Riesgo de sobreajuste | - Soporte técnico especializado<br>- Automatización interna<br>- Clasificación avanzada | - Pipeline de ML Ops<br>- Versionamiento de modelos<br>- Evaluación continua<br>- Uso de GPUs |
| **SLM open-source** (Mistral 7B, LLaMA 3) | Modelos más pequeños que pueden ejecutarse localmente o en infraestructura propia. | - Privacidad total<br>- Sin costo por token<br>- Control completo del sistema<br>- Despliegue on-premise | - Menor capacidad de razonamiento<br>- Requiere optimización<br>- Mayor complejidad técnica<br>- Dependencia de hardware | - Datos sensibles<br>- Sistemas offline<br>- Proyectos personalizados | - Deployment con Docker/GPU<br>- Optimización (quantization)<br>- Gestión de memoria (VRAM)<br>- Ajustes tipo LoRA |
| **RAG + LLM (seleccionado)** | Arquitectura híbrida que combina un LLM con recuperación de información en tiempo real desde bases de datos o documentos. | - Alta precisión con datos reales<br>- Reduce alucinaciones<br>- No requiere reentrenamiento<br>- Escalable y flexible<br>- Control de datos | - Complejidad inicial alta<br>- Requiere arquitectura adicional<br>- Latencia mayor<br>- Necesita buen diseño de búsqueda | - Chatbots empresariales<br>- QA sobre documentos<br>- Soporte al cliente<br>- Sistemas con datos dinámicos | - Pipeline de embeddings<br>- Vector DB (FAISS, Pinecone)<br>- Orquestación (LangChain)<br>- Chunking y ranking |



---

## Modelo seleccionado: Arquitectura Híbrida RAG + LLM

### Justificación de la selección

Se selecciona una arquitectura híbrida basada en RAG (Retrieval-Augmented Generation) combinada con un LLM, ya que permite integrar la capacidad de generación de lenguaje natural con el acceso a información actualizada y específica del negocio.

Un LLM sin contexto de datos reales presenta un problema crítico para EcoMarket: **las alucinaciones**. Por ejemplo, si un cliente consulta por el estado del pedido #ECO-12346, el modelo no tiene forma de conocer la respuesta y podría inventarla. El enfoque RAG resuelve esta limitación al recuperar primero la información real desde la base de datos y luego inyectarla en el prompt, garantizando que el modelo genere respuestas basadas únicamente en datos verificados.

Además, esta arquitectura elimina la necesidad de reentrenar el modelo, mejora la precisión de las respuestas, mantiene el control sobre la información sensible y ofrece una solución escalable y eficiente en costos. Por estas razones, RAG + LLM se considera la opción más adecuada para entornos empresariales con información dinámica y crítica.


### ¿Por qué no un modelo fine-tuned?

El fine-tuning, aunque permite adaptar un modelo a un dominio específico, presenta varias limitaciones en el contexto de EcoMarket. En primer lugar, es un proceso computacionalmente costoso, ya que requiere infraestructura especializada (GPUs), tiempo de entrenamiento y un conjunto de datos cuidadosamente curado y etiquetado.

Además, implica un **alto costo de mantenimiento**. Cada vez que cambian los datos del negocio —como nuevos productos, actualizaciones en políticas, precios o estados de pedidos— es necesario volver a entrenar o ajustar el modelo para mantener la precisión, lo cual no es viable en entornos donde la información es dinámica.

Otro aspecto crítico es la **falta de acceso a información en tiempo real**. Un modelo fine-tuned “memoriza” patrones durante el entrenamiento, pero no puede consultar directamente bases de datos ni sistemas transaccionales, lo que lo hace propenso a desactualización o respuestas incorrectas en escenarios operativos.

En contraste, la arquitectura RAG permite desacoplar el conocimiento del modelo, delegando la actualización de la información a fuentes externas (bases de datos, documentos, APIs). Esto elimina la necesidad de reentrenamiento constante, reduce costos operativos y garantiza que las respuestas estén siempre basadas en información actualizada y verificable.

Por estas razones, aunque el fine-tuning puede ser útil en tareas muy específicas, no es la opción más eficiente ni escalable para el caso de uso planteado.


### ¿Por qué un modelo open-source?

La elección de un modelo open-source frente a un modelo propietario como GPT-4o responde principalmente a criterios de privacidad, costos y control operativo dentro del entorno de EcoMarket.

En primer lugar, la **privacidad** es un factor crítico. Al utilizar modelos open-source desplegados en infraestructura propia, se garantiza que los datos sensibles de los clientes —como información de pedidos, direcciones y datos personales— nunca salen del entorno controlado de la empresa. Esto facilita el cumplimiento de políticas de seguridad y regulaciones de protección de datos.

En segundo lugar, el **costo** es significativamente menor a escala. Modelos como LLaMA 3.1 8B o Mistral 7B eliminan el costo por token asociado a APIs externas, permitiendo predecir y controlar mejor el gasto operativo. Aunque existe un costo inicial de infraestructura, a mediano y largo plazo resulta más eficiente, especialmente en escenarios de alto volumen de consultas.

Adicionalmente, el uso de modelos open-source ofrece un mayor **control** sobre el sistema. EcoMarket puede definir cuándo y cómo actualizar el modelo, aplicar optimizaciones (como quantization o fine-tuning ligero), y adaptar su comportamiento según necesidades específicas del negocio sin depender de cambios o restricciones impuestas por terceros.

Finalmente, esta elección se alinea mejor con una arquitectura RAG, donde el valor principal proviene de la integración con datos propios. En este contexto, no es imprescindible utilizar el modelo más grande o avanzado, sino uno que ofrezca un buen balance entre rendimiento, eficiencia y control.

Por estas razones, un modelo open-source representa una alternativa más adecuada y sostenible para el caso de uso planteado.

---

## Arquitectura propuesta (dos niveles)

La solución se diseña bajo un enfoque híbrido que combina automatización inteligente con supervisión humana, permitiendo escalar la atención al cliente sin perder calidad en casos complejos.


### Nivel 1 — Chatbot automatizado (80% de consultas)

Este nivel resuelve de forma automática las consultas repetitivas y de baja complejidad, que representan la mayoría de interacciones en EcoMarket.

**Componentes:**

1. **Clasificador de intención**  
   Analiza la consulta del usuario mediante técnicas de NLP para identificar su propósito (estado de pedido, devoluciones, información de producto, etc.).  
   Este componente permite enrutar la solicitud correctamente dentro del sistema.

2. **Módulo RAG (Retrieval-Augmented Generation)**  
   Recupera información relevante desde fuentes internas (base de datos de pedidos, políticas, catálogo de productos).  
   Incluye procesos de:
   - Búsqueda semántica (embeddings + vector DB)  
   - Selección de contexto (top-k documentos más relevantes)  
   - Preparación del prompt enriquecido  

3. **LLM (llama-3.3-70b-versatile)**  
   Genera la respuesta final utilizando el contexto recuperado.  
   Su función no es “inventar” información, sino estructurar una respuesta clara, coherente y natural basada en datos reales.

4. **Capa de validación**  
   Actúa como mecanismo de control para asegurar la confiabilidad de la respuesta.  
   - Verifica consistencia con la base de datos  
   - Detecta posibles alucinaciones o inconsistencias  
   - Aplica reglas de negocio (por ejemplo, políticas de devolución)  

**Resultado:**  
Respuestas automáticas precisas, rápidas y basadas en información verificada, reduciendo significativamente la carga operativa del equipo humano.

---

### Nivel 2 — Asistente de agente humano (20% de casos complejos)

Este nivel entra en acción cuando la consulta no puede resolverse automáticamente o requiere juicio humano (casos excepcionales, clientes insatisfechos, problemas no estructurados).

**El sistema NO reemplaza al agente, lo potencia:**

1. **Análisis de conversación**  
   El sistema procesa el historial completo de interacción y genera un resumen estructurado del problema, permitiendo al agente entender rápidamente el contexto.

2. **Recuperación de información del cliente**  
   Extrae automáticamente datos relevantes como:
   - Historial de pedidos  
   - Interacciones previas  
   - Estado actual del caso  

3. **Generación de respuestas sugeridas**  
   Propone respuestas alineadas con:
   - Políticas de la empresa  
   - Tono empático y consistente con la marca  
   - Contexto específico del cliente  

4. **Intervención humana (Human-in-the-loop)**  
   El agente revisa, ajusta si es necesario y envía la respuesta final.  
   Esto garantiza control de calidad y manejo adecuado de situaciones sensibles.

**Impacto esperado:**  
- Reducción del tiempo de respuesta de ~24 horas a menos de 2 horas  
- Mejora en la experiencia del cliente  
- Aumento en la productividad del equipo de soporte  

---


## Justificación multifactor

La solución propuesta se justifica a partir de criterios clave para entornos empresariales, tales como costo, escalabilidad, facilidad de integración y calidad de la respuesta esperada.

| Criterio | Evaluación |
|----------|-----------|
| **Costo** | El uso de modelos open-source elimina el costo variable por token asociado a APIs externas. Aunque implica una inversión en infraestructura, esta es predecible y puede optimizarse a medida que escala la operación, resultando más eficiente en escenarios de alto volumen. |
| **Escalabilidad** | La arquitectura permite escalar horizontalmente mediante la adición de instancias según la demanda. Esto evita dependencias de límites impuestos por terceros y garantiza adaptabilidad ante incrementos en el número de consultas. |
| **Facilidad de integración** | La solución se integra mediante APIs REST con sistemas existentes como CRM o plataformas de soporte (por ejemplo, Zendesk o Freshdesk), lo que facilita su adopción sin requerir cambios significativos en la infraestructura actual. |
| **Calidad de la respuesta** | La combinación de RAG y LLM permite generar respuestas coherentes, naturales y basadas en información actualizada. Esto asegura un equilibrio entre precisión factual y experiencia conversacional, reduciendo errores y mejorando la satisfacción del usuario. |
| **Privacidad de datos** | Al operar sobre infraestructura propia, los datos sensibles permanecen dentro del entorno de la empresa, lo que reduce riesgos de seguridad y facilita el cumplimiento de normativas de protección de datos. |
| **Precisión factual** | El uso de RAG garantiza que las respuestas estén fundamentadas en datos reales y actualizados, evitando alucinaciones en información crítica del negocio como pedidos o políticas. |




