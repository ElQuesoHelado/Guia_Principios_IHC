# Alcance y tareas de Lingua IA

## Usuario y propósito

Estudiante universitario hispanohablante, aproximadamente B1–B2, que necesita comprender vocabulario, escribir con intención propia y practicar respuestas en sesiones breves. El objetivo es construir conocimiento del inglés mediante producción, comparación y transferencia.

## Tres tareas sin IA y su adaptación

1. **Aprender a escribir un correo formal.** Sin IA: analizar modelos, planificar, redactar, autoevaluar con una lista de comprobación, consultar una guía o persona y escribir otro correo. Interfaz: Comprender → Escribir → Revisar → Transferir. La guía es opcional y se puede abrir, ocultar, saltar o retomar; el correo y sus cuatro sugerencias localizadas siempre están accesibles. El borrador propio se conserva separado del ejemplo; el estudiante justifica un cambio, revisa su borrador y produce un correo para otra situación.
2. **Practicar conversación escrita.** Sin IA: preparar recursos, conversar por mensajes con otra persona, reformular y reflexionar. Interfaz: Preparar → Conversar → Revisar → Transferir. Escenarios predefinidos, mensajes, pistas y avance voluntario; revisión razonada y diálogo nuevo.
3. **Aprender vocabulario en contexto.** Sin IA: leer, inferir, contrastar con diccionario y ejemplos, registrar y recuperar. Interfaz: Leer → Descubrir → Registrar → Practicar. Notas de hipótesis, comparación, registro contextual y oración propia.

## Evidencias y progreso

`js/learning.js` presenta una actividad contextual por etapa. Las notas sobreviven al cambio de actividad en memoria. “Guardar mis notas” permite registrar una nota parcial, sin exigir todos los campos ni la autoevaluación. Editar las notas invalida el registro de ese paso; navegar nunca lo completa. El progreso distingue pasos registrados, notas, palabras guardadas y decisiones sobre sugerencias. Ningún indicador acredita dominio ni corrección lingüística.

## Ideas y principios conservados

Se mantienen comparación original/propuesta, reglas y ejemplos, ayuda graduada en la revisión, criterios y plan editables, decisiones localizadas y reversibles, versiones del ejemplo, consultas contextuales y turnos controlados. La relación con cada paper se documenta en `guiaPapers.md`; el catálogo de 71 principios se mantiene en `GUIA_PRINCIPIOS_IHC`.

## Alcance técnico

Demo frontend con contenido predefinido y estado en memoria, sin evaluación de textos libres ni envío de correos. Las notas y mensajes desaparecen al recargar. La conversación se realiza por texto; los hallazgos sobre voz de las entrevistas no son funciones implementadas.


El apoyo pedagógico es opcional: se accede directamente a correo, lectura o conversación. Las sugerencias están inicialmente ocultas y pueden abrirse u ocultarse en cualquier momento. En el correo, “Ver ejemplos de correo” abre el modelo directamente; Original, Borrador, Versión actual, Ver cambios, Versiones y Deshacer siguen accesibles al cambiar de sugerencia.
