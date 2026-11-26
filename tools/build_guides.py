"""Genera guía vigente de 71 principios desde la matriz original y evidencias actuales."""
from pathlib import Path
from collections import Counter
import json,html,re
from zipfile import ZipFile
from xml.etree import ElementTree as ET
BASE=Path(__file__).resolve().parent.parent
MATRIX_SOURCE=BASE/'Matriz_reglas_condicion_Lingua_IA.docx'
AUTHORS=json.loads((BASE/'docs/hta_v8/contenido.json').read_text())['authors']
# Estado, evidencia de implementación, selector DOM, captura reproducible.
APPLIED={
'C1.1':('Acciones con resultado explícito: Añadir a mi mensaje, Conservar mi frase y Recuperar una versión.','[data-action="use-prompt"]','02'),
'C1.2':('La cabecera permanece visible durante el desplazamiento; el compositor y las acciones conservan estilo y función entre correo y vocabulario.','.app-header','01'),
'C1.3':('Se comienza con una intención libre y la ayuda se deriva de destinatario, contexto y propósito de aprendizaje.','#prompt-assist','02'),
'C2.1':('Cada revisión agrupa fragmento, propuesta, motivo y decisión; la consulta léxica conserva su oración.','.correction-card','04'),
'C2.2':('Botones, tarjetas y estados equivalentes reutilizan componentes y estilos.','.card','04'),
'C2.3':('Lectura, comparación y acciones comparten ejes; la ruta mantiene el orden de las sugerencias.','#stagebar','03'),
'C2.4':('Iconos lineales simples acompañan etiquetas; el envío tiene un nombre accesible.','#send-btn','01'),
'C2.5':('Columna central y comparaciones de igual peso; en móvil las alternativas se apilan sin perder su asociación.','.comparison','03'),
'C2.6':('Conversaciones se abre en un panel lateral izquierdo de alto completo; los paneles solicitados usan dialog con fondo separado, foco modal y cierre.','#workspace-dialog','07'),
'C3.1':('Los apoyos lingüísticos se solicitan en el chat; el patrón que conecta significado y estructura se despliega bajo demanda.','.rule','14'),
'C3.2':('La intención precede a los mensajes; las propuestas y acciones se distinguen por tamaño, espacio y contraste.','.conversation-heading','03'),
'C3.4':('Explorar ejemplos separa correo, vocabulario y Por explorar en grupos con encabezados; el historial mantiene esas categorías. Elegir un ejemplo prepara otro chat y conserva las demás conversaciones.','.demo-group','17'),
'C3.7':('Los valores limitados de tarea, etapa y decisión se eligen con botones que ofrecen las opciones disponibles; el mensaje, que admite contenido abierto, usa texto libre. No se piden fechas o teléfonos mediante controles genéricos.','#task-choice','11'),
'C3.8':('Tu frase, Propuesta y la categoría se encuentran junto a sus valores, también en la comparación léxica.','.diff-line','04'),
'C4.1':('Gramática usa azul y Tono usa ocre, con nombres visibles. La decisión no depende del color.','.badge.grammar','04'),
'C4.4':('No se depende del par rojo/verde; categorías y estados se repiten en texto. No equivale a una validación con personas con daltonismo.','.badge.tone','04'),
'C4.5':('Categoría, antes/después, decisión y estado se expresan mediante rótulos, no solo color.','.badge','04'),
'C5.1':('La sugerencia de consulta aparece junto al compositor y la explicación junto al fragmento que se revisa.','#prompt-assist','02'),
'C5.8':('Sin sonidos, ventanas automáticas ni avisos repetitivos; la confirmación permanece junto al mensaje.','#composer-notice','04'),
'C5.9':('Las categorías del historial mantienen el orden Correo, Vocabulario y Por explorar; las conversaciones conservan su orden de creación.','.history-group','08'),
'C5.10':('Iconos de documento, libro, nuevo chat y conversaciones mantienen siluetas diferentes, acompañadas de etiquetas o nombres accesibles.','.header-actions','01'),
'C6.2':('Las expresiones de asunto, saludo, petición, razón/finalidad y cierre aparecen en inglés con explicaciones de significado y uso en español.','.language-lesson','14'),
'C6.3':('Se usa una tipografía sans serif del sistema sin depender de descargas ni fuentes decorativas para la lectura.','body','01'),
'C6.4':('Títulos e instrucciones utilizan mayúsculas y minúsculas; no hay párrafos en mayúsculas sostenidas.','#welcome-title','01'),
'C6.5':('Los textos se leen sobre fondos sólidos; no hay imágenes ni patrones detrás de las explicaciones.','.reading-card','05'),
'C6.7':('Mensajes, correos, lectura y explicaciones se alinean a la izquierda; solo se centran título inicial y metadatos breves.','.message-content','05'),
'C6.8':('Las tarjetas equivalentes comparten márgenes y las comparaciones mantienen alineación.','.comparison','03'),
'C6.9':('Títulos reales, rótulos, separación y detalles facilitan recorrer original, alternativa y razón.','.correction-card','04'),
'C6.10':('El inicio contiene una invitación, un compositor y dos ideas; la ruta y las explicaciones extensas se despliegan a petición.','#welcome','01'),
'C6.11':('No hay panel lateral permanente que repita texto o progreso; la información auxiliar se consulta cuando se necesita.','#learning-plan','01'),
'C7.1':('Contexto, mensajes, borrador y versiones se conservan por conversación y se recuperan desde el historial local.','.session-link','08'),
'C7.5':('La tarea y la etapa se muestran en una franja fija; el compositor indica la actividad pendiente. Cambiar tarea permite corregir la clasificación y la recuperación sin ejemplos tiene un aviso persistente. Al abrir un apoyo o revisar un correo se actualiza esa ubicación.','#task-label','11'),
'C7.8':('Dos ideas de inicio y acceso directo al historial, ruta y notas; no hay un asistente secuencial obligatorio.','#starter-actions','01'),
'C7.10':('Reglas, ejemplos y versiones siguen accesibles. La recuperación sin apoyo es una práctica explícita y voluntaria, con opción de consultar.','#recall-banner','06'),
'C8.1':('La intención, la lectura y la producción propia ocupan el centro. La ruta permanece plegada inicialmente.','#main','01'),
'C8.2':('Aplicar, conservar y deshacer un fragmento muestran una confirmación junto al compositor y un estado en la propuesta. Al pegar otro borrador, las propuestas antiguas se identifican como pertenecientes a una versión anterior; no se borran las versiones.','#composer-notice','04'),
'C8.3':('El indicador siempre visible muestra Etapa actual de cuatro. La ruta distingue Actual, Aporte guardado y Sin aporte aún. Cambiar de actividad actualiza la etapa; abrirla no registra una producción ni certifica dominio.','#stagebar','11'),
'C8.5':('Los grupos distinguen aprender inglés con correo y aprender vocabulario. Preparar ejemplo anticipa un mensaje editable, y Revisar un correo pegado, Probar con mis palabras e Intentar sin ejemplos describen objetivos diferentes.','[data-action="load-demo"]','17'),
'C8.6':('Confirmaciones y decisiones usan verbos concretos, incluida la acción de deshacer o usar una versión.','[data-action="undo-correction"]','04'),
'C8.7':('Los caminos usan conceptos del aprendizaje: comprender una expresión, comparar, producir, revisar, recordar y reutilizar. Pegar un correo permite revisar directamente; los ejemplos son casos del HTA general y no obligan a seguir una secuencia fija.','#learning-plan','14'),
'C8.10':('El cierre es una acción explícita en Mi aprendizaje: resume actividad, permite descargar notas y dejar una duda para retomar. No declara una tarea dominada por navegar hasta el final.','[data-action="finish"]','07'),
}
OTHER={
'C3.5':('No aplica','La condición de la matriz trata de separar números largos para hacerlos legibles. La interfaz no presenta ese tipo de dato. Agrupar tarjetas, aportes o métricas no demuestra esta condición.','.metrics'),
'C4.3':('Parcial','Hay texto, bordes y fondos diferenciados, pero no se ha comprobado que todas las categorías y estados codificados por color se distingan por saturación y brillo además del tono. Las etiquetas redundantes apoyan C4.5 y no sustituyen esta comprobación.','.badge'),
'C7.7':('Parcial','Enviar y algunos botones de práctica comparten énfasis verde; además pueden permanecer acciones primarias de mensajes anteriores. Hay prioridad local dentro de cada propuesta, pero no se garantiza una única acción dominante en toda la pantalla.','.primary'),
'C2.7':('Excluido','No hay contenido en movimiento que deba agruparse. Se evita añadir animación sin una función de aprendizaje.','body'),
'C2.8':('Pendiente','La agrupación se ha inspeccionado en capturas; faltan revisión por dos personas y pruebas de percepción con usuarios.','.comparison'),
'C3.3':('Parcial','Hay encabezados semánticos h1/h2/h3, labels, dialog y log. Falta comprobar toda la interacción con un lector de pantalla real.','#chat-title'),
'C3.6':('No aplica','No se piden identificadores, teléfonos ni fechas compuestas. Fragmentar el mensaje libre volvería a introducir el formulario que se quiere evitar.','#chat-input'),
'C3.9':('No aplica','No existe una página de resultados de búsqueda. Las fichas preparadas no se presentan como resultados de una búsqueda.','.word-detail'),
'C4.2':('Aplicado','La revisión utiliza azul y ocre sobre fondos suaves, separados por espacio; no hay rojo y verde saturados yuxtapuestos.','.badge'),
'C4.6':('Parcial','Foco visible de 3 px e iconos oscuros. No se declara una medición exhaustiva de contraste para todos los bordes y estados.','#send-btn'),
'C4.7':('Pendiente','Falta comprobar pantallas, brillo, reflejos y dispositivos reales del público objetivo. Las capturas de un navegador no sustituyen esa prueba.','body'),
'C5.2':('No aplica','No hay errores de validación de formularios. El envío vacío se deshabilita y las limitaciones de revisión aparecen junto al texto.','#composer-notice'),
'C5.3':('Aplicado','La propuesta gramatical muestra un símbolo y el rótulo Gramática; la elección de tono usa su propia etiqueta. No se emplea rojo para señalar una preferencia estilística.','.badge.grammar'),
'C5.4':('Excluido','No existen avisos periféricos urgentes. Las sugerencias se sitúan junto a la escritura y pueden ignorarse.','#prompt-assist'),
'C5.5':('Aplicado','No se abren ventanas automáticas. Los paneles se solicitan expresamente; reglas y explicaciones se despliegan en el mismo contexto.','.rule'),
'C5.6':('No aplica','La práctica seleccionada es textual y no necesita sonidos de alerta ni audio.','#chat-messages'),
'C5.7':('No aplica','No hay parpadeos ni animaciones de aviso; no existe una duración de movimiento que limitar.','body'),
'C6.1':('Parcial','El cuerpo y el compositor usan 16 px, pero algunas etiquetas y botones de tarea bajan de ese tamaño, sobre todo en móvil. La ausencia de desbordamiento no demuestra que todo el texto esencial respete el tamaño base exigido por la matriz. Falta probar lectura con el público objetivo.','body'),
'C6.6':('Parcial','Se usa texto oscuro sobre fondos claros; falta una auditoría completa de todos los pares, estados, zoom y ajustes del usuario. No se afirma conformidad WCAG global.','body'),
'C6.12':('Pendiente','No se ha realizado una prueba de comprensión y lectura con estudiantes del público objetivo. Las pruebas automáticas no cubren este principio.','.reading-card'),
'C7.2':('No aplica','No hay salida de voz; el contenido se comunica por texto al ritmo del estudiante.','#chat-messages'),
'C7.3':('No aplica','No hay interfaz de voz ni listas de opciones habladas.','#chat-input'),
'C7.4':('No aplica','No existe una interfaz de voz que deba acompañarse de salida visual.','#chat-messages'),
'C7.6':('No aplica','No existe búsqueda externa ni una página de resultados. El mensaje original sí se conserva en el chat.','#chat-messages'),
'C7.9':('No aplica','La navegación es poco profunda: chat y panel solicitado. El encabezado identifica la actividad sin necesitar una ruta de carpetas.','#task-label'),
'C7.11':('No aplica','El prototipo no administra cuentas, contraseñas ni recuperación de autenticación.','.app-header'),
'C8.4':('Parcial','Se pueden guardar y retirar palabras del repaso. No se añaden colores personales ni reordenamiento de elementos; no es necesario para demostrar las dos tareas.','[data-action="save-word"]'),
'C8.8':('Parcial','Hay confirmaciones, notas persistentes y reversión de decisiones y versiones. No existe deshacer global de mensajes o todas las acciones; no se declara cumplimiento total.','[data-action="undo-correction"]'),
'C8.9':('Aplicado','Se usan Enter para enviar, Shift+Enter para otra línea y Escape nativo para cerrar dialog. El compositor muestra los atajos familiares.','.composer-footnote'),
'C8.11':('Parcial','La práctica sin modelo se indica de forma explícita y permite salir con Consultar el apoyo anterior. No expira por tiempo: una salida automática interrumpiría la recuperación al ritmo del estudiante.','#recall-banner'),
}
CAPTURES={'01':'01_inicio.png','02':'02_sugerencia.png','03':'03_comparar.png','04':'04_revision.png','05':'05_vocabulario.png','06':'06_recuperar.png','07':'07_aprendizaje.png','08':'08_historial.png','11':'11_etapas.png','14':'14_expresiones.png','15':'15_razon_finalidad_movil.png','16':'16_sugerencia_ingles.png','17':'17_ejemplos_separados.png','18':'15_expresiones.png','19':'16_consulta_retorno.png','20':'17_repaso_contextos.png','21':'18_consulta_movil.png'}
INTRO='''Fuente principal: Matriz_reglas_condicion_Lingua_IA.docx y su PDF de referencia. Cada entrada conserva el identificador, el nombre, la condición completa y la clasificación original de esa matriz (44 Cumple y 27 No cumple). La valoración actual se hace contra la interfaz vigente y se muestra por separado; no hereda automáticamente el cumplimiento anterior.

Aplicado significa una decisión de diseño inspeccionable que responde a la condición de la matriz; no acredita aprobación docente ni validación experimental. Parcial indica cobertura incompleta, Pendiente una comprobación necesaria, Excluido una decisión de alcance y No aplica la ausencia de la situación descrita. Estas categorías no se cuentan como cumplimiento total.

El HTA v8 describe el proceso general ante contenido o expresiones desconocidos. La interfaz lo ilustra con ejemplos preparados de correo y vocabulario en grupos separados, revisión directa de correos pegados y apoyos de asunto, saludo, petición, razón/finalidad y cierre. Los intentos propios, recuperación y transferencia se registran sin calificar su corrección. Se añaden consultas con retorno al punto de origen, revisión de una aparición del fragmento y repaso por palabra y oración; los ejemplos no acreditan cobertura total del proceso general.

Se corrigieron valoraciones que no respondían a la condición exacta: C3.5 se refiere a números largos y no aplica a esta tarea; C4.3, C6.1 y C7.7 quedan parciales por límites de color, tamaño de texto y competencia entre acciones. Se conserva la clasificación original para que la diferencia sea visible.

La matriz original permanece intacta. Los originales anteriores de la guía están en docs/originales/principios-anterior/. Las capturas vigentes se generan con tools/generate_screenshots.py. Los recorridos y límites de la demo están en guia.md y la correspondencia con el HTA en docs/REVISION_HTA_Y_TRAZABILIDAD.md.'''

def matrix_rows():
 ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
 catalog=json.loads((BASE/'docs/principios-base.json').read_text())
 index={item['id']:item for item in catalog}
 with ZipFile(MATRIX_SOURCE) as z:
  root=ET.fromstring(z.read('word/document.xml'))
 rows=[]
 for row in root.findall('.//w:tbl/w:tr',ns):
  cells=[' '.join(t.text or '' for t in cell.findall('.//w:t',ns)) for cell in row.findall('./w:tc',ns)]
  if not cells:continue
  match=re.match(r'(C[1-8]\.\d+)\s*·\s*',cells[0])
  if not match:continue
  item=index[match[1]]
  rule=cells[0][match.end():]
  assert rule.startswith(item['title']+' '),('Nombre distinto en la matriz',item['id'])
  assert cells[1]==item['baseline'],('Clasificación distinta en la matriz',item['id'])
  rows.append({**item,'condition':rule[len(item['title']):].strip()})
 assert len(rows)==71 and len({r['id'] for r in rows})==71
 assert set(APPLIED).isdisjoint(OTHER)
 assert set(APPLIED)|set(OTHER)==set(index)
 return rows

def get_rows():
 rows=[]
 for item in matrix_rows():
  code=item['id']
  if code in APPLIED:
   reason,selector,picture=APPLIED[code];status='Aplicado'
  else:
   status,reason,selector=OTHER[code];picture={'C4.3':'04','C6.1':'15','C7.7':'14'}.get(code)
  rows.append({**item,'status':status,'reason':reason,'selector':selector,'picture':picture})
 assert len(rows)==71
 return rows

def main():
 rows=get_rows();counts=Counter(r['status'] for r in rows)
 md=['# Guía de principios IHC · interfaz conversacional','', 'Revisión técnica: 26/11/2026 · Correo y vocabulario · Prototipo local','', 'Alumnos: '+AUTHORS,'','Documento base: [Matriz en Word](Matriz_reglas_condicion_Lingua_IA.docx) · [Matriz en PDF](Matriz_reglas_condicion_Lingua_IA.pdf).','',INTRO,'','## Resultado de la revisión','', '| Estado actual | Cantidad |','|---|---:|']+[f'| {k} | {v} |' for k,v in counts.items()]
 md+=['','La matriz original conserva 44 Cumple y 27 No cumple. La valoración actual no modifica esa fuente ni fuerza que sus 44 casos sigan aplicados; se explican las diferencias por regla. Las pruebas funcionales no acreditan comprensión, accesibilidad completa ni reducción de prompts.','','## Recorrido para revisar','', '1. Abre index.html y escribe una dificultad de inglés: contrasta la sugerencia opcional con C1.3 y C5.1; añádela, edítala o descártala.','2. En Explorar ejemplos comprueba los grupos separados de correo y vocabulario (C3.4 y C8.5). Cada ejemplo prepara un chat independiente sin enviar el mensaje.','3. Pega un correo, incluso con un apoyo pendiente: compara Gramática/Tono, aplica o conserva y deshaz; recupera el original desde Mi aprendizaje (C2.1, C4.5 y C8.2). La revisión es limitada a reglas de ejemplo.','4. Prueba un apoyo lingüístico o vocabulario: escribe una interpretación, contrasta y produce con tus palabras. Intenta recuperar sin ejemplos o definición; consulta apoyo si lo necesitas (C6.2, C7.10 y C8.7).','5. Abre Mi aprendizaje y Conversaciones: comprueba tema, aportes, versiones y ayuda utilizada; retoma después en el mismo navegador (C7.1 y C8.3). Consulta guia.md para los mensajes exactos y los límites.','','## Catálogo de los 71 principios','']
 chapters=['La percepción es sesgada','La visión está optimizada para ver estructura','Buscamos y usamos estructura visual','La visión del color es limitada','La visión periférica es pobre','Leer no es natural','La atención es limitada; la memoria es imperfecta','Los límites de la atención moldean pensamiento y acción']
 blocks=[]
 for c,title in enumerate(chapters,1):
  md+= [f'### C{c} · {title}','']
  blocks.append(f'<h2 id="chapter-{c}">C{c} · {html.escape(title)}</h2>')
  for r in rows:
   if not r['id'].startswith(f'C{c}.'):continue
   md += [f"#### {r['id']} · {r['title']}",'',f"- Condición de la matriz: {r['condition']}",f"- Matriz original: **{r['baseline']}**. Estado actual: **{r['status']}**.",f"- Evidencia / razón: {r['reason']}",f"- Localización real: `{r['selector']}`."]
   pic=f"docs/screenshots/actual/{CAPTURES[r['picture']]}" if r['picture'] else None
   if pic:md.append(f"- Captura del escenario: [{CAPTURES[r['picture']]}]({pic}).")
   md.append('')
   blocks.append(f'<article id="{r["id"]}"><h3>{r["id"]} · {html.escape(r["title"])}</h3><p><strong>Condición de la matriz:</strong> {html.escape(r["condition"])}</p><p class="status">Matriz original: {r["baseline"]} · <strong>{r["status"]}</strong></p><p>{html.escape(r["reason"])}</p><p>Localización: <code>{html.escape(r["selector"])}</code></p>{f"<a href={pic}>Ver captura de escenario</a>" if pic else ""}</article>')
 md+=['## Evidencias visuales actuales','']
 for code,name in CAPTURES.items():md+=[f'![Escenario actual {code}](docs/screenshots/actual/{name})','']
 md+=['## Límites de la evaluación','','Las fichas, escenarios y reglas son material de demostración, no consultas a una IA o diccionario en vivo. Las fechas de aportes son registros locales; la adquisición de conocimiento debe evaluarse mediante explicaciones, transferencia y recuperación posterior con usuarios. No se declara una mejora medida de consultas, tiempo, tokens ni aprendizaje.']
 (BASE/'GUIA_PRINCIPIOS_IHC.md').write_text('\n'.join(md)+'\n')
 nav=''.join(f'<a href="#chapter-{c}">C{c} · {html.escape(t)}</a>' for c,t in enumerate(chapters,1))
 gallery=''.join(f'<figure><img loading="lazy" src="docs/screenshots/actual/{n}" alt="Escenario actual {i}"><figcaption>{html.escape(n)}</figcaption></figure>' for i,n in CAPTURES.items())
 doc='<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Guía de principios · Lingua IA</title><style>body{font:16px/1.7 system-ui;color:#202c2c;max-width:1040px;margin:auto;padding:32px}h1,h2,h3{line-height:1.35}h1{font-size:2rem}h2{border-bottom:1px solid #ccc;padding-top:24px}article{border:1px solid #d2ddda;border-radius:12px;padding:20px;margin:18px 0;break-inside:avoid}article p{margin:10px 0}a{color:#0b665d}nav{display:flex;flex-wrap:wrap;gap:12px}code{font-size:.9em;overflow-wrap:anywhere}.status{color:#0b665d}img{width:100%;height:auto}figure{margin:24px 0}figcaption{font-size:14px;color:#596968}button{padding:10px 16px;font:inherit}table{border-collapse:collapse}td,th{border:1px solid #ccd8d3;padding:8px 16px}@media print{nav,button{display:none}body{padding:0}figure{break-inside:avoid}}</style><header><h1>Guía de principios IHC</h1><p>Lingua IA · Interfaz conversacional · Revisión técnica 26/11/2026</p><p>Alumnos: '+html.escape(AUTHORS)+'</p><p>Fuente: <a href="Matriz_reglas_condicion_Lingua_IA.docx">Matriz original en Word</a> · <a href="Matriz_reglas_condicion_Lingua_IA.pdf">Matriz original en PDF</a></p><button onclick="window.print()">Imprimir o guardar como PDF</button><p><a href="index.html">Abrir prototipo</a> · <a href="guia.md">Guía de demostración</a></p></header>'
 doc+=''.join('<p>'+html.escape(p)+'</p>' for p in INTRO.split('\n\n'))+'<table><tr><th>Estado</th><th>Cantidad</th></tr>'+''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k,v in counts.items())+'</table><p>Se conserva la clasificación original de la matriz; la valoración actual se contrasta con su condición completa. No se afirma validación experimental.</p><nav>'+nav+'</nav>'+''.join(blocks)+'<h2>Evidencias visuales actuales</h2>'+gallery+'</html>'
 (BASE/'GUIA_PRINCIPIOS_IHC.html').write_text(doc)
 (BASE/'guia.html').write_text(doc)
 print('Guías actualizadas:',dict(counts))
if __name__=='__main__':main()
