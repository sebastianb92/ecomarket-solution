# Fase 2 — Fortalezas, Limitaciones y Riesgos Éticos

## Fortalezas del sistema propuesto

### Disponibilidad y velocidad
- **24/7/365**: Responde en cualquier momento sin depender de horarios de agentes.
- **Tiempo de respuesta < 2 minutos** para el 80% de las consultas (vs. 24 horas actuales).
- **Escalabilidad ante picos**: Black Friday, campañas o lanzamientos sin degradación del servicio.

### Calidad y consistencia
- **Respuestas basadas en datos reales** gracias al módulo RAG → sin alucinaciones sobre pedidos.
- **Tono uniforme y profesional** en todas las interacciones, eliminando variabilidad humana negativa.
- **Multicanal**: El mismo backend atiende chat, email y redes sociales con coherencia.
- **Multilingüe**: Español, inglés, portugués sin costo adicional.

### Eficiencia operativa
- **Reducción estimada del 60–70%** de la carga de trabajo del equipo de soporte.
- **Los agentes se liberan** para casos de alto valor (empatía, negociación, resolución creativa).
- **Aprendizaje continuo**: Los logs de conversación retroalimentan mejoras iterativas.

---

## Limitaciones técnicas y operativas

> ⚠️ Reconocer las limitaciones es parte del diseño responsable. Cada una se asocia a una estrategia compensatoria.

### Limitaciones del modelo
- **No maneja el 20% complejo**: Consultas que requieren empatía genuina, negociación o criterio ético no pueden automatizarse de forma segura.
- **Dependencia de la calidad de datos**: Si la BD de pedidos tiene datos inconsistentes, las respuestas serán incorrectas (garbage in, garbage out).
- **Errores de clasificación**: El clasificador puede confundir una consulta compleja como simple, enviándola al flujo automatizado.
- **No detecta matices emocionales**: Sarcasmo, ironía o crisis emocional del cliente no son detectados con la misma precisión que un agente experimentado.

### Limitaciones operativas
- **Curva de aprendizaje**: El equipo necesita capacitación para supervisar y ajustar prompts.
- **Integración técnica**: Conectar RAG con las APIs internas requiere 8–12 semanas de ingeniería.
- **Mantenimiento de prompts**: Los prompts deben revisarse cuando cambian las políticas o el catálogo.

---

## Riesgos Éticos y Plan de Mitigación

### Riesgo 1: Alucinaciones del modelo

| Campo | Detalle |
|-------|---------|
| **Descripción** | El LLM podría generar información inventada sobre pedidos, fechas, precios o políticas si no tiene contexto real. |
| **Impacto** | Cliente recibe información incorrecta → pérdida de confianza, disputas comerciales, implicaciones legales. |
| **Mitigación** | RAG inyecta solo información verificada de la BD. Capa de validación post-generación. Prompt instruye "di No tengo información si los datos no están disponibles". |

### Riesgo 2: Sesgo en las respuestas

| Campo | Detalle |
|-------|---------|
| **Descripción** | El modelo podría tratar de forma diferente a clientes según patrones de lenguaje, dialecto o nombre. |
| **Impacto** | Servicio no equitativo. Riesgo reputacional y posible violación de normas de no discriminación. |
| **Mitigación** | Auditorías de sesgo mensuales. Prompt con instrucciones explícitas de trato igualitario. Monitoreo de CSAT segmentado por perfil de cliente. |

### Riesgo 3: Privacidad y protección de datos

| Campo | Detalle |
|-------|---------|
| **Descripción** | Datos sensibles del cliente (nombre, dirección, historial) se inyectan como contexto en los prompts. |
| **Marco normativo** | RGPD (operaciones en UE), Ley de Protección de Datos local, PCI-DSS para datos de pago. |
| **Mitigación** | LLM ejecutado on-premise o en nube privada. Seudonimización de datos antes del prompt. Nunca incluir datos de pago. Política de retención y borrado de logs. DPA con proveedores. |

### Riesgo 4: Impacto laboral

**Postura del equipo: Empoderar, no reemplazar.**

El objetivo de este sistema NO es eliminar empleos de atención al cliente, sino transformarlos:

- Los agentes dejan de ser "respondedores de FAQs" y pasan a ser "especialistas en casos complejos".
- Mayor satisfacción laboral, menor agotamiento por consultas repetitivas.
- El sistema de IA actúa como asistente que les prepara el terreno.

**Plan de transición:**
1. Re-skilling del equipo en supervisión de IA y gestión de casos complejos.
2. Política de no despidos derivados de la IA (primeros 2 años).
3. Sistema de bonificación por calidad de casos resueltos, no por volumen.

---

## Mapa resumen de riesgos

| Riesgo | Probabilidad | Impacto | Estrategia principal |
|--------|-------------|---------|---------------------|
| Alucinaciones | Media | Alto | Módulo RAG + validación post-generación |
| Sesgo en respuestas | Baja-Media | Medio | Auditorías + diseño de prompt |
| Privacidad de datos | Media | Muy Alto | LLM on-premise + seudonimización |
| Impacto laboral negativo | Baja | Alto (reputacional) | Política de empoderar, re-skilling |
| Error de clasificación | Media | Medio | Umbral de confianza + escalado automático |
