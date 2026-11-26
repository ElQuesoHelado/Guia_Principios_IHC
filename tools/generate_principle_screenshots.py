#!/usr/bin/env python3
"""
Genera las capturas de evidencia de los 44 principios aplicados.

El generador parte de la interfaz real (`index.html`) y aplica estados
deterministas con `DemoState` antes de capturar. No crea pantallas falsas:
solo selecciona estados, acciones y recortes.

Uso:
    python tools/generate_principle_screenshots.py
    python tools/generate_principle_screenshots.py --only C1.3 C2.1
    python tools/generate_principle_screenshots.py --out /tmp/opencode/preview
"""

from __future__ import annotations

import argparse
import io
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = Path(__file__).resolve().parent.parent
URL = (BASE_DIR / "index.html").resolve().as_uri()
DEFAULT_OUT = BASE_DIR / "docs" / "screenshots" / "principles"
WINDOW_SIZE = (1440, 986)  # Firefox headless deja un viewport de 1440x900.
VIEWPORT = (1440, 900)

STATUSES = {
    "c1": "pending",
    "c2": "pending",
    "c3": "pending",
    "c4": "pending",
}

COMPLETED = {
    "writing": [0, 1],
    "conversation": [0],
    "lessons": [0],
}


def base_state(**overrides):
    state = {
        "homeOpen": False,
        "mode": "writing",
        "help": "pista",
        "tab": "criteria",
        "version": "draft",
        "detailsLevel": 0,
        "activeStage": 2,
        "completedStages": {k: list(v) for k, v in COMPLETED.items()},
        "statuses": dict(STATUSES),
        "historyOpen": False,
        "suggestionsOpen": False,
        "supportOpen": False,
        "sideOpen": False,
        "sideAnswer": None,
        "selectedWord": None,
        "quickstartFeedback": "",
        "quickstartDraft": "",
    }
    state.update(overrides)
    return state


def all_status(value: str):
    return {key: value for key in STATUSES}


@dataclass
class Spec:
    pid: str
    filename: str
    state: dict
    selectors: list[str] = field(default_factory=list)
    viewport: bool = False
    window_height: int = WINDOW_SIZE[1]
    scroll: str | None = None
    scroll_block: str = "start"
    padding: int = 12
    pad_y: int | None = None
    setup_js: str = ""
    actions: list[tuple[str, float]] = field(default_factory=list)
    min_colors: int = 4


# Las capturas que ya estaban bien se conservan; estas son las 34 que hay que
# rehacer (26 reportadas + 8 que estaban en blanco).
SPECS: list[Spec] = [
    Spec(
        "C1.3",
        "c1_3_workspace_goal_context.png",
        base_state(),
        viewport=True,
        window_height=936,  # viewport 850: muestra la tarjeta y su acción sin el chat cortado
        scroll=".writing-draft-preview",
    ),
    Spec(
        "C2.1",
        "c2_1_proximity_draft_card.png",
        base_state(),
        selectors=[".writing-draft-preview", '[data-card="c1"]'],
        scroll=".writing-draft-preview",
    ),
    Spec(
        "C2.2",
        "c2_2_similarity_buttons.png",
        base_state(homeOpen=True),
        selectors=[".quickstart-options"],
        padding=16,
    ),
    Spec(
        "C2.3",
        "c2_3_continuity_stagebar.png",
        base_state(),
        selectors=["#stagebar"],
        padding=14,
    ),
    Spec(
        "C2.4",
        "c2_4_closure_icons.png",
        base_state(),
        selectors=[
            "#aside-content .panel-head",
            "#aside-content .criterion-card:nth-child(1)",
            "#aside-content .criterion-card:nth-child(2)",
            "#aside-content .criterion-card:nth-child(3)",
        ],
    ),
    Spec(
        "C2.5",
        "c2_5_symmetry_progress.png",
        base_state(tab="progress"),
        selectors=[
            "#aside-tabs",
            "#aside-content .panel-head",
            "#aside-content .stat-grid",
            "#aside-content .panel-note",
        ],
    ),
    Spec(
        "C3.1",
        "c3_1_structured_correction.png",
        base_state(),  # custom
    ),
    Spec(
        "C3.5",
        "c3_5_chunking_plan_steps.png",
        base_state(detailsLevel=1, tab="plan"),
        selectors=[
            "#aside-content .panel-head",
            "#aside-content .stack",
            "#aside-content .panel-actions",
        ],
    ),
    Spec(
        "C3.7",
        "c3_7_specific_controls_pills.png",
        base_state(),
        selectors=["#help-levels", ".composer-box"],
        padding=12,
        pad_y=4,
    ),
    Spec(
        "C4.1",
        "c4_1_distinct_colors_legend.png",
        base_state(),
        selectors=[".writing-draft-preview .text-box", ".legend"],
        scroll=".writing-draft-preview",
        padding=10,
    ),
    Spec(
        "C4.3",
        "c4_3_luminance_contrast_badges.png",
        base_state(tab="changes", statuses={
            "c1": "accepted",
            "c2": "rejected",
            "c3": "accepted",
            "c4": "pending",
        }),  # custom
    ),
    Spec(
        "C4.4",
        "c4_4_colorblind_neutral_tone.png",
        base_state(detailsLevel=1, tab="rules"),  # custom
    ),
    Spec(
        "C4.5",
        "c4_5_redundant_channels.png",
        base_state(statuses=all_status("rejected")),
        selectors=['[data-card="c4"]'],
        scroll='[data-card="c4"]',
        scroll_block="center",
    ),
    Spec(
        "C5.1",
        "c5_1_foveal_central_placement.png",
        base_state(
            help="explicacion",
            statuses={"c1": "accepted", "c2": "accepted", "c3": "pending", "c4": "pending"},
        ),
        selectors=['[data-card="c3"]'],
        scroll='[data-card="c3"]',
        scroll_block="center",
    ),
    Spec(
        "C5.8",
        "c5_8_unobtrusive_inline_feedback.png",
        base_state(statuses=all_status("accepted")),
        selectors=['[data-card="c4"]'],
        scroll='[data-card="c4"]',
        scroll_block="center",
    ),
    Spec(
        "C5.9",
        "c5_9_history_fixed_order.png",
        base_state(),  # custom
    ),
    Spec(
        "C6.2",
        "c6_2_plain_language_instructions.png",
        base_state(homeOpen=True),
        selectors=[".quickstart-content"],
        padding=16,
    ),
    Spec(
        "C6.3",
        "c6_3_clean_typography.png",
        base_state(),
        selectors=[".writing-draft-preview .text-box"],
        scroll=".writing-draft-preview",
        padding=10,
    ),
    Spec(
        "C6.4",
        "c6_4_mixed_case_body.png",
        base_state(help="explicacion"),
        selectors=['[data-card="c1"] .hint-box', '[data-card="c1"] .why'],
        scroll='[data-card="c1"]',
        scroll_block="center",
        pad_y=0,
    ),
    Spec(
        "C6.7",
        "c6_7_left_aligned_paragraphs.png",
        base_state(mode="lessons", tab="vocabulary"),
        selectors=[
            ".reading-card .section-head",
            ".reading-card p:nth-of-type(1)",
            ".reading-card p:nth-of-type(2)",
        ],
        scroll=".reading-card",
        padding=12,
    ),
    Spec(
        "C6.8",
        "c6_8_consistent_alignment_chat.png",
        base_state(mode="conversation", tab="vocabulary"),
        selectors=[".scenario-strip", ".chat-context-note", ".chat-messages"],
        setup_js="""
            const st = DemoState.get();
            const messages = JSON.parse(JSON.stringify(st.messages));
            messages.conversation.push({
                role: 'user',
                text: 'I have five years of experience in customer support, and I enjoy solving problems.'
            });
            DemoState.set({ messages });
        """,
        padding=12,
    ),
    Spec(
        "C6.9",
        "c6_9_scannable_rules.png",
        base_state(detailsLevel=1, tab="rules"),
        selectors=[".modal"],
        actions=[('[data-action="open-rule"][data-id="r1"]', 0.35)],
        padding=12,
    ),
    Spec(
        "C6.10",
        "c6_10_minimal_prosa.png",
        base_state(
            statuses={"c1": "accepted", "c2": "pending", "c3": "pending", "c4": "pending"},
        ),
        selectors=['[data-card="c2"]'],
        scroll='[data-card="c2"]',
        scroll_block="center",
    ),
    Spec(
        "C6.11",
        "c6_11_uncluttered_side_panel.png",
        base_state(),
        selectors=[
            "#aside-tabs",
            "#aside-content .panel-head",
            "#aside-content .panel-note",
        ],
    ),
    Spec(
        "C7.1",
        "c7_1_stagebar_versions_state.png",
        base_state(version="final", statuses={"c1": "accepted", "c2": "pending", "c3": "pending", "c4": "pending"}),
        selectors=["#stagebar", ".writing-draft-head", ".writing-draft-preview .version-tabs"],
        scroll=".writing-draft-preview",
        scroll_block="start",
        padding=12,
    ),
    Spec(
        "C7.5",
        "c7_5_visible_mode_indicator.png",
        base_state(),
        selectors=[".composer-box", ".composer-hint"],
        padding=12,
        pad_y=2,
    ),
    Spec(
        "C7.7",
        "c7_7_dominant_primary_cta.png",
        base_state(),
        selectors=['[data-card="c1"]'],
        scroll='[data-card="c1"]',
        scroll_block="center",
    ),
    Spec(
        "C7.10",
        "c7_10_contextual_popover_definition.png",
        base_state(mode="lessons", tab="vocabulary", selectedWord="productive"),
        selectors=[".reading-card"],
        scroll=".reading-card",
        scroll_block="start",
        padding=12,
    ),
    Spec(
        "C8.1",
        "c8_1_quiet_software_reading.png",
        base_state(mode="lessons", tab="vocabulary"),
        viewport=True,
        scroll=".reading-card",
        scroll_block="start",
    ),
    Spec(
        "C8.2",
        "c8_2_salient_changes_undo.png",
        base_state(tab="changes", statuses={
            "c1": "accepted",
            "c2": "rejected",
            "c3": "accepted",
            "c4": "pending",
        }),
        selectors=[
            "#aside-tabs",
            "#aside-content .panel-head",
            "#aside-content .change-row:nth-child(1)",
            "#aside-content .change-row:nth-child(2)",
        ],
    ),
    Spec(
        "C8.3",
        "c8_3_done_pending_stages.png",
        base_state(tab="progress"),
        window_height=936,  # viewport 850: evita el fragmento de chat sobre el borrador
        selectors=[
            "#stagebar",
            "#aside-tabs",
            "#aside-content .panel-head",
            "#aside-content .stat-grid",
            "#aside-content .panel-note",
        ],
        setup_js="document.querySelector('.chat-scroll').scrollTop = 9999;",
    ),
    Spec(
        "C8.5",
        "c8_5_information_scent_options.png",
        base_state(detailsLevel=2),
        selectors=[
            "#aside-tabs",
            "#aside-content .panel-head",
            "#aside-content .advanced-menu-note",
            "#aside-content .advanced-menu-list",
        ],
    ),
    Spec(
        "C8.6",
        "c8_6_specific_action_verbs.png",
        base_state(version="draft"),
        selectors=[".modal"],
        actions=[('[data-action="open-version-history"]', 0.35)],
        padding=12,
    ),
    Spec(
        "C8.10",
        "c8_10_closure_completion.png",
        base_state(),  # custom
    ),
]


def start_driver() -> webdriver.Firefox:
    options = Options()
    options.add_argument("-headless")
    options.binary_location = "/usr/bin/firefox"
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(*WINDOW_SIZE)
    return driver


def wait_ready(driver: webdriver.Firefox) -> None:
    WebDriverWait(driver, 15).until(
        lambda d: d.execute_script("return document.readyState === 'complete' && !!window.DemoState")
    )
    try:
        driver.execute_async_script(
            "const done = arguments[0]; document.fonts.ready.then(() => done(true));"
        )
    except Exception:
        pass
    time.sleep(0.25)


def load(driver: webdriver.Firefox) -> None:
    driver.get(URL)
    wait_ready(driver)


def js_click(driver: webdriver.Firefox, selector: str) -> None:
    clicked = driver.execute_script(
        """
        const el = document.querySelector(arguments[0]);
        if (!el) return false;
        el.click();
        return true;
        """,
        selector,
    )
    if not clicked:
        raise RuntimeError(f"No se encontró el selector para click: {selector}")


def apply_state(driver: webdriver.Firefox, state: dict, setup_js: str = "") -> None:
    driver.execute_script("window.DemoState.set(arguments[0]);", state)
    if setup_js:
        driver.execute_script(setup_js)
    time.sleep(0.35)


def scroll_to(driver: webdriver.Firefox, selector: str, block: str = "start") -> None:
    found = driver.execute_script(
        """
        const el = document.querySelector(arguments[0]);
        if (!el) return false;
        el.scrollIntoView({ block: arguments[1], inline: 'nearest' });
        return true;
        """,
        selector,
        block,
    )
    if not found:
        raise RuntimeError(f"No se encontró el selector para scroll: {selector}")
    time.sleep(0.25)


def rect_of(driver: webdriver.Firefox, selector: str):
    return driver.execute_script(
        """
        const el = document.querySelector(arguments[0]);
        if (!el) return null;
        const r = el.getBoundingClientRect();
        if (r.width <= 0 || r.height <= 0) return null;
        return { left: r.left, top: r.top, right: r.right, bottom: r.bottom };
        """,
        selector,
    )


def screenshot_image(driver: webdriver.Firefox) -> Image.Image:
    return Image.open(io.BytesIO(driver.get_screenshot_as_png())).convert("RGB")


def crop_selectors(
    driver: webdriver.Firefox,
    selectors: Iterable[str],
    padding: int,
    pad_y: int | None = None,
) -> Image.Image:
    rects = []
    for selector in selectors:
        rect = rect_of(driver, selector)
        if rect:
            rects.append(rect)
    if not rects:
        raise RuntimeError(f"Ningún selector visible: {list(selectors)}")

    left = min(r["left"] for r in rects)
    top = min(r["top"] for r in rects)
    right = max(r["right"] for r in rects)
    bottom = max(r["bottom"] for r in rects)

    vertical = padding if pad_y is None else pad_y
    left = max(0, int(left - padding))
    top = max(0, int(top - vertical))
    right = min(VIEWPORT[0], int(right + padding))
    bottom = min(VIEWPORT[1], int(bottom + vertical))

    if right - left < 80 or bottom - top < 30:
        raise RuntimeError(f"Recorte demasiado pequeño: {(left, top, right, bottom)}")

    return screenshot_image(driver).crop((left, top, right, bottom))


def save_image(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, optimize=True)


def assert_not_blank(img: Image.Image, pid: str, min_colors: int = 4) -> None:
    colors = img.getcolors(maxcolors=4_000_000)
    count = len(colors) if colors else 4_000_001
    if count < min_colors:
        raise RuntimeError(f"{pid}: captura sospechosa con {count} colores: {img.size}")
    print(f"  {pid}: {img.width}x{img.height}px · {count} colores")


def capture_spec(driver: webdriver.Firefox, spec: Spec, out_dir: Path) -> Image.Image:
    print(f"- {spec.pid} → {spec.filename}")
    driver.set_window_size(WINDOW_SIZE[0], spec.window_height)
    load(driver)
    apply_state(driver, spec.state, spec.setup_js)

    # Las capturas de workspace no deben heredar el quickstart de la carga
    # inicial: si aparece, la evidencia mostraría una pantalla equivocada.
    if not spec.state.get("homeOpen"):
        in_quickstart = driver.execute_script(
            "return document.body.classList.contains('quickstart-mode')"
        )
        if in_quickstart:
            raise RuntimeError(f"{spec.pid}: el quickstart sigue visible en una captura de workspace")

    if spec.scroll:
        scroll_to(driver, spec.scroll, spec.scroll_block)

    for selector, delay in spec.actions:
        js_click(driver, selector)
        time.sleep(delay)

    if spec.viewport:
        img = screenshot_image(driver)
    else:
        img = crop_selectors(driver, spec.selectors, spec.padding, spec.pad_y)

    assert_not_blank(img, spec.pid, spec.min_colors)
    save_image(img, out_dir / spec.filename)
    return img


# ---------------------------------------------------------------------------
# Composiciones derivadas de capturas reales
# ---------------------------------------------------------------------------

def font(size: int = 14):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def with_border(img: Image.Image, color=(210, 215, 223)) -> Image.Image:
    from PIL import ImageOps

    return ImageOps.expand(img, border=1, fill=color)


def side_by_side(
    left: Image.Image,
    right: Image.Image,
    labels: tuple[str, str],
    out_path: Path,
    gap: int = 18,
    margin: int = 14,
    label_height: int = 28,
) -> Image.Image:
    left = with_border(left)
    right = with_border(right)
    width = left.width + gap + right.width + margin * 2
    height = max(left.height, right.height) + label_height + margin * 2
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, margin - 2), labels[0], fill=(59, 68, 87), font=font(13))
    draw.text((margin + left.width + gap, margin - 2), labels[1], fill=(59, 68, 87), font=font(13))
    y = margin + label_height
    canvas.paste(left, (margin, y))
    canvas.paste(right, (margin + left.width + gap, y))
    save_image(canvas, out_path)
    return canvas


def stack_vertical(images: list[Image.Image], out_path: Path, gap: int = 16, margin: int = 0) -> Image.Image:
    width = max(img.width for img in images) + margin * 2
    height = sum(img.height for img in images) + gap * (len(images) - 1) + margin * 2
    canvas = Image.new("RGB", (width, height), "white")
    y = margin
    for img in images:
        canvas.paste(img, ((width - img.width) // 2, y))
        y += img.height + gap
    save_image(canvas, out_path)
    return canvas


def grayscale(img: Image.Image) -> Image.Image:
    return img.convert("L").convert("RGB")


def deuteranopia(img: Image.Image) -> Image.Image:
    # Matriz estándar de simulación para deuteranopia.
    matrix = (
        0.625, 0.375, 0.0, 0.0,
        0.700, 0.300, 0.0, 0.0,
        0.000, 0.300, 0.700, 0.0,
    )
    return img.convert("RGB", matrix)


def capture_structured_corrections(driver: webdriver.Firefox, out_dir: Path) -> None:
    pid = "C3.1"
    print(f"- {pid} → c3_1_structured_correction.png")

    load(driver)
    apply_state(driver, base_state())
    scroll_to(driver, '[data-card="c1"]', "center")
    first = crop_selectors(driver, ['[data-card="c1"]'], 10)

    load(driver)
    apply_state(
        driver,
        base_state(
            statuses={
                "c1": "accepted",
                "c2": "accepted",
                "c3": "pending",
                "c4": "pending",
            }
        ),
    )
    scroll_to(driver, '[data-card="c3"]', "center")
    third = crop_selectors(driver, ['[data-card="c3"]'], 10)

    assert_not_blank(first, pid)
    assert_not_blank(third, pid)
    result = stack_vertical([first, third], out_dir / "c3_1_structured_correction.png", gap=18)
    print(f"  compuesta: {result.width}x{result.height}px")


def capture_color_composites(driver: webdriver.Firefox, out_dir: Path) -> None:
    # C4.3: estados con distinta luminancia + escala de grises.
    print("- C4.3 → c4_3_luminance_contrast_badges.png")
    load(driver)
    apply_state(
        driver,
        base_state(
            tab="changes",
            statuses={
                "c1": "accepted",
                "c2": "rejected",
                "c3": "accepted",
                "c4": "pending",
            },
        ),
    )
    changes = crop_selectors(
        driver,
        [
            "#aside-tabs",
            "#aside-content .panel-head",
            "#aside-content .stack",
        ],
        10,
    )
    assert_not_blank(changes, "C4.3")
    side_by_side(
        changes,
        grayscale(changes),
        ("Vista normal", "Escala de grises"),
        out_dir / "c4_3_luminance_contrast_badges.png",
    )

    # C4.4: categorías + simulación de deuteranopia.
    print("- C4.4 → c4_4_colorblind_neutral_tone.png")
    load(driver)
    apply_state(driver, base_state(detailsLevel=1, tab="rules"))
    rules = crop_selectors(
        driver,
        [
            "#aside-content .panel-head",
            "#aside-content .rule-card:nth-child(1)",
            "#aside-content .rule-card:nth-child(2)",
            "#aside-content .rule-card:nth-child(3)",
        ],
        10,
    )
    assert_not_blank(rules, "C4.4")
    side_by_side(
        rules,
        deuteranopia(rules),
        ("Vista normal", "Simulación deuteranopia"),
        out_dir / "c4_4_colorblind_neutral_tone.png",
    )


def capture_history_order(driver: webdriver.Firefox, out_dir: Path) -> None:
    print("- C5.9 → c5_9_history_fixed_order.png")

    history_selectors = [
        "#history-drawer .history-head",
        "#history-drawer .history-groups",
    ]

    load(driver)
    apply_state(driver, base_state(historyOpen=True))
    before = crop_selectors(driver, history_selectors, 10)
    assert_not_blank(before, "C5.9")

    load(driver)
    apply_state(driver, base_state(historyOpen=True))
    js_click(driver, '[data-action="select-session"][data-session="s2"]')
    time.sleep(0.25)
    js_click(driver, '[data-action="toggle-history"]')
    time.sleep(0.35)
    after = crop_selectors(driver, history_selectors, 10)
    assert_not_blank(after, "C5.9")

    side_by_side(
        before,
        after,
        ("Orden inicial", "Tras seleccionar otra sesión"),
        out_dir / "c5_9_history_fixed_order.png",
        gap=16,
    )


def capture_closure(driver: webdriver.Firefox, out_dir: Path) -> None:
    print("- C8.10 → c8_10_closure_completion.png")
    load(driver)
    apply_state(driver, base_state())
    for _ in range(2):
        js_click(driver, '[data-stage="3"]')
        time.sleep(0.18)

    toast_visible = driver.execute_script(
        "return !document.querySelector('#toast').hidden && document.querySelector('#toast').classList.contains('is-visible')"
    )
    if not toast_visible:
        raise RuntimeError("C8.10: el aviso de cierre no está visible")

    # La vista completa conserva la stagebar, el aviso de cierre y el texto:
    # el estado final se entiende sin recortes que oculten el contexto.
    result = screenshot_image(driver)
    assert_not_blank(result, "C8.10")
    save_image(result, out_dir / "c8_10_closure_completion.png")
    print(f"  vista completa: {result.width}x{result.height}px")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="*", default=None, help="IDs concretos, por ejemplo C1.3 C2.1")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Directorio de salida")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    selected = set(args.only) if args.only else None
    specs = [spec for spec in SPECS if selected is None or spec.pid in selected]
    custom = {
        "C3.1": capture_structured_corrections,
        "C4.3": capture_color_composites,
        "C4.4": capture_color_composites,
        "C5.9": capture_history_order,
        "C8.10": capture_closure,
    }

    driver = start_driver()
    try:
        rendered = set()
        for spec in specs:
            if spec.pid in custom:
                # Las funciones compuestas generan más de un archivo a la vez.
                if spec.pid in {"C4.3", "C4.4"}:
                    if "color" not in rendered:
                        capture_color_composites(driver, out_dir)
                        rendered.add("color")
                elif spec.pid not in rendered:
                    custom[spec.pid](driver, out_dir)
                    rendered.add(spec.pid)
                continue
            capture_spec(driver, spec, out_dir)
    finally:
        driver.quit()

    print(f"\nCapturas generadas en {out_dir}")


if __name__ == "__main__":
    main()
