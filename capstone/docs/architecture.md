# Architecture

## System context (C2)

Current proposal for the capstone; update the diagram as implementation and source access are confirmed. The daily batch choice is recorded in ADR 0001.

```mermaid
graph LR
    Source[Source A] -->|raw extract| Pipeline[Daily batch pipeline]
    Pipeline -->|validated daily records| Warehouse[(Warehouse)]
    Warehouse --> Dashboard[Daily dashboard]
    Stakeholder[Dashboard stakeholder] -->|uses| Dashboard
