# Fase 2 — Fortalezas, Limitaciones y Riesgos Éticos

## Fortalezas del sistema propuesto

El sistema propuesto presenta múltiples fortalezas que impactan directamente la disponibilidad del servicio, la calidad de las respuestas y la eficiencia operativa del área de atención al cliente.


### Disponibilidad y velocidad

- **Disponibilidad continua (24/7/365)**: El sistema puede atender consultas en cualquier momento, eliminando la dependencia de horarios laborales y mejorando la experiencia del cliente en términos de acceso al servicio.
- **Reducción significativa en los tiempos de respuesta**: Se estima un tiempo de respuesta inferior a 2 minutos para aproximadamente el 80% de las consultas, en comparación con los tiempos actuales que pueden alcanzar hasta 24 horas.
- **Capacidad de escalamiento ante alta demanda**: La arquitectura permite soportar picos de tráfico, como eventos comerciales (por ejemplo, campañas o temporadas de alto volumen), sin degradación significativa en el rendimiento.


### Calidad y consistencia

- **Respuestas basadas en información verificable**: Gracias al uso de un módulo RAG, las respuestas se fundamentan en datos reales provenientes de las bases internas, lo que reduce significativamente el riesgo de alucinaciones en información crítica como pedidos o políticas.
- **Consistencia en el tono y estilo de comunicación**: El sistema garantiza uniformidad en las respuestas, manteniendo un tono profesional y alineado con la identidad de la empresa, evitando variaciones propias de la interacción humana.
- **Soporte multicanal**: La solución permite atender diferentes canales (chat, correo electrónico, redes sociales) utilizando una misma lógica central, asegurando coherencia en las respuestas independientemente del punto de contacto.
- **Capacidad multilingüe**: El sistema puede operar en múltiples idiomas (como español, inglés y portugués), ampliando el alcance del servicio sin requerir costos adicionales significativos.


### Eficiencia operativa

- **Reducción de la carga operativa**: Se estima una disminución del 60% al 70% en el volumen de consultas gestionadas manualmente por el equipo de soporte, permitiendo optimizar recursos.
- **Enfoque en tareas de mayor valor**: Los agentes humanos pueden concentrarse en casos complejos que requieren empatía, juicio o toma de decisiones, mejorando la calidad del servicio en situaciones críticas.
- **Mejora continua del sistema**: El almacenamiento y análisis de las interacciones permite identificar patrones, errores y oportunidades de mejora, facilitando la evolución constante del sistema mediante ajustes en prompts, reglas o fuentes de información.



---

## Limitaciones técnicas y operativas

A pesar de las ventajas del sistema propuesto, es importante reconocer ciertas limitaciones tanto a nivel técnico como operativo, las cuales deben ser gestionadas adecuadamente para garantizar un funcionamiento óptimo.


### Limitaciones del modelo

- **Cobertura limitada en casos complejos**: Aproximadamente un 20% de las consultas, aquellas que requieren empatía, negociación o juicio ético, no pueden ser automatizadas de forma completamente confiable. Estos casos deben ser gestionados por agentes humanos bajo un enfoque *human-in-the-loop*.
- **Dependencia de la calidad de los datos**: El desempeño del sistema está directamente ligado a la calidad de las fuentes de información. Si la base de datos contiene errores, inconsistencias o información desactualizada, el sistema replicará dichas fallas en sus respuestas (principio de *garbage in, garbage out*).
- **Errores en la clasificación de intención**: El clasificador puede presentar fallos al interpretar correctamente la intención del usuario, lo que podría derivar en que consultas complejas sean tratadas como simples, afectando la calidad de la respuesta automatizada.
- **Limitaciones en la comprensión emocional**: Aunque el modelo puede simular un tono empático, no posee una comprensión real de emociones complejas. Esto limita su capacidad para interpretar adecuadamente situaciones con sarcasmo, ironía o clientes en estado de frustración elevada.


### Limitaciones operativas

- **Curva de aprendizaje del equipo**: La implementación del sistema requiere que el equipo adquiera nuevas habilidades, como supervisión de modelos, ajuste de prompts y análisis de resultados, lo que implica un proceso de capacitación inicial.
- **Complejidad en la integración técnica**: La conexión entre el módulo RAG, las bases de datos internas y los sistemas existentes (como CRM o APIs) puede requerir entre 8 y 12 semanas de desarrollo e implementación, dependiendo de la madurez tecnológica de la organización.
- **Mantenimiento continuo de prompts y reglas**: Los prompts y configuraciones del sistema deben actualizarse periódicamente para reflejar cambios en políticas, productos o procesos internos, lo que implica un esfuerzo de mantenimiento constante.


---
## Riesgos éticos y plan de mitigación

La implementación de sistemas basados en inteligencia artificial en entornos empresariales conlleva una serie de riesgos éticos que deben ser identificados y gestionados de manera proactiva. A continuación, se presentan los principales riesgos asociados al sistema propuesto, junto con sus respectivos planes de mitigación.


### Riesgo 1: Alucinaciones del modelo

|  | Detalle |
|-------|---------|
| **Descripción** | El modelo de lenguaje podría generar información incorrecta o no verificada sobre pedidos, fechas, precios o políticas, especialmente en ausencia de contexto suficiente. |
| **Impacto** | La entrega de información errónea puede generar pérdida de confianza por parte del cliente, reclamaciones, conflictos comerciales e incluso implicaciones legales. |
| **Mitigación** | Se implementa un enfoque RAG que garantiza el uso de información verificada, junto con una capa de validación posterior a la generación y prompts que instruyen al modelo a reconocer cuando no dispone de información suficiente. |


### Riesgo 2: Sesgo en las respuestas

|  | Detalle |
|-------|---------|
| **Descripción** | El modelo podría presentar sesgos en sus respuestas, tratando de manera diferenciada a los usuarios según características implícitas como lenguaje, dialecto o nombre. |
| **Impacto** | Puede derivar en un servicio inequitativo, afectando la reputación de la empresa y generando posibles incumplimientos de normativas de no discriminación. |
| **Mitigación** | Se realizan auditorías periódicas de sesgo, se diseñan prompts con lineamientos explícitos de trato equitativo y se monitorean indicadores de satisfacción del cliente segmentados para detectar desviaciones. |


### Riesgo 3: Privacidad y protección de datos

|  | Detalle |
|-------|---------|
| **Descripción** | El sistema utiliza datos sensibles del cliente (como nombre, dirección o historial de pedidos) como parte del contexto para generar respuestas. |
| **Impacto** | Un manejo inadecuado de esta información puede generar riesgos de seguridad, sanciones legales y pérdida de confianza del cliente. |
| **Mitigación** | El modelo se despliega en entornos controlados (on-premise o nube privada), se aplican técnicas de seudonimización, se restringe el uso de datos sensibles (especialmente datos de pago) y se implementan políticas de retención y eliminación de logs. |


### Riesgo 4: Impacto laboral

|  | Detalle |
|-------|---------|
| **Descripción** | La automatización de procesos de atención al cliente puede generar incertidumbre en el equipo humano respecto a la estabilidad de sus roles laborales. |
| **Impacto** | Puede afectar la motivación del equipo, generar resistencia al cambio y tener implicaciones reputacionales para la organización. |
| **Mitigación** | Se adopta un enfoque de empoderamiento del talento humano mediante estrategias de re-skilling, políticas que eviten la sustitución directa de personal en fases iniciales y rediseño de roles hacia tareas de mayor valor agregado. |


---

## Mapa resumen de riesgos

A continuación, se presenta una visión consolidada de los principales riesgos identificados, junto con su probabilidad, nivel de impacto y estrategia de mitigación asociada.

| Riesgo | Probabilidad | Impacto | Estrategia principal |
|--------|-------------|---------|---------------------|
| **Alucinaciones del modelo** | Media | Alto | Implementación de arquitectura RAG para asegurar el uso de información verificada, complementada con una capa de validación posterior a la generación. |
| **Sesgo en las respuestas** | Baja-Media | Medio | Ejecución de auditorías periódicas de sesgo, junto con el diseño de prompts que garanticen trato equitativo y monitoreo de métricas de satisfacción segmentadas. |
| **Privacidad de datos** | Media | Muy alto | Despliegue del modelo en entornos controlados (on-premise o nube privada) y aplicación de técnicas de seudonimización para proteger la información sensible. |
| **Impacto laboral negativo** | Baja | Alto (reputacional) | Implementación de una estrategia centrada en el re-skilling del personal y el uso de la IA como herramienta de apoyo, evitando su sustitución directa. |
| **Error en la clasificación de intención** | Media | Medio | Definición de umbrales de confianza y mecanismos de escalamiento automático hacia agentes humanos en casos de ambigüedad. |

---

### Análisis general

El mapa de riesgos evidencia que los principales desafíos se concentran en aspectos técnicos (como alucinaciones y clasificación) y éticos (privacidad y sesgo). No obstante, todos los riesgos identificados cuentan con estrategias de mitigación claras y viables, lo que permite reducir su impacto y asegurar una implementación controlada del sistema.

En este sentido, el enfoque adoptado no busca eliminar completamente los riesgos —lo cual no es realista en sistemas de IA— sino gestionarlos de manera efectiva mediante controles técnicos, operativos y organizacionales.
