# Contexto del Proyecto para Agentes · Lingua IA

Este documento (`agents.md`) sirve como fuente de verdad y memoria técnica para cualquier agente de IA o desarrollador que trabaje en este repositorio. Describe la arquitectura del software, las decisiones de diseño de Interacción Humano-Computador (IHC), los artefactos generados y las pautas para mantener la integridad del proyecto.

---

## 1. Visión General del Proyecto

- **Nombre:** Lingua IA
- **Propósito:** Prototipo interactivo de nivel medio de un tutor de inglés asistido por IA generativa para estudiantes universitarios (nivel B1–B2).
- **Asignatura / Contexto:** Curso de Interacción Humano-Computador (IHC), basado en el libro *Designing with the Mind in Mind* de Jeff Johnson (71 principios de diseño divididos en los capítulos C1 a C8).
- **Naturaleza técnica:** Prototipo **100% frontend** (mock interactivo con estado local reactivo en JavaScript). **No cuenta con backend, servidor ni llamadas a APIs de LLM externas**. Todo el contenido, sugerencias y respuestas son datos simulados situados en `js/data.js`.

---

## 2. Decisiones Clave de Alcance y Diseño (Lo que NO se debe alterar)

1. **Tres actividades principales exclusivas:**
   - **Redacción asistida (`writing`):** Revisar un correo formal, comparar fragmento original con propuesta (diff), leer pista/explicación y aceptar o rechazar la sugerencia.
   - **Lecciones y repaso (`lessons`):** Leer un artículo, tocar palabras resaltadas para ver significado y ejemplos en contexto, y guardarlas en el panel de vocabulario.
   - **Conversación escrita (`conversation`):** Simulación de entrevista de trabajo o charla por chat en turnos breves, con solicitud de pistas.
2. **Exclusiones deliberadas del alcance (Decisión pedagógica e IHC):**
   - **Sin audio ni voz:** No hay micrófono, reconocimiento de voz ni evaluación de pronunciación. La interacción es exclusivamente por texto para reducir la fricción y la ansiedad del estudiante.
   - **Sin árboles de análisis complejos:** Se retiraron gráficos de operaciones, glifos de datos, ramas y etiquetas metodológicas de papers de investigación (WaitGPT, LightVA, WoZ) para no sobrecargar cognitivamente al aprendiz.
   - **Sin persistencia en base de datos:** El estado se gestiona en memoria (`js/state.js`).

---

## 3. Estructura de Archivos del Repositorio

```
/home/josealva/Projects/IHC/interfazIdioma/
├── index.html                   # Shell principal de la aplicación y layout
├── css/
│   └── style.css                # Sistema de diseño (Tokens, Figtree, Teal #0F766E, componentes)
├── js/
│   ├── icons.js                 # Biblioteca de iconos SVG inline (Icons.*)
│   ├── data.js                  # Datos mock: textos, correcciones, reglas, escenarios, artículos
│   ├── state.js                 # Gestor de estado reactivo mínimo (DemoState: get, set, subscribe)
│   ├── corrections.js           # Renderizado de tarjetas de corrección y diffs
│   ├── panels.js                # Renderizado de pestañas laterales, drawer, footer y popover
│   ├── chat.js                  # Lógica de renderizado de mensajes de chat y respuestas simuladas
│   └── app.js                   # Bootstrap, orquestación global y delegación de eventos [data-action]
├── docs/
│   └── screenshots/             # 14 miniaturas recortadas para la documentación y guía
├── tools/
│   ├── generate_screenshots.py  # Script automatizado con Firefox Headless y Pillow
│   └── test_guide_integrity.py  # Test automatizado de integridad referencial y anti-alucinación
├── GUIA_PRINCIPIOS_IHC.md       # Guía de evaluación docente en Markdown (71 principios)
├── GUIA_PRINCIPIOS_IHC.html     # Guía interactiva/imprimible con sidebar adhesivo y checklist
├── Informe_principios_Lingua_IA (1).docx # Informe original previo (auditoría base)
├── guia.md / guiaPapers.md / plan.md / reference.md # Documentación interna de alcance
└── agents.md                    # Este documento de contexto para agentes
```

---

## 4. Estado de Cobertura de los 71 Principios de IHC

La auditoría técnica real del prototipo clasifica los 71 principios en:

| Categoría | Total | Detalle |
|---|:---:|---|
| **✅ Aplicados** | **44** | Comprobables directamente en el DOM y en las interacciones (ej. C1.1, C1.2, C2.1, C4.1, C4.5, C7.5, C8.2, etc.). |
| **🟡 Parciales** | **11** | Operativos en la demo pero con margen de extensión analítica o de hardware (ej. C2.8, C3.3, C4.2, C4.6, C5.3, C6.1, C6.6, C8.4, C8.8, C8.9). |
| **🔴 Pendientes** | **2** | Requieren pruebas de laboratorio con usuarios humanos reales (C4.7 calibración de monitores, C6.12 pruebas de lectura). |
| **⛔ Excluidos deliberados** | **2** | Descartados conscientemente por criterio anti-distracción (C2.7 movimiento/animación cinemática, C5.4 pop-out periférico). |
| **➖ Fuera de alcance** | **12** | Funcionalidades de voz VUI (C7.2–C7.4), formularios rígidos (C3.6, C5.2), búsqueda web (C3.9, C7.6), breadcrumbs (C7.9), cuentas (C7.11) o temporizadores destructivos (C8.11). |

**Métrica clave:** La cobertura sobre principios aplicables al software es del **93.2%** (55 de 59).

---

## 5. Herramientas y Scripts del Repositorio

### A. Generador de Capturas de Pantalla (`tools/generate_screenshots.py`)
Genera 14 capturas recortadas de alta resolución en `docs/screenshots/` utilizando Firefox en modo headless y Pillow (PIL).  
Ejecución:
```bash
python3 tools/generate_screenshots.py
```
*Nota técnica:* Crea un archivo temporal `harness_temp.html` en la raíz para resolver correctamente las rutas relativas de CSS y JS, inyecta el estado deseado y recorta la caja delimitadora (bounding box) exacta.

### B. Suite de Pruebas de Integridad y Anti-Alucinación (`tools/test_guide_integrity.py`)
Valida de forma automatizada que:
1. Las 14 capturas referenciadas existan físicamente en disco y no estén rotas.
2. Cada selector DOM citado en la guía (`#mode-nav`, `#stagebar`, `.correction-card`, `.type-badge`, `#help-levels`, etc.) exista estrictamente en el código de `index.html` o `js/*.js`.
3. Los 71 principios (C1.1 al C8.11) estén presentes sin omisiones.

Ejecución:
```bash
python3 tools/test_guide_integrity.py
```

### C. Generador de Guías (`tools/build_guides.py`)
Si se requiere actualizar el contenido o la redacción de las guías, este script compila sincronizadamente tanto `GUIA_PRINCIPIOS_IHC.md` como `GUIA_PRINCIPIOS_IHC.html`.
```bash
python3 tools/build_guides.py
```

---

## 6. Reglas Críticas para Futuros Agentes

1. **Protocolo Anti-Alucinación:**
   - Nunca afirmes que la interfaz tiene funcionalidades que no están en el código (ej. no digas que graba audio, que evalúa pronunciación, que guarda en backend o que hay login).
   - Si citas un principio en la interfaz, indica siempre el selector CSS o la acción `[data-action]` que lo respalda.
2. **Defensa de Principios Excluidos:**
   - Si te preguntan por qué no se implementó un principio como C2.7 (movimiento) o C7.2 (salida de voz), defiende la decisión en términos de **carga cognitiva, reducción de distracciones y delimitación de alcance** según se documenta en la Sección 4 de `GUIA_PRINCIPIOS_IHC.md`.
3. **Mantenimiento de Imágenes:**
   - Si realizas cambios visuales en el CSS o HTML que alteren la posición de componentes, vuelve a ejecutar `python3 tools/generate_screenshots.py` y `python3 tools/test_guide_integrity.py` para asegurar que las capturas sigan alineadas con el código.
