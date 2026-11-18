import os
import subprocess
import time
from PIL import Image

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs", "screenshots")
os.makedirs(DOCS_DIR, exist_ok=True)

HARNESS_HTML = os.path.join(BASE_DIR, "harness_temp.html")

def create_harness(state_js_code):
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()
    
    injection = f"""
    <script>
    document.addEventListener('DOMContentLoaded', () => {{
        setTimeout(() => {{
            {state_js_code}
            if (window.DemoState) window.DemoState.touch();
        }}, 200);
    }});
    </script>
    </body>
    """
    modified_html = html.replace("</body>", injection)
    with open(HARNESS_HTML, "w", encoding="utf-8") as f:
        f.write(modified_html)

def take_raw_screenshot(output_png):
    cmd = [
        "firefox",
        "--headless",
        f"--screenshot={output_png}",
        f"file://{HARNESS_HTML}",
        "--window-size=1440,900"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# Capturas requeridas con sus bounding boxes precisos en 1440x900
CAPTURE_SPECS = [
    # 01: Header y navegación
    ("01_header_nav.png", "", (0, 0, 1440, 68)),
    # 02: Barra de etapas y botón progreso
    ("02_stagebar.png", "", (280, 64, 1160, 126)),
    # 03: Tarjeta de corrección central
    ("03_correction_card.png", "", (300, 230, 1140, 520)),
    # 04: Badges de tipo
    ("04_type_badges.png", "", (315, 240, 640, 285)),
    # 05: Niveles de ayuda gradual
    ("05_help_levels.png", "", (200, 680, 1000, 718)),
    # 06: Panel lateral de criterios
    ("06_side_criteria.png", "", (1020, 64, 1440, 650)),
    # 07: Panel lateral de progreso
    ("07_side_progress.png", "window.DemoState.set({tab: 'progress', detailsLevel: 0});", (1020, 64, 1440, 480)),
    # 08: Panel lateral de reglas
    ("08_side_rules.png", "window.DemoState.set({tab: 'rules'});", (1020, 64, 1440, 680)),
    # 09: Lecciones y lectura interactiva
    ("09_lessons_reading.png", "window.DemoState.set({mode: 'lessons', selectedWord: 'productive'});", (300, 120, 1140, 650)),
    # 10: Conversación escrita y diálogo
    ("10_conversation_chat.png", "window.DemoState.set({mode: 'conversation'});", (300, 120, 1140, 620)),
    # 11: Drawer menú de tareas
    ("11_drawer_menu.png", "window.DemoState.set({drawerOpen: true});", (0, 0, 420, 750)),
    # 12: Drawer de historial agrupado
    ("12_history_drawer.png", "window.DemoState.set({historyOpen: true});", (0, 0, 420, 800)),
    # 13: Modal de regla abierta
    ("13_modal_rule.png", "const c = window.DemoData.corrections[0]; window.DemoState.helpers.rule ? null : null; document.querySelector('[data-action=\"correction-rule\"]')?.click();", (420, 150, 1020, 750)),
    # 14: Composer e indicación de atajos
    ("14_composer_hints.png", "", (200, 715, 1000, 804)),
]

def main():
    print("Iniciando generación de capturas...")
    raw_tmp = os.path.join(BASE_DIR, "tools", "raw_temp.png")
    for filename, code, box in CAPTURE_SPECS:
        print(f"Generando {filename}...")
        create_harness(code)
        take_raw_screenshot(raw_tmp)
        img = Image.open(raw_tmp)
        cropped = img.crop(box)
        dest = os.path.join(DOCS_DIR, filename)
        cropped.save(dest, optimize=True)
    if os.path.exists(raw_tmp): os.remove(raw_tmp)
    if os.path.exists(HARNESS_HTML): os.remove(HARNESS_HTML)
    print(f"¡Éxito! 14 imágenes creadas en {DOCS_DIR}")

if __name__ == "__main__":
    main()
