# Lingua IA: alcance del prototipo y relación con las lecturas

## Actividades principales

1. **Redacción y revisión:** el estudiante aporta un texto, recibe una corrección localizada con una explicación y decide si la acepta.
2. **Lectura y vocabulario:** puede usar el texto de ejemplo o pegar una lectura propia, consultar una palabra en su contexto, ver ejemplos y guardarla.
3. **Conversación escrita:** practica por chat en un escenario breve, responde a su ritmo y puede pedir una pista.

Las dudas puntuales se envían en el chat de la actividad correspondiente. La conversación se realiza por texto; este prototipo no incluye micrófono, grabación ni evaluación de pronunciación.

## Principios de los artículos que sí se conservan

| Aporte de lectura | Uso en Lingua IA | Por qué ayuda al aprendizaje |
|---|---|---|
| Gu et al., CHI 2024: hacer verificables las respuestas de la IA | Mostrar texto original, propuesta y explicación; permitir aceptar o rechazar | El estudiante compara, comprende el cambio y conserva la decisión. |
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
