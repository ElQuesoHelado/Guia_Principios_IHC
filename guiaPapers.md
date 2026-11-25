# Ideas de los papers incorporadas

Fuente exclusiva para esta selección: **Anexo D — Papers** de `LINGUA IA PLUS (1).docx`, incluidos los aportes de edición localizada y versiones al final del anexo. Los usuarios y las tareas proceden del HTA unificado v7, no de la propuesta anterior de Lingua IA Plus.

Las atribuciones y títulos siguientes se conservan como aparecen en el documento del equipo. Se adaptan sus ideas al prototipo; **no se han verificado aquí las publicaciones originales, sus citas, páginas, fechas ni resultados**. No se reproducen como citas científicas comprobadas ni se atribuye eficacia experimental a esta entrega.

| Referencia identificada en el anexo | Idea seleccionada | Adaptación implementada | Tarea y evidencia real |
|---|---|---|---|
| Gu y colaboradores: *How Do Analysts Understand and Verify AI-Assisted Data Analyses?* | Hacer verificable una respuesta | Regla y motivo junto a original y propuesta; distinción entre error y opción de cortesía | Correo C5; `.correction-card`, `.rule`, `.diff-line` |
| Gu | Conectar resultado con material original | Hipótesis junto a la acepción del ejemplo; contexto visible | Vocabulario V2–V3; `.word-detail` |
| Gu | Localizar aquello que requiere verificación | Revisiones solo de fragmentos reconocidos del borrador; no se inventa una corrección global | Correo C5; `review()` |
| Kazemitabaar y colaboradores: *Improving Steering and Verification in AI-Assisted Data Analysis with Interactive Task Decomposition* | Descomponer en objetivos comprensibles | Cuatro sugerencias de ruta agrupan los siete grupos de cada tarea; acceso libre | C1–C7 y V1–V7; `#learning-plan`, `#stagebar` |
| Kazemitabaar | Mostrar interpretaciones y supuestos | Contexto de tarea indicado junto al mensaje; **Cambiar tarea** permite corregirlo; una oración propia no recibe la acepción de otro ejemplo | C1.2 y V3; `#composer-mode-hint`, `change-task`, `startIntro()` |
| Kazemitabaar | Permitir intervenir | Usar, conservar o explicar antes de decidir; no se modifica automáticamente el correo | C5.3–C5.4; `accept`, `reject`, `justify` |
| Kazemitabaar | Mostrar procedimiento y resultado | Original, propuesta, explicación y versiones; el procedimiento técnico del dominio de datos se traduce a evidencia lingüística | C5; `versions()`, `.diff-line` |
| LightVA: *Lightweight Visual Analytics with LLM Agent-Based Task Planning and Execution* | Plan visible | Etapa actual visible durante el desplazamiento, ruta desplegable y aportes guardados; no abre una ficha obligatoria | C/V; `#stagebar` |
| LightVA | Acciones sugeridas y lenguaje natural | Botones contextuales y un único chat; sugerencias mientras se escribe, editables y descartables | C2, C5, V2, V6; `#prompt-assist`, `#chat-input` |
| LightVA | Aprobar o rechazar acciones | Decisiones de revisión y libertad para saltar la hipótesis o consultar un ejemplo | C5, V3; `accept`, `reject`, `definition` |
| LightVA | Observar progreso acumulado | Producciones, hipótesis, explicaciones y fechas; palabras guardadas se cuentan aparte | C6–C7, V6–V7; `notebook()` |
| LightVA y descomposición interactiva | Volver a un estado anterior | Recuperar un borrador conserva todas las versiones y crea otra; deshacer un cambio evita borrar modificaciones posteriores | C5; `restore`, `undo-correction` |
| WaitGPT, adaptación de refinamiento granular consignada en el anexo | Cambiar solo la sección pertinente | Sustitución de un fragmento exacto; resto conservado; antes/después visible | C5.1–C5.4; `review()`, `accept` |
| Yang y colaboradores: *Mapping the Wizards' Path: A Systematic Review of Wizard-of-Oz in HCI* | Transparencia de la simulación | Identificación visible de respuestas de ejemplo; no se finge conexión a un LLM | Ambas tareas; `.app-footer`, `demo()` |
| Yang | Escenarios acotados | Profesora y compañero; tres palabras con fichas preparadas. El ejemplo contextual no se presenta como interpretación general de cualquier texto | C2/C7 y V2/V7; `TutorData`, `startIntro()` |
| Yang | Control de ritmo y comunicación | Enviar es decisión del estudiante; no hay turnos automáticos, cuenta regresiva ni voz | Ambas; `#send-btn`, teclado |
| Yang | Ayuda situada y graduada | Pista, significado, explicación o modelo se abren bajo demanda; se puede recuperar sin material y volver a consultarlo | C3/C6 y V2/V6; `clue`, `definition`, `model`, `reveal-support` |
| Yang | Evitar perder contexto entre superficies | Original y propuesta dentro del chat; ficha contextual con hipótesis; historial local conserva la práctica | Ambas; `.word-detail`, `history()`, localStorage |

## Ideas con cobertura parcial o excluidas

- **Ramas de versiones completas:** se implementa recuperación no destructiva y una lista lineal de versiones; no un árbol de ramas con fusión. Es suficiente para demostrar comparar, conservar y recuperar un fragmento sin introducir un editor de análisis de datos.
- **Supuestos y plan arbitrarios editables:** se permite corregir la clasificación, escribir restricciones y elegir la ruta; no hay un editor genérico de suposiciones ni replanificación con un agente real.
- **Verificación externa:** las fichas son didácticas; no se conecta un diccionario ni se verifica una producción arbitraria. Otros contextos quedan pendientes de contraste, en vez de recibir evidencia inventada.
- **Porcentaje de dominio:** se excluye. Que un agente marque una tarea como realizada o que alguien descarte una propuesta no demuestra aprendizaje. Se muestran aportes y actividad.
- **Voz, control de turnos orales y WoZ con una persona operadora:** fuera de las tareas seleccionadas. Se conserva transparencia, ritmo voluntario y ayuda graduada en texto.
- **Código generado, gráficos analíticos, glifos, tablas de frecuencia y controles de investigación:** pertenecen al dominio de los artículos. La adaptación pertinente es comparar expresiones, explicar elecciones y recuperar versiones.
- **Predicción generativa:** no se incorpora un servicio externo. Las reglas locales demuestran cuándo podría sugerirse una mejora de consulta; el efecto sobre cantidad de prompts y aprendizaje necesita evaluación.

## Demostración

Los recorridos reproducibles están en `guia.md`: afinar consulta, revisar sin perder partes del correo, inferir/contrastar una palabra, recuperar con material oculto y retomar otro día. Los aportes se guardan en el mismo navegador; no hay métricas semanales ficticias ni una cuenta de dominio.
