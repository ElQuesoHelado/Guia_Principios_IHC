import os
import re
import subprocess
import shutil

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
import sys
sys.path.insert(0, os.path.join(BASE_DIR, "tools"))
from build_guides import PRINCIPLES_DATA, NON_USED_PRINCIPLES

PDF_OUTPUT = os.path.join(BASE_DIR, "GUIA_PRINCIPIOS_IHC.pdf")
TEX_FILE = os.path.join(BASE_DIR, "tools", "guia_documento.tex")

def clean_text(text):
    if not text:
        return ""
    t = str(text)
    # Reemplazar flechas y emojis comunes
    t = t.replace("→", "$\\rightarrow$")
    t = t.replace("✅", "[APLICADO] ")
    t = t.replace("🟡", "[PARCIAL] ")
    t = t.replace("⛔", "[EXCLUIDO] ")
    t = t.replace("🔴", "[PENDIENTE] ")
    t = t.replace("➖", "[-] ")
    t = t.replace("📊", "")
    t = t.replace("⏱️", "")
    t = t.replace("🚀", "")
    t = t.replace("📖", "")
    t = t.replace("✓", "V")
    t = t.replace("✗", "X")
    t = t.replace("○", "O")
    t = t.replace("·", "--")
    t = t.replace("“", "``").replace("”", "''")
    t = t.replace("‘", "`").replace("’", "'")
    t = t.replace("–", "--").replace("—", "---")
    
    # Escapar caracteres de LaTeX
    t = t.replace("\\", "\\textbackslash{}")
    for char in ["&", "%", "$", "#", "_", "{", "}"]:
        t = t.replace(char, "\\" + char)
    
    # Manejar `código inline` -> \texttt{código}
    t = re.sub(r'`(.*?)`', r'\\texttt{\1}', t)
    # Manejar **negrita** -> \textbf{negrita}
    t = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', t)
    # Manejar *cursiva* -> \textit{cursiva}
    t = re.sub(r'\*(.*?)\*', r'\\textit{\1}', t)
    
    return t

def generate_tex():
    tex = []
    tex.append(r"""
\documentclass[10pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1.8cm,top=2.2cm,bottom=2.2cm]{geometry}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{fancyhdr}
\usepackage{tcolorbox}
\tcbuselibrary{breakable}
\setlength{\headheight}{20pt}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{float}

% Colores del sistema Lingua IA
\definecolor{linguaTeal}{HTML}{0F766E}
\definecolor{linguaDarkTeal}{HTML}{0B5F58}
\definecolor{linguaSoftTeal}{HTML}{E0F2EF}
\definecolor{linguaText}{HTML}{1B2433}
\definecolor{linguaRed}{HTML}{A32B2B}
\definecolor{linguaAmber}{HTML}{8A5A0B}
\definecolor{linguaBorder}{HTML}{D5DBE6}

\hypersetup{
    colorlinks=true,
    linkcolor=linguaDarkTeal,
    urlcolor=linguaTeal,
    pdftitle={Guía de Principios de IHC - Lingua IA},
    pdfauthor={Lingua IA IHC Team}
}

% Configuración de cabeceras y pies de página
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textbf{\textcolor{linguaDarkTeal}{Lingua IA}} \textbar{} Guía de Evaluación de Principios de IHC}
\fancyhead[R]{\small\textcolor{gray}{Jeff Johnson (Designing with the Mind in Mind)}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\headrule}{\hbox to\headwidth{\color{linguaBorder}\leaders\hrule height \headrulewidth\hfill}}

% Estilo de títulos
\titleformat{\section}{\Large\bfseries\color{linguaDarkTeal}}{}{0em}{}[\vspace{-0.2em}\color{linguaTeal}\rule{\textwidth}{1.5pt}]
\titleformat{\subsection}{\large\bfseries\color{linguaDarkTeal}}{\thesubsection}{0.6em}{}

% Cajas de principios con tcolorbox
\tcbset{
    principlebox/.style={
        colback=white,
        colframe=linguaTeal,
        coltitle=white,
        fonttitle=\bfseries\small,
        boxrule=1pt,
        arc=3mm,
        left=8pt, right=8pt, top=6pt, bottom=6pt,
        boxsep=2pt,
        before skip=10pt, after skip=10pt,
        breakable
    },
    excludedbox/.style={
        colback=white,
        colframe=linguaRed,
        coltitle=white,
        fonttitle=\bfseries\small,
        boxrule=1pt,
        arc=3mm,
        left=8pt, right=8pt, top=6pt, bottom=6pt,
        boxsep=2pt,
        before skip=8pt, after skip=8pt,
        breakable
    }
}

\begin{document}

% --- PORTADA / ENCABEZADO PRINCIPAL ---
\begin{center}
    {\huge\textbf{\textcolor{linguaDarkTeal}{Lingua IA}}}\\[0.3em]
    {\Large\textbf{Guía de Evaluación de Principios de IHC para el Docente}}\\[0.5em]
    {\normalsize\textbf{Marco Teórico:} Jeff Johnson, \textit{Designing with the Mind in Mind} (71 Principios, Capítulos C1 a C8)}\\[0.3em]
    {\small\textbf{Repositorio:} \url{https://github.com/ElQuesoHelado/Guia_Principios_IHC}}\\[0.2em]
    {\small\textbf{Web Prototipo:} \url{https://elquesohelado.github.io/Guia_Principios_IHC/}} \quad \textbar{} \quad
    {\small\textbf{Web Guía:} \url{https://elquesohelado.github.io/Guia_Principios_IHC/guia.html}}
\end{center}

\vspace{0.8em}
\hrule height 1pt
\vspace{1em}

% --- 1. DASHBOARD DE COBERTURA ---
\section{Dashboard de Cobertura de Principios (71 Principios Auditados)}

El presente documento constituye el instrumento técnico de contrastación empírica en tiempo real sobre el prototipo interactivo de \textbf{Lingua IA}. Todos los principios implementados han sido verificados contra los selectores del DOM y funciones JavaScript reales, erradicando cualquier alucinación documental.

\vspace{0.6em}
\begin{table}[H]
\centering
\small
\begin{tabular}{lccl}
\toprule
\textbf{Estado en la Interfaz} & \textbf{Cantidad} & \textbf{\% del Total} & \textbf{Justificación de Ingeniería e IHC} \\
\midrule
\textbf{Aplicado} & 44 & 62.0\% & Verificado con evidencia empírica directa y componentes en el DOM. \\
\textbf{Parcial} & 11 & 15.5\% & Operativo en la demo interactiva; margen de enriquecimiento analítico. \\
\textbf{Pendiente de prueba} & 2 & 2.8\% & Requiere pruebas formales con usuarios en laboratorio (C4.7, C6.12). \\
\textbf{Excluido deliberado} & 2 & 2.8\% & Omitido para proteger la concentración lectora del estudiante (C2.7, C5.4). \\
\textbf{No aplica al alcance} & 12 & 16.9\% & Funcionalidades fuera del alcance (interfaces de voz VUI, base de datos). \\
\midrule
\textbf{TOTAL GENERAL} & \textbf{71} & \textbf{100\%} & \textbf{Cobertura sobre principios aplicables: 93.2\% (55 de 59)} \\
\bottomrule
\end{tabular}
\end{table}

\vspace{0.8em}

% --- 2. RUTA RÁPIDA ---
\section{Ruta de Evaluación Rápida en 5 Minutos (Para el Profesor)}

Para comprobar interactivamente la coherencia y fidelidad del diseño sin recorrer los 71 principios uno a uno, siga esta secuencia guiada en el navegador con \texttt{index.html} abierto:

\begin{enumerate}[leftmargin=1.8em, itemsep=0.4em]
    \item \textbf{Barra superior persistente (1 clic):} Alterne entre ``Conversación escrita'', ``Lecciones y repaso'' y ``Redacción asistida''. Compruebe que el cambio es instantáneo, el botón activo se resalta en verde-teal y el pie del chat confirma el modo activo (\textit{C1.1, C1.2, C7.5, C7.8}).
    \item \textbf{Tarjeta de corrección foveal con diff:} En ``Redacción asistida'', examine la tarjeta central. Compruebe la categoría con badge de color y texto (``Gramática''), la frase original tachada en rojo suave y la propuesta en verde suave. Pulse ``Usar esta sugerencia'' y observe el cambio de estado con botón ``Deshacer'' (\textit{C2.1, C4.1, C4.5, C5.1, C8.2, C8.8}).
    \item \textbf{Niveles de ayuda graduada a demanda:} Bajo el chat, pulse ``Pista'', ``Explicación'' y ``Ejemplo''. La tarjeta revela progresivamente más contenido sin recargar la página (\textit{C1.3, C3.7, C6.10, C7.10}).
    \item \textbf{Acceso al progreso en 1 clic:} Pulse el botón ``Ver progreso'' junto a las etapas numeradas. Se despliega inmediatamente el resumen de la sesión en el panel lateral derecho (\textit{C3.5, C7.1, C7.8, C8.3, C8.5}).
    \item \textbf{Lectura interactiva y guardado léxico:} Cambie a ``Lecciones y repaso''. En el artículo central, toque la palabra ``productive'', revise la definición contextual y pulse ``Guardar palabra''. La palabra se archiva en la pestaña ``Vocabulario'' (\textit{C3.4, C8.4, C8.7}).
    \item \textbf{Historial inmutable de chats:} En el footer, abra ``Ver chats'' y verifique que las sesiones pasadas mantienen un orden taxonómico estable sin reordenarse arbitrariamente (\textit{C1.2, C5.9, C7.1}).
\end{enumerate}

\newpage

% --- 3. CATÁLOGO DE PRINCIPIOS VERIFICADOS ---
\section{Catálogo de Principios Verificados en la Interfaz (55 Principios)}

A continuación se detallan los 55 principios implementados y comprobables en el código fuente de Lingua IA, organizados por capítulos según Jeff Johnson:
""")

    current_ch = ""
    for p in PRINCIPLES_DATA:
        ch = clean_text(p["chapter"])
        if ch != current_ch:
            current_ch = ch
            tex.append(f"\n\\subsection*{{{current_ch}}}\n")
        
        status_color = "linguaTeal" if p["status"] == "Aplicado" else "linguaAmber"
        status_label = clean_text(p["status"].upper())
        pid = clean_text(p["id"])
        pname = clean_text(p["name"])
        rule = clean_text(p["rule"])
        loc = clean_text(p["location"])
        how = clean_text(p["how_to_check"])
        just = clean_text(p["justification"])
        
        # Ruta de la imagen
        img_path = os.path.join(BASE_DIR, p["image"])
        
        box = f"""
\\begin{{tcolorbox}}[principlebox, title={{{pid} -- {pname} \\hfill \\colorbox{{{status_color}}}{{\\scriptsize\\textbf{{{status_label}}}}}}}]
\\small
\\textbf{{Regla Teórica:}} {rule}\\\\
\\textbf{{Ubicación en UI:}} \\texttt{{{loc}}}\\\\
\\textbf{{Cómo Comprobarlo:}} {how}\\\\
\\textbf{{Justificación de IHC:}} {just}

\\vspace{{0.5em}}
\\begin{{center}}
    \\includegraphics[width=0.88\\textwidth,height=3.5cm,keepaspectratio]{{{img_path}}}
\\end{{center}}
\\end{{tcolorbox}}
"""
        tex.append(box)

    # --- 4. PRINCIPIOS NO UTILIZADOS (SECCIÓN FINAL) ---
    tex.append(r"""
\newpage
\section{Sección Final: Catálogo de Principios No Utilizados / Excluidos y Justificación Técnica de IHC}

Para asegurar rigor académico absoluto, a continuación se detallan los \textbf{16 principios que NO forman parte del prototipo}, explicando para cada uno la justificación pedagógica, ergonómica o técnica de su exclusión:
""")

    current_cat = ""
    for p in NON_USED_PRINCIPLES:
        cat = clean_text(p["category"])
        if cat != current_cat:
            current_cat = cat
            tex.append(f"\n\\subsection*{{{current_cat}}}\n")
        
        pid = clean_text(p["id"])
        pname = clean_text(p["name"])
        brule = clean_text(p["book_rule"])
        why = clean_text(p["why_excluded"])
        defense = clean_text(p["design_defense"])
        
        box = (
            "\\begin{tcolorbox}[excludedbox, title={" + pid + " -- " + pname + " \\hfill \\colorbox{linguaRed}{\\scriptsize\\textbf{EXCLUIDO}}}]\n"
            "\\small\n"
            "\\textbf{Regla Teórica del Libro:} \\textit{``" + brule + "''}\\\\\n"
            "\\textbf{Por qué NO se incluyó en Lingua IA:} " + why + "\\\\\n"
            "\\textbf{Sustento de Diseño e IHC:} " + defense + "\n"
            "\\end{tcolorbox}\n"
        )
        tex.append(box)

    tex.append(r"""
\end{document}
""")

    with open(TEX_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(tex))
    print(f"Generado archivo TeX: {TEX_FILE}")

def compile_pdf():
    print("Compilando PDF con XeLaTeX (pasada 1)...")
    res1 = subprocess.run(["xelatex", "-interaction=nonstopmode", "-output-directory=" + os.path.dirname(TEX_FILE), TEX_FILE],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res1.returncode != 0:
        print("Error en pasada 1:")
        print(res1.stdout.decode("utf-8", errors="ignore")[-2000:])
        return False
    
    print("Compilando PDF con XeLaTeX (pasada 2 para referencias)...")
    res2 = subprocess.run(["xelatex", "-interaction=nonstopmode", "-output-directory=" + os.path.dirname(TEX_FILE), TEX_FILE],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    gen_pdf = os.path.join(os.path.dirname(TEX_FILE), "guia_documento.pdf")
    if os.path.exists(gen_pdf):
        shutil.move(gen_pdf, PDF_OUTPUT)
        print(f"¡Éxito! PDF generado en: {PDF_OUTPUT}")
        
        # Limpieza de temporales
        for ext in [".aux", ".log", ".out", ".toc"]:
            fpath = os.path.join(os.path.dirname(TEX_FILE), "guia_documento" + ext)
            if os.path.exists(fpath):
                os.remove(fpath)
        return True
    else:
        print("No se generó el archivo PDF.")
        return False

if __name__ == "__main__":
    generate_tex()
    compile_pdf()
