# Lingua IA · práctica conversacional de inglés

Prototipo frontend local para **aprender expresiones de correo** y **vocabulario en contexto**, basado en las tareas 1 y 3 de `HTA_unificado_sin_IA_v7.pdf` y el feedback docente recibido el 24/11/2026.

Abre `index.html` o ejecuta `python3 -m http.server 8000` desde esta carpeta y visita `http://localhost:8000`. No hay dependencias de frontend, backend, claves ni llamadas a un LLM. El navegador guarda conversaciones, notas y versiones en localStorage; recupera las prácticas desde el icono de conversaciones, que abre un panel lateral izquierdo. La disponibilidad de almacenamiento en archivos locales depende del navegador; con HTTP se conserva por dirección y puerto.

El inicio es un chat vacío. Las ideas de inicio preparan un mensaje editable y las sugerencias contextuales pueden añadirse, editarse, ignorarse o descartarse. El usuario escribe hipótesis, producciones y explicaciones en el mismo chat. El menú y la etapa actual permanecen visibles al desplazarse. La ruta es opcional y sus etapas se pueden abrir desde ese indicador. El progreso describe actividad, no dominio.

- [Guía de demostración y mensajes exactos](guia.md)
- [Revisión del HTA, planes complementarios y trazabilidad](docs/REVISION_HTA_Y_TRAZABILIDAD.md)
- [Ideas de papers y límites de su adaptación](guiaPapers.md)
- [Guía vigente de los 71 principios](GUIA_PRINCIPIOS_IHC.html) · [Markdown](GUIA_PRINCIPIOS_IHC.md) · [PDF](GUIA_PRINCIPIOS_IHC.pdf)
- [Capturas actuales](docs/screenshots/actual/)
- [Guía anterior preservada](docs/originales/principios-anterior/)

## Código activo

`index.html` carga `js/icons.js`, `js/tutor-data.js` y `js/tutor.js`; el diseño está en `css/style.css`. Los demás archivos JS corresponden a la implementación anterior y no se cargan. Las respuestas y reglas son material didáctico preparado. La revisión de texto arbitrario, evaluación automática de aprendizaje, diccionario en vivo y predicción generativa quedan fuera del prototipo.

## Comprobación y regeneración

```bash
python3 tools/test_navigation_scroll.py
python3 tools/test_learning_flow.py
python3 tools/test_guide_integrity.py
python3 tools/generate_screenshots.py
python3 tools/build_guides.py
python3 tools/build_pdf.py
```

Ejecutar secuencialmente: las comprobaciones de navegador comparten un archivo temporal. Requieren Firefox; el PDF usa pdflatex. Las pruebas recorren la app real a 1440, 390 y 320 px. No sustituyen una evaluación con estudiantes.
