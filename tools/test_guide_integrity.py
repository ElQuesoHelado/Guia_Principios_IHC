import os
import re
import glob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUIDE_MD = os.path.join(BASE_DIR, "GUIA_PRINCIPIOS_IHC.md")
GUIDE_HTML = os.path.join(BASE_DIR, "GUIA_PRINCIPIOS_IHC.html")

def test_screenshots_exist():
    print("1. Verificando capturas de pantalla...")
    with open(GUIDE_MD, "r", encoding="utf-8") as f:
        content = f.read()
    images = re.findall(r'!\[.*?\]\((docs/screenshots/.*?)\)', content)
    assert len(images) >= 14, f"Se esperaban al menos 14 imágenes, encontradas: {len(images)}"
    for img_rel in images:
        full_path = os.path.join(BASE_DIR, img_rel)
        assert os.path.exists(full_path), f"ERROR: Imagen no encontrada: {full_path}"
    print(f"   -> {len(images)} referencias a imágenes verificadas físicamente en disco.")

def test_selectors_exist_in_code():
    print("2. Verificando veracidad de selectores en código (Anti-Alucinación)...")
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
        codebase = f.read()
    for js_path in glob.glob(os.path.join(BASE_DIR, "js", "*.js")):
        with open(js_path, "r", encoding="utf-8") as f:
            codebase += "\n" + f.read()
    for css_path in glob.glob(os.path.join(BASE_DIR, "css", "*.css")):
        with open(css_path, "r", encoding="utf-8") as f:
            codebase += "\n" + f.read()

    selectors = [
        "mode-nav", "stagebar", "stages", "correction-card", "diff-line",
        "type-badge", "help-levels", "data-criterion", "aside-content",
        "word-chip", "history-drawer", "modal-overlay", "toast",
        "composer-mode-hint", "save-word", "correction-undo"
    ]
    for sel in selectors:
        assert sel in codebase, f"ERROR DE ALUCINACIÓN: Selector '{sel}' no existe en el código real!"
    print(f"   -> {len(selectors)} selectores auditados existen exactamente en la app.")

def test_principles_count():
    print("3. Verificando conteo de principios...")
    with open(GUIDE_MD, "r", encoding="utf-8") as f:
        content = f.read()
    found_ids = set(re.findall(r'C[1-8]\.[0-9]+', content))
    assert len(found_ids) == 71, f"ERROR: Se esperaban 71 principios únicos, encontrados: {len(found_ids)}"
    print(f"   -> Los 71 principios (C1.1 a C8.11) están catalogados sin omisiones.")

if __name__ == "__main__":
    test_screenshots_exist()
    test_selectors_exist_in_code()
    test_principles_count()
    print("¡TODAS LAS PRUEBAS DE INTEGRIDAD PASARON CON ÉXITO!")
