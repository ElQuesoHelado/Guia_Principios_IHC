import os
import re
import docx
from PIL import Image
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ARCHIVE_DIR = os.path.join(BASE_DIR, "docs", "originales", "previo-v8")
# Herramienta histórica: no genera la guía vigente del prototipo.
SRC_DOCX = os.path.join(ARCHIVE_DIR, "Evaluacion_detallada_reglas_Lingua_IA.docx")
OUT_DOCX = os.path.join(ARCHIVE_DIR, "Evaluacion_detallada_reglas_Lingua_IA_con_capturas_regenerada.docx")
IMG_DIR = os.path.join(BASE_DIR, "docs", "screenshots", "principles")

# Catálogo completo de las 44 capturas precisas y sus pies de figura
CROPS = {
    'C1.1': ('c1_1_mode_nav.png', 'Barra superior con botones y tareas explícitas sin ambigüedad'),
    'C1.2': ('c1_2_header_nav.png', 'Navegación persistente y uniforme en el header con tratamiento consistente de estados'),
    'C1.3': ('c1_3_workspace_goal_context.png', 'Workspace de Redacción con la tarea, el texto revisado, la tarjeta de decisión y sus acciones en la misma pantalla'),
    'C2.1': ('c2_1_proximity_draft_card.png', 'Agrupación por proximidad: el texto en revisión y la tarjeta de corrección con diff y decisión integrados'),
    'C2.2': ('c2_2_similarity_buttons.png', 'Similitud visual: las tres actividades de inicio comparten estructura, tipografía y tratamiento de tarjeta'),
    'C2.3': ('c2_3_continuity_stagebar.png', 'Continuidad visual en la secuencia horizontal y lineal de etapas de la tarea'),
    'C2.4': ('c2_4_closure_icons.png', 'Iconos lineales simples y distinguibles por su silueta dentro de tarjetas de contorno completo'),
    'C2.5': ('c2_5_symmetry_progress.png', 'Cuadrícula simétrica de métricas de progreso: dos tarjetas del mismo tamaño y peso visual'),
    'C2.6': ('c2_6_figure_ground_modal.png', 'Separación nítida de planos de figura y fondo mediante overlay oscurecido y elevación del diálogo modal'),
    'C3.1': ('c3_1_structured_correction.png', 'Dos tarjetas de corrección consecutivas comparten la misma estructura modular en bloques (tipo, título, diff, ayuda y acciones)'),
    'C3.2': ('c3_2_visual_hierarchy.png', 'Jerarquía visual clara: navegación superior, área central de trabajo y panel de apoyo lateral'),
    'C3.4': ('c3_4_grouped_content_vocab.png', 'Agrupación homogénea de términos y vocabulario guardado en tarjetas en el panel lateral'),
    'C3.5': ('c3_5_chunking_plan_steps.png', 'Chunking aplicado a la tarea: pasos numerados del 1 al 5 en bloques separados y verificables'),
    'C3.7': ('c3_7_specific_controls_pills.png', 'Control segmentado de nivel de ayuda: un dominio finito de opciones evita valores inválidos'),
    'C3.8': ('c3_8_labels_adjacent_diff.png', 'Etiquetas identificadoras inmediatamente adyacentes a sus respectivos valores en la línea de diff'),
    'C4.1': ('c4_1_distinct_colors_legend.png', 'Leyenda y marcas del borrador con cuatro colores de categoría claramente distintos entre sí'),
    'C4.3': ('c4_3_luminance_contrast_badges.png', 'Comparación en escala de grises: los estados conservan contraste de luminancia sin depender solo del tono'),
    'C4.4': ('c4_4_colorblind_neutral_tone.png', 'Simulación de deuteranopia sobre las categorías de reglas: las etiquetas y los estados siguen siendo identificables'),
    'C4.5': ('c4_5_redundant_channels.png', 'Estado rechazado comunicado por color, etiqueta textual y nota de estado, no solo por el color'),
    'C5.1': ('c5_1_foveal_central_placement.png', 'La explicación y la decisión aparecen dentro de la misma tarjeta, junto al texto revisado'),
    'C5.8': ('c5_8_unobtrusive_inline_feedback.png', 'Confirmación rutinaria integrada en la tarjeta, sin modal ni alerta fuerte que sature la atención'),
    'C5.9': ('c5_9_history_fixed_order.png', 'Historial con orden estable: al cambiar de sesión solo se mueve la marca \'actual\', no las actividades'),
    'C5.10': ('c5_10_distinct_icons_drawer.png', 'Iconografía con contornos contrastantes y siluetas periféricas claramente distinguibles'),
    'C6.2': ('c6_2_plain_language_instructions.png', 'Instrucciones en español cotidiano y directo, sin jerga técnica ni términos computacionales opacos'),
    'C6.3': ('c6_3_clean_typography.png', 'Tipografía sans-serif limpia y familiar (Figtree) con espaciado optimizado para la lectura en pantalla'),
    'C6.4': ('c6_4_mixed_case_body.png', 'Pista y explicación en caja mixta: el cuerpo no usa mayúsculas sostenidas y conserva la silueta de las palabras'),
    'C6.5': ('c6_5_quiet_background.png', 'Fondo plano y limpio de alto contraste sin texturas ni interferencias detrás del texto'),
    'C6.7': ('c6_7_left_aligned_paragraphs.png', 'Párrafos de lectura alineados a la izquierda para un anclaje ocular uniforme al inicio de cada línea'),
    'C6.8': ('c6_8_consistent_alignment_chat.png', 'Alineación consistente en la conversación: convención espacial tutor a la izquierda y usuario a la derecha'),
    'C6.9': ('c6_9_scannable_rules.png', 'Diseño escaneable: tarjetas de reglas con bloques visuales destacados de \'Correcto\' y \'Evitar\''),
    'C6.10': ('c6_10_minimal_prosa.png', 'Pista breve y explicación bajo demanda: la tarjeta no muestra prosa completa de entrada'),
    'C6.11': ('c6_11_uncluttered_side_panel.png', 'Panel lateral reducido a pestañas contextuales: no repite el texto ni el artículo del área central'),
    'C7.1': ('c7_1_stagebar_versions_state.png', 'Visualización persistente del progreso de etapas y del estado de versiones del borrador'),
    'C7.5': ('c7_5_visible_mode_indicator.png', 'Indicador persistente y explícito del modo de tarea activo visible al pie del área de entrada'),
    'C7.7': ('c7_7_dominant_primary_cta.png', 'Llamada a la acción dominante destacada en color de marca (\'Usar esta sugerencia\') frente a opciones secundarias'),
    'C7.8': ('c7_8_flat_broad_navigation.png', 'Arquitectura de navegación horizontal y plana accesible con un solo clic sin submenús anidados'),
    'C7.10': ('c7_10_contextual_popover_definition.png', 'Definición y ejemplos situados inmediatamente junto al término seleccionado sin exigir memorización'),
    'C8.1': ('c8_1_quiet_software_reading.png', 'Interfaz despejada y silenciosa que sitúa el material de lectura en primer plano visual'),
    'C8.2': ('c8_2_salient_changes_undo.png', 'Cambios revisados con estado visible (\'Aceptada\'/\'Rechazada\') y acción Deshacer en cada fila'),
    'C8.3': ('c8_3_done_pending_stages.png', 'Etapas completadas, etapa actual y pendientes visibles a la vez en la barra y en el panel de progreso'),
    'C8.5': ('c8_5_information_scent_options.png', 'Rastro de información explícito en los botones de actividad, describiendo claramente el objetivo resultante'),
    'C8.6': ('c8_6_specific_action_verbs.png', 'Verbos de acción específicos en los controles (\'Usar esta sugerencia\' y \'Mantener mi frase\') en lugar de botones genéricos'),
    'C8.7': ('c8_7_task_oriented_concepts.png', 'Conceptos y caminos de interacción basados en las tareas del estudiante (\'Conversación\', \'Lecciones\', \'Redacción\')'),
    'C8.10': ('c8_10_closure_completion.png', 'Cierre de la actividad: las cuatro etapas quedan completadas y el aviso confirma que los cambios siguen disponibles')
}

def validate_image(code, path):
    img = Image.open(path).convert('RGB')
    width, height = img.size
    if width < 100 or height < 40:
        raise RuntimeError(f"{code}: imagen demasiado pequeña ({width}x{height}): {path}")
    colors = img.getcolors(maxcolors=4_000_000)
    unique = len(colors) if colors else 4_000_001
    if unique < 4:
        raise RuntimeError(f"{code}: imagen en blanco o casi vacía ({unique} colores): {path}")
    return img


def get_dimensions(w, h, max_w=5.2, max_h=3.2):
    aspect = w / h
    w_in = max_w
    h_in = w_in / aspect
    if h_in > max_h:
        h_in = max_h
        w_in = h_in * aspect
    if w < 400:
        w_in = min(w_in, 3.5)
        h_in = w_in / aspect
    return w_in

def main():
    doc = docx.Document(SRC_DOCX)
    base_images = len(doc.inline_shapes)  # el documento fuente ya puede traer un logo
    targets = []

    for i, p in enumerate(doc.paragraphs[:370]):
        m = re.match(r'^(C\d+\.\d+)', p.text.strip())
        if m:
            code = m.group(1)
            j = i + 1
            cond_val = None
            why_p = None
            while j < len(doc.paragraphs[:370]):
                pj = doc.paragraphs[j]
                if pj.style.name.startswith('Heading'):
                    break
                t = pj.text.strip()
                if t.startswith('Condición:'):
                    cond_val = t.replace('Condición:', '').strip()
                elif t.startswith('Por qué:'):
                    why_p = pj
                j += 1
            if cond_val == 'Cumple' and why_p is not None:
                targets.append((code, why_p))

    print(f"Principios que cumplen a procesar: {len(targets)}")
    if len(targets) != len(CROPS):
        raise RuntimeError(
            f"Desajuste: {len(targets)} principios 'Cumple' frente a {len(CROPS)} capturas en CROPS"
        )

    target_codes = [code for code, _ in targets]
    missing_specs = [code for code in target_codes if code not in CROPS]
    extra_specs = [code for code in CROPS if code not in target_codes]
    if missing_specs or extra_specs:
        raise RuntimeError(f"IDs sin captura: {missing_specs}; capturas sin principio: {extra_specs}")

    # Preflight: ninguna captura ausente o en blanco puede llegar al DOCX.
    for code in target_codes:
        fname, _ = CROPS[code]
        img_path = os.path.join(IMG_DIR, fname)
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"{code}: falta la captura {img_path}")
        validate_image(code, img_path)
    print(f"Capturas verificadas: {len(target_codes)}")

    for code, why_p in targets:
        if code in CROPS:
            fname, cap_text = CROPS[code]
            img_path = os.path.join(IMG_DIR, fname)
            pil_img = validate_image(code, img_path)
            w_px, h_px = pil_img.size
            w_in = get_dimensions(w_px, h_px)

            # 1. Párrafo de imagen
            img_p = doc.add_paragraph()
            img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            img_p.paragraph_format.space_before = Pt(8)
            img_p.paragraph_format.space_after = Pt(2)
            run = img_p.add_run()
            run.add_picture(img_path, width=Inches(w_in))

            # 2. Párrafo de pie de figura
            cap_p = doc.add_paragraph()
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap_p.paragraph_format.space_before = Pt(0)
            cap_p.paragraph_format.space_after = Pt(8)
            cap_run = cap_p.add_run(f"Evidencia de interfaz ({code}): {cap_text}")
            cap_run.font.size = Pt(9)
            cap_run.font.italic = True
            cap_run.font.color.rgb = RGBColor(100, 116, 139)

            # Insertar en orden después de Por qué:
            why_p._p.addnext(cap_p._p)
            why_p._p.addnext(img_p._p)

    doc.save(OUT_DOCX)

    check = docx.Document(OUT_DOCX)
    images = len(check.inline_shapes)
    captions = sum(
        1 for p in check.paragraphs if p.text.startswith("Evidencia de interfaz (")
    )
    expected_images = base_images + len(CROPS)
    if images != expected_images or captions != len(CROPS):
        raise RuntimeError(
            f"Documento incompleto: {images} imágenes y {captions} leyendas; "
            f"se esperaban {expected_images} imágenes ({base_images} base + {len(CROPS)} evidencias) "
            f"y {len(CROPS)} leyendas"
        )
    print(f"Verificación final: {images} imágenes y {captions} leyendas")
    print(f"¡Éxito! Documento generado en: {OUT_DOCX}")

if __name__ == "__main__":
    main()
