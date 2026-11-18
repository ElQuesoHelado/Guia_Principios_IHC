# Lingua IA — alcance actualizado del prototipo

## Propósito

Prototipo de nivel medio para acompañar el aprendizaje del inglés mediante tareas con respuesta a eventos. La interfaz es una demo visual con datos simulados; no conecta con servicios de IA ni envía mensajes reales.

## Actividades principales

1. **Redacción asistida:** revisar un texto en inglés; observar una pista, comparar el fragmento original con una propuesta, leer la explicación y aceptar o rechazar el cambio.
2. **Lecciones y repaso:** leer un texto de ejemplo o pegar uno propio; seleccionar una palabra, revisar su significado en contexto y ejemplos adicionales, y guardarla para repasar.
3. **Conversación escrita:** elegir un escenario, responder por chat a preguntas breves y solicitar pistas cuando hagan falta.

Las preguntas puntuales se escriben en el chat de la actividad activa. La conversación es únicamente por texto: no hay micrófono, grabación, evaluación de pronunciación ni métricas de minutos hablados.

## Organización de la interfaz

- El selector principal muestra solo las tres actividades anteriores; cada una se alcanza desde la barra superior con un clic. El menú también ofrece el selector como ruta alternativa.
- La barra de etapas muestra la etapa actual y conserva el estado completado por tarea. “Ver progreso” abre directamente el resumen contextual; en el móvil también abre el panel de apoyo.
- El área central contiene la lectura o conversación y el contenido que el estudiante debe revisar.
- El panel lateral ofrece únicamente apoyo relacionado con la actividad activa: criterios, reglas, escenarios, vocabulario, historial o progreso.
- El panel de apoyo ofrece vistas contextuales. En redacción, el plan y el progreso aparecen como pestañas del mismo panel; el contenido central que se repite se filtra. “Ver progreso” abre esa pestaña directamente en un clic sin cambiar el nivel de la interfaz; para editar el plan desde esa vista, se abre “Más apoyo” y luego “Plan” (3 clics en total).
- El historial se abre desde su propio control y agrupa chats por actividad. En escritorio se abre en dos acciones (abrir historial y elegir chat); en móvil, en tres (menú, chats recientes y selección).

## Criterios de diseño derivados de las lecturas

- Mostrar la frase original, la propuesta y la razón del cambio; el estudiante conserva la decisión.
- Entregar ayuda gradual: primero una pista, luego explicación o ejemplos si se solicitan.
- Permitir revisar ejemplos en contexto y guardar vocabulario.
- Mantener un flujo corto con progreso ligado a los eventos de la sesión, sin métricas semanales simuladas que parezcan datos reales ni diagramas de operaciones, relaciones AND/DOWN, datos de protocolo o etiquetas académicas en la experiencia del estudiante.
- Ofrecer el historial de versiones cuando el estudiante necesite recuperar una redacción anterior.

## Paleta de apoyo

- Rojo coral: gramática.
- Azul: vocabulario.
- Gris azulado neutro: tono.
- Amarillo ámbar: claridad.
- Verde azulado: avance y acciones principales.

Los colores se acompañan de etiquetas de texto e iconos para que la distinción no dependa únicamente del color.
