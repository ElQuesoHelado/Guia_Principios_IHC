# Feedback docente para la próxima revisión del HTA

Material recibido el **24 de noviembre de 2026**. Se incorpora como referencia para preparar la siguiente mejora del análisis de tareas y, después, su traducción a la interfaz de Lingua IA.

**Estado:** transcripciones incorporadas; revisión del HTA y propuesta de interfaz pendientes. Este registro no acredita que la profesora haya aprobado el HTA, los documentos o el prototipo actuales.

## Fuentes

| Archivo | Contenido | Última marca de tiempo recibida |
|---|---|---|
| [Audio 1 — Feedback sobre el HTA de correos](01_feedback_hta_correos.md) | Feedback directo al grupo: aprendizaje de inglés, detalle de las tareas, ayuda para formular prompts y raíz del HTA. | 07:41 |
| [Audio 2 — Jerarquía, planes y contexto de uso](02_jerarquia_planes_y_contexto.md) | Explicación sobre objetivo raíz, descomposición, prerrequisitos, alternativas y comportamiento actual del usuario. | 25:17 |
| [Audio 3 — Construcción de conocimiento, prompts y predicción](03_conocimiento_prompts_y_prediccion.md) | Explicación sobre aprendizaje progresivo, continuidad, sugerencias contextuales y derivación de la interfaz desde las tareas. | 27:49 |

La fuente es el texto transcrito que proporcionó el usuario; no se dispone aquí de las grabaciones para comprobarlo. La fecha de la carpeta corresponde a la recepción, no a una fecha confirmada de grabación. Se conservan las marcas de tiempo, los hablantes, las repeticiones, `[ininteligible]` y los fragmentos incompletos, sin completar frases ni corregir el discurso.

Las secciones siguientes son una **síntesis editorial para orientar la revisión**. Las transcripciones enlazadas conservan las palabras atribuidas a cada hablante. Las preguntas de estudiantes, los ejemplos de clase y las interpretaciones de este índice no equivalen a instrucciones aprobadas para el proyecto.

## Observaciones que deben guiar la siguiente mejora

| Observación docente | Referencia | Aplicación propuesta para la revisión, pendiente de desarrollar |
|---|---|---|
| Identificar las partes de un correo no demuestra por sí solo aprendizaje de inglés. Se cuestiona el carácter general de las tareas. | [Audio 1](01_feedback_hta_correos.md), 00:11–02:06; [Audio 3](03_conocimiento_prompts_y_prediccion.md), 10:33. | Describir las dificultades lingüísticas concretas: cómo expresar en inglés el asunto, el saludo, la solicitud o la despedida según la situación; cómo comprender y usar las alternativas. |
| Se pide reducir la cantidad para trabajar con mayor profundidad. | [Audio 1](01_feedback_hta_correos.md), 02:18 y 06:47–06:50; [Audio 2](02_jerarquia_planes_y_contexto.md), 13:47. | Proponer un alcance más concentrado, tomando el correo como candidato principal. No asumir que ya se decidió eliminar las otras actividades ni fijar una cantidad universal de tareas a partir de intervenciones de contextos distintos. |
| Debe existir una tarea raíz y una jerarquía de subtareas conectadas mediante planes. | [Audio 1](01_feedback_hta_correos.md), 06:50; [Audio 2](02_jerarquia_planes_y_contexto.md), 00:31–03:21. | Revisar el objetivo 0, las relaciones entre niveles y la representación gráfica. No resolver el problema únicamente renumerando o añadiendo una raíz demasiado amplia. |
| Los prerrequisitos y planes expresan dependencias, orden y alternativas condicionadas. | [Audio 2](02_jerarquia_planes_y_contexto.md), 04:00–08:23; [Audio 3](03_conocimiento_prompts_y_prediccion.md), 12:38 y 21:40. | Especificar qué información o tarea se necesita antes de otra, cuándo se elige una ruta, cuándo se repite y dónde se reúnen las alternativas. |
| Se analiza cómo el usuario realiza actualmente la tarea, incluidas las tecnologías que ya utiliza; no se parte de lo que hará la aplicación propuesta. | [Audio 2](02_jerarquia_planes_y_contexto.md), 10:32–11:19. | Separar el HTA de la práctica actual sin la solución propuesta y la posterior propuesta de apoyo con IA. Evitar ajustar artificialmente el HTA a los controles del prototipo. |
| Las variantes del contexto y las vías externas también importan, aunque no terminen implementándose todas. | [Audio 2](02_jerarquia_planes_y_contexto.md), 11:49–16:38. | Recoger las formas relevantes de realizar la actividad y justificar después la cobertura de la solución. Los ejemplos de cine ilustran el método; no son tareas que deban copiarse al caso de inglés. |
| Las alternativas y los criterios que procesa el usuario deben explicitarse. Su variedad y cantidad afectan a la interfaz. | [Audio 2](02_jerarquia_planes_y_contexto.md), 17:15–19:08; [Audio 3](03_conocimiento_prompts_y_prediccion.md), 15:35–20:32. | Precisar las alternativas lingüísticas y los criterios de elección del caso estudiado, diferenciando los confirmados de los ejemplos por validar. Evitar listas genéricas que oculten decisiones importantes. |
| El proyecto debe ayudar a construir y afinar prompts mediante sugerencias contextuales mientras el usuario escribe; no basta con trasladar la tarea a formularios o listas de selección. | [Audio 1](01_feedback_hta_correos.md), 02:35–05:36; [Audio 3](03_conocimiento_prompts_y_prediccion.md), 02:56, 07:00–12:38. | Derivar cada sugerencia del contexto y de una necesidad identificada. Explicar qué la activa, qué propone y cómo puede el estudiante utilizarla o descartarla. Esto es una propuesta por diseñar, no una capacidad ya implementada. |
| El destinatario de la solución busca aprender y revisar lo obtenido; la construcción de conocimiento puede extenderse a varias sesiones. | [Audio 3](03_conocimiento_prompts_y_prediccion.md), 00:00–03:21. | Considerar comprensión del feedback, continuidad del contexto y recuperación del trabajo. No presentar la generación de un correo como evidencia suficiente de aprendizaje. |
| Llevar el HTA a la interfaz es un proceso posterior de abstracción: varias tareas pueden representarse en un mismo elemento. | [Audio 2](02_jerarquia_planes_y_contexto.md), 22:01–22:15; [Audio 3](03_conocimiento_prompts_y_prediccion.md), 17:08–17:32. | Mantener trazabilidad entre tareas y apoyo visible sin exigir un botón por subtarea. Justificar agrupación, navegación y orden desde las necesidades analizadas. |

## Trabajo pendiente para otros agentes

1. **Revisar el alcance y el objetivo raíz.** Preparar una propuesta concentrada en el aprendizaje de inglés mediante correos, indicando qué se conserva y qué se posterga respecto a las tres actividades actuales. Mantener esa reducción como propuesta hasta concretarla con el usuario.
2. **Reconstruir la tarea actual con evidencia.** Describir cómo el estudiante resuelve hoy sus dificultades lingüísticas, con los recursos que realmente utiliza. Señalar qué proviene de observación o consulta al usuario y qué falta confirmar; estas grabaciones aportan criterios docentes, no una investigación completa de usuarios.
3. **Descomponer decisiones y acciones significativas.** Sustituir etiquetas demasiado generales por acciones que permitan entender el trabajo lingüístico y sus alternativas. La profundidad debe servir al análisis; añadir números o cambiar la indentación por sí solo no resuelve las observaciones.
4. **Redactar los planes de las tareas descompuestas.** Referenciar sus identificadores y explicitar secuencia, condiciones, opciones, repetición y retorno. Distinguir condiciones de entrada de instrucciones sobre cómo combinar las subtareas.
5. **Derivar la ayuda contextual para prompts.** Proponer, para cada necesidad, el contexto que permite sugerir una expresión o refinar una consulta, la aportación al aprendizaje y el control del usuario. Distinguir esta propuesta del HTA sin la solución.
6. **Preparar la correspondencia con la interfaz.** Relacionar tarea y subtarea con el apoyo propuesto; al contrastar el prototipo, indicar si está representado, simulado o pendiente y citar el elemento real que lo respalda. No inventar capacidades para cerrar la matriz.
7. **Revisar continuidad y evidencias de aprendizaje.** Plantear cómo se retoma una sesión y cómo se comprueba que el estudiante comprende y puede reutilizar lo aprendido, diferenciando esas propuestas del comportamiento actual.

Como formato de revisión, se propone registrar cada hallazgo con: **fuente y tiempo → tarea afectada → problema → cambio propuesto → evidencia o duda pendiente → efecto previsto en la interfaz**. Este formato es editorial, no una plantilla dictada por la profesora.

## Límites de interpretación

- **Instrucciones docentes:** atribuirlas a un audio y a sus marcas de tiempo. Conservar las expresiones incompletas o ambiguas en la fuente y señalar las dudas en la revisión.
- **Evidencia del usuario:** no convertir ejemplos de clase ni afirmaciones generales sobre estudiantes en hábitos observados de nuestros usuarios.
- **Decisiones de diseño:** separar de la transcripción las opciones de alcance, los ejemplos de inglés, la arquitectura, el almacenamiento y la forma de presentar las sugerencias. Deben justificarse en la siguiente propuesta.
- **Resultados:** la intención de reducir consultas, tokens o carga cognitiva no demuestra una reducción medida. No afirmar ahorros, mejora de aprendizaje o validación de usabilidad sin evidencia.
- **Documentación anterior:** el HTA, los PDF, las matrices y las guías previas permiten entender el estado del trabajo; no sustituyen este feedback ni acreditan aprobación docente. Contrastar cada afirmación sobre funcionamiento con el código de la rama que se esté revisando.

En esta incorporación documental se guardan las fuentes y la guía de revisión. La modificación del HTA, de la interfaz y de los entregables de presentación corresponde a la siguiente iteración.
