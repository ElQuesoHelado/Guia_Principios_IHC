# Relación entre lecturas y decisiones de diseño

La literatura informa las decisiones, pero sus herramientas de análisis de datos no se muestran como funciones de aprendizaje de idiomas.

| Lectura | Idea útil | Aplicación en Lingua IA |
|---|---|---|
| Gu et al., *How Do Analysts Understand and Verify AI-Assisted Data Analyses?* | Hacer que una sugerencia de IA pueda comprobarse. | Tarjetas que muestran el texto original, el cambio propuesto, una explicación y un ejemplo; el estudiante acepta o rechaza. |
| Kazemitabaar et al., *Improving Steering and Verification in AI-Assisted Data Analysis with Interactive Task Decomposition* | Mantener al usuario en control y permitir consultas situadas. | Pistas graduales, consultas en el chat de la tarea y ejemplos adicionales para una palabra seleccionada. |
| LightVA | Dividir una tarea compleja y hacer visible el avance relevante. | Etapas breves y progreso sencillo, contextual a cada actividad. No se exponen relaciones técnicas entre subtareas. |
| WaitGPT | Facilitar la inspección de cambios y la recuperación de versiones. | Comparación por fragmento e historial para retomar una versión anterior. |
| Yang et al. | Diseñar una interacción guiada y transparente para las capacidades simuladas. | Escenarios breves por texto, turnos controlados por el estudiante y pistas opcionales. No hay audio ni evaluación de voz. |

## Decisiones de alcance

Se mantienen tres actividades: redacción, lectura y vocabulario, y conversación escrita. Las dudas se resuelven dentro de la actividad activa, por lo que no existe un cuarto modo de preguntas rápidas.

Se dejan fuera del recorrido del estudiante las ramas, la vista por procedimiento/datos, el gráfico de operaciones, los glifos, la reproducción del análisis, las etiquetas de papers y los controles de protocolo/debriefing. Estos mecanismos explican métodos de los artículos, pero agregan pasos o lenguaje técnico sin ayudar directamente a construir conocimiento del inglés.

La conversación por audio queda fuera de esta versión. La necesidad o preferencia de voz registrada en una entrevista puede mencionarse en el análisis de usuarios, identificándola como hallazgo y diferenciándola del alcance implementado.

## Evidencias de aprendizaje

Las tres actividades añaden notas y producción propia en `js/learning.js`. En el correo se trabaja modelo, plan, borrador, autoevaluación, explicación, revisión y transferencia. Las sugerencias del ejemplo y sus versiones se conservan; no se presentan como análisis del borrador libre. El registro valida presencia de evidencias, no dominio lingüístico.


El apoyo pedagógico es opcional: se accede directamente a correo, lectura o conversación. Las sugerencias están inicialmente ocultas y pueden abrirse u ocultarse en cualquier momento. En el correo, “Ver ejemplos de correo” abre el modelo directamente; Original, Borrador, Versión actual, Ver cambios, Versiones y Deshacer siguen accesibles al cambiar de sugerencia.
