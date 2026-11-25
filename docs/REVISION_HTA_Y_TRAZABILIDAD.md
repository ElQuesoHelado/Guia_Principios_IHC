# Revisión del HTA y traducción a la interfaz

Fecha: 25/11/2026. Fuentes: `HTA_unificado_sin_IA_v7.pdf` (usuarios p. 1; correo pp. 2–4; vocabulario pp. 8–10) y las transcripciones de `feedback_docente/2026-11-24/`. No se modificaron los PDF de entrada. Esta revisión no equivale a aprobación docente.

## Dictamen

El HTA v7 **sí se orienta a construir conocimiento**: plantea inferir, explicar, contrastar, producir, recuperar y transferir, y distingue los productos de una simple corrección. Sus raíces describen aprendizaje lingüístico, no operaciones de una aplicación. Sin embargo, **cumple parcialmente el feedback completo**: faltan planes en varios nodos descompuestos, una representación gráfica verificable, evidencia suficiente de cómo se ejecutan actualmente todas las alternativas y criterios de evaluación contrastados con estudiantes. La interfaz anterior con notas por apartados no resolvía la observación sobre prompts.

Se seleccionan la tarea 1 (correo) y la tarea 3 (vocabulario), por instrucción del usuario. La conversación escrita de la tarea 2 queda fuera de esta iteración. Se conservan las dos raíces e identificadores del PDF; `C` y `V` abajo son prefijos documentales para distinguirlos, no una renumeración de la fuente.

## Contraste con la profesora

| Fuente | Hallazgo en v7 | Resolución y límite |
|---|---|---|
| Audio 1, 00:11–02:06; Audio 3, 10:33 | La redacción incorpora registro, modales y justificación; supera identificar partes genéricas. | Comparación de igual intención con distinto destinatario; diferencia explícita entre gramática y cortesía. Falta observar si el estudiante comprende esa diferencia. |
| Audio 1, 02:18 y 06:47–06:50 | Tres tareas amplias. | Se implementan dos; correo tiene mayor profundidad. No se atribuye esta selección exacta a la profesora. |
| Audio 1, 06:50; Audio 2, 00:31–03:21 | Hay una raíz 0 por actividad, jerarquía hasta nivel 3. | Estructura válida para dos HTA independientes. El PDF presenta listas, no demuestra una diagramación validada. |
| Audio 2, 04:00–08:23; Audio 3, 12:38 y 21:40 | Correo: planes 0, 2, 6 y 7; vocabulario: 0, 3, 6 y 7. | Se complementan abajo los planes faltantes. La interfaz sugiere dependencias, permite entrar con un borrador y no obliga a recorrer etapas. |
| Audio 2, 10:32–11:19 | Precondiciones sin IA y caracterización que menciona traductores, diccionario e IA. | No se afirma que toda la secuencia haya sido observada. Falta validar qué recursos usa realmente cada estudiante y cuándo alterna entre ellos. |
| Audio 2, 11:49–19:08 | Hay excepciones, pero no un inventario completo de alternativas reales. | Se demuestran dos relaciones de confianza y tres palabras. No cubren todos los correos, niveles ni acepciones. |
| Audio 1, 02:35–05:36; Audio 3, 07:00–12:38 | El HTA sin solución no describe predicción, lo que es correcto. | La capa posterior deriva sugerencias mientras se escribe a partir de intención, destinatario y contexto. Son reglas locales, no predicción generativa. |
| Audio 3, 00:00–03:21 | Recuperación y transferencia están en el objetivo. | Se conservan notas y versiones en localStorage. El repaso posterior se inicia manualmente; no se simulan sesiones pasadas. |
| Audio 2, 22:01–22:15; Audio 3, 17:08–17:32 | Muchas acciones no requieren controles separados. | Un único chat recoge hipótesis, redacción y explicación; cuatro sugerencias de ruta agrupan siete grupos del HTA. |

Las marcas de tiempo son de las transcripciones suministradas, no de grabaciones verificadas. Los escenarios de demostración son decisiones de diseño; no son observaciones de usuarios.

## Planes complementarios propuestos para la práctica sin la solución

Se conservan los planes del PDF. Lo siguiente completa las ramas sin plan, como propuesta por validar. No introduce controles de interfaz en el análisis de la tarea actual.

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

**Regla para todos los nodos de tercer nivel:** cuando el PDF descompone un nodo en `.1` y `.2`, se propone realizar primero la localización/identificación y después la explicación/producción indicada, sobre el mismo fragmento; volver a `.1` si `.2` no tiene respaldo. Esa regla completa la secuencia básica, pero las alternativas concretas deben validarse en campo. Los planes de grupo anteriores y los del PDF tienen prioridad sobre esta regla general.

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
