# Correspondencia por nodo · HTA v8

Fuente: [HTA_correo_vocabulario_v8.pdf](../HTA_correo_vocabulario_v8.pdf), sin modificaciones. Esta tabla usa extractos breves como rótulos; el texto completo y los planes están en la fuente.

Los 29 planes y las 80 hojas se relacionan con un escenario ejecutable del mock. No se crea un control por cada identificador. Las consultas externas se registran sin fingir conexiones ni verificación; los ejemplos internos son preparados. La cobertura técnica no certifica aprendizaje ni aprobación docente.

Prueba: [test_hta_complete.py](../tools/test_hta_complete.py). El test ejecuta interacciones y condiciones y comprueba que no falte ningún identificador del [catálogo](hta-v8-coverage.json).

## Planes y nodos descompuestos

| ID | Extracto identificador de la fuente | Apoyo / comportamiento | Selector de acceso | Escenario de prueba |
|---|---|---|---|---|
| C0 | Aprender a comprender y redactar peticiones en correos académicos en inglés | Correo completo y consulta con retorno | `[data-action="hta-return"]` | `email-link` |
| C1 | Precisar la intención, la relación y | Intención, relación, datos y dudas | `[data-action="hta-situation"]` | `email-context` |
| C1.1 | Delimitar qué respuesta se necesita del destinatario | Intención, relación, datos y dudas | `[data-action="hta-situation"]` | `email-context` |
| C2 | Comprender y comparar expresiones de | Modelos de igual intención y explicación propia | `[data-action="compare"]` | `email-models` |
| C3 | Elegir expresiones según intención y | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.1 | Formular un asunto informativo en inglés | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.2 | Elegir un saludo acorde con la relación y la información disponible | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.3 | Elegir una petición comprensible que conserve la intención | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.5 | Elegir un cierre coherente con el resto del correo | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C4 | Resolver una duda mediante los recursos disponibles | Fragmento, vías de consulta y retorno | `[data-action="hta-resources"]` | `resources` |
| C4.2 | Elegir una vía de consulta ya disponible para el estudiante | Fragmento, vías de consulta y retorno | `[data-action="hta-resources"]` | `resources` |
| C5 | Redactar un correo propio y comprender | Revisión localizada, datos, decisión y explicación | `[data-action="hta-review-fragment"]` | `email-review` |
| C5.2 | Clasificar una diferencia entre el fragmento propio y una alternativa | Revisión localizada, datos, decisión y explicación | `[data-action="hta-review-fragment"]` | `email-review` |
| C5.3 | Decidir sobre el fragmento sin perder las partes que funcionan | Revisión localizada, datos, decisión y explicación | `[data-action="hta-review-fragment"]` | `email-review` |
| C6 | Recuperar expresiones y transferirlas | Recuperación, otra relación y comparación | `[data-action="hta-productions"]` | `email-transfer` |
| C7 | Cerrar y retomar el aprendizaje del | Cierre parcial, dudas y continuidad | `[data-action="hta-resume-plan"]` | `continuity` |
| V0 | Aprender a comprender y reutilizar vocabulario en contexto académico | Vocabulario completo y regreso al correo | `[data-action="hta-return"]` | `vocab-link` |
| V1 | Situar la lectura y seleccionar una | Lectura, relevancia y oración exacta | `[data-action="hta-reading-note"]` | `reading` |
| V2 | Proponer una hipótesis mediante pistas | Pistas reales, hipótesis opcional y contexto insuficiente | `[data-action="hta-lexical-tools"]` | `inference` |
| V2.2 | Buscar pistas que sostengan una interpretación | Pistas reales, hipótesis opcional y contexto insuficiente | `[data-action="hta-lexical-tools"]` | `inference` |
| V3 | Contrastar acepciones y corregir la | Fuentes, acepciones e interpretación propia | `[data-action="hta-interpret"]` | `senses` |
| V3.1 | Elegir un recurso para contrastar el significado en la oración | Fuentes, acepciones e interpretación propia | `[data-action="hta-interpret"]` | `senses` |
| V3.3 | Decidir qué interpretación tiene apoyo contextual | Fuentes, acepciones e interpretación propia | `[data-action="hta-interpret"]` | `senses` |
| V4 | Distinguir significado, registro y patrones de uso | Registro, patrón y anotación | `[data-action="hta-register-note"]` | `lexical-note` |
| V4.2 | Determinar qué puede afirmarse del registro a partir de la fuente | Registro, patrón y anotación | `[data-action="hta-register-note"]` | `lexical-note` |
| V5 | Producir una oración propia y | Producción, conservación, reformulación o sustitución | `[data-action="hta-vocab-write"]` | `vocab-production` |
| V5.3 | Decidir cómo conservar la intención de la oración | Producción, conservación, reformulación o sustitución | `[data-action="hta-vocab-write"]` | `vocab-production` |
| V6 | Recuperar la expresión y transferirla | Recuperación, transferencia y correo vinculado | `[data-action="hta-transfer-email"]` | `vocab-transfer` |
| V7 | Registrar y retomar el vocabulario en | Entrada por contexto, repaso elegido y pendientes | `[data-action="hta-entry-recall"]` | `review` |

## Hojas: acciones y decisiones

| ID | Extracto identificador de la fuente | Apoyo / comportamiento | Selector de acceso | Escenario de prueba |
|---|---|---|---|---|
| C1.1.1 | Pedir apuntes o material: identificar exactamente el material que se necesita. | Intención, relación, datos y dudas | `[data-action="hta-situation"]` | `email-context` |
| C1.1.2 | Pedir más tiempo: distinguir la fecha vigente de la fecha que se quiere proponer. | Intención, relación, datos y dudas | `[data-action="hta-situation"]` | `email-context` |
| C1.1.3 | Aclarar una entrega: precisar la duda concreta sobre fecha o forma de presentación. | Intención, relación, datos y dudas | `[data-action="hta-situation"]` | `email-context` |
| C1.2 | Distinguir compañero de confianza, docente o persona de relación desconocida; comprobar | Intención, relación, datos y dudas | `[data-action="hta-situation"]` | `email-context` |
| C1.3 | Recuperar una expresión conocida y señalar qué no se sabe expresar: asunto, saludo, petición, | Intención, relación, datos y dudas | `[data-action="hta-situation"]` | `email-context` |
| C2.1 | Localizar qué se solicita y qué información expresa motivo, material o plazo en un modelo del | Modelos de igual intención y explicación propia | `[data-action="compare"]` | `email-models` |
| C2.2 | Alinear peticiones de igual intención a un compañero y a un docente para localizar diferencias | Modelos de igual intención y explicación propia | `[data-action="compare"]` | `email-models` |
| C2.3 | Explicar con palabras propias qué aportan can, could y please a la petición, sin confundir | Modelos de igual intención y explicación propia | `[data-action="compare"]` | `email-models` |
| C3.1.1 | Expresar el material solicitado: “Request for lecture notes”. | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.1.2 | Expresar la solicitud de plazo: “Request for an extension until Friday”. | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.1.3 | Expresar la duda de entrega: “Question about the submission deadline”. | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.2.1 | Usar “Dear Professor Rivera,” si se conoce que ese es el tratamiento y apellido pertinentes. | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.2.2 | Usar “Dear Alex Rivera,” como opción con nombre completo conocido, sin atribuir un | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.2.3 | Usar “Hi Alex,” cuando la cercanía y el uso habitual de nombres lo permiten. | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.2.4 | Comprobar cómo se identifica el destinatario si no se conoce su nombre o tratamiento; | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.3.1 | Pedir material con una fórmula directa entre personas de confianza: “Can you send me | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.3.2 | Pedir el mismo material con una alternativa más cortés: “Could you please send me the | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.3.3 | Pedir permiso para otro plazo: “Could I have an extension until Friday?”. | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.3.4 | Aclarar una fecha: “Could you please confirm the submission deadline?”. | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.4 | Conectar motivo y petición mediante una razón pertinente: “I need more time to review my | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.5.1 | Considerar “Best regards,” como despedida habitual en correspondencia académica o pro- | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C3.5.2 | Considerar “Thanks,” cuando el agradecimiento breve encaja con la relación y la petición. | Alternativas de asunto, saludo, petición, motivo y cierre | `[data-action="hta-parts"]` | `email-parts` |
| C4.1 | Aislar la frase dudosa, conservar su contexto y precisar si la duda afecta al significado, a la | Fragmento, vías de consulta y retorno | `[data-action="hta-resources"]` | `resources` |
| C4.2.1 | Consultar un diccionario o un modelo para comprobar significado, construcción y ejemplos. | Fragmento, vías de consulta y retorno | `[data-action="hta-resources"]` | `resources` |
| C4.2.2 | Contrastar una traducción con la oración original para detectar pérdidas de intención o | Fragmento, vías de consulta y retorno | `[data-action="hta-resources"]` | `resources` |
| C4.2.3 | Si utiliza una IA existente, consultar sobre el fragmento y pedir explicación de significado | Fragmento, vías de consulta y retorno | `[data-action="hta-resources"]` | `resources` |
| C4.2.4 | Solicitar a un docente o compañero una explicación del fragmento si se dispone de esa | Fragmento, vías de consulta y retorno | `[data-action="hta-resources"]` | `resources` |
| C4.3 | Comparar la explicación o acepción obtenida con la intención original, identificando qué se | Fragmento, vías de consulta y retorno | `[data-action="hta-resources"]` | `resources` |
| C4.4 | Reformular solo la duda que continúa abierta: añadir contexto, pedir otra acepción o pedir un | Fragmento, vías de consulta y retorno | `[data-action="hta-resources"]` | `resources` |
| C5.1 | Redactar una versión propia con asunto, saludo, petición, motivo pertinente y cierre; conservar | Revisión localizada, datos, decisión y explicación | `[data-action="hta-review-fragment"]` | `email-review` |
| C5.2.1 | Comprobar una construcción gramatical, por ejemplo “I am agree” frente a “I agree”, | Revisión localizada, datos, decisión y explicación | `[data-action="hta-review-fragment"]` | `email-review` |
| C5.2.2 | Distinguir una elección de registro, por ejemplo “I want you to send me. . . ” frente a | Revisión localizada, datos, decisión y explicación | `[data-action="hta-review-fragment"]` | `email-review` |
| C5.2.3 | Detectar cambios de significado o datos, como confundir Friday con Monday o una solicitud | Revisión localizada, datos, decisión y explicación | `[data-action="hta-review-fragment"]` | `email-review` |
| C5.3.1 | Incorporar una alternativa comprendida cuando conserva la intención y mejora el aspecto | Revisión localizada, datos, decisión y explicación | `[data-action="hta-review-fragment"]` | `email-review` |
| C5.3.2 | Mantener la frase propia cuando es pertinente o la alternativa altera la intención. | Revisión localizada, datos, decisión y explicación | `[data-action="hta-review-fragment"]` | `email-review` |
| C5.3.3 | Pedir una explicación o una segunda alternativa cuando todavía no se entiende el efecto | Revisión localizada, datos, decisión y explicación | `[data-action="hta-review-fragment"]` | `email-review` |
| C5.4 | Explicar una decisión con palabras propias y conservar el antes, el después y la razón de cambiar | Revisión localizada, datos, decisión y explicación | `[data-action="hta-review-fragment"]` | `email-review` |
| C6.1 | Apartar modelo y apuntes y formular una petición para una intención conocida. | Recuperación, otra relación y comparación | `[data-action="hta-productions"]` | `email-transfer` |
| C6.2 | Explicar por qué la fórmula recuperada corresponde al destinatario y señalar cualquier ayuda | Recuperación, otra relación y comparación | `[data-action="hta-productions"]` | `email-transfer` |
| C6.3 | Componer otro correo con una relación distinta, cambiando por ejemplo de docente a com- | Recuperación, otra relación y comparación | `[data-action="hta-productions"]` | `email-transfer` |
| C6.4 | Comparar las dos producciones y explicar qué cambió en el tono, qué significado se conservó y | Recuperación, otra relación y comparación | `[data-action="hta-productions"]` | `email-transfer` |
| C7.1 | Conservar intención, relación, versión propia, explicación comprendida y una duda pendiente | Cierre parcial, dudas y continuidad | `[data-action="hta-resume-plan"]` | `continuity` |
| C7.2 | Al retomar, identificar lo ya comprendido y priorizar una duda que afecte al sentido, a la | Cierre parcial, dudas y continuidad | `[data-action="hta-resume-plan"]` | `continuity` |
| C7.3 | Intentar recuperar una expresión en otra sesión antes de releer su modelo y registrar el apoyo | Cierre parcial, dudas y continuidad | `[data-action="hta-resume-plan"]` | `continuity` |
| C7.4 | Valorar el intento mediante comprensión del significado, adecuación al destinatario y uso propio; | Cierre parcial, dudas y continuidad | `[data-action="hta-resume-plan"]` | `continuity` |
| V1.1 | Reconocer fuente, destinatario e idea general de una lectura o de un correo breve. | Lectura, relevancia y oración exacta | `[data-action="hta-reading-note"]` | `reading` |
| V1.2 | Priorizar una expresión desconocida si impide comprender la idea principal, cambia la petición | Lectura, relevancia y oración exacta | `[data-action="hta-reading-note"]` | `reading` |
| V1.3 | Conservar la oración exacta y explicar qué no se comprende, distinguiendo una palabra de- | Lectura, relevancia y oración exacta | `[data-action="hta-reading-note"]` | `reading` |
| V2.1 | Examinar la función gramatical: por ejemplo, reconocer que dedicated modifica space en “a | Pistas reales, hipótesis opcional y contexto insuficiente | `[data-action="hta-lexical-tools"]` | `inference` |
| V2.2.1 | Relacionar una finalidad o resultado con la palabra: “space” y “focus on your work” | Pistas reales, hipótesis opcional y contexto insuficiente | `[data-action="hta-lexical-tools"]` | `inference` |
| V2.2.2 | Aprovechar una reformulación, ejemplo o contraste explícito en las oraciones próximas, si | Pistas reales, hipótesis opcional y contexto insuficiente | `[data-action="hta-lexical-tools"]` | `inference` |
| V2.2.3 | Relacionar una combinación conocida o un componente de la palabra con el contexto, | Pistas reales, hipótesis opcional y contexto insuficiente | `[data-action="hta-lexical-tools"]` | `inference` |
| V2.3 | Expresar un significado provisional y justificarlo con una pista; si no se puede inferir, explicitar | Pistas reales, hipótesis opcional y contexto insuficiente | `[data-action="hta-lexical-tools"]` | `inference` |
| V3.1.1 | Consultar las acepciones y los ejemplos de un diccionario disponible. | Fuentes, acepciones e interpretación propia | `[data-action="hta-interpret"]` | `senses` |
| V3.1.2 | Comparar una traducción con la oración, comprobando si conserva la relación entre sus | Fuentes, acepciones e interpretación propia | `[data-action="hta-interpret"]` | `senses` |
| V3.1.3 | Si se utiliza una IA existente, aportar la oración y pedir acepciones posibles y pistas para | Fuentes, acepciones e interpretación propia | `[data-action="hta-interpret"]` | `senses` |
| V3.1.4 | Solicitar una explicación o un ejemplo a un docente o compañero cuando ese recurso esté | Fuentes, acepciones e interpretación propia | `[data-action="hta-interpret"]` | `senses` |
| V3.2 | Relacionar cada acepción plausible con un ejemplo y con la oración propia; conservar la refer- | Fuentes, acepciones e interpretación propia | `[data-action="hta-interpret"]` | `senses` |
| V3.3.1 | En “A dedicated space helps you focus on your work”, contrastar la acepción reservado | Fuentes, acepciones e interpretación propia | `[data-action="hta-interpret"]` | `senses` |
| V3.3.2 | En “She is a dedicated teacher”, contrastar la acepción comprometida con la referencia a | Fuentes, acepciones e interpretación propia | `[data-action="hta-interpret"]` | `senses` |
| V3.3.3 | Mantener abiertas varias acepciones cuando la oración no permite distinguirlas y buscar | Fuentes, acepciones e interpretación propia | `[data-action="hta-interpret"]` | `senses` |
| V3.4 | Comparar la hipótesis inicial con la interpretación contrastada y reformularla con palabras | Fuentes, acepciones e interpretación propia | `[data-action="hta-interpret"]` | `senses` |
| V4.1 | Comparar ejemplos de una misma acepción en situaciones diferentes, evitando llamar diferencia | Registro, patrón y anotación | `[data-action="hta-register-note"]` | `lexical-note` |
| V4.2.1 | Si hay una nota explícita de uso formal, informal o neutro, relacionarla con la acepción y | Registro, patrón y anotación | `[data-action="hta-register-note"]` | `lexical-note` |
| V4.2.2 | Si no hay una nota fiable, dejar el registro sin determinar y describir solo la situación de | Registro, patrón y anotación | `[data-action="hta-register-note"]` | `lexical-note` |
| V4.3 | Reconocer combinaciones y estructuras pertinentes: dedicated + sustantivo y dedicated to + | Registro, patrón y anotación | `[data-action="hta-register-note"]` | `lexical-note` |
| V4.4 | Redactar una nota propia que conecte significado, oración de origen, patrón, situación de uso | Registro, patrón y anotación | `[data-action="hta-register-note"]` | `lexical-note` |
| V5.1 | Elegir una idea personal y expresarla con la palabra: por ejemplo, describir un espacio reservado | Producción, conservación, reformulación o sustitución | `[data-action="hta-vocab-write"]` | `vocab-production` |
| V5.2 | Contrastar la oración con ejemplos de la misma acepción y revisar referente, combinación | Producción, conservación, reformulación o sustitución | `[data-action="hta-vocab-write"]` | `vocab-production` |
| V5.3.1 | Mantener el uso cuando la acepción y el patrón son pertinentes, explicando una coinci- | Producción, conservación, reformulación o sustitución | `[data-action="hta-vocab-write"]` | `vocab-production` |
| V5.3.2 | Reformular la construcción cuando la idea es pertinente pero el patrón no encaja. | Producción, conservación, reformulación o sustitución | `[data-action="hta-vocab-write"]` | `vocab-production` |
| V5.3.3 | Elegir otra palabra si la acepción estudiada no expresa la intención, en vez de incorporarla | Producción, conservación, reformulación o sustitución | `[data-action="hta-vocab-write"]` | `vocab-production` |
| V6.1 | Apartar definición y apuntes; explicar el significado y producir una frase recordando solo la | Recuperación, transferencia y correo vinculado | `[data-action="hta-transfer-email"]` | `vocab-transfer` |
| V6.2 | Elegir un contexto distinto y pertinente: proponer un espacio para el proyecto, una reunión | Recuperación, transferencia y correo vinculado | `[data-action="hta-transfer-email"]` | `vocab-transfer` |
| V6.3 | Incorporar la expresión a un correo breve y justificar su significado y adecuación al destinatario; | Recuperación, transferencia y correo vinculado | `[data-action="hta-transfer-email"]` | `vocab-transfer` |
| V6.4 | usando otra situación, no copiando la frase inicial. Si el nuevo significado o patrón no encaja, volver a V3–V5. | Recuperación, transferencia y correo vinculado | `[data-action="hta-transfer-email"]` | `vocab-transfer` |
| V7.1 | Conservar palabra, oración de origen, significado explicado, producción propia disponible y | Entrada por contexto, repaso elegido y pendientes | `[data-action="hta-entry-recall"]` | `review` |
| V7.2 | En una sesión posterior, recuperar la palabra o situación sin mostrar primero la definición y | Entrada por contexto, repaso elegido y pendientes | `[data-action="hta-entry-recall"]` | `review` |
| V7.3 | Intentar una explicación y una oración propias antes de contrastarlas; anotar la fecha y el apoyo | Entrada por contexto, repaso elegido y pendientes | `[data-action="hta-entry-recall"]` | `review` |
| V7.4 | Decidir si se necesita repetir el contraste, el patrón o la recuperación, según el significado y uso | Entrada por contexto, repaso elegido y pendientes | `[data-action="hta-entry-recall"]` | `review` |
