# Lingua IA: alcance del prototipo y relación con las lecturas

## Actividades principales

1. **Redacción y revisión:** el estudiante aporta un texto, recibe una corrección localizada con una explicación y decide si la acepta.
2. **Lectura y vocabulario:** puede usar el texto de ejemplo o pegar una lectura propia, consultar una palabra en su contexto, ver ejemplos y guardarla.
3. **Conversación escrita:** practica por chat en un escenario breve, responde a su ritmo y puede pedir una pista.

Las dudas puntuales se envían en el chat de la actividad correspondiente. La conversación se realiza por texto; este prototipo no incluye micrófono, grabación ni evaluación de pronunciación.

## Principios de los artículos que sí se conservan

| Aporte de lectura | Uso en Lingua IA | Por qué ayuda al aprendizaje |
|---|---|---|
| Gu et al., CHI 2024: hacer verificables las respuestas de la IA | Mostrar desde el inicio texto original y propuesta, añadir explicación según el nivel de ayuda y permitir aceptar o rechazar | El estudiante compara, comprende el cambio y conserva la decisión. |
| Kazemitabaar et al., UIST 2024: dividir tareas y permitir intervención del usuario | Etapas breves y ayuda gradual en la tarea actual | Orienta el siguiente paso sin exponer un proceso técnico innecesario. |
| LightVA: representar el avance y hacer visibles los pasos relevantes | Una secuencia breve de etapas y un botón “Ver progreso” que abre directamente el avance de la tarea; en lectura, el resumen incluye palabras guardadas | Ayuda a saber dónde está el estudiante y qué puede hacer después. |
| WaitGPT: facilitar el control de cambios y versiones | Correcciones por fragmento e historial de versiones cuando se necesita | Permite recuperar una opción y revisar cómo cambió el texto. |
| Yang et al., CHI 2026: control de la interacción y transparencia | Escenarios acotados, conversación escrita, turnos y pistas | Reduce la presión de responder de inmediato y mantiene al estudiante activo. |

## Elementos retirados o fuera del alcance

- El modo independiente **Dudas rápidas**, porque duplicaba el chat; las consultas se escriben en la actividad activa.
- Micrófono, grabación y práctica por audio; no son necesarios para demostrar las tareas y complican la implementación.
- Gráfico de operaciones, glifos de datos, ramas y controles de análisis de datos; responden al dominio de los papers y no al aprendizaje de inglés.
- Etiquetas de papers, protocolo WoZ, debriefing y controles de reproducción en la interfaz del estudiante; son material de documentación o evaluación.
- La tarjeta de pasos que repetía la secuencia de la barra superior y la tarjeta que repetía el texto de ayuda para pegar una lectura.
- La ruta intermedia “Ver proceso” y el modal común de herramientas; “Ver progreso” abre el resumen en un paso. El plan sigue disponible como pestaña contextual en Redacción asistida.

## Criterio de diseño

La interfaz conserva las ideas de verificación, control del estudiante, ejemplos contextuales y progreso. Cada una aparece cuando es pertinente para la actividad. El progreso refleja el estado local de la sesión (etapas, respuestas, sugerencias o palabras), no estadísticas semanales de uso. La literatura guía el diseño, pero las etiquetas y mecanismos propios del análisis de datos no se presentan como herramientas de aprendizaje de idiomas.


## Adaptación a construcción de conocimiento (22 de noviembre de 2026)

Las ideas se conservan y se sitúan en las tres tareas del HTA. El análisis sin IA describe acciones con modelos, diccionario, apuntes y otras personas; los papers informan el diseño posterior de la ayuda.

| Aporte conservado | Interacción verificable | Evidencia que produce el estudiante |
|---|---|---|
| Gu: comparar y verificar con evidencias | `.diff-line`, `correction-rule`, significado contextual | Explicación de un cambio; contraste entre hipótesis y significado |
| Kazemitabaar: pasos, criterios e intervención | `#stagebar`, `[data-criterion]`, `[data-plan]`, decisiones de corrección | Plan, autoevaluación y decisión razonada |
| LightVA: plan visible y avance | `learning-save`, `open-progress-view` | Etapas con notas opcionales, diferenciadas de dominio del idioma |
| WaitGPT y análisis de versiones: edición localizada y recuperación | `correction-undo`, `set-version`, `open-version-history` | Comparación reversible del ejemplo; borrador y revisión propios en campos separados |
| Yang: escenarios, transparencia y turnos | `select-scenario`, `next-prompt`, `#chat-form` | Preparación, mensajes, respuesta reformulada y diálogo de transferencia |

El título de Kazemitabaar recogido en el documento del equipo es *Improving Steering and Verification in AI-Assisted Data Analysis with Interactive Task Decomposition*. Se usa ese análisis como referencia interna; no se verificaron aquí las citas o resultados de los papers. El progreso cuantifica evidencias y actividad, no adquisición demostrada. El prototipo no ofrece evaluación de textos libres, audio, ramas completas de versiones ni persistencia entre recargas.


El apoyo pedagógico es opcional: se accede directamente a correo, lectura o conversación. Las sugerencias están inicialmente ocultas y pueden abrirse u ocultarse en cualquier momento. En el correo, “Ver ejemplos de correo” abre el modelo directamente; Original, Borrador, Versión actual, Ver cambios, Versiones y Deshacer siguen accesibles al cambiar de sugerencia.
