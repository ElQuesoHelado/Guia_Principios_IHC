# HTA v8 y correspondencia con la interfaz

Fuente vigente e inalterada: [HTA_correo_vocabulario_v8.pdf](../HTA_correo_vocabulario_v8.pdf). Se conservan C0 y V0 y sus enlaces. Las [transcripciones](feedback_docente/2026-11-24/README.md) son criterios docentes, no aprobación de esta entrega. La decisión de dos raíces es la explicitada en la v8.

## Cobertura y forma de leerla

El análisis contiene **109 nodos: 29 planes y 80 hojas**. La interfaz ofrece una acción, un ejemplo preparado o un registro propio para cada hoja del alcance delimitado. Los recorridos reproducibles prueban las alternativas y retornos; no certifican comprensión ni usabilidad empírica.

La [matriz por nodo](HTA_V8_COBERTURA.md) y su [catálogo verificable](hta-v8-coverage.json) relacionan cada identificador con comportamiento, selector y escenario de prueba. Ninguna hoja se interpreta como obligación de crear un botón independiente. Los ejemplos se revelan bajo demanda en el mismo chat; la ruta es opcional y no existe un formulario obligatorio por tarea.

## Correo

| Grupo v8 | Interacción real | Ejemplo o evidencia |
|---|---|---|
| C1: intención, relación y dudas | `hta-situation`, `hta-case`, `hta-facts`, `hta-known` | Apuntes/material, prórroga y aclaración. Datos aportados, relación desconocida y dudas explícitas; combinación de solicitudes solo cuando se declara necesaria. |
| C2: comprender y comparar | `model`, `compare`, `hta-identify-model`, `justify` | Modelos del mismo caso; can/could/please; peticiones de igual intención y explicación propia. Los datos ficticios del modelo se identifican como tales. |
| C3: elegir expresiones | `hta-parts`, `hta-try-part` | Tres asuntos; saludos con título confirmado, nombre completo o confianza; peticiones, razón pertinente y dos cierres. Datos desconocidos no se inventan. |
| C4: resolver una duda | `hta-consult`, `hta-doubt`, `hta-resources`, `hta-return` | Fragmento y versión de origen, clasificación de duda, vías alternativas, contraste, reformulación de lo incierto y retorno. |
| C5: comprender la revisión | `hta-review-fragment`, `hta-review-range`, `review`, `accept`, `reject`, `justify`, `hta-candidate` | Rangos exactos, apariciones repetidas, gramática, registro, significado/datos, alternativa propia, explicaciones y versiones. Los cambios desactualizados no se aplican sobre otro fragmento. |
| C6: recuperar y transferir | `recall`, `transfer`, `hta-productions`, `hta-compare-own` | Producciones separadas, otra relación y comparación del significado, tono y apoyo. |
| C7: cerrar y retomar | `finish`, `reflection`, `history`, `hta-resume-plan` | Estado parcial o práctica registrada, dudas, versiones y mensaje sin enviar. Apoyo anterior oculto al retomar; el estudiante decide si intenta recuperar o continúa donde quedó. |

Las reglas automáticas de gramática/tono son acotadas. Para otras expresiones se permite proponer una alternativa y explicar su efecto, sin una calificación inventada. La diferencia Friday/Monday o entre apuntes y permiso se presenta como ejemplo adverso para contrastar, no como mejora recomendada.

## Vocabulario

| Grupo v8 | Interacción real | Ejemplo o evidencia |
|---|---|---|
| V1: situar y priorizar | `reading`, `hta-reading-note`, `hta-priority`, `hta-context` | Fuente didáctica y destinatario explícitos; conocimientos previos, idea general, relevancia y oración exacta o ampliada. |
| V2: pistas e hipótesis | `clue`, `hta-lexical-tools`, `hta-infer`, `definition` | Función gramatical, finalidad, reformulación explícita en otro ejemplo y combinación conocida como indicio. Inferir es opcional. |
| V3: contrastar | `hta-resource`, `hta-external`, `hta-interpret` | Fuentes preparadas o externas registradas, dos acepciones de dedicated, hipótesis frente a contraste y duda cuando falta evidencia. |
| V4: significado, registro y patrón | `hta-register-note`, `hta-register-unknown`, `hta-usage`, `hta-lexical-note` | Nota de fuente aportada por el estudiante, registro sin determinar, patrón, situación y nota propia. No se atribuye formalidad a partir de una palabra aislada. |
| V5: producir y revisar | `hta-vocab-write`, `hta-production-keep`, `hta-production-rewrite`, `hta-production-replace` | Oración propia, contraste con el mismo sentido y decisión de conservar, reformular el patrón o cambiar de palabra. Se preservan las producciones anteriores. |
| V6: recuperar y transferir | `recall`, `transfer`, `hta-transfer-email`, `hta-productions` | Significado y uso propios sin definición, otra situación escrita, correo vinculado y comparación de apoyos. |
| V7: registrar y retomar | `save-word`, `hta-entry-recall`, `repaso`, `hta-pending`, `history` | Entradas por palabra y contexto, varias acepciones guardadas, elección de repaso, fecha, ayuda y dudas posteriores. |

La hipótesis inicial no se reconstruye después de consultar. Si se declara que no se pudo inferir, se conserva ese punto de partida; una explicación posterior se identifica como interpretación después del contraste. Guardar una entrada o cerrar una práctica no acredita dominio.

## Consultas y enlaces de retorno

| Enlace de la v8 | Estado que se conserva y devuelve |
|---|---|
| C4.1 → V0 | Oración, fragmento, intención, versión, actividad y mensaje pendiente del correo. Las dudas gramaticales o de registro pueden consultarse sin pasar por una acepción léxica. |
| V4.4 → C4.3 | Explicación propia o duda, contexto, patrón preparado disponible, fuentes y pendientes. El resultado no sustituye automáticamente el fragmento. Se puede volver antes de V5–V7 y retomar después. |
| V6 → C1.2 / C5.2 | Producción léxica de origen, correo propio y revisión necesaria. Volver conserva ambos trabajos. |
| C7 / V7 → otra sesión | Estado local versionado, entradas, producciones, pendientes y pila de retorno. La recarga no elimina la consulta intermedia. |

Las órdenes explícitas de consultar o volver se atienden aunque hubiera una respuesta pendiente. Las consultas anidadas conservan sus puntos de origen. Cambiar de tarea manualmente también conserva la etapa y la actividad de cada raíz.

## Procedencia y límites del mock

Las cuatro vías de consulta muestran **material didáctico preparado**, no resultados de servicios ni respuestas de personas reales. El estudiante también puede aportar recurso, referencia y explicación externa; se registran como no verificados. Una consulta sin respuesta conserva su referencia como pendiente. Si una fuente no basta, se puede contrastar otra, ampliar contexto o conservar la incertidumbre.

Las fichas se resuelven por palabra y oración, incluyendo dedicated como finalidad y compromiso personal. Las tarjetas anteriores conservan su contexto. Una oración diferente no recibe una definición ni traducción preparada para otro ejemplo. La interpretación de texto arbitrario, el diccionario en vivo y la evaluación general de aprendizaje siguen fuera del mock.

Durante recuperación se oculta el material anterior visualmente y para tecnología de asistencia. Abrir notas, versiones u otro apoyo durante el intento registra ayuda; no se impide consultar fuera de la aplicación. La separación temporal y la retención no se evalúan automáticamente.

## Verificación reproducible

- `python3 tools/test_hta_complete.py`: recorridos de los 109 nodos, alternativas, rangos, procedencia, fuentes, retorno en ambos sentidos, producción y recarga intermedia a 1440, 390 y 320 px. Las acciones verifican que el control tiene geometría visible y abren los detalles necesarios.
- `python3 tools/test_learning_flow.py` y `python3 tools/test_navigation_scroll.py`: regresiones del chat, decisiones, historial y navegación.
- `python3 tools/test_hta_v8.py`: los 29 planes, integridad del archivo y migración de sesiones v1.
- `python3 tools/test_guide_integrity.py`: catálogo y selectores de la guía vigente.

Ejecutar secuencialmente: las pruebas de navegador comparten un archivo temporal. Estas comprobaciones no sustituyen una revisión con estudiantes, una evaluación completa con lector de pantalla ni aprobación docente. Los [originales anteriores](originales/previo-v8/README.md) y las transcripciones se conservan intactos.
