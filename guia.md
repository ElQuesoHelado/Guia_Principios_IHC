# Demostrar los recorridos de Lingua IA · HTA v8

La fuente es [HTA_correo_vocabulario_v8.pdf](HTA_correo_vocabulario_v8.pdf). La [matriz por nodo](docs/HTA_V8_COBERTURA.md) relaciona sus 29 planes y 80 hojas con la interfaz. Es un mock: ejemplos preparados, reglas locales y aportes del estudiante; no una IA conectada ni una evaluación general de textos.

Abre `index.html` o sirve la carpeta con `python3 -m http.server 8000`. Usa el mismo navegador, dirección y puerto para retomar datos. El estado v2 migra las prácticas v1 sin borrar su clave original. El chat empieza vacío; abrir etapas no acredita aprendizaje.

## 1. Afinar la consulta y precisar la situación

1. Escribe `Quiero aprender a escribir un correo` sin enviar. Prueba **Descartar**, **Añadir a mi mensaje**, **Editar la sugerencia** y **Deshacer**. Añadir no envía; si escribes después, deshacer no borra esa escritura.
2. Añade `para pedir una prórroga a mi profesora`. Envía. En **Otros apoyos para esta situación → Precisar mi situación** puedes revisar intención y relación, sin una ficha obligatoria.
3. Abre **Precisar relación, datos y dudas → Aportar los datos que conozco**. Un mensaje de demostración es:

```text
nombre: Alex Rivera; tratamiento: Professor; fecha vigente: Thursday; fecha propuesta: Friday; motivo: necesito revisar mi ensayo
```

4. Para probar el caso desconocido, elige **Relación desconocida**. No se completa un título por suposición. **Recordar una expresión y señalar mi duda** recoge lo que ya sabes y lo que necesitas aprender.
5. Prueba también **Solicitar apuntes o material** y **Aclarar una entrega**. **Combinar solicitudes necesarias** pide indicar qué solicitudes distintas se necesitan; no las combina por defecto.

## 2. Modelos y alternativas lingüísticas

1. **Comparar dos peticiones** conserva la intención elegida y contrasta can/could/please. Explica qué efecto tienen y cuándo elegirías cada una.
2. **Ver el correo completo** muestra un modelo del mismo caso. Nombres y fechas se identifican como ficticios. **Explicar la intención y los datos del modelo** permite señalar petición, motivo y material o plazo.
3. En **Otros apoyos → Encontrar una expresión**, despliega **Asunto**, **Saludo**, **Petición**, **Motivo** y **Cierre**. Hay asuntos para los tres casos; saludos con tratamiento confirmado, nombre completo o confianza; peticiones y cierres alternativos.
4. **Probar mi expresión** recibe tu redacción y justificación en el mismo chat. Los ejemplos no se insertan automáticamente en el borrador. Comprobar la fecha, el nombre y la pertinencia de la razón sigue siendo decisión del estudiante.

## 3. Producción, revisión localizada y conservación de datos

En **Probar mi propia frase**, escribe:

```text
Subject: Request for lecture notes
Dear Professor Rivera,
I want you to send me the notes.
I am agree with the deadline.
Best regards,
Alex
```

1. **Revisar una frase** propone cambios de gramática y tono solo para estructuras conocidas. Abre la explicación y prueba **Usar esta sugerencia**, **Conservar mi frase**, **Explicar mi decisión** y **Deshacer decisión**.
2. Se muestra otra tarjeta con la versión guardada al aplicar o deshacer. **Mi aprendizaje → Ver versiones del correo** conserva y recupera las anteriores.
3. **Revisar un fragmento** permite copiar una frase exacta. Si aparece dos veces, se elige la aparición antes de revisar. Por ejemplo, dos líneas `Send me the notes.` permiten corregir solo la segunda; el resultado termina en `?`, no en `?.`.
4. **Contrastar significado y datos** muestra un ejemplo adverso: cambiar Friday por Monday o pedir permiso en vez de apuntes. Se debe explicar si conserva la intención; no se presenta como mejora recomendada.
5. **Proponer otra frase** permite una alternativa propia. Se contrasta y puede aplicarse solo al rango de la versión conservada. Si el borrador cambió, hay que seleccionar otra vez; no se sustituye otra aparición a ciegas.

## 4. Consultar y volver al punto de origen

Para un recorrido léxico preparado, guarda este correo mediante **Probar mi propia frase**:

```text
Dear Professor Rivera,
A dedicated space helps you focus on your work.
Could you please send me the notes?
Best regards,
Alex
```

1. En su tarjeta pulsa **Consultar esta expresión**. Puedes seleccionar texto dentro del correo o copiar `A dedicated space helps you focus on your work.` cuando se solicite. Se conservan versión, oración, actividad y mensaje sin enviar.
2. La franja fija muestra **Volver al correo**. Formula una hipótesis o consulta directamente. **Explorar pistas, fuentes y producción propia** ofrece apoyos adicionales.
3. **Contrastar con un recurso** permite explorar diccionario/modelo, traducción, IA existente o persona. Todas las respuestas internas están identificadas como ejemplos preparados.
4. **Registrar una respuesta externa** solicita recurso/referencia, explicación recibida y qué aclara o deja pendiente. No verifica esa respuesta ni finge una conexión real. La referencia queda conservada aunque la consulta se interrumpa.
5. **Precisar la duda que sigue abierta** recoge únicamente lo incierto. **Volver al correo** devuelve explicación o duda, contexto, patrón disponible y fuentes, sin reemplazar el texto automáticamente. Se puede regresar antes de terminar la práctica de vocabulario.
6. Para una expresión no reconocida se pregunta si la duda es de significado, construcción o registro. Las dudas gramaticales/de tono pueden consultarse y volver dentro del correo; las léxicas llevan a vocabulario.
7. Una pregunta explícita como `¿Qué significa dedicated en “She is a dedicated teacher”?` se atiende aunque estuvieras preparando otra respuesta. `volver al correo` permite retomar la actividad pendiente.

## 5. Vocabulario: punto de partida, contraste y producción

En **Nuevo chat**, envía:

```text
¿Qué significa dedicated en “A dedicated space helps you focus on your work”? Quiero inferir su significado antes de ver la definición.
```

1. Responde `Creo que es reservado para una finalidad, por space y focus on your work.` La hipótesis aparece junto al contraste. También puedes consultar directamente o indicar `No puedo inferir todavía.`; no se inventa una hipótesis.
2. Prueba `¿Qué significa dedicated en “She is a dedicated teacher”?` en otro chat: se muestra compromiso personal. Una oración no preparada conserva su duda y permite consulta externa, sin recibir una acepción ajena.
3. **Ver otra lectura** permite relacionar título, fuente y destinatario con lo que sabes, resumir la idea y decidir qué palabra es relevante. Las tres palabras conservan su oración exacta. Para deadline, la pista corresponde a “each task” y “when to finish”.
4. En **Pistas y patrones**, explora función gramatical, finalidad, otra reformulación explícita preparada y combinaciones como indicios. Un ejemplo adicional se distingue de las pistas presentes en la oración original.
5. **Reformular mi interpretación** conserva lo aprendido tras el contraste. Si ya se vio una explicación, una respuesta posterior no se presenta como hipótesis inicial.
6. **Registrar una etiqueta de mi fuente** conserva etiqueta y referencia como aporte no verificado; sin etiqueta fiable elige **Dejar el registro sin determinar**. **Justificar una situación y destinatario** distingue registro de cambio de acepción.
7. **Redactar mi nota** conecta significado, oración, patrón, situación y duda. **Probar una oración** conserva la producción y permite **Conservar y justificar**, **Reformular el patrón** o **Elegir otra palabra** sin borrar lo anterior.
8. **Usarla en un correo** abre una producción vinculada. Redacta y revisa el correo; **Volver al vocabulario** conserva ambos trabajos.

## 6. Recuperación, comparación y continuidad

1. Elige **Recuperar sin modelo** o **Recordar sin definición**. El material anterior se oculta visualmente y para tecnología de asistencia. Consultar apoyo, notas o versiones durante el intento se registra como ayuda.
2. Escribe un intento y después compara; **Probar en otra situación** pide otro destinatario o contexto. **Comparar mis producciones** muestra las versiones propias y permite explicar qué significado se conservó, qué cambió y qué apoyo se necesitó.
3. Guarda dos acepciones de dedicated o varias palabras. En **Mi aprendizaje → Retomar un repaso sin definición** puedes elegir la entrada concreta; no se repasa siempre la primera. Las entradas se guardan por palabra y oración.
4. **Cerrar esta práctica** conserva el estado parcial o registrado, permite descargar notas y anotar una duda. El cierre no certifica autonomía.
5. Recarga. El inicio vuelve vacío; abre **Conversaciones** y retoma la práctica. Primero se ofrece un punto de partida con el apoyo anterior oculto. **Mostrar dónde quedé** continúa; **Intentar sin modelo/definición** comienza otro intento. El mensaje sin enviar y los retornos de una consulta intermedia se conservan.
6. No hay recordatorios automáticos ni una calificación de retención. El estudiante decide cuándo repetir contraste, patrón o recuperación.

El menú, la etapa y el retorno de una consulta permanecen accesibles durante el desplazamiento. La ruta y los apoyos se abren voluntariamente; no es necesario recorrer todos los recursos o pantallas.
