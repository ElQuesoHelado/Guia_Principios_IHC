# Revisión del HTA y traducción a la interfaz

## Acciones del HTA e infinitivos · 26/11/2026

Por instrucción del usuario, cada título del HTA v8 empieza con un verbo en infinitivo y nombra una sola acción. Las operaciones antes reunidas en una frase se descomponen en hijos con un plan específico. Por ejemplo, la reformulación de una interpretación comprende ahora comparar la hipótesis, explicar el significado y conservar las incertidumbres en subtareas distintas. Las condiciones y decisiones de recorrido se expresan en los planes.

Se conservan las dos actividades y los identificadores anteriores; los nuevos nodos son descendientes de la operación correspondiente. La profundidad responde a las acciones del proceso, sin imponer igual cantidad de niveles en todas las ramas. La correspondencia de la interfaz con los grupos principales sigue siendo válida, sin atribuirle cobertura automática de cada nuevo nodo. Esta revisión actualiza el PDF y el Word del HTA; no modifica el prototipo ni la matriz de principios.

## Generalización del HTA v8 · 26/11/2026

Por instrucción del usuario, el árbol y los planes describen el proceso del estudiante ante contenido y recursos del inglés que pueden ser desconocidos. Se retiran las tareas ligadas a frases, nombres, fechas, errores o palabras ya elegidos. Se mantienen dos actividades diferenciadas: aprender inglés mediante correos y aprender vocabulario en contexto.

El análisis contempla partir de una necesidad propia, un correo recibido, una consigna o un borrador. Reconocer lo que no comprende precede a buscar una explicación; no se presupone que el estudiante sepa nombrar la construcción o elegir la acepción. Los planes contemplan recuperar lo conocido, consultar recursos disponibles, ampliar contexto, contrastar respuestas, intentar un uso y volver a lo que sigue incierto. Puede conservar una expresión que ya comprende, omitir una ayuda innecesaria o dejar una duda pendiente cuando no haya respaldo suficiente.

Las vías de consulta se apoyan en el perfil anterior; su disponibilidad, elección y secuencia necesitan contraste con usuarios. El análisis no afirma que todas las personas sigan los mismos pasos. Explicar, recuperar y transferir son actividades propuestas para examinar el aprendizaje, no costumbres universales acreditadas.

La interfaz conserva sus casos preparados como ilustraciones particulares. La correspondencia siguiente identifica qué parte del proceso general muestran; las expresiones concretas pertenecen a la demo y no definen el contenido del HTA. No se modificó la interfaz en esta generalización documental.

## Ampliación de la interfaz según v8 · 26/11/2026

El objetivo de esta iteración es aprender recursos del inglés mediante tareas comunicativas. El correo sitúa la práctica; completar sus partes no basta como evidencia. El HTA v8 se conserva con sus dos árboles relacionados y no se presenta como resolución del pedido docente de una raíz única ni como análisis validado con usuarios.

| Nodos del v8 | Apoyo implementado en el chat | Evidencia y límite |
|---|---|---|
| C1.1; C3.1 | `email-lesson` con `data-topic="subject"` | Contraste de `request for` y `question about`, vocabulario del material/plazo y producción explicada. No verifica semánticamente datos de un asunto arbitrario. |
| C1.2; C3.2 | `email-lesson` con `data-topic="greeting"` | Contrasta `Dear`, `Hi` y formas de tratamiento sin inventar nombres o títulos. No determina automáticamente la relación real. |
| C2; C3.3 | `email-lesson` con `data-topic="request"` y comparación de peticiones | Modal, sujeto y verbo; material, plazo y aclaración. La persona explica quién pide qué; no hay evaluación gramatical general. |
| C3.4 | `email-lesson` con `data-topic="reason"` | Contrasta `because + oración` y `to + verbo`, con razón/finalidad explicadas y variantes propias. Los datos son ejemplos identificados. |
| C3.5 | `email-lesson` con `data-topic="closing"` | Función de `Best regards` y `Thanks`; elección explicada según contexto. No impone una equivalencia universal con formalidad. |
| C5 | `.language-attempt`; `email-practice`; `write`; versiones | Producción y explicación en el mismo chat; contraste y reformulación voluntarios. Practicar una expresión conserva el borrador aparte. La revisión automática mantiene solo las reglas acotadas anteriores. |
| C6–C7 | `recall`, `transfer`, `stage`, `notebook`, `history`, `export` | Recuperación y transferencia del mismo recurso, tema guardado y apoyo consultado identificado. Abrir ejemplos no añade evidencia; los intentos no se califican ni prueban retención duradera. |
| V1–V7 | Lectura, hipótesis, fichas contextuales, producción, recuperación y repaso existentes | Se mantiene la práctica preparada de `dedicated`, `productive` y `deadline`; otros contextos requieren contraste externo. No se añade un diccionario en vivo. |

Las sugerencias de `suggest()` priorizan, ante una consulta temática reconocida, comparar significado y estructura del recurso. Se añaden como texto editable y no se envían automáticamente. Se mantiene la navegación libre, un único compositor, apoyos opcionales y el inicio vacío. Las consultas nuevas pueden abrir otro apoyo mientras hay un intento pendiente; no se registran como una producción de aprendizaje.

La implementación no cubre todas las alternativas del HTA: las rutas de consulta con otras personas, traductores o IA externa siguen fuera de esta demo; tampoco hay evaluación automática de una producción arbitraria. La correspondencia se comprueba mediante recorridos en Firefox a 1440, 390 y 320 px, incluidos borrador conservado, tema de recuperación y ayuda registrada. Esto es verificación funcional, no evidencia experimental de aprendizaje.

## Revisión anterior del v7 · 25/11/2026

Las secciones siguientes conservan la evaluación y numeración del v7; no describen por sí solas la cobertura actual del v8.

Fecha: 25/11/2026. Fuentes: `HTA_unificado_sin_IA_v7.pdf` (usuarios p. 1; correo pp. 2–4; vocabulario pp. 8–10) y las transcripciones de `feedback_docente/2026-11-24/`. No se modificaron los PDF de entrada. Esta revisión no equivale a aprobación docente.

## Dictamen

El HTA v7 **sí se orienta a construir conocimiento**, pero **todavía no cumple el conjunto de observaciones docentes**. Incluye inferencia, explicación, contraste, producción, recuperación y transferencia. Sin embargo, mantiene **tres raíces independientes** frente al pedido explícito de una sola raíz conectada con subtareas y planes; faltan planes, alternativas lingüísticas concretas y representación suficiente de cómo trabaja actualmente el usuario.

**Corrección de esta revisión:** la versión anterior consideraba aceptable presentar dos HTA independientes y trataba la ausencia de IA como una separación correcta sin más condiciones. Esa lectura fue demasiado permisiva frente al Audio 1, 06:50, y al Audio 2, 11:04–11:19. El análisis debe ser independiente de la solución propuesta, pero debe incluir las tecnologías que el usuario ya utiliza, incluso IA si corresponde a su práctica actual. Las propuestas complementarias y las cuatro etapas de la interfaz **no corrigen por sí solas el PDF v7**.

Se seleccionan la tarea 1 (correo) y la tarea 3 (vocabulario), por instrucción del usuario. La conversación escrita de la tarea 2 queda fuera de esta iteración. Para localizar los hallazgos se cita la numeración original de esas dos actividades; `C` y `V` son prefijos documentales, no una renumeración ni una recomendación de mantener raíces desconectadas.

## Contraste con la profesora

| Fuente | Hallazgo en v7 | Resolución y límite |
|---|---|---|
| Audio 1, 00:11–02:06; Audio 3, 10:33 | La redacción incorpora registro, modales y justificación; supera identificar partes genéricas. | Comparación de igual intención con distinto destinatario; diferencia explícita entre gramática y cortesía. Falta observar si el estudiante comprende esa diferencia. |
| Audio 1, 02:18 y 06:47–06:50 | Tres tareas amplias. | Se implementan dos; correo tiene mayor profundidad. No se atribuye esta selección exacta a la profesora. |
| Audio 1, 06:50; Audio 2, 00:31–03:21 | Hay una raíz 0 por actividad, jerarquía hasta nivel 3. | No satisface el pedido de una raíz única para el análisis presentado como unificado. Hay raíces 0 en pp. 2, 5 y 8, sin plan común ni conexiones de retorno entre actividades. El PDF presenta listas jerárquicas, no un árbol unificado. |
| Audio 2, 04:00–08:23; Audio 3, 12:38 y 21:40 | Correo: planes 0, 2, 6 y 7; vocabulario: 0, 3, 6 y 7. | Los planes faltantes siguen ausentes del PDF. Los complementos de este documento son propuestas separadas y no acreditan que se haya corregido la fuente. También faltan planes explícitos para las descomposiciones de niveles inferiores. |
| Audio 2, 10:32–11:19 | Precondiciones sin IA y caracterización que menciona traductores, diccionario e IA. | La caracterización menciona IA y traductores, pero las tareas no describen esas rutas actuales. No basta con excluir la solución propuesta: deben documentarse las herramientas y decisiones que ya usa el estudiante, con su evidencia y sus puntos de retorno. |
| Audio 2, 11:49–19:08 | Hay excepciones, pero no un inventario completo de alternativas reales. | Se demuestran dos relaciones de confianza y tres palabras. No cubren todos los correos, niveles ni acepciones. |
| Audio 1, 02:35–05:36; Audio 3, 07:00–12:38 | El HTA no debe describir los controles futuros, pero tampoco explicita suficientemente las alternativas lingüísticas y las dificultades de consulta actuales. | Se necesita una derivación posterior desde tarea, condición y alternativa hacia una sugerencia. Las reglas implementadas son una demostración parcial; no prueban que el análisis del PDF sea completo. |
| Audio 3, 00:00–03:21 | Recuperación y transferencia están en el objetivo. | Se conservan notas y versiones en localStorage. El repaso posterior se inicia manualmente; no se simulan sesiones pasadas. |
| Audio 2, 22:01–22:15; Audio 3, 17:08–17:32 | Muchas acciones no requieren controles separados. | Un único chat recoge hipótesis, redacción y explicación; cuatro sugerencias de ruta agrupan siete grupos del HTA. |

Las marcas de tiempo son de las transcripciones suministradas, no de grabaciones verificadas. Los escenarios de demostración son decisiones de diseño; no son observaciones de usuarios.

## Hallazgos concretos de la segunda revisión

Esta sección contrasta el PDF original con las transcripciones, sin usar las funciones de la interfaz como prueba de corrección del HTA. `C` identifica correo y `V` vocabulario; ambos conservan aquí su numeración original.

### 1. Una raíz para el análisis unificado: no resuelto

**Fuente:** [Audio 1, 06:50](feedback_docente/2026-11-24/01_feedback_hta_correos.md), reforzado por Audio 2, 00:31–03:21. La profesora dice: «es una sola tarea raíz» y señala que las tareas independientes no se comunican mediante planes.

**En el PDF:** la p. 2 comienza con `0. Aprender expresiones para correos en inglés`; la p. 5 vuelve a `0. Aprender recursos de conversación escrita en inglés`; la p. 8 vuelve a `0. Aprender vocabulario en contexto`. No hay un objetivo 0 común ni un plan que establezca cómo una duda de vocabulario interrumpe y luego permite retomar el correo. El Plan V7 menciona usar vocabulario en un correo o diálogo, pero no enlaza sus identificadores con las tareas de otra raíz.

Presentar un HTA por actividad puede documentar análisis separados; no demuestra que se haya resuelto el pedido de una raíz única para este trabajo unificado.

**Corrección requerida:** concentrar el análisis y representar las tareas elegidas bajo una raíz concreta con sus relaciones. No basta con añadir un título amplio como «aprender inglés». Como ejemplo de delimitación por validar, «Aprender a comprender y utilizar expresiones en correos académicos en inglés» permite relacionar comprensión léxica y producción escrita. Debe explicarse cómo se cubre la práctica de vocabulario que se quiera conservar; no se puede introducir esa raíz solo para hacer coincidir la interfaz existente.

### 2. Planes: existen, pero la cobertura es incompleta

**Fuente:** [Audio 2, 04:00–08:23](feedback_docente/2026-11-24/02_jerarquia_planes_y_contexto.md); Audio 3, 12:38 y 21:40. Los planes deben expresar secuencia, condiciones, alternativas y dependencias también en los niveles descompuestos.

| Actividad del PDF | Planes escritos | Grupos de primer nivel sin plan |
|---|---|---|
| Correo, p. 4 | 0, 2, 6 y 7 | 1, 3, 4 y 5 |
| Vocabulario, p. 10 | 0, 3, 6 y 7 | 1, 2, 4 y 5 |
| Conversación, p. 7; fuera del alcance activo | 0, 5, 6 y 7 | 1, 2, 3 y 4 |

Además, no aparecen planes específicos para nodos como C2.2, C4.2, V2.3 o V3.1 que tienen sus propias subtareas. La numeración y el orden de una lista no explican por sí solos qué pasa cuando no se conoce el destinatario, varias acepciones encajan o la primera explicación no se comprende.

Los planes existentes sí aportan condiciones útiles: C2 evita asociar formalidad con palabras difíciles; V3 contempla varias acepciones; C6/V6 contemplan dificultades de recuperación. Se deben conservar y conectar con el resto.

### 3. Alternativas lingüísticas para sugerir: aún demasiado generales

**Fuente:** [Audio 1, 01:20 y 02:35–05:36](feedback_docente/2026-11-24/01_feedback_hta_correos.md); [Audio 3, 10:33–12:38 y 20:32](feedback_docente/2026-11-24/03_conocimiento_prompts_y_prediccion.md).

**Correo:** C2.2 dice clasificar saludos y despedidas; C4.2 dice elegir un saludo e incorporar un cierre. No precisa las expresiones en inglés entre las que el usuario decide ni las señales de relación que justifican elegirlas. C3.2 menciona un modal, pero no especifica las construcciones que se comparan. C4.3 menciona una expresión conocida sin identificar los recursos para conectar motivo y petición. **No se incluye el asunto del correo**, pese a que la profesora lo señala expresamente en Audio 1, 02:35.

Como ejemplos de detalle pendiente —propuestas didácticas, no alternativas observadas— se pueden contrastar saludos con nombre conocido o tratamiento pertinente, fórmulas como `Can you…?` y `Could you please…?`, y asuntos que expresen con claridad una solicitud académica concreta. Hay que explicar qué cambia, por qué y cuándo conservar la expresión inicial. Dos ejemplos no constituyen un inventario exhaustivo de formalidad.

**Vocabulario:** V3.1–V3.3 describen comparar y descartar acepciones, pero no concretan las alternativas y pistas del caso elegido; V4.2 requiere notas de registro sin establecer qué hacer si el diccionario no proporciona ninguna. V5.1–V5.2 deben precisar qué combinaciones y estructuras se examinan dentro del caso. La regla «si no hay etiqueta fiable, no atribuir registro» aparece como complemento propuesto, no como plan del PDF.

### 4. Algunos niveles añaden numeración, pero poco detalle

**Fuente:** Audio 2, 01:48–03:21 y 17:15–19:08; Audio 3, 20:32–22:55.

Por ejemplo, V2.1 «Localizar una palabra relevante de significado desconocido» se descompone en V2.1.1 «Localizar una expresión de significado desconocido» y V2.1.2 «Valorar su relevancia». Esa rama sí separa dos operaciones, pero la primera casi repite el nodo padre y la segunda no aclara el criterio: ¿la palabra impide comprender la idea principal, cambia la petición o se necesita para una producción propia? En V6.1.1, «evocar la palabra» tampoco explica las pistas o vías de recuperación del caso.

Esto no invalida todos los nodos cognitivos: la profesora pide describir lo que el usuario procesa. El problema es detener la descomposición en frases generales que todavía no permiten decidir qué ayuda sería pertinente. No se necesita dar a todas las ramas la misma profundidad ni dividir cada una obligatoriamente en dos hijos.

### 5. Práctica actual y propuesta pedagógica: deben distinguirse

**Fuente:** [Audio 2, 10:32–11:19 y 13:47](feedback_docente/2026-11-24/02_jerarquia_planes_y_contexto.md).

La p. 1 afirma que en las entrevistas aparecen traductores, diccionarios e IA. Sin embargo, los árboles se formulan como una práctica ideal con modelos, apuntes y otras personas, bajo el rótulo «sin IA generativa». No hay una ruta para comparar una traducción, pedir a una IA ya utilizada un ejemplo o afinar una consulta cuando la respuesta resulta ambigua. Tampoco se identifica qué secuencias están observadas y cuáles son propuestas de enseñanza.

La indicación docente permite incluir tecnología existente; lo que se debe evitar es describir de antemano los controles del nuevo prototipo. Antes de añadir rutas, comprobar cuáles están respaldadas por las entrevistas originales. No inventar hábitos ni convertir los ejemplos de clase en evidencia del grupo de usuarios.

### 6. Perfil y continuidad: alineación parcial

**Fuente:** Audio 3, 00:00–03:21.

La caracterización B1–B2 y sus dificultades de gramática, registro y vocabulario son pertinentes para el caso. No obstante, la p. 1 también incluye resolver una tarea rápidamente entre las actitudes posibles. Conviene delimitar explícitamente que el destinatario de esta solución quiere comprender, revisar y reutilizar lo obtenido, sin equiparar toda rapidez con falta de interés.

C6–C7 y V6–V7 sí modelan recuperación, transferencia y dudas posteriores. En particular, V7.4 contempla otro momento de repaso: es un acierto. Falta detallar cómo retoma el estudiante la situación anterior, identifica lo ya comprendido y decide qué duda continuar. Esto pertenece a la continuidad del trabajo, no exige escribir «localStorage» o nombres de controles en el HTA.

### Qué conservar y qué corregir primero

- **Conservar:** objetivos lingüísticos; comparación de igual intención y distinto registro; distinción entre gramática y tono; hipótesis antes del contraste; producciones propias; recuperación y transferencia. Son coherentes con la construcción de conocimiento que pide la profesora.
- **Primero:** resolver raíz, alcance y conexión entre correo y vocabulario. La conversación puede identificarse como material previo o fuera de alcance; no debe quedar como una tercera raíz activa sin explicación.
- **Después:** completar planes de los nodos descompuestos y concretar alternativas, criterios y retornos dentro de los casos seleccionados, incluido el asunto del correo si se mantiene el alcance de aprendizaje de correos completos.
- **A continuación:** distinguir recorridos actuales respaldados por usuarios de propuestas pedagógicas; representar la jerarquía y los planes de forma legible.
- **Finalmente:** derivar sugerencias de consulta desde esas tareas y condiciones. La profesora pide la predicción como traducción posterior del análisis; el HTA base no necesita convertirse en un conjunto de botones o pasos de implementación.

Las cuatro etapas de la interfaz son una agrupación de presentación. No sustituyen los planes del HTA ni demuestran que se haya resuelto su raíz. Esta revisión identifica cambios pendientes; **no modifica ni da por corregido el PDF original**.

## Planes complementarios propuestos para la práctica sin la solución

Se conservan los planes del PDF. Lo siguiente propone planes para algunos grupos sin plan, pendientes de validación e incorporación al HTA revisado. No resuelve las raíces separadas, las alternativas ausentes ni todos los planes de niveles inferiores. No introduce controles de interfaz en el análisis de la tarea actual.

### Correo

- **Plan C1:** realizar C1.1 sobre la petición principal, C1.2 sobre la relación y C1.3 sobre la función de cada fragmento. Si no se conoce al destinatario, buscar señales en saludo, propósito y contexto; mantener la relación como incierta si faltan datos. Terminar con una intención y una relación justificadas.
- **Plan C3:** realizar C3.1 antes de consultar; en C3.2 relacionar el modal con la petición; contrastar en C3.3 con modelo o diccionario; reformular en C3.4. Si no hay equivalencia, volver a las pistas y consultar otro ejemplo. No asumir que una traducción aislada confirma el uso.
- **Plan C4:** precisar necesidad y redactar C4.1; elegir saludo/cierre en C4.2 según la relación ya identificada; articular motivo y petición en C4.3. Si falta una expresión, consultar un recurso puntual de C3 y volver a la producción. Terminar con un correo propio, aunque queden dudas para C5.
- **Plan C5:** alinear el fragmento y alternativa en C5.1; contrastar la regla o registro en C5.2; justificar en C5.3 y reformular en C5.4 solo si corresponde a la intención. Si no se comprende el cambio, solicitar un ejemplo o explicación y repetir el contraste. Se puede conservar una frase gramatical cuando su tono sea pertinente.

### Vocabulario

- **Plan V1:** relacionar el título con una experiencia en V1.1, considerar fuente y destinatario en V1.2 y comprobar el tema leyendo V1.3. Si el texto resulta demasiado difícil, elegir uno de dificultad próxima. Mantener como incierto lo que la fuente no permita inferir.
- **Plan V2:** localizar una expresión relevante en V2.1; examinar pistas en V2.2; proponer significado en V2.3 y justificar en V2.4 antes de V3. Si no hay pistas suficientes, ampliar la oración o consultar otra fuente; se permite registrar que no se pudo inferir.
- **Plan V4:** comparar ejemplos de la misma acepción en V4.1; consultar etiquetas explícitas de uso en V4.2; distinguir registro de cambio de significado en V4.3; justificar situación y destinatario en V4.4. Si no hay una etiqueta fiable, dejar el registro sin determinar en vez de inventarlo.
- **Plan V5:** observar combinaciones en V5.1, relacionarlas con su estructura en V5.2 y sintetizar significado/contexto/uso en V5.3; explicar la anotación con palabras propias en V5.4. Si los ejemplos no sostienen el patrón, buscar otro y repetir antes de memorizar una generalización.

**Regla para todos los nodos de tercer nivel:** cuando el PDF descompone un nodo en `.1` y `.2`, se propone realizar primero la localización/identificación y después la explicación/producción indicada, sobre el mismo fragmento; volver a `.1` si `.2` no tiene respaldo. Esa regla es una hipótesis de secuencia y no sustituye los planes específicos ni permite declarar completa la jerarquía. Las condiciones, alternativas y retornos deben detallarse por nodo y validarse con la práctica del usuario. Los planes de grupo anteriores y los del PDF tienen prioridad sobre esta regla general.

## Correspondencia con la interfaz implementada

| Grupo del HTA | Interacción / selector real | Evidencia o límite |
|---|---|---|
| C1: intención, relación y función | Consulta libre; `#prompt-assist`; `[data-action="model"]` | La intención/destinatario proceden del mensaje. El modelo explica saludo, petición y cierre; no hay extracción semántica general. |
| C2: registro y cortesía | `[data-action="compare"]`, `.comparison` | Misma petición a compañero y profesora. El estudiante escribe una explicación; no se clasifica automáticamente su corrección. |
| C3: inferencia y modales | Modelo y explicación junto al fragmento; `.rule` | Función de could y relación con intención. No hay diccionario en vivo ni evaluación de una paráfrasis arbitraria. |
| C4: producción propia | `[data-action="write"]`, `#chat-input`, `.doc-text` | Producción libre conservada como versión; no hay casillas de saludo, propósito o fecha. |
| C5: comprender feedback | `.correction-card`, `.diff-line`; `accept`, `reject`, `justify`, `undo-correction` | Reglas acotadas: I am agree y peticiones con I want you to send me / Send me. Cambios locales; otros textos quedan por revisar. |
| C6: recuperar | `[data-action="recall"]`, `#recall-banner` | Oculta material anterior visualmente y para tecnología de asistencia. Si se abre apoyo queda registrado. No impide consultar fuera de la página. |
| C7: transferir | `[data-action="transfer"]` | Producción a compañero de confianza frente al ejemplo con profesora; explicación y dudas quedan en el chat. |
| V1: activar lectura | `.reading-card` | Fuente y destinatario del texto didáctico explícitos; título, texto y conversación. Cobertura parcial de conocimientos previos. |
| V2: inferir | `.word-chip`, `[data-action="clue"]`; mensaje de hipótesis | Pista contextual e hipótesis opcional. Consultar directamente sigue permitido. |
| V3: contrastar | `.word-detail`, `.diff-line` | Hipótesis junto a acepción del ejemplo y contraste con otro uso. Contextos propios no reciben automáticamente la acepción preparada. |
| V4: significado y registro | `.word-detail .rule` | Ejemplos distinguen sentidos; no se atribuye formalidad sin fuente. No incluye etiquetas de un diccionario: cobertura parcial. |
| V5: patrones y anotación | `vocab-explain`, `save-word`, ficha de patrón | Explicación libre y palabra para repasar. No se evalúa el patrón ni se obliga a completar una ficha. |
| V6: recuperar | `recall`, `reveal-support`, `.recall-hidden` | Oración/explicación propia, registro de ayuda y contraste posterior. No se califica gramática arbitraria. |
| V7: transferir y repasar | `transfer`, `repaso`, historial por tarea | Otra situación, fecha de aporte y repaso manual. La separación temporal depende del estudiante; no hay calendario ni evaluación longitudinal. |

## Reglas de sugerencias mientras se escribe

Implementación: `detect()` y `suggest()` en `js/tutor.js`. No se envía texto a servicios externos.

| Contexto detectado | Sugerencia opcional | Dependencia que la justifica |
|---|---|---|
| Correo sin relación identificada | Comparar cómo cambia la petición según la confianza | C1.2 → C2 |
| Correo con destinatario y sin petición de contraste | Comparar dos formas de pedir y explicar tono | C2.1–C2.3 |
| Correo con contraste ya pedido | Cambiar solo el fragmento revisado | C5.1–C5.4 |
| Palabra sin oración indicada | Pedir contexto antes de elegir acepción | V2 → V3 |
| Palabra con oración, sin inferencia solicitada | Pista antes de definición | V2.3 → V3.4 |
| Consulta léxica con inferencia | Probar una oración propia y otro contexto | V6 → V7 |
| Mensaje insuficiente o ambiguo | Conservarlo y preguntar actividad | Evitar inventar una intención |

“Añadir” y “Editar” colocan texto editable en el mismo mensaje, sin enviarlo; “Descartar” no altera el texto; “Deshacer” restaura el mensaje si no hubo escritura posterior. Las sugerencias pueden ignorarse y no son prerrequisitos para continuar. Las reglas no completan nombres, fechas, motivos ni relaciones que el usuario no haya aportado.

## Qué falta validar

Entrevistas y observación de los recorridos actuales, amplitud de alternativas lingüísticas, diagrama HTA contrastado, comprensión de las sugerencias, retorno tras días de separación y efecto sobre independencia. Para estudiar reducción de prompts, comparar tareas equivalentes con/sin sugerencias: consultas enviadas, reformulaciones, pertinencia de la respuesta y explicación/transferencia propia. Menos mensajes por sí solos no implica mejor aprendizaje. Esta entrega no afirma un ahorro medido ni una validación experimental.
