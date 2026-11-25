"""PDF de la misma revisión de 71 principios. Requiere pdflatex local."""
from pathlib import Path
import subprocess,tempfile
from collections import Counter
from build_guides import BASE,get_rows,INTRO

def tex(text):
 replacements={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','→':' -- ','–':'--','—':'---','“':'``','”':"''",'…':'...'}
 return ''.join(replacements.get(c,c) for c in str(text))

if __name__=='__main__':
 rows=get_rows();counts=Counter(r['status'] for r in rows)
 content=[r'\documentclass[11pt,a4paper]{article}',r'\usepackage[utf8]{inputenc}',r'\usepackage[T1]{fontenc}',r'\usepackage[margin=2cm]{geometry}',r'\usepackage{hyperref}',r'\usepackage{graphicx}',r'\setlength{\parindent}{0pt}',r'\setlength{\parskip}{7pt}',r'\begin{document}',r'\section*{Lingua IA -- Guía de principios IHC}',tex('Revisión técnica: 25/11/2026. Correo y vocabulario. Prototipo local.'),tex(INTRO),r'\subsection*{Estados actuales}']
 content.extend(tex(f'{k}: {v}.')+r'\par' for k,v in counts.items())
 content.append(tex('Se mantienen los 44 aplicados de la matriz original, con nuevas evidencias. No se declara aprobación docente ni validación experimental. Los recorridos exactos están en guia.md.'))
 for r in rows:
  content += [r'\subsection*{'+tex(r['id']+' -- '+r['title'])+'}',r'\textbf{'+tex('Matriz original: '+r['baseline']+'. Estado actual: '+r['status']+'.')+'}',tex(r['reason']),tex('Localización: '+r['selector'])]
 content += [r'\section*{Evidencias visuales actuales}']
 for name in ['01_inicio.png','02_sugerencia.png','03_comparar.png','04_revision.png','05_vocabulario.png','06_recuperar.png','07_aprendizaje.png','08_historial.png','11_etapas.png']:
  path=BASE/'docs/screenshots/actual'/name
  if path.exists():content += [r'\clearpage',r'\subsection*{'+tex(name)+'}',r'\includegraphics[width=\linewidth,height=.86\textheight,keepaspectratio]{'+path.as_posix()+'}']
 content += [r'\end{document}']
 with tempfile.TemporaryDirectory(prefix='lingua-pdf-') as tmp:
  source=Path(tmp)/'guia.tex';source.write_text('\n'.join(content))
  result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',tmp,str(source)],capture_output=True,text=True,errors='replace')
  if result.returncode:raise RuntimeError(result.stdout[-2500:])
  (BASE/'GUIA_PRINCIPIOS_IHC.pdf').write_bytes((Path(tmp)/'guia.pdf').read_bytes())
 print('PDF actual actualizado con los 71 principios.')
