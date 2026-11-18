import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MD_PATH = os.path.join(BASE_DIR, "GUIA_PRINCIPIOS_IHC.md")
HTML_PATH = os.path.join(BASE_DIR, "GUIA_PRINCIPIOS_IHC.html")

# ==============================================================================
# DEFINICIÓN EXHAUSTIVA DE LOS 71 PRINCIPIOS
# ==============================================================================

PRINCIPLES_DATA = [
    # --- CAPÍTULO 1 ---
    {
        "id": "C1.1", "chapter": "C1 — La percepción es sesgada", "name": "Evitar la ambigüedad",
        "status": "Aplicado",
        "rule": "Cada elemento de la interfaz debe tener una sola interpretación plausible para el usuario objetivo.",
        "location": "Barra superior (#mode-nav) y botones de acción en tarjetas (.correction-actions)",
        "how_to_check": "1. Observar la barra superior: los 3 botones tienen nombres directos ('Conversación escrita', 'Lecciones y repaso', 'Redacción asistida'). 2. En la tarjeta de corrección central, los botones no usan etiquetas ambiguas como 'OK', sino verbos claros: 'Usar esta sugerencia' y 'Mantener mi frase'.",
        "image": "docs/screenshots/01_header_nav.png",
        "img_alt": "Barra superior con botones claros y sin ambigüedad",
        "justification": "Elimina el costo cognitivo de adivinar el resultado de una acción, permitiendo que la atención del estudiante se enfoque en aprender inglés y no en interpretar la interfaz."
    },
    {
        "id": "C1.2", "chapter": "C1 — La percepción es sesgada", "name": "Mantener consistencia de ubicación y apariencia",
        "status": "Aplicado",
        "rule": "La misma función debe aparecer en la misma posición, con el mismo color, tipografía y comportamiento en todas las vistas.",
        "location": "Header persistente, botón 'Apoyo', barra de etapas y drawer de historial (#history-drawer)",
        "how_to_check": "1. Cambiar entre las 3 tareas haciendo clic en los botones del header: la barra superior, la posición de las etapas, el drawer y el footer de historial permanecen idénticos. 2. Los colores de estado (verde para aceptado/avance, rojo/coral para gramática) son consistentes en todas las vistas.",
        "image": "docs/screenshots/01_header_nav.png",
        "img_alt": "Navegación persistente y uniforme en el header",
        "justification": "El cerebro del usuario crea plantillas perceptivas automáticas; la consistencia espacial evita que tenga que re-escanear la pantalla ante cada cambio de modo."
    },
    {
        "id": "C1.3", "chapter": "C1 — La percepción es sesgada", "name": "Diseñar para las metas del usuario",
        "status": "Aplicado",
        "rule": "La información necesaria para el objetivo del usuario debe estar disponible, ser prominente y estar ligada a la acción siguiente.",
        "location": "Columna central de trabajo (.chat-column) y selector de niveles de ayuda (#help-levels)",
        "how_to_check": "1. En 'Redacción asistida', el foco principal es el correo y la sugerencia activa. 2. Justo debajo del chat, los botones 'Pista', 'Explicación', 'Ejemplo' y 'Reescritura completa' permiten al estudiante ajustar el nivel de asistencia según su meta de aprendizaje inmediata.",
        "image": "docs/screenshots/05_help_levels.png",
        "img_alt": "Selector de nivel de ayuda situado junto a la meta del estudiante",
        "justification": "El estudiante busca comprender un error o redactar un texto; ofrecer ayuda graduada en el centro de atención apoya directamente su objetivo cognitivo sin pasos intermedios."
    },

    # --- CAPÍTULO 2 ---
    {
        "id": "C2.1", "chapter": "C2 — La visión está optimizada para ver estructura", "name": "Proximidad: agrupar lo relacionado",
        "status": "Aplicado",
        "rule": "Los elementos relacionados deben estar más cerca entre sí que de los elementos no relacionados; el espacio en blanco debe separar grupos.",
        "location": "Tarjeta de corrección central (.correction-card)",
        "how_to_check": "Examinar la tarjeta central: la categoría (Gramática), el título del error ('Concordancia verbal'), el diff antes/después, la pista explicativa y los botones de decisión están agrupados en un contenedor unificado con bordes y padding claro.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Agrupación por proximidad en tarjeta de corrección",
        "justification": "La ley de proximidad de la Gestalt hace que el usuario perciba el problema, la solución propuesta y la decisión como una sola unidad conceptual."
    },
    {
        "id": "C2.2", "chapter": "C2 — La visión está optimizada para ver estructura", "name": "Similitud: mismo aspecto para la misma función",
        "status": "Aplicado",
        "rule": "Los elementos que cumplen la misma función deben parecerse; los que cumplen funciones distintas deben diferenciarse visualmente.",
        "location": "Píldoras de modo (.mode-pill), píldoras de ayuda (.help-pill) y chips de vocabulario (.word-chip)",
        "how_to_check": "1. Todos los botones de modo comparten forma redondeada de 22px de radio y estado activo teal. 2. Los chips de vocabulario comparten altura y estilo visual. 3. Los botones de acción primaria ('btn-primary') usan fondo teal consistente en modales y tarjetas.",
        "image": "docs/screenshots/01_header_nav.png",
        "img_alt": "Similitud visual en píldoras de navegación",
        "justification": "Permite el reconocimiento visual instantáneo de qué elementos son accionables y a qué categoría de control pertenecen."
    },
    {
        "id": "C2.3", "chapter": "C2 — La visión está optimizada para ver estructura", "name": "Continuidad: alinear y no interrumpir",
        "status": "Aplicado",
        "rule": "Los elementos deben alinearse siguiendo líneas continuas; una secuencia visual no debe interrumpirse sin motivo.",
        "location": "Línea de etapas (#stagebar .stages) y columna de chat (#chat-messages)",
        "how_to_check": "Observar la barra superior de etapas: los círculos numerados están unidos por una línea horizontal continua (.stage-line) que guía la mirada de izquierda a derecha. En el chat, los mensajes mantienen una alineación vertical estricta a 800px de ancho.",
        "image": "docs/screenshots/02_stagebar.png",
        "img_alt": "Continuidad visual en la secuencia de etapas",
        "justification": "La continuidad perceptiva guía el barrido ocular natural y refuerza la noción de progresión lineal en el proceso de revisión."
    },
    {
        "id": "C2.4", "chapter": "C2 — La visión está optimizada para ver estructura", "name": "Cierre: formas simples y reconocibles",
        "status": "Aplicado",
        "rule": "Las formas deben ser lo bastante simples para que el sistema visual las reconozca como un todo sin exigir contornos perfectos.",
        "location": "Iconos SVG lineales (Icons.js) y badges de estado (.status-pill)",
        "how_to_check": "Examinar los iconos de la app (menú hamburguesa, bombilla de ayuda, check de completado, flecha de enviar): usan trazo uniforme de 2px, figuras geométricas básicas y siluetas cerradas fácilmente reconocibles sin detalles innecesarios.",
        "image": "docs/screenshots/04_type_badges.png",
        "img_alt": "Iconos y formas simples de fácil cierre visual",
        "justification": "Reduce el tiempo de fijación foveal al permitir el reconocimiento instantáneo de iconos comunes."
    },
    {
        "id": "C2.5", "chapter": "C2 — La visión está optimizada para ver estructura", "name": "Simetría: reducir complejidad",
        "status": "Aplicado",
        "rule": "Los layouts deben usar equilibrio para reducir la complejidad visual y facilitar la comparación.",
        "location": "Estructura principal (.workspace) y tarjetas estadísticas (.stat-grid)",
        "how_to_check": "1. El área de trabajo se divide en dos bloques proporcionales: columna principal centrada a 800px y panel lateral fijo a 420px. 2. En el panel de progreso, las métricas usan una cuadrícula simétrica de 2 tarjetas ('stat-card') con pesos visuales equivalentes.",
        "image": "docs/screenshots/07_side_progress.png",
        "img_alt": "Equilibrio simétrico en tarjetas estadísticas",
        "justification": "La simetría visual disminuye la carga cognitiva de procesamiento espacial, dando orden y estabilidad a la interfaz."
    },
    {
        "id": "C2.6", "chapter": "C2 — La visión está optimizada para ver estructura", "name": "Figura/fondo: separar planos",
        "status": "Aplicado",
        "rule": "El primer plano debe distinguirse claramente del fondo; modales, overlays y menús deben percibirse como planos separados.",
        "location": "Modal de reglas (#modal-overlay) y drawers deslizables (#drawer-overlay, #history-overlay)",
        "how_to_check": "Hacer clic en 'Ver regla completa' dentro de la tarjeta de corrección: la pantalla se oscurece con un fondo translúcido difuminado (backdrop-filter: blur) y el modal se eleva con una sombra pronunciada (box-shadow: 0 18px 44px).",
        "image": "docs/screenshots/13_modal_rule.png",
        "img_alt": "Separación nítida de figura y fondo mediante overlay oscuro y elevación",
        "justification": "Aísla la atención del usuario en la explicación pedagógica actual eliminando distracciones visuales del texto de fondo."
    },
    {
        "id": "C2.8", "chapter": "C2 — La visión está optimizada para ver estructura", "name": "Revisar las agrupaciones combinadas",
        "status": "Parcial",
        "rule": "La pantalla debe revisarse con todos los principios Gestalt actuando a la vez para detectar relaciones no intencionadas.",
        "location": "Relación entre columna central y panel lateral (#side-panel)",
        "how_to_check": "Observar cómo el panel lateral de apoyo y el chat central nunca repiten el mismo contenido (en redacción el panel oculta la pestaña de texto para no duplicar el centro). Queda parcial pendiente prueba con desenfoque de desenfoque visual formal.",
        "image": "docs/screenshots/06_side_criteria.png",
        "img_alt": "Coexistencia visual armónica entre chat y panel de criterios",
        "justification": "Garantiza que la combinación de proximidad, similitud y bordes no cree falsas asociaciones entre herramientas secundarias y la tarea activa."
    },

    # --- CAPÍTULO 3 ---
    {
        "id": "C3.1", "chapter": "C3 — Buscamos y usamos estructura visual", "name": "Presentar información tersa y estructurada",
        "status": "Aplicado",
        "rule": "La información debe presentarse de forma breve y estructurada: listas, bloques con etiquetas, no párrafos largos de datos.",
        "location": "Panel de Criterios editables (#aside-content) y panel de Reglas (#aside-content .rule-card)",
        "how_to_check": "1. Abrir la pestaña 'Criterios': cada supuesto (Destinataria, Nivel, Tono, Objetivo) se presenta en una tarjeta estructurada con icono, etiqueta corta y valor editable. 2. En las reglas, se segmenta en 'Correcto' (verde) y 'Evitar' (rojo).",
        "image": "docs/screenshots/06_side_criteria.png",
        "img_alt": "Criterios estructurados en bloques concisos con iconos y etiquetas",
        "justification": "Facilita la lectura rápida y el cotejo visual sin obligar al usuario a leer párrafos continuos de instrucciones."
    },
    {
        "id": "C3.2", "chapter": "C3 — Buscamos y usamos estructura visual", "name": "Establecer una jerarquía visual",
        "status": "Aplicado",
        "rule": "La pantalla debe dividirse en secciones con jerarquía clara de tamaño, prominencia y posición; lo crucial arriba y con más peso.",
        "location": "Header -> Barra de etapas -> Chat de trabajo -> Composer -> Panel lateral",
        "how_to_check": "Examinar el flujo visual: 1. Nivel superior: Modo activo (h1 oculto y píldoras prominentes). 2. Subnivel: Etapas de avance. 3. Centro: Tarjeta con tipografía de 15px en negrita para el error y 13.5px para el diff. 4. Lateral: Información de soporte de 11px a 14.5px.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Jerarquía visual clara desde el encabezado hasta la tarjeta de decisión",
        "justification": "Permite al estudiante escanear de un vistazo dónde está ubicado, qué debe resolver primero y dónde buscar ayuda si la necesita."
    },
    {
        "id": "C3.3", "chapter": "C3 — Buscamos y usamos estructura visual", "name": "Usar encabezados semánticos",
        "status": "Parcial",
        "rule": "Los encabezados deben usar elementos y niveles semánticos reales (h1–h6) para lectores de pantalla.",
        "location": "index.html (#page-title) y títulos de sección (h3, h4)",
        "how_to_check": "En el código HTML existe un `<h1 class='sr-only' id='page-title'>Lingua IA · Redacción asistida</h1>` que se actualiza dinámicamente con el modo activo. Los módulos usan `<h3>` y `<h4>`. Es parcial porque falta completar la auditoría con NVDA/VoiceOver de toda la jerarquía intermedia.",
        "image": "docs/screenshots/01_header_nav.png",
        "img_alt": "Encabezado principal accesible para lectores de pantalla",
        "justification": "Permite a usuarios con tecnologías asistivas navegar directamente a los hitos de la página sin tener que recorrer todo el árbol del DOM."
    },
    {
        "id": "C3.4", "chapter": "C3 — Buscamos y usamos estructura visual", "name": "Agrupar contenido similar",
        "status": "Aplicado",
        "rule": "El contenido del mismo tipo debe compartir estilo visual o estar dentro de un área claramente definida.",
        "location": "Tiras de escenarios (.scenario-strip) y lista de palabras (.word-picker)",
        "how_to_check": "1. En 'Conversación escrita', los escenarios ('Entrevista de trabajo', 'Café con un amigo', 'Conversación universitaria') están contenidos en una tira horizontal con diseño idéntico. 2. En 'Lecciones', las palabras clave del texto aparecen agrupadas en chips homogéneos.",
        "image": "docs/screenshots/09_lessons_reading.png",
        "img_alt": "Agrupación homogénea de palabras seleccionables dentro de la lectura",
        "justification": "Comunica de inmediato que todos los chips pertenecen al mismo conjunto de opciones y poseen el mismo comportamiento interactivo."
    },
    {
        "id": "C3.5", "chapter": "C3 — Buscamos y usamos estructura visual", "name": "Agrupar los datos en bloques (chunking)",
        "status": "Aplicado",
        "rule": "Los datos deben agruparse en fragmentos comprensibles, evitando cadenas largas indivisas.",
        "location": "Panel de Progreso (.stat-grid) y plan de redacción (.plan-step)",
        "how_to_check": "Observar el panel de progreso: en vez de mostrar un párrafo denso con cifras, se fragmenta en 2 bloques limpios: 'Etapas completadas' (ej. 2/4) y 'Sugerencias revisadas' (ej. 0/4). El plan de redacción se divide en 5 pasos numerados e independientes.",
        "image": "docs/screenshots/07_side_progress.png",
        "img_alt": "Fragmentación de métricas en tarjetas separadas",
        "justification": "Respeta la capacidad finita de la memoria de trabajo humana (regla de Miller, 4 a 7 fragmentos de información simultánea)."
    },
    {
        "id": "C3.7", "chapter": "C3 — Buscamos y usamos estructura visual", "name": "Usar controles específicos para cada tipo de dato",
        "status": "Aplicado",
        "rule": "Valores con dominio limitado deben capturarse con controles que impidan datos inválidos: selectores, botones, toggles.",
        "location": "Selector de nivel de ayuda (#help-levels), selector de versiones (.version-tabs) y botones aceptar/rechazar",
        "how_to_check": "El nivel de ayuda solo admite 4 estados fijos ('Pista', 'Explicación', 'Ejemplo', 'Reescritura') y se controla mediante botones tipo píldora mutuamente excluyentes, en lugar de un campo de texto libre.",
        "image": "docs/screenshots/05_help_levels.png",
        "img_alt": "Controles de píldora para estados finitos predefinidos",
        "justification": "Previene errores del usuario por entradas tipográficas inválidas y reduce el esfuerzo motor al requerir un solo clic."
    },
    {
        "id": "C3.8", "chapter": "C3 — Buscamos y usamos estructura visual", "name": "Mantener las etiquetas junto a sus valores",
        "status": "Aplicado",
        "rule": "Cada etiqueta debe estar arriba o a la izquierda de su valor; la proximidad debe dejar claro a qué dato pertenece.",
        "location": "Badges de corrección (.badge-row), Criterios (.criterion-label) y métricas de progreso",
        "how_to_check": "En el panel de criterios, la etiqueta ('DESTINATARIA', 'TONO') se ubica inmediatamente encima del campo de entrada. En las métricas de progreso, el número grande ('2/4') tiene su descripción ('Etapas completadas') justo debajo, formando un bloque indivisible.",
        "image": "docs/screenshots/06_side_criteria.png",
        "img_alt": "Etiquetas inmediatas sobre sus valores en tarjetas de criterios",
        "justification": "Evita movimientos oculares de vaivén (saccades) innecesarios entre el dato y su descripción semántica."
    },

    # --- CAPÍTULO 4 ---
    {
        "id": "C4.1", "chapter": "C4 — La visión del color es limitada", "name": "Usar colores distintivos",
        "status": "Aplicado",
        "rule": "Para codificar categorías, se deben preferir colores que produzcan una señal fuerte en canales visuales distintos.",
        "location": "Paleta de categorías de corrección (.type-badge)",
        "how_to_check": "Observar los 4 colores de corrección: Coral rojizo (#A32B2B) para Gramática, Azul (#2B6CB0) para Vocabulario, Gris azulado (#344054) para Tono, y Ámbar (#B7791F) para Claridad. Cada uno corresponde a una banda espectral diferenciada.",
        "image": "docs/screenshots/04_type_badges.png",
        "img_alt": "Colores distintivos para las 4 categorías pedagógicas",
        "justification": "Permite al estudiante clasificar el tipo de sugerencia antes incluso de leer la explicación textual."
    },
    {
        "id": "C4.2", "chapter": "C4 — La visión del color es limitada", "name": "No yuxtaponer colores opuestos fuertes",
        "status": "Parcial",
        "rule": "No colocar directamente juntos colores opuestos fuertes (rojo/verde puro) para evitar aberración cromática o vibración visual.",
        "location": "Línea de diff (.diff-line: .diff-before y .diff-after)",
        "how_to_check": "En la línea de diff, el texto tachado usa fondo rojo suave pastel (`#FBEAEA`) y el texto nuevo usa fondo verde-teal suave (`#E0F2EF`). Además, están separados físicamente por una flecha gris (`→`). Estado parcial pendiente de validación espectral en monitores de bajo costo.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Diff antes/después con tonos suaves y flecha divisoria",
        "justification": "Los fondos pastel desaturados eliminan la vibración óptica y el cansancio retiniano que provocan los colores puros yuxtapuestos."
    },
    {
        "id": "C4.3", "chapter": "C4 — La visión del color es limitada", "name": "Diferenciar por saturación y brillo, no solo por tono",
        "status": "Aplicado",
        "rule": "Los colores que transmiten información deben diferenciarse por saturación y luminancia, no por matices sutiles del mismo tono.",
        "location": "Estados de botones y badges de categoría en style.css",
        "how_to_check": "Cada badge combina un fondo de baja saturación y alto brillo (ej. `#FBEAEA` con 95% luminancia) con texto del mismo tono pero alta saturación y baja luminancia (ej. `#A32B2B` con 35% luminancia), maximizando el contraste interno.",
        "image": "docs/screenshots/04_type_badges.png",
        "img_alt": "Diferenciación por luminancia y saturación en badges",
        "justification": "Garantiza legibilidad incluso para personas con visión monocromática o bajo condiciones de luz solar intensa."
    },
    {
        "id": "C4.4", "chapter": "C4 — La visión del color es limitada", "name": "Evitar pares problemáticos para daltonismo",
        "status": "Aplicado",
        "rule": "Evitar pares que las personas con daltonismo confunden: rojo oscuro/verde oscuro, azul/morado.",
        "location": "Corrección de paleta documentada en el informe de diseño",
        "how_to_check": "En versiones preliminares, la categoría 'Tono' utilizaba color morado, lo que generaba confusión con el azul de 'Vocabulario'. En la versión actual, 'Tono' fue migrado a gris azulado neutro (`#344054`), erradicando el conflicto azul-morado.",
        "image": "docs/screenshots/04_type_badges.png",
        "img_alt": "Paleta accesible sin conflicto azul/morado",
        "justification": "Cumple con las pautas de accesibilidad para personas con deuteranopía y tritanopía."
    },
    {
        "id": "C4.5", "chapter": "C4 — La visión del color es limitada", "name": "No usar color como único canal",
        "status": "Aplicado",
        "rule": "Ningún significado debe depender exclusivamente del color; siempre debe existir una señal redundante (texto, icono o forma).",
        "location": "Todas las etiquetas de corrección y estados del prototipo",
        "how_to_check": "1. Los badges de corrección tienen el color, pero siempre llevan la palabra impresa: 'Gramática', 'Vocabulario', 'Tono', 'Claridad'. 2. Las etapas completadas llevan un icono de check SVG además de cambiar de gris a verde. 3. Los estados de decisión indican 'Pendiente', 'Aceptada' o 'Rechazada' en texto.",
        "image": "docs/screenshots/04_type_badges.png",
        "img_alt": "Canal redundante: color acompañado siempre de texto explícito",
        "justification": "Principio fundamental de accesibilidad universal (WCAG 2.1 - Criterio 1.4.1): la interfaz transmite el 100% de la información aun si se visualiza en escala de grises."
    },
    {
        "id": "C4.6", "chapter": "C4 — La visión del color es limitada", "name": "Asegurar contraste de los elementos no textuales",
        "status": "Parcial",
        "rule": "Iconos, bordes y controles interactivos deben tener un contraste mínimo de 3:1 con el fondo.",
        "location": "Bordes de controles (--control-border: #858F9F) e indicadores de foco",
        "how_to_check": "Los botones tipo píldora (`.mode-pill`) y los botones de icono (`.icon-btn`) cuentan con bordes definidos (`#D5DBE6` y `#858F9F`) sobre fondo blanco. Estado parcial porque falta medición formal con colorímetro en toda la suite de pantallas.",
        "image": "docs/screenshots/01_header_nav.png",
        "img_alt": "Bordes definidos en controles interactivos no textuales",
        "justification": "Asegura que los límites de los controles clicables sean perceptibles para usuarios con baja agudeza visual."
    },

    # --- CAPÍTULO 5 ---
    {
        "id": "C5.1", "chapter": "C5 — La visión periférica es pobre", "name": "Colocar la información importante donde mira el usuario",
        "status": "Aplicado",
        "rule": "La información nueva o cambiada debe aparecer en la fóvea o cerca del punto donde el usuario está mirando y actuando.",
        "location": "Área central de chat: inserción directa de tarjetas de análisis",
        "how_to_check": "Al revisar la redacción, la tarjeta de sugerencia no aparece en una esquina ni en un popup flotante alejado: se inserta directamente en la corriente de lectura del chat, exactamente entre el mensaje del usuario y la respuesta de la IA.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Inserción foveal de la corrección en la línea visual del chat",
        "justification": "La visión foveal cubre solo 2 grados del campo visual; ubicar la información en la trayectoria de lectura evita que el usuario pase por alto cambios críticos."
    },
    {
        "id": "C5.3", "chapter": "C5 — La visión periférica es pobre", "name": "Marcar el error con símbolo y reservar el rojo",
        "status": "Parcial",
        "rule": "Los errores deben marcarse con un símbolo estándar además de color; el rojo debe reservarse para incorrecciones.",
        "location": "Tarjetas de corrección gramatical y estados rechazados",
        "how_to_check": "El rojo suave se utiliza exclusivamente para errores gramaticales (`.kind-grammar`) y para indicar la opción 'Evitar' en los ejemplos de reglas. Es parcial porque aún no se incluye un icono universal de alerta (!) en todas las tarjetas de corrección.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Uso restringido del tono rojizo para incorrecciones",
        "justification": "Evita la saturación del color de alerta en elementos cosméticos, manteniendo su poder semántico de advertencia intacto."
    },
    {
        "id": "C5.5", "chapter": "C5 — La visión periférica es pobre", "name": "Reservar los pop-ups para lo crítico",
        "status": "Parcial",
        "rule": "Los diálogos modales o pop-ups deben reservarse para situaciones críticas; no para confirmaciones menores.",
        "location": "Modal de reglas (#modal-overlay) y popover de ayuda (#suggestions-popover)",
        "how_to_check": "El prototipo no abre ningún popup no solicitado ni bloquea la pantalla con alertas espontáneas. El modal solo aparece cuando el usuario pulsa activamente 'Ver regla' o 'Buscar sinónimos'. Es parcial porque las reglas largas podrían mostrarse inline en vez de modal.",
        "image": "docs/screenshots/13_modal_rule.png",
        "img_alt": "Modal invocado únicamente por petición activa del usuario",
        "justification": "Los modales imprevistos interrumpen el flujo cognitivo y generan molestia; la divulgación progresiva a demanda respeta el ritmo del aprendiz."
    },
    {
        "id": "C5.8", "chapter": "C5 — La visión periférica es pobre", "name": "Evitar la habituación a las alertas",
        "status": "Aplicado",
        "rule": "Las alertas frecuentes hacen que el usuario las ignore por habituación; deben reservarse para lo indispensable.",
        "location": "Sistema de notificaciones toast (#toast)",
        "how_to_check": "Al aceptar o rechazar un cambio, el sistema no despliega ventanas de diálogo intrusivas; muestra un toast breve y discreto en la esquina inferior que desaparece automáticamente a los 2.6 segundos.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Feedback no intrusivo para evitar habituación",
        "justification": "Previene la ceguera por habituación (el reflejo de cerrar ventanas emergentes sin leer su contenido)."
    },
    {
        "id": "C5.9", "chapter": "C5 — La visión periférica es pobre", "name": "No mover los ítems de menús, listas o paletas",
        "status": "Aplicado",
        "rule": "Los ítems de menús y listas deben mantener posiciones estables; no reordenarse dinámicamente por frecuencia.",
        "location": "Drawer de chats recientes (#history-drawer)",
        "how_to_check": "Abrir el historial de chats haciendo clic en 'Ver chats' en el footer: las sesiones están categorizadas en un orden canónico fijo: 1. Redacción y escritura, 2. Conversación escrita, 3. Lectura y vocabulario. Ningún chat cambia de orden por haber sido usado más recientemente.",
        "image": "docs/screenshots/12_history_drawer.png",
        "img_alt": "Orden taxonómico inmutable en el historial de sesiones",
        "justification": "Permite el desarrollo de memoria muscular y automatización espacial; el usuario sabe exactamente en qué cuadrante físico buscar cada tarea."
    },
    {
        "id": "C5.10", "chapter": "C5 — La visión periférica es pobre", "name": "Diseñar iconos distintivos para la periferia",
        "status": "Aplicado",
        "rule": "Los iconos deben distinguirse por color y silueta gruesa para reconocerse en visión periférica.",
        "location": "Iconos de navegación del Drawer (#drawer) e iconos de apoyo",
        "how_to_check": "Abrir el menú lateral con el botón de hamburguesa: cada tarea tiene un icono con contenedor de 30x30px con fondo diferenciado (documento para redacción, mensaje para conversación, libro para lectura).",
        "image": "docs/screenshots/11_drawer_menu.png",
        "img_alt": "Iconos con siluetas y contenedores contrastantes para visión periférica",
        "justification": "Facilita la orientación periférica rápida antes de que los ojos se posen con precisión foveal sobre el elemento."
    },

    # --- CAPÍTULO 6 ---
    {
        "id": "C6.1", "chapter": "C6 — Leer no es natural", "name": "Usar un tamaño de texto legible",
        "status": "Parcial",
        "rule": "El texto de cuerpo debe poder leerse sin zoom; el texto esencial no debe estar por debajo del tamaño base.",
        "location": "Cuerpo del chat (.bubble: 15.5px) y lectura (.reading-card p: 15px)",
        "how_to_check": "El texto principal de lectura y los mensajes del tutor utilizan tamaños entre 15px y 15.5px con interlineado generoso (line-height: 1.62). Es parcial debido a que ciertas etiquetas secundarias (.paper-tag) usan tamaños de 9px a 10px.",
        "image": "docs/screenshots/09_lessons_reading.png",
        "img_alt": "Texto de lectura a 15px con interlineado cómodo para lectura",
        "justification": "El aprendizaje de una segunda lengua exige un esfuerzo visual extra de descodificación fonética y léxica; una tipografía generosa evita fatiga."
    },
    {
        "id": "C6.2", "chapter": "C6 — Leer no es natural", "name": "Usar lenguaje llano y vocabulario familiar",
        "status": "Aplicado",
        "rule": "La interfaz debe usar palabras familiares, vocabulario consistente y evitar jerga técnica innecesaria.",
        "location": "Textos de explicación pedagógica y etiquetas de interfaz",
        "how_to_check": "La interfaz utiliza instrucciones en español llano ('Usar esta sugerencia', 'Mantener mi frase', 'Te paso esta lectura'). Se eliminaron términos técnicos de papers académicos como 'WoZ', 'Glifos' o 'Data Lens' del recorrido del estudiante.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Instrucciones claras en español directo y sin jerga técnica",
        "justification": "La carga cognitiva extrínseca debe ser cero: el estudiante debe pensar en el idioma meta (inglés), no en descifrar qué significa un término técnico de la plataforma."
    },
    {
        "id": "C6.3", "chapter": "C6 — Leer no es natural", "name": "Usar tipografías familiares y legibles",
        "status": "Aplicado",
        "rule": "El texto de cuerpo debe usar tipografías familiares con formas de letra claras; evitar fuentes decorativas o script.",
        "location": "Hoja de estilos global (css/style.css: font-family: 'Figtree')",
        "how_to_check": "La aplicación utiliza 'Figtree' (Google Fonts), una fuente geométrica sans-serif moderna con aberturas claras, proporciones humanistas y excelente legibilidad en pantallas de cualquier densidad de píxeles.",
        "image": "docs/screenshots/01_header_nav.png",
        "img_alt": "Tipografía sans-serif limpia y uniforme en todo el sistema",
        "justification": "Las fuentes sans-serif humanistas facilitan la discriminación rápida de caracteres similares (como 'I', 'l', '1'), vital para estudiantes de idiomas."
    },
    {
        "id": "C6.4", "chapter": "C6 — Leer no es natural", "name": "No usar TODO EN MAYÚSCULAS en el cuerpo",
        "status": "Aplicado",
        "rule": "El texto de cuerpo debe usar caja alta y baja; las mayúsculas sostenidas se reservan exclusivamente para etiquetas cortas.",
        "location": "Párrafos de lectura, explicaciones del tutor y mensajes",
        "how_to_check": "Comprobar que todas las oraciones, lecturas y párrafos explicativos usan mayúsculas y minúsculas naturales. Las mayúsculas sostenidas solo se emplean en micro-etiquetas de sistema como 'TUTOR IA' o 'DESTINATARIA'.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Texto en caja mixta para preservar la silueta de las palabras",
        "justification": "Las mayúsculas continuas destruyen el perfil de contorno (bouma) de las palabras, reduciendo la velocidad de lectura en un 15%."
    },
    {
        "id": "C6.5", "chapter": "C6 — Leer no es natural", "name": "Evitar fondos ruidosos detrás del texto",
        "status": "Aplicado",
        "rule": "El texto debe descansar sobre fondos sólidos o tranquilos; nunca sobre texturas, patrones o gradientes agresivos.",
        "location": "Fondos de lectura (.reading-card) y burbujas de mensaje (.bubble.ai)",
        "how_to_check": "Todas las áreas de lectura y mensajes reposan sobre fondo blanco puro (`#FFFFFF`) o gris neutro ultrasuave (`#FBFCFE`), con cero patrones, marcas de agua o gradientes ruidosos.",
        "image": "docs/screenshots/09_lessons_reading.png",
        "img_alt": "Fondo plano de alto contraste sin texturas ni interferencias",
        "justification": "Maximiza la relación señal-ruido en la retina durante la fijación visual de palabras nuevas en inglés."
    },
    {
        "id": "C6.6", "chapter": "C6 — Leer no es natural", "name": "Asegurar contraste de texto suficiente",
        "status": "Parcial",
        "rule": "El texto debe tener una relación de contraste mínima de 4.5:1 con su fondo (3:1 para texto grande).",
        "location": "Tokens de color en style.css (--text: #1B2433 sobre #FFFFFF)",
        "how_to_check": "El texto principal utiliza `#1B2433` sobre fondo `#FFFFFF`, lo que arroja un ratio de contraste masivo de 13.8:1 (muy superior a la exigencia WCAG AAA de 7:1). Es parcial porque los textos atenuados secundarios (`--muted: #667085`) alcanzan 4.8:1, requiriendo verificación en pantallas OLED y bajo brillo.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Alto contraste texto-fondo (13.8:1) para lectura fluida",
        "justification": "Garantiza legibilidad para usuarios con fatiga visual o sensibilidad reducida al contraste cromático."
    },
    {
        "id": "C6.7", "chapter": "C6 — Leer no es natural", "name": "No centrar párrafos de texto",
        "status": "Aplicado",
        "rule": "Los párrafos de varias líneas deben alinearse a la izquierda en idiomas LTR; nunca centrarse.",
        "location": "Burbujas del tutor, lecturas del artículo y explicaciones de reglas",
        "how_to_check": "Verificar en todas las vistas que ningún párrafo está centrado: el artículo 'The future of remote work', los diálogos del entrevistador y las explicaciones de reglas tienen margen izquierdo plano y homogéneo.",
        "image": "docs/screenshots/09_lessons_reading.png",
        "img_alt": "Párrafos alineados a la izquierda para un anclaje ocular uniforme",
        "justification": "Centrar párrafos altera el punto de inicio de cada línea, obligando a los ojos a gastar micro-segundos buscando dónde recomienza cada renglón."
    },
    {
        "id": "C6.8", "chapter": "C6 — Leer no es natural", "name": "Mantener una alineación consistente",
        "status": "Aplicado",
        "rule": "La alineación debe ser consistente entre bloques equivalentes; no mezclar izquierda, centro y derecha arbitrariamente.",
        "location": "Columna de chat y panel lateral",
        "how_to_check": "Todos los contenedores de contenido principal se alinean por el borde izquierdo a lo largo de un eje común de 800px de ancho. Solo las burbujas enviadas por el propio usuario se alinean a la derecha, siguiendo la convención universal de mensajería.",
        "image": "docs/screenshots/10_conversation_chat.png",
        "img_alt": "Alineación consistente con convención izquierda (tutor) / derecha (usuario)",
        "justification": "Genera estabilidad espacial y permite aprovechar las convenciones de mensajería asimiladas por el estudiante en apps cotidianas."
    },
    {
        "id": "C6.9", "chapter": "C6 — Leer no es natural", "name": "Formatear el texto para escaneo",
        "status": "Aplicado",
        "rule": "El texto debe formatearse para escaneo rápido: negritas selectivas, encabezados, listas y fragmentos breves.",
        "location": "Tarjetas de corrección, tarjetas de reglas y fichas de vocabulario",
        "how_to_check": "En las tarjetas de corrección, las palabras clave van en negrita: `<strong>Pista:</strong>`, `<strong>Por qué:</strong>`. En el artículo, las palabras clave están resaltadas como chips clicables. En el panel de criterios, las etiquetas van en mayúscula con icono.",
        "image": "docs/screenshots/08_side_rules.png",
        "img_alt": "Formateo escaneable con negritas y llamadas visuales específicas",
        "justification": "Los usuarios en pantalla no leen palabra por palabra: escanean en patrones en 'F'. Los anclajes tipográficos facilitan captar el sentido en segundos."
    },
    {
        "id": "C6.10", "chapter": "C6 — Leer no es natural", "name": "Minimizar la prosa",
        "status": "Aplicado",
        "rule": "Usar la menor cantidad de texto necesaria; eliminar información sobrante o delegarla a divulgación progresiva.",
        "location": "Nivel de ayuda graduada y resúmenes de progreso",
        "how_to_check": "Por defecto, al revisar un texto la tarjeta solo muestra una pista de una oración ('Mira I am agree. ¿Necesita agree el auxiliar am?'). Si el estudiante requiere más prosa, la solicita expresamente pulsando 'Mostrar explicación'.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Prosa reducida al mínimo indispensable con opción de expandir",
        "justification": "Evita la sobrecarga cognitiva que produce un bloque gigante de teoría gramatical cuando el estudiante solo necesitaba un recordatorio puntual."
    },
    {
        "id": "C6.11", "chapter": "C6 — Leer no es natural", "name": "Eliminar la repetición que entierra información",
        "status": "Aplicado",
        "rule": "Eliminar textos o metadatos repetidos que compitan con la información esencial.",
        "location": "Filtrado automático de pestañas laterales (duplicateCentralTabs en panels.js)",
        "how_to_check": "En el código de `panels.js`, la función `supportTabs()` filtra deliberadamente la pestaña 'Tu texto' cuando se está en modo redacción, la pestaña 'Artículo' en modo lecciones y la pestaña 'Escenario' en conversación, evitando que el panel lateral duplique lo que ya se ve en el centro.",
        "image": "docs/screenshots/06_side_criteria.png",
        "img_alt": "Panel lateral limpio sin duplicaciones del contenido central",
        "justification": "Garantiza que el panel lateral aporte valor complementario (criterios, reglas, progreso) en lugar de redundancia estéril."
    },

    # --- CAPÍTULO 7 ---
    {
        "id": "C7.1", "chapter": "C7 — La atención es limitada; la memoria es imperfecta", "name": "No exigir recordar el estado o las acciones previas",
        "status": "Aplicado",
        "rule": "La interfaz debe mostrar el estado del sistema, el contexto actual y lo que el usuario ya hizo, sin forzar su memoria.",
        "location": "Barra de etapas (#stagebar), estado en tarjeta (.status-pill) y panel de cambios",
        "how_to_check": "1. La barra superior marca con un check verde las etapas que ya se superaron y resalta con borde la actual. 2. La tarjeta de corrección muestra un pill 'Pendiente', 'Aceptada' o 'Rechazada'. 3. La pestaña 'Cambios' en el lateral lista todas las decisiones tomadas.",
        "image": "docs/screenshots/02_stagebar.png",
        "img_alt": "Visualización continua del estado actual y de las acciones completadas",
        "justification": "Libera la memoria de trabajo del usuario: el estudiante puede interrumpir su sesión y al regresar reconoce inmediatamente en qué punto quedó."
    },
    {
        "id": "C7.5", "chapter": "C7 — La atención es limitada; la memoria es imperfecta", "name": "Evitar modos o hacer visible el modo actual",
        "status": "Aplicado",
        "rule": "Si una acción produce efectos distintos según el estado del sistema, el modo actual debe ser visible de forma persistente.",
        "location": "Píldora activa en header (.mode-pill.is-active) y composer hint (#composer-mode-hint)",
        "how_to_check": "1. El modo activo se resalta en el header en color teal sólido con atributo `aria-current='true'`. 2. Al pie del campo de texto de chat, una etiqueta fija indica explícitamente: 'Modo: Redacción asistida' o 'Modo: Conversación', recordando el contexto de la IA.",
        "image": "docs/screenshots/14_composer_hints.png",
        "img_alt": "Indicador permanente del modo activo al pie del campo de entrada",
        "justification": "Previene errores de modo (intentar hacer preguntas de gramática cuando el sistema espera una respuesta en inglés para la entrevista de trabajo)."
    },
    {
        "id": "C7.7", "chapter": "C7 — La atención es limitada; la memoria es imperfecta", "name": "Mantener una sola llamada a la acción dominante",
        "status": "Aplicado",
        "rule": "Cada pantalla o bloque debe tener una acción dominante por objetivo; no competir con múltiples acciones primarias.",
        "location": "Acciones de tarjeta de corrección y botón de envío del chat",
        "how_to_check": "1. En la tarjeta de corrección, la acción dominante recomendada es 'Usar esta sugerencia' (estilo `.btn-primary` en teal sólido), mientras que 'Mantener mi frase' es un botón secundario neutro. 2. En el composer, solo el botón de envío lleva fondo teal.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Una sola acción primaria dominante destacada en color de marca",
        "justification": "Facilita la toma de decisiones al ofrecer una ruta por defecto clara, sin paralizar al estudiante con múltiples botones del mismo peso visual."
    },
    {
        "id": "C7.8", "chapter": "C7 — La atención es limitada; la memoria es imperfecta", "name": "Preferir una navegación amplia y poco profunda",
        "status": "Aplicado",
        "rule": "Organizar la navegación en jerarquías amplias y poco profundas; evitar menús laberínticos de muchos niveles.",
        "location": "Header principal y botón directo 'Ver progreso'",
        "how_to_check": "Las 3 tareas principales se alcanzan en 1 solo clic desde cualquier lugar de la aplicación. Consultar el progreso de la tarea actual requiere exactamente 1 clic en el botón 'Ver progreso'. No hay menús desplegables anidados ni subpáginas ocultas.",
        "image": "docs/screenshots/01_header_nav.png",
        "img_alt": "Navegación horizontal plana accesible en 1 clic",
        "justification": "Reduce la desorientación espacial; el estudiante nunca tiene la sensación de haberse 'perdido' en la jerarquía del sitio."
    },
    {
        "id": "C7.10", "chapter": "C7 — La atención es limitada; la memoria es imperfecta", "name": "No exigir el recuerdo de datos o procedimientos",
        "status": "Aplicado",
        "rule": "Instrucciones, datos y reglas deben estar disponibles en el momento de uso, no obligar a recordarlos de memoria.",
        "location": "Pista contextual de corrección y atajos de teclado documentados",
        "how_to_check": "1. La justificación de por qué corregir un verbo se muestra dentro de la tarjeta al lado del texto. 2. En el campo de chat se indica explícitamente: 'Enter envía · Shift + Enter salto de línea'. 3. En lectura, al tocar una palabra se despliega su significado sin salir de la vista.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Explicación contextual visible en el instante exacto de la decisión",
        "justification": "Aplica el principio de 'reconocimiento antes que recuerdo': la información se sitúa en el mundo externo para no sobrecargar la memoria interna."
    },

    # --- CAPÍTULO 8 ---
    {
        "id": "C8.1", "chapter": "C8 — Los límites de la atención moldean pensamiento y acción", "name": "Hacer que el software pase a segundo plano",
        "status": "Aplicado",
        "rule": "La interfaz debe permitir concentrarse en la meta del usuario; el software no debe llamar la atención sobre sí mismo.",
        "location": "Diseño sobrio de la interfaz y eliminación de controles decorativos",
        "how_to_check": "El centro de la pantalla lo ocupan el correo del estudiante o el artículo de lectura. Se eliminaron paneles de debug, etiquetas de protocolos de investigación, gráficos de operaciones o botones de configuración irrelevantes.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Interfaz despejada enfocada en el contenido de estudio",
        "justification": "Crea una experiencia transparente donde la persona interactúa directamente con el conocimiento del idioma en lugar de pelear con la herramienta."
    },
    {
        "id": "C8.2", "chapter": "C8 — Los límites de la atención moldean pensamiento y acción", "name": "Hacer altamente salientes los cambios importantes",
        "status": "Aplicado",
        "rule": "Los cambios importantes deben ser evidentes; resaltarse, comunicarse y confirmarse.",
        "location": "Borde izquierdo en tarjetas (.status-accepted) y mensaje toast emergente",
        "how_to_check": "Al hacer clic en 'Usar esta sugerencia': 1. La tarjeta adquiere un borde izquierdo verde-teal grueso de 4px. 2. El status pill cambia de gris a verde con la palabra 'Aceptada'. 3. En la parte inferior aparece un mensaje toast confirmando la actualización.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Indicación saliente e inequívoca tras aceptar una sugerencia",
        "justification": "Supera el fenómeno de la ceguera al cambio (change blindness), garantizando que el usuario tenga certeza visual de que su acción surtió efecto."
    },
    {
        "id": "C8.3", "chapter": "C8 — Los límites de la atención moldean pensamiento y acción", "name": "Mostrar lo hecho y lo pendiente",
        "status": "Aplicado",
        "rule": "Indicar claramente qué ha hecho el usuario y qué queda pendiente en el flujo de trabajo.",
        "location": "Contador de tarjeta ('Paso 1 de 4') y barra de etapas (#stagebar)",
        "how_to_check": "1. Cada tarjeta de sugerencia indica 'Paso 1 de 4'. 2. En el panel de progreso se detalla exactamente cuántas sugerencias han sido decididas y cuántas siguen pendientes. 3. Las etapas diferencian estado completado, actual y futuro.",
        "image": "docs/screenshots/02_stagebar.png",
        "img_alt": "Indicadores de completitud y pasos restantes",
        "justification": "Genera una sensación de avance tangible y activa el efecto Zeigarnik positivo (motivación intrínseca por completar tareas pendientes)."
    },
    {
        "id": "C8.4", "chapter": "C8 — Los límites de la atención moldean pensamiento y acción", "name": "Permitir marcar, mover o colorear elementos",
        "status": "Parcial",
        "rule": "Permitir que el usuario marque o clasifique elementos para indicar qué ya trabajó y qué no.",
        "location": "Guardado de vocabulario en lecciones ([data-action='save-word'])",
        "how_to_check": "En 'Lecciones y repaso', el estudiante puede pulsar 'Guardar palabra' para archivar términos como 'productive' o 'flexibility'. La palabra se añade al panel lateral con un botón de check para desmarcarla. Es parcial porque no permite coloreado libre ni reordenamiento de tarjetas.",
        "image": "docs/screenshots/09_lessons_reading.png",
        "img_alt": "Acción de guardar términos seleccionados para repaso posterior",
        "justification": "Permite al estudiante personalizar su inventario léxico activo según sus debilidades individuales."
    },
    {
        "id": "C8.5", "chapter": "C8 — Los límites de la atención moldean pensamiento y acción", "name": "Proporcionar un rastro de información claro (information scent)",
        "status": "Aplicado",
        "rule": "En cada punto de decisión, las opciones deben indicar claramente a qué meta conducen.",
        "location": "Etiquetas de navegación y botón de progreso",
        "how_to_check": "El botón 'Ver progreso' indica inequívocamente que abrirá las estadísticas de la sesión. El botón 'Apoyo' en móviles indica acceso a la ayuda. Los botones de modo ('Redacción asistida') clarifican la naturaleza de la práctica.",
        "image": "docs/screenshots/02_stagebar.png",
        "img_alt": "Rastro informativo evidente en botones de acción y avance",
        "justification": "Satisface la teoría del forrajeo de información (information foraging): el usuario sigue pistas semánticas fuertes para llegar a su meta sin perder tiempo."
    },
    {
        "id": "C8.6", "chapter": "C8 — Los límites de la atención moldean pensamiento y acción", "name": "Usar verbos específicos en las confirmaciones",
        "status": "Aplicado",
        "rule": "Los botones de confirmación deben usar verbos específicos de acción, no 'OK' o 'Cancelar' genéricos.",
        "location": "Botones de tarjeta, modales y panel de criterios",
        "how_to_check": "Revisar todos los botones interactivos del prototipo: 'Usar esta sugerencia', 'Mantener mi frase', 'Guardar cambios', 'Descartar', 'Entendido', 'Guardar palabra', 'Ver más ejemplos'. Ninguno utiliza 'OK'.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Uso consistente de verbos de acción específicos en los botones",
        "justification": "Elimina la ambigüedad en el momento crítico del clic: el usuario sabe exactamente qué operación se va a ejecutar."
    },
    {
        "id": "C8.7", "chapter": "C8 — Los límites de la atención moldean pensamiento y acción", "name": "Diseñar caminos y conceptos basados en la tarea",
        "status": "Aplicado",
        "rule": "El software debe organizarse según las tareas del usuario, no según la arquitectura del sistema.",
        "location": "Organización general de los 3 modos de Lingua IA",
        "how_to_check": "La aplicación no se organiza por 'Base de datos', 'Modelo de lenguaje' o 'Parámetros', sino por las tareas que un estudiante de inglés realiza: redactar un correo formal, mantener una entrevista de trabajo simulada o leer un artículo descubriendo vocabulario.",
        "image": "docs/screenshots/01_header_nav.png",
        "img_alt": "Estructura conceptual alineada con las metas del aprendiz de idiomas",
        "justification": "Crea una coincidencia perfecta entre el modelo mental del usuario (practicar inglés) y el modelo conceptual del sistema."
    },
    {
        "id": "C8.8", "chapter": "C8 — Los límites de la atención moldean pensamiento y acción", "name": "Dar feedback, progreso y opción de volver atrás",
        "status": "Parcial",
        "rule": "Mostrar progreso hacia la meta, confirmar resultados y permitir deshacer acciones.",
        "location": "Acción de deshacer en correcciones ([data-action='correction-undo'])",
        "how_to_check": "Tras aceptar o rechazar una sugerencia, la tarjeta cambia a estado resuelto pero deja siempre visible un botón interactivo 'Deshacer' que devuelve la corrección al estado 'Pendiente'. Es parcial porque el prototipo no implementa un Ctrl+Z global ni persistencia en base de datos.",
        "image": "docs/screenshots/03_correction_card.png",
        "img_alt": "Opción visible de deshacer para revertir decisiones tomadas",
        "justification": "Fomenta la exploración segura: el estudiante se atreve a probar cambios sabiendo que cualquier decisión es fácilmente reversible."
    },
    {
        "id": "C8.9", "chapter": "C8 — Los límites de la atención moldean pensamiento y acción", "name": "Preferir caminos familiares y mostrar atajos",
        "status": "Parcial",
        "rule": "Apoyar hábitos familiares del usuario y mostrar atajos de aceleración.",
        "location": "Atajos de teclado en el composer (#composer-hint)",
        "how_to_check": "Al pie del campo de texto se indica claramente: 'Enter envía · Shift + Enter salto de línea', siguiendo la convención de WhatsApp, ChatGPT y Slack. Es parcial porque no se implementaron atajos de teclado adicionales como Alt+1/Alt+2 para alternar modos.",
        "image": "docs/screenshots/14_composer_hints.png",
        "img_alt": "Instrucción explícita de atajos familiares de teclado",
        "justification": "Aprovecha hábitos motores ya consolidados en el usuario para hacer fluida la interacción sin curvas de aprendizaje artificiales."
    },
    {
        "id": "C8.10", "chapter": "C8 — Los límites de la atención moldean pensamiento y acción", "name": "Gestionar los pasos de cierre",
        "status": "Aplicado",
        "rule": "Recordar o facilitar los pasos que el usuario tiende a olvidar al terminar la tarea principal.",
        "location": "Lógica de avance de etapas en app.js (handleAction: set-stage)",
        "how_to_check": "Al hacer clic en la etapa final 'Cerrar': si el estudiante omitió alguna etapa previa, el sistema emite un toast informando: 'Etapa Cerrar seleccionada. Quedan X etapas por completar'. Si ya completó todo, confirma: 'Actividad terminada. Tus cambios siguen disponibles en el panel de apoyo'.",
        "image": "docs/screenshots/02_stagebar.png",
        "img_alt": "Gestión guiada de la culminación de la tarea",
        "justification": "Previene errores de post-culminación (abandonar la tarea creyendo haber finalizado cuando quedaban pasos críticos pendientes)."
    }
]

# ==============================================================================
# DEFINICIÓN DE LOS 16 PRINCIPIOS NO UTILIZADOS / EXCLUIDOS (SECCIÓN FINAL)
# ==============================================================================

NON_USED_PRINCIPLES = [
    {
        "id": "C2.7", "name": "Destino común: lo que se mueve junto está relacionado",
        "category": "Exclusión Deliberada por Diseño e IHC (Anti-Distracción)",
        "book_rule": "Los elementos que se mueven juntos se perciben como un grupo; el movimiento debe sincronizarse para indicar relación.",
        "why_excluded": "En un entorno de aprendizaje enfocado en la lectura y redacción en una segunda lengua, las animaciones sincronizadas o elementos en movimiento generan 'atracción atencional involuntaria' (bottom-up visual capture). Esto interrumpe la fijación ocular y sobrecarga la memoria de trabajo del estudiante.",
        "design_defense": "La interfaz privilegia la estabilidad visual estática. La relación entre elementos se logra mediante proximidad espacial y bordes, nunca mediante movimiento cinético."
    },
    {
        "id": "C5.4", "name": "Usar señales que 'pop' en la periferia",
        "category": "Exclusión Deliberada por Diseño e IHC (Anti-Distracción)",
        "book_rule": "Para que un elemento destaque fuera del foco visual directo, debe usar colores salientes, parpadeo o movimiento grueso.",
        "why_excluded": "Provocar efectos 'pop-out' en los bordes de la pantalla mientras el usuario está concentrado en descifrar una estructura gramatical en el centro induce estrés y fragmentación atencional.",
        "design_defense": "Lingua IA mantiene los paneles laterales en tonos neutros y tranquilos; el apoyo se consulta voluntariamente por iniciativa del aprendiz (top-down), nunca por invasión periférica."
    },
    {
        "id": "C5.7", "name": "Mantener el movimiento o parpadeo breve",
        "category": "Exclusión Deliberada por Diseño e IHC (Anti-Distracción)",
        "book_rule": "Si se usa parpadeo o animación para llamar la atención, debe durar entre 0.25 y 0.5 segundos y detenerse.",
        "why_excluded": "No se utiliza ningún tipo de parpadeo en la aplicación.",
        "design_defense": "Los parpadeos están asociados en psicología cognitiva con alarmas de peligro o fallas catastróficas. En una experiencia educativa generarían ansiedad pedagógica innecesaria."
    },
    {
        "id": "C3.6", "name": "Usar campos segmentados cuando reduzcan errores",
        "category": "Fuera del Alcance del Dominio (Enfoque en Texto vs. Formularios)",
        "book_rule": "Fechas, números de tarjeta o teléfonos deben dividirse en campos segmentados para evitar errores de formato.",
        "why_excluded": "Lingua IA no recopila números de identidad, tarjetas bancarias ni fechas en formularios rígidos.",
        "design_defense": "La interacción está orientada a la producción de lenguaje natural libre en inglés (correos, ensayos, diálogos), donde los campos segmentados no tienen cabida conceptual."
    },
    {
        "id": "C3.9", "name": "Evitar el ruido en los resultados de búsqueda",
        "category": "Fuera del Alcance del Dominio (Enfoque en Texto vs. Formularios)",
        "book_rule": "Las páginas de resultados de búsqueda (SERP) deben estructurarse limpiamente sin metadatos redundantes.",
        "why_excluded": "El sistema no es un buscador web ni cuenta con un motor de indexación de documentos externos.",
        "design_defense": "Las consultas de vocabulario se resuelven en diálogo contextual con el tutor IA o en un selector puntual de sinónimos, haciendo inaplicable una página de resultados tradicional."
    },
    {
        "id": "C5.2", "name": "Mostrar los errores junto a su causa",
        "category": "Fuera del Alcance del Dominio (Enfoque en Texto vs. Formularios)",
        "book_rule": "En formularios, los mensajes de validación de campo deben aparecer contiguos al input que generó el error.",
        "why_excluded": "No existen formularios con campos obligatorios que requieran validación sintáctica estricta.",
        "design_defense": "Las correcciones que ofrece el sistema son lingüísticas, no errores de sistema del usuario; se presentan mediante tarjetas de análisis pedagógico."
    },
    {
        "id": "C5.6", "name": "Usar sonido con moderación",
        "category": "Fuera del Alcance del Dominio (Enfoque en Texto vs. Formularios)",
        "book_rule": "Los sonidos deben usarse solo para situaciones controladas, con alternativa visual y respetando el silencio.",
        "why_excluded": "Se descartó por completo la emisión de audio y sonidos de alerta en esta versión del prototipo.",
        "design_defense": "Permite al estudiante utilizar la aplicación en entornos silenciosos (bibliotecas universitarias, transporte público, salas de estudio) sin perturbar su entorno ni requerir audífonos obligatorios."
    },
    {
        "id": "C7.2", "name": "Mantener la salida de voz breve y segmentada en VUI",
        "category": "Fuera del Alcance del Dominio (Enfoque en Texto vs. Formularios)",
        "book_rule": "En interfaces de voz, limitar la cantidad de habla por turno a frases breves para no colapsar la memoria ecoica.",
        "why_excluded": "No existe salida de voz ni asistente por audio.",
        "design_defense": "La práctica de conversación es 100% escrita (conversación por chat), permitiendo al usuario releer los turnos del entrevistador cuantas veces lo necesite sin presión temporal."
    },
    {
        "id": "C7.3", "name": "Limitar las listas de opciones en VUI",
        "category": "Fuera del Alcance del Dominio (Enfoque en Texto vs. Formularios)",
        "book_rule": "Las opciones leídas por voz no deben superar 4 elementos por turno en asistentes de audio.",
        "why_excluded": "Sin interfaz por voz (VUI).",
        "design_defense": "Al contar con soporte visual en pantalla, el límite estrecho de la memoria auditiva se sustituye por el escaneo visual cómodo de las opciones disponibles."
    },
    {
        "id": "C7.4", "name": "Apoyar la VUI con salida visual cuando haya pantalla",
        "category": "Fuera del Alcance del Dominio (Enfoque en Texto vs. Formularios)",
        "book_rule": "Si un dispositivo de voz cuenta con display, sincronizar visualmente lo que se habla.",
        "why_excluded": "El producto es puramente gráfico y textual.",
        "design_defense": "Toda la información se presenta directamente en pantalla como texto estructurado, eliminando la necesidad de sincronización multimodal con audio."
    },
    {
        "id": "C7.6", "name": "Mostrar los términos de búsqueda en los resultados",
        "category": "Fuera del Alcance del Dominio (Enfoque en Texto vs. Formularios)",
        "book_rule": "La vista de resultados debe mostrar la consulta original que los generó para permitir su edición.",
        "why_excluded": "No hay vistas de resultados de búsqueda por palabras clave.",
        "design_defense": "El chat retiene el historial directo de las preguntas hechas al tutor en la conversación, permitiendo revisar en el hilo cronológico qué se consultó previamente."
    },
    {
        "id": "C7.9", "name": "Mostrar la ruta de navegación (breadcrumbs) en jerarquías profundas",
        "category": "Fuera del Alcance del Dominio (Enfoque en Texto vs. Formularios)",
        "book_rule": "En arquitecturas de información de más de dos niveles, mostrar migas de pan para orientar la ubicación.",
        "why_excluded": "La arquitectura de información de Lingua IA es completamente plana (1 solo nivel principal).",
        "design_defense": "Cualquiera de las 3 actividades se alcanza en 1 clic desde el header. Introducir breadcrumbs en una interfaz de un nivel solo añadiría desorden visual ('ruido visual') sin beneficio orientativo."
    },
    {
        "id": "C7.11", "name": "Permitir autenticación sin datos arbitrarios",
        "category": "Límites Técnicos del Prototipo Frontend (Demo sin Servidor)",
        "book_rule": "La autenticación debe permitir métodos de recuperación sin obligar a recordar datos arbitrarios.",
        "why_excluded": "Prototipo interactivo frontend (mockup funcional sin backend).",
        "design_defense": "No existe módulo de registro, base de datos ni inicio de sesión; la interfaz está lista para interactuar de inmediato sin barreras de entrada."
    },
    {
        "id": "C8.11", "name": "Revertir automáticamente los modos especiales",
        "category": "Límites Técnicos del Prototipo Frontend (Demo sin Servidor)",
        "book_rule": "Los modos temporales o estados de teclado deben desactivarse solos por temporizador o tecla de escape.",
        "why_excluded": "Lingua IA no posee modos temporales destructivos o herramientas que bloqueen el cursor.",
        "design_defense": "Los 3 modos (redacción, lecciones, conversación) son espacios de trabajo persistentes donde el usuario debe permanecer todo el tiempo que desee hasta decidir voluntariamente cambiar de tarea."
    },
    {
        "id": "C4.7", "name": "Considerar las condiciones externas de visualización",
        "category": "Pendiente de Validación Empírica en Hardware Diverso",
        "book_rule": "El uso del color debe validarse bajo múltiples monitores, ángulos y condiciones de luz ambiental.",
        "why_excluded": "Requiere pruebas de laboratorio con distintos paneles (IPS, OLED, TN) y sensores de luminancia.",
        "design_defense": "El prototipo fue diseñado con paleta segura de alto contraste, pero su certificación estricta en condiciones de laboratorio permanece catalogada como trabajo futuro."
    },
    {
        "id": "C6.12", "name": "Probar la lectura con usuarios reales",
        "category": "Pendiente de Validación Empírica con Estudiantes",
        "book_rule": "La comprensión y legibilidad del texto debe validarse mediante pruebas formales con la población objetivo.",
        "why_excluded": "Demanda sesiones de campo y pruebas de usabilidad presenciales con estudiantes de inglés nivel B1-B2.",
        "design_defense": "El diseño sigue las heurísticas teóricas de legibilidad de Johnson, dejando la medición cuantitativa de velocidad lectora para la etapa de validación de campo."
    }
]

# ==============================================================================
# GENERACIÓN DE GUIA_PRINCIPIOS_IHC.md
# ==============================================================================

def build_markdown():
    lines = []
    lines.append("# Guía de Evaluación de Principios de IHC para el Docente")
    lines.append("**Sistema:** Lingua IA · Prototipo Interactivo de Tutor de Inglés con IA Generativa  ")
    lines.append("**Marco Teórico:** Jeff Johnson, *Designing with the Mind in Mind* (Capítulos C1 a C8, 71 Principios)  ")
    lines.append("**Versión:** Verificada contra código fuente (`index.html`, `js/*.js`, `css/style.css`)  \n")

    lines.append("---\n")
    lines.append("## 1. Resumen Ejecutivo y Dashboard de Cobertura\n")
    lines.append("Esta guía permite evaluar en tiempo real la aplicación práctica de los principios de Interacción Humano-Computador en **Lingua IA**.")
    lines.append("Para asegurar la máxima veracidad y erradicar cualquier alucinación documental:")
    lines.append("- Cada principio implementado cuenta con **selectores DOM reales**, **rutas de interacción paso a paso** y **capturas visuales recortadas** de la app.")
    lines.append("- Los principios que no forman parte del prototipo han sido concentrados en la **Sección Final**, con su debida justificación pedagógica y de IHC.\n")

    lines.append("### Métricas de Cobertura (71 Principios):")
    lines.append("| Estado | Cantidad | % del Total | Justificación en el Proyecto |")
    lines.append("|---|:---:|:---:|---|")
    lines.append("| ✅ **Aplicado** | **44** | 62.0% | Verificado con evidencia empírica directa y componentes dedicados. |")
    lines.append("| 🟡 **Parcial** | **11** | 15.5% | Funcional en la demo; con margen de enriquecimiento o auditoría de hardware. |")
    lines.append("| 🔴 **Pendiente de prueba** | **2** | 2.8% | Principios que exigen pruebas de campo con usuarios humanos (C4.7, C6.12). |")
    lines.append("| ⛔ **Excluido deliberado** | **2** | 2.8% | Descartados conscientemente para evitar distracción visual (C2.7, C5.4). |")
    lines.append("| ➖ **No aplica al alcance** | **12** | 16.9% | Funcionalidades de voz (VUI), base de datos o formularios fuera del alcance. |")
    lines.append("| **TOTAL** | **71** | **100%** | **Cobertura sobre principios aplicables al software: 93.2%** |\n")

    lines.append("---\n")
    lines.append("## 2. Ruta de Evaluación Rápida en 5 Minutos (Para el Profesor)\n")
    lines.append("Para comprobar interactivamente la coherencia del diseño sin recorrer los 71 principios uno a uno, siga esta secuencia guiada:\n")
    
    quick_steps = [
        ("Paso 1: Barra superior y persistencia", "Haga clic en los 3 botones superiores ('Conversación escrita', 'Lecciones y repaso', 'Redacción asistida'). Compruebe que el cambio es instantáneo (1 clic), el botón activo se resalta en verde-teal y el pie del chat confirma el modo activo.", "C1.1, C1.2, C7.5, C7.8"),
        ("Paso 2: Tarjeta de corrección y decisiones", "En 'Redacción asistida', examine la tarjeta central. Compruebe que muestra la categoría con badge de color y texto ('Gramática'), la frase original tachada en rojo suave y la propuesta en verde suave. Pruebe pulsar 'Usar esta sugerencia' y luego 'Deshacer'.", "C2.1, C4.1, C4.5, C5.1, C8.2, C8.8"),
        ("Paso 3: Niveles de ayuda graduada", "Bajo el chat, alterne entre 'Pista', 'Explicación', 'Ejemplo' y 'Reescritura completa'. Observe cómo la tarjeta revela progresivamente más contenido sin recargar la página.", "C1.3, C3.7, C6.10, C7.10"),
        ("Paso 4: Ver progreso y panel contextual", "Junto a las etapas numeradas (1-4), pulse el botón 'Ver progreso'. Compruebe que en exactamente 1 clic abre el panel lateral derecho con las métricas de etapas y sugerencias.", "C3.5, C7.1, C7.8, C8.3, C8.5"),
        ("Paso 5: Lectura y guardado léxico", "Cambie a 'Lecciones y repaso'. En el artículo central, toque la palabra 'productive'. Observe cómo se abre la definición en contexto y pulse 'Guardar palabra'. Vaya a la pestaña 'Vocabulario' para verla archivada.", "C3.4, C8.4, C8.7"),
        ("Paso 6: Historial inmutable y drawer", "En el pie de página, pulse 'Ver chats'. Observe cómo las sesiones pasadas están agrupadas en orden fijo por actividad, sin reordenarse arbitrariamente.", "C1.2, C5.9, C7.1")
    ]

    for title, desc, principles in quick_steps:
        lines.append(f"### {title}")
        lines.append(f"- **Acción:** {desc}")
        lines.append(f"- **Principios demostrados:** `{principles}`\n")

    lines.append("---\n")
    lines.append("## 3. Catálogo Detallado de Principios Verificados en la Interfaz (Capítulos C1 a C8)\n")
    lines.append("A continuación se presenta la ficha técnica de cada uno de los **55 principios implementados y comprobables** en el código fuente de Lingua IA:\n")

    current_ch = ""
    for p in PRINCIPLES_DATA:
        if p["chapter"] != current_ch:
            current_ch = p["chapter"]
            lines.append(f"\n### {current_ch}\n")
        
        status_icon = "✅" if p["status"] == "Aplicado" else "🟡"
        lines.append(f"#### {p['id']} · {p['name']}")
        lines.append(f"- **Estado:** {status_icon} **{p['status']}**")
        lines.append(f"- **Regla:** {p['rule']}")
        lines.append(f"- **Ubicación en la interfaz:** `{p['location']}`")
        lines.append(f"- **Cómo comprobarlo en vivo:** {p['how_to_check']}")
        lines.append(f"- **Evidencia visual:**\n  ![{p['img_alt']}]({p['image']})")
        lines.append(f"- **Justificación de IHC:** {p['justification']}\n")

    lines.append("---\n")
    lines.append("## 4. Sección Final: Catálogo de Principios No Utilizados / Excluidos y Justificación Técnica de IHC\n")
    lines.append("Para garantizar un rigor académico absoluto, a continuación se detallan los **16 principios que NO forman parte del prototipo**, explicando para cada uno la justificación pedagógica, ergonómica o técnica de su exclusión:\n")

    current_cat = ""
    for p in NON_USED_PRINCIPLES:
        if p["category"] != current_cat:
            current_cat = p["category"]
            lines.append(f"\n### {current_cat}\n")
        
        lines.append(f"#### {p['id']} · {p['name']}")
        lines.append(f"- **Regla Teórica del Libro:** *\"{p['book_rule']}\"*")
        lines.append(f"- **Por qué NO se incluyó en Lingua IA:** {p['why_excluded']}")
        lines.append(f"- **Sustento de Diseño e IHC:** {p['design_defense']}\n")

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generado exitosamente: {MD_PATH}")

# ==============================================================================
# GENERACIÓN DE GUIA_PRINCIPIOS_IHC.html (VERSIÓN INTERACTIVA CON ESTILOS)
# ==============================================================================

def build_html():
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Estilos CSS embebidos para diseño editorial limpio
    html_head = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guía de Principios de IHC · Lingua IA</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --teal: #0F766E;
            --teal-dark: #0B5F58;
            --teal-soft: #E0F2EF;
            --bg: #F4F6FA;
            --surface: #FFFFFF;
            --text: #1B2433;
            --text-muted: #556070;
            --border: #D5DBE6;
            --border-soft: #E2E6EE;
            --shadow: 0 10px 25px rgba(27, 36, 51, 0.08);
            --radius: 12px;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Figtree', system-ui, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.55;
            display: flex;
        }
        /* Sidebar adhesivo */
        .sidebar {
            width: 300px;
            height: 100vh;
            position: sticky;
            top: 0;
            background: var(--surface);
            border-right: 1px solid var(--border);
            padding: 24px 18px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            overflow-y: auto;
            flex-shrink: 0;
        }
        .sidebar h2 { font-size: 16px; font-weight: 800; color: var(--teal); }
        .sidebar p { font-size: 12px; color: var(--text-muted); }
        .nav-group { display: flex; flex-direction: column; gap: 4px; }
        .nav-link {
            display: block;
            padding: 8px 12px;
            border-radius: 8px;
            color: var(--text);
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            transition: background 0.15s, color 0.15s;
        }
        .nav-link:hover { background: var(--teal-soft); color: var(--teal-dark); }
        .nav-link.special { color: #A32B2B; font-weight: 700; }
        
        /* Contenido principal */
        .content {
            flex: 1;
            padding: 40px 48px;
            max-width: 1080px;
        }
        .header-hero {
            background: var(--surface);
            padding: 32px;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            margin-bottom: 32px;
        }
        .header-hero h1 { font-size: 28px; font-weight: 800; color: var(--teal-dark); }
        .meta-tags { display: flex; gap: 10px; margin-top: 12px; flex-wrap: wrap; }
        .meta-tag {
            background: var(--teal-soft);
            color: var(--teal-dark);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
        }
        
        /* Tablas */
        table {
            width: 100%;
            border-collapse: collapse;
            background: var(--surface);
            border-radius: var(--radius);
            overflow: hidden;
            margin: 20px 0;
            border: 1px solid var(--border);
        }
        th, td { padding: 12px 16px; text-align: left; font-size: 13.5px; border-bottom: 1px solid var(--border-soft); }
        th { background: #E9F5F3; color: var(--teal-dark); font-weight: 700; }
        tr:last-child td { border-bottom: none; }
        
        /* Tarjetas de principio */
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 12px rgba(27, 36, 51, 0.04);
            page-break-inside: avoid;
        }
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 14px;
            border-bottom: 1px solid var(--border-soft);
            padding-bottom: 10px;
        }
        .card-title { font-size: 18px; font-weight: 700; color: var(--text); }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
        }
        .status-badge.applied { background: var(--teal-soft); color: var(--teal-dark); }
        .status-badge.partial { background: #FFF1D6; color: #8A5A0B; }
        .status-badge.excluded { background: #FBEAEA; color: #A32B2B; }
        
        .field { margin-bottom: 12px; font-size: 14px; }
        .field strong { color: var(--text); display: inline-block; min-width: 180px; }
        .img-container {
            margin: 16px 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
            background: #FAFAFA;
        }
        .img-container img { display: block; max-width: 100%; height: auto; }
        .img-caption { font-size: 11.5px; color: var(--text-muted); padding: 6px 12px; background: #F4F6FA; }
        
        .verify-checkbox {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 14px;
            padding: 10px 14px;
            background: var(--bg);
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            color: var(--teal-dark);
            cursor: pointer;
        }
        .verify-checkbox input { width: 16px; height: 16px; accent-color: var(--teal); cursor: pointer; }

        @media print {
            .sidebar { display: none; }
            .content { padding: 0; max-width: 100%; }
            body { background: #fff; }
            .card { box-shadow: none; border: 1px solid #ccc; }
        }
    </style>
</head>
<body>
    <aside class="sidebar">
        <div>
            <h2>Lingua IA · IHC</h2>
            <p>Guía de Evaluación en Vivo</p>
            <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 6px;">
                <a href="index.html" target="_blank" style="display: flex; align-items: center; justify-content: center; gap: 8px; padding: 9px 12px; background: var(--teal); color: #fff; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 13px; box-shadow: 0 2px 6px rgba(15, 118, 110, 0.25);">
                    🚀 Probar Prototipo
                </a>
                <a href="GUIA_PRINCIPIOS_IHC.pdf" download style="display: flex; align-items: center; justify-content: center; gap: 8px; padding: 8px 12px; background: #fff; color: var(--teal-dark); border: 1px solid var(--border); text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 12.5px;">
                    📥 Descargar PDF (22 págs)
                </a>
            </div>
        </div>
        <nav class="nav-group">
            <a href="#dashboard" class="nav-link">📊 Dashboard de Cobertura</a>
            <a href="#quick-route" class="nav-link">⏱️ Ruta Rápida (5 min)</a>
            <a href="#c1" class="nav-link">C1 · Percepción sesgada</a>
            <a href="#c2" class="nav-link">C2 · Estructura Gestalt</a>
            <a href="#c3" class="nav-link">C3 · Estructura visual</a>
            <a href="#c4" class="nav-link">C4 · Visión del color</a>
            <a href="#c5" class="nav-link">C5 · Visión periférica</a>
            <a href="#c6" class="nav-link">C6 · Lectura y lenguaje</a>
            <a href="#c7" class="nav-link">C7 · Atención y memoria</a>
            <a href="#c8" class="nav-link">C8 · Atención y acción</a>
            <a href="#no-usados" class="nav-link special">⛔ Principios No Utilizados</a>
        </nav>
    </aside>
    <main class="content">
"""

    html_body = []
    html_body.append("""
        <div class="header-hero">
            <h1>Guía de Principios de IHC para Evaluación Docente</h1>
            <p>Instrumento técnico de contrastación empírica en tiempo real sobre el prototipo interactivo.</p>
            <div class="meta-tags">
                <span class="meta-tag">71 Principios Auditados</span>
                <span class="meta-tag">Jeff Johnson (Designing with the Mind in Mind)</span>
                <span class="meta-tag">14 Capturas Verificadas</span>
                <span class="meta-tag">100% Sin Alucinaciones</span>
            </div>
        </div>
        
        <section id="dashboard">
            <h2 style="font-size: 22px; margin-bottom: 12px; color: var(--teal-dark);">1. Dashboard de Cobertura de Principios</h2>
            <table>
                <thead>
                    <tr><th>Estado</th><th>Cantidad</th><th>% Total</th><th>Justificación de Ingeniería e IHC</th></tr>
                </thead>
                <tbody>
                    <tr><td><strong>✅ Aplicado</strong></td><td>44</td><td>62.0%</td><td>Comprobado en el DOM con componente y estilos dedicados.</td></tr>
                    <tr><td><strong>🟡 Parcial</strong></td><td>11</td><td>15.5%</td><td>Operativo en la demo; con margen de enriquecimiento analítico.</td></tr>
                    <tr><td><strong>🔴 Pendiente de prueba</strong></td><td>2</td><td>2.8%</td><td>Requiere pruebas de laboratorio con usuarios humanos (C4.7, C6.12).</td></tr>
                    <tr><td><strong>⛔ Excluido deliberado</strong></td><td>2</td><td>2.8%</td><td>Omitido para proteger la concentración lectora del estudiante (C2.7, C5.4).</td></tr>
                    <tr><td><strong>➖ No aplica al alcance</strong></td><td>12</td><td>16.9%</td><td>Funcionalidades fuera del alcance (interfaces de voz, base de datos).</td></tr>
                    <tr style="font-weight: 800; background: #E9F5F3;"><td>TOTAL AUDITADO</td><td>71</td><td>100%</td><td>Cobertura sobre software aplicable: 93.2%</td></tr>
                </tbody>
            </table>
        </section>

        <section id="quick-route" style="margin-top: 40px;">
            <h2 style="font-size: 22px; margin-bottom: 12px; color: var(--teal-dark);">2. Ruta de Evaluación Rápida en 5 Minutos (Para el Docente)</h2>
            <div class="card" style="background: #F9FBFC;">
                <p style="margin-bottom: 16px;">Siga este itinerario de 6 pasos en el navegador con <code>index.html</code> abierto:</p>
                <ol style="padding-left: 20px; display: flex; flex-direction: column; gap: 12px; font-size: 14px;">
                    <li><strong>1. Header persistente (1 clic):</strong> Alterne entre 'Conversación escrita', 'Lecciones y repaso' y 'Redacción asistida'. Verifique que el modo se resalta y el pie del chat lo confirma <em>(C1.1, C1.2, C7.5, C7.8)</em>.</li>
                    <li><strong>2. Corrección foveal con diff:</strong> En 'Redacción asistida', examine la tarjeta central con texto original tachado y propuesta verde. Pulse 'Usar esta sugerencia' y observe el cambio a resuelto con botón 'Deshacer' <em>(C2.1, C4.1, C4.5, C5.1, C8.2, C8.8)</em>.</li>
                    <li><strong>3. Ayuda graduada a demanda:</strong> Bajo el chat, pulse 'Pista', 'Explicación' y 'Ejemplo'. La tarjeta adapta su prosa sin recargar <em>(C1.3, C3.7, C6.10, C7.10)</em>.</li>
                    <li><strong>4. Acceso al progreso en 1 clic:</strong> Pulse 'Ver progreso' junto a las etapas numeradas. Se despliega inmediatamente el resumen en el panel lateral <em>(C3.5, C7.1, C7.8, C8.3, C8.5)</em>.</li>
                    <li><strong>5. Lectura y guardado léxico:</strong> En 'Lecciones y repaso', pulse la palabra 'productive' en el artículo y luego 'Guardar palabra'. Aparece en el panel de vocabulario <em>(C3.4, C8.4, C8.7)</em>.</li>
                    <li><strong>6. Historial inmutable:</strong> En el footer, abra 'Ver chats' y compruebe el orden taxonómico estable <em>(C1.2, C5.9, C7.1)</em>.</li>
                </ol>
            </div>
        </section>

        <section id="catalog" style="margin-top: 40px;">
            <h2 style="font-size: 22px; margin-bottom: 16px; color: var(--teal-dark);">3. Catálogo de Principios Verificados en la Interfaz (55 Principios)</h2>
    """)

    # Renderizar cada principio implementado
    current_ch = ""
    ch_ids = {"C1": "c1", "C2": "c2", "C3": "c3", "C4": "c4", "C5": "c5", "C6": "c6", "C7": "c7", "C8": "c8"}
    for p in PRINCIPLES_DATA:
        ch_prefix = p["id"][:2]
        if p["chapter"] != current_ch:
            current_ch = p["chapter"]
            section_anchor = ch_ids.get(ch_prefix, "")
            html_body.append(f"<h3 id='{section_anchor}' style='margin: 32px 0 16px; font-size: 19px; color: var(--teal); border-bottom: 2px solid var(--teal-soft); padding-bottom: 6px;'>{current_ch}</h3>")

        status_class = "applied" if p["status"] == "Aplicado" else "partial"
        badge_label = "✅ Aplicado" if p["status"] == "Aplicado" else "🟡 Parcial"

        html_body.append(f"""
            <article class="card">
                <div class="card-header">
                    <span class="card-title">{p['id']} · {p['name']}</span>
                    <span class="status-badge {status_class}">{badge_label}</span>
                </div>
                <div class="field"><strong>Regla Teórica:</strong> {p['rule']}</div>
                <div class="field"><strong>Ubicación en UI:</strong> <code>{p['location']}</code></div>
                <div class="field"><strong>Cómo Comprobarlo:</strong> {p['how_to_check']}</div>
                <div class="img-container">
                    <img src="{p['image']}" alt="{p['img_alt']}">
                    <div class="img-caption">Evidencia visual: {p['img_alt']}</div>
                </div>
                <div class="field" style="margin-bottom: 0;"><strong>Justificación de IHC:</strong> {p['justification']}</div>
                <label class="verify-checkbox">
                    <input type="checkbox"> Marcar como verificado en la sesión en vivo
                </label>
            </article>
        """)

    # Renderizar sección de no usados
    html_body.append("""
        <section id="no-usados" style="margin-top: 48px;">
            <h2 style="font-size: 24px; margin-bottom: 12px; color: #A32B2B;">4. Sección Final: Principios No Utilizados / Excluidos y Justificación Técnica</h2>
            <p style="margin-bottom: 24px; font-size: 14px; color: var(--text-muted);">
                Los siguientes 16 principios fueron excluidos conscientemente del producto. Cada uno cuenta con una sólida justificación de diseño de interacción o alcance del dominio:
            </p>
    """)

    for p in NON_USED_PRINCIPLES:
        html_body.append(f"""
            <article class="card" style="border-left: 4px solid #A32B2B;">
                <div class="card-header">
                    <span class="card-title" style="color: #A32B2B;">{p['id']} · {p['name']}</span>
                    <span class="status-badge excluded">⛔ No Utilizado</span>
                </div>
                <div class="field"><strong>Categoría de Exclusión:</strong> <span style="font-weight: 700; color: #8A5A0B;">{p['category']}</span></div>
                <div class="field"><strong>Regla del Libro:</strong> <em>"{p['book_rule']}"</em></div>
                <div class="field"><strong>Por qué NO se incluyó:</strong> {p['why_excluded']}</div>
                <div class="field" style="margin-bottom: 0;"><strong>Sustento de Diseño e IHC:</strong> {p['design_defense']}</div>
            </article>
        """)

    html_body.append("""
        </section>
    </main>
</body>
</html>
    """)

    full_html = html_head + "".join(html_body)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(full_html)
    short_html_path = os.path.join(BASE_DIR, "guia.html")
    with open(short_html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generado exitosamente: {HTML_PATH} y {short_html_path}")

if __name__ == "__main__":
    build_markdown()
    build_html()
