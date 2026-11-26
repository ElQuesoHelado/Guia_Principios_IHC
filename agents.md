# Contexto vigente para agentes · Lingua IA · HTA v8

## Fuente y alcance

La referencia vigente es [HTA_correo_vocabulario_v8.pdf](HTA_correo_vocabulario_v8.pdf), proporcionado por el usuario el 25/11/2026. Conservarlo sin modificaciones. Describe dos raíces relacionadas: C0, aprendizaje de peticiones en correos académicos; V0, aprendizaje de vocabulario en contexto académico. Tiene 29 planes para los 29 nodos descompuestos. No añadir otra raíz ni reutilizar los identificadores del v7 como si fueran los actuales.

Leer [README.md](README.md), [guia.md](guia.md), [revisión y trazabilidad](docs/REVISION_HTA_Y_TRAZABILIDAD.md) y [guiaPapers.md](guiaPapers.md) antes de editar. Consultar las [transcripciones docentes](docs/feedback_docente/2026-11-24/README.md) como criterios de revisión; preservarlas literalmente. No equivalen a aprobación docente ni a observaciones completas de usuarios.

El usuario confirmó mantener un **mock con respuestas preparadas**, documentos vigentes alineados con v8 y coherencia entre palabra, oración y explicación. El historial llamado Conversaciones es la lista de chats de estas dos actividades, no una actividad adicional.

## Implementación y límites

`index.html` carga únicamente `js/icons.js`, `js/tutor-data.js`, `js/tutor-hta.js` y `js/tutor.js`; estilos en `css/style.css`. Los demás JS son históricos y no se cargan. No hay backend ni LLM externo, diccionario en vivo, evaluación general de texto ni envío real de correo.

La interfaz comienza con un chat vacío; sugerencias editables y descartables acompañan la escritura. Los apoyos y etapas son opcionales. Las fichas léxicas deben coincidir con la palabra y oración: dedicated como espacio reservado o persona comprometida son casos distintos. No usar una ficha preparada para otro contexto ni dejar que la navegación omita esa comprobación. Los botones de mensajes anteriores mantienen su contexto.

localStorage conserva prácticas, notas, versiones, palabras y contexto de repaso. El estado vigente usa `lingua-tutor-v2` y migra las sesiones de `lingua-tutor-v1` sin borrar esa clave. Mantener compatibles las sesiones anteriores; ante un contexto no preparado registrar incertidumbre, sin inventar una definición. Aportes, cambios aceptados y etapas abiertas no acreditan dominio.

La extensión de recorridos conserva fragmento, versión, actividad y mensaje pendiente en una pila de retorno; cubre C4→V0→C4 y V6→correo→vocabulario. Registrar también el retorno parcial y las dudas. La matriz por nodo está en `docs/HTA_V8_COBERTURA.md` y su catálogo en `docs/hta-v8-coverage.json`: 109 nodos, 29 planes, 80 hojas. La v8 no obliga a implementar cada hoja como botón.

## Documentos actuales y archivo

La v8 y la guía vigente de 71 principios son entregables actuales. Los documentos de versiones anteriores están en [docs/originales/previo-v8](docs/originales/previo-v8/README.md), con hashes para los once originales. La guía anterior de principios sigue en `docs/originales/principios-anterior/`. No usar esos archivos para atribuir comportamientos actuales. La matriz original de principios se conserva como referencia de comparación, no como definición de tareas.

## Verificación

Ejecutar secuencialmente `python3 tools/test_learning_flow.py`, `python3 tools/test_navigation_scroll.py`, `python3 tools/test_guide_integrity.py` , `python3 tools/test_hta_v8.py` y `python3 tools/test_hta_complete.py`. Las pruebas y capturas de navegador comparten `harness_temp.html`; no ejecutarlas en paralelo.

Capturas: `python3 tools/generate_screenshots.py`. Matriz: `python3 tools/build_hta_coverage.py`. Guías: `python3 tools/build_guides.py` y después `python3 tools/build_pdf.py`. Firefox es necesario para navegador; ImageMagick para recortes; pdflatex para la guía PDF. Las pruebas no validan empíricamente aprendizaje ni usabilidad completa. Citar controles reales y límites, sin atribuir eficacia a los papers no verificados.

Las vías de diccionario/modelo, traducción, IA y persona son ejemplos preparados o aportes externos no verificados, nunca conexiones reales. No reconstruir una hipótesis inicial después de mostrar el significado. El repaso debe permitir elegir palabra y contexto, y retomar sin mostrar primero la respuesta. Cada decisión sobre corrección se vincula a su rango y versión; conservar y comparar producciones propias.
