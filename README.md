# EcoMarket AI Support — Taller Práctico #1

Sistema de atención al cliente basado en **IA Generativa** para EcoMarket, una empresa de e-commerce sostenible.

## Descripción

Este repositorio implementa la solución propuesta en el Taller Práctico #1, demostrando cómo la ingeniería de prompts puede transformar la atención al cliente automatizando el 80% de consultas repetitivas mediante un modelo LLM open-source con contexto RAG simulado.

**Modelo utilizado:** `llama-3.3-70b-versatile` via [Groq API](https://groq.com)

---

## Estructura del Repositorio

```
ecomarket-solution/
├── README.md
├── requirements.txt
├── docs/
│   ├── fase1_selección_de_modelo.md
│   └── fase2_fortalezas_limitaciones_riesgos.md
│
├── prompts/
│   ├── order_status_prompt.txt
│   ├── return_policy_prompt.txt
│   └── system_prompt.txt
│
├── data/
│   ├── orders_database.txt
│   └── policies.txt
│
├── notebooks/
│   └── EcoMarket_AI_Solution.ipynb

```



---
## Uso

La solución se ejecuta principalmente a través de un notebook interactivo que integra los prompts y las fuentes de datos de EcoMarket.

---

### Ejecución del notebook

1. Abrir el notebook en Google Colab:

 [Abrir en Colab](./notebooks/EcoMarket_AI_Solution.ipynb)

2. Ejecutar las celdas en orden para:
   - Cargar los prompts desde la carpeta `/prompts`
   - Cargar los datos desde `/data`
   - Inicializar el modelo LLM
   - Probar los diferentes casos de uso

---

### Casos de uso incluidos

El notebook permite simular los principales flujos del sistema:

#### Consultar estado de un pedido

Ejemplos incluidos:
- Pedido válido
- Pedido retrasado
- Pedido no encontrado

Se utiliza:
- `order_status_prompt.txt`
- `orders_database.txt`



#### Solicitar devolución de producto

Ejemplos incluidos:
- Devolución válida
- Producto no elegible (higiene)
- Devolución fuera de plazo

Se utiliza:
- `return_policy_prompt.txt`
- `policies.txt`



### Estructura utilizada en la ejecución

El notebook hace uso de los siguientes componentes del proyecto:

- **Prompts** (`/prompts`): definen la lógica de interacción con el modelo
- **Datos** (`/data`): contienen la información de pedidos y políticas
- **Notebook** (`/notebooks`): orquesta la ejecución e integración de todos los componentes



### Notas

- No es necesario ejecutar scripts adicionales; toda la lógica está contenida en el notebook.
- El sistema puede adaptarse fácilmente a producción reemplazando las fuentes de datos por APIs o bases de datos reales.


---

## Casos de prueba incluidos

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

##  Arquitectura de la solución

```
Consulta del cliente
        │
        ▼
┌───────────────────┐
│  Clasificador     │ ──► simple (80%) ──► RAG + LLM ──► Respuesta automática
│  de intención     │
└───────────────────┘ ──► compleja (20%) ──► Asistente de agente humano
```


---

## Autores

* Johan Sebastian Bonilla

* Edwin Gómez

