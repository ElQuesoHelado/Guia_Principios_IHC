# Cómo abrir y demostrar Lingua IA

Abre `index.html` en Firefox o Chromium. No requiere instalación, API ni conexión. También puedes servir esta carpeta con `python3 -m http.server 8000` y abrir `http://localhost:8000`; usa siempre la misma dirección para recuperar lo guardado. El almacenamiento de archivos locales depende del navegador.

El inicio contiene un único chat y dos ideas opcionales. **Explorar ejemplos** prepara mensajes editables: no los envía automáticamente. El prototipo usa reglas y respuestas de ejemplo; no evalúa cualquier texto con una IA real.

## 1. Afinar una consulta sin obligar a seguir una ruta

1. Escribe `Quiero aprender a escribir un correo` sin enviarlo. Aparece una sugerencia sobre el destinatario.
2. Prueba **Descartar**: tu mensaje sigue igual y puedes enviarlo.
3. Añade ` a mi profesora`. La sugerencia propone comparar tono. **Añadir a mi mensaje** la incorpora sin enviar; **Editar la sugerencia** permite modificarla en el mismo campo. **Deshacer** recupera el mensaje anterior si no escribiste después.
4. Envía. El chat queda en **Correo en inglés**. **Cambiar tarea** permite corregir la clasificación.
5. **Comparar dos peticiones** muestra la misma intención con distinto grado de confianza. Explica en el chat por qué elegirías una; no hay un formulario de evidencias.

## 2. Revisar y conservar lo que funciona

Desde **Explorar ejemplos → Revisar sin perder tu voz → Preparar ejemplo**, envía el texto. También puedes pegarlo:

```text
Revisa el tono de este correo a mi profesora y conserva el resto:
Dear Professor,
I want you to send me the notes.
I am agree with the deadline.
Best regards,
Alex
```

1. Se guarda el borrador y se muestran dos propuestas. **I am agree** se trata como gramática; **I want you to…** como una elección de tono, no como error gramatical.
2. Abre **Por qué se propone este cambio**. Prueba **Usar esta sugerencia**, **Conservar mi frase** y **Deshacer decisión**.
3. En **Mi aprendizaje → Ver versiones del correo**, compara el texto y recupera el original. Recuperar añade una versión y conserva las demás. Las propuestas anteriores se identifican como pertenecientes a otro borrador.
4. Si aplicas dos cambios, deshaz primero el último; si hay modificaciones posteriores, la interfaz ofrece versiones para evitar perderlas.
5. Para producir desde cero, usa **Probar mi propia frase** o **Escribir mi petición**. El mismo chat recibe el borrador. La demo solo revisa algunas estructuras conocidas; otros textos se conservan sin una corrección inventada.

## 3. Vocabulario: hipótesis, contraste y uso

En **Nuevo chat**, escribe:

```text
¿Qué significa dedicated en “A dedicated space helps you focus on your work”? Quiero inferir su significado antes de ver la definición.
```

1. La pista propone relacionar *space* y *focus*. Escribe: `Creo que significa reservado para trabajar, porque habla de space y focus.`
2. La ficha conserva tu hipótesis junto a la acepción del ejemplo. Abre **Contrastar acepciones, patrón y ejemplos**: no se confunde *dedicated space* con una persona comprometida ni se atribuye formalidad sin evidencia.
3. Prueba **Guardar palabra** y **Quitar del repaso**. **Explicar con mis palabras** recoge una explicación en el chat.
4. Puedes usar **Ver significado ahora** para saltar la inferencia. El apoyo es opcional.
5. **Ver otra lectura** ofrece *dedicated*, *productive* y *deadline*. Cada palabra tiene su propio contexto y ficha.
6. Para mostrar el límite de la demo, prueba en un chat nuevo `¿Qué significa dedicated en “She is a dedicated teacher”?`. Se conserva ese contexto y se pide una hipótesis; no se aplica la definición preparada para un espacio.

## 4. Recuperar, transferir y retomar después

1. La etapa actual permanece visible al desplazarte, por ejemplo **Etapa 2 de 4 · Escribir y decidir**. Despliega **Ver etapas** y elige **Recuperar sin modelo** o **Recordar sin definición**. El material anterior desaparece de la vista y de la navegación accesible.
2. Escribe un intento propio. En correo: `Could I have more time? Elijo un tono cortés para mi profesora.` En vocabulario: `I have a dedicated desk for my homework.`
3. Si pulsas **Consultar el apoyo anterior**, el aporte registra que se consultó ayuda. No se califica automáticamente la respuesta.
4. **Probar en otra situación** propone otro destinatario o contexto. Redacta y explica la elección. Volver a consultar queda permitido.
5. **Mi aprendizaje** muestra producciones, explicaciones, palabras y fechas; abrir etapas no suma aportes. **Cerrar esta práctica** permite dejar una duda y descargar notas como TXT.
6. Recarga la página. El inicio vuelve a estar vacío; en el botón de conversaciones, arriba a la izquierda, abre el panel lateral izquierdo y recupera tu chat. Puedes cerrarlo con la X, Escape o pulsando fuera del panel. El borrador, las versiones, las palabras y el mensaje sin enviar se mantienen en ese navegador.
7. En otro momento, usa **Mi aprendizaje → Retomar un repaso sin definición**. No hay recordatorios automáticos ni se afirma que el intervalo haya sido suficiente para demostrar retención.

El menú superior, la tarea y el indicador de etapa permanecen accesibles al bajar por un chat largo. La ruta se despliega a petición; en pantallas pequeñas su altura está limitada y permite desplazarse dentro de ella. Volver a comprender o escribir termina la práctica sin modelo y actualiza la actividad pendiente. Navegar no marca etapas como aprendidas.

## 5. Caso ambiguo y libertad de navegación

Envía `Quiero mejorar mi inglés`. El mensaje no se pierde: la interfaz pide un punto de partida y permite escoger correo o vocabulario. Las categorías del historial mantienen el orden Correo, Vocabulario y Por explorar. Puedes navegar por la ruta, escribir libremente o abrir apoyos sin completar requisitos.

## Qué revisar en la exposición

- La sugerencia cambia según lo escrito antes de enviar y explica su propósito.
- Un botón opcional puede ahorrar la redacción de una instrucción, pero no se afirma que reduzca consultas sin medirlo.
- La evidencia es lo que escribe el estudiante; aceptar cambios o guardar palabras muestra actividad.
- **Guía de principios:** `GUIA_PRINCIPIOS_IHC.html` o su versión Markdown. **HTA:** `docs/REVISION_HTA_Y_TRAZABILIDAD.md`. **Papers:** `guiaPapers.md`.

## Verificación técnica

```bash
python3 tools/test_navigation_scroll.py
python3 tools/test_learning_flow.py
python3 tools/test_guide_integrity.py
python3 tools/generate_screenshots.py
```

Las pruebas funcionales ejecutan Firefox real en 1440, 390 y 320 píxeles. El capturador usa Firefox y perfiles temporales. Ejecútalos secuencialmente: comparten un archivo de captura temporal. No son un estudio con usuarios ni una auditoría completa de accesibilidad.
