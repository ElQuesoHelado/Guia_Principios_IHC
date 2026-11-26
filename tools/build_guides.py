"""Genera guía vigente de 71 principios desde la matriz original y evidencias actuales."""
from pathlib import Path
from collections import Counter
import json,html
BASE=Path(__file__).resolve().parent.parent
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
'C3.1':('Explicaciones breves; detalles de reglas y ejemplos se revelan bajo demanda.','.rule','05'),
'C3.2':('La intención precede a los mensajes; las propuestas y acciones se distinguen por tamaño, espacio y contraste.','.conversation-heading','03'),
'C3.4':('El panel lateral izquierdo agrupa correo, vocabulario y chats por explorar por tarea; las palabras permanecen junto al contexto.','.history-group','08'),
'C3.5':('Las métricas separan aportes y palabras. Las revisiones se dividen en antes, propuesta, motivo y decisión.','.metrics','07'),
'C3.7':('Texto libre para producir y razonar; botones para aceptar, conservar, guardar o mostrar apoyos. No se convierte la tarea en una ficha.','#chat-input','04'),
'C3.8':('Tu frase, Propuesta y la categoría se encuentran junto a sus valores, también en la comparación léxica.','.diff-line','04'),
'C4.1':('Gramática usa azul y Tono usa ocre, con nombres visibles. La decisión no depende del color.','.badge.grammar','04'),
'C4.3':('Texto oscuro sobre fondos suaves; el foco y el borde de la propuesta añaden diferencias de luminosidad.','.diff-line.proposal','04'),
'C4.4':('No se depende del par rojo/verde; categorías y estados se repiten en texto. No equivale a una validación con personas con daltonismo.','.badge.tone','04'),
'C4.5':('Categoría, antes/después, decisión y estado se expresan mediante rótulos, no solo color.','.badge','04'),
'C5.1':('La sugerencia de consulta aparece junto al compositor y la explicación junto al fragmento que se revisa.','#prompt-assist','02'),
'C5.8':('Sin sonidos, ventanas automáticas ni avisos repetitivos; la confirmación permanece junto al mensaje.','#composer-notice','04'),
'C5.9':('Las categorías del historial mantienen el orden Correo, Vocabulario y Por explorar; las conversaciones conservan su orden de creación.','.history-group','08'),
'C5.10':('Iconos de documento, libro, nuevo chat y conversaciones mantienen siluetas diferentes, acompañadas de etiquetas o nombres accesibles.','.header-actions','01'),
'C6.2':('Las instrucciones usan español cotidiano y el inglés se reserva al material de aprendizaje.','.message-content','03'),
'C6.3':('Se usa una tipografía sans serif del sistema sin depender de descargas ni fuentes decorativas para la lectura.','body','01'),
'C6.4':('Títulos e instrucciones utilizan mayúsculas y minúsculas; no hay párrafos en mayúsculas sostenidas.','#welcome-title','01'),
'C6.5':('Los textos se leen sobre fondos sólidos; no hay imágenes ni patrones detrás de las explicaciones.','.reading-card','05'),
'C6.7':('Mensajes, correos, lectura y explicaciones se alinean a la izquierda; solo se centran título inicial y metadatos breves.','.message-content','05'),
'C6.8':('Las tarjetas equivalentes comparten márgenes y las comparaciones mantienen alineación.','.comparison','03'),
'C6.9':('Títulos reales, rótulos, separación y detalles facilitan recorrer original, alternativa y razón.','.correction-card','04'),
'C6.10':('El inicio contiene una invitación, un compositor y dos ideas; la ruta y las explicaciones extensas se despliegan a petición.','#welcome','01'),
'C6.11':('No hay panel lateral permanente que repita texto o progreso; la información auxiliar se consulta cuando se necesita.','#learning-plan','01'),
'C7.1':('Contexto, mensajes, borrador y versiones se conservan por conversación y se recuperan desde el historial local.','.session-link','08'),
'C7.5':('La tarea y la etapa actual permanecen en una franja fija bajo el menú; Cambiar tarea permite corregir la ubicación. No hay cambios silenciosos entre actividades al escribir.','#task-label','03'),
'C7.7':('Enviar es la acción principal del compositor; cada propuesta distingue su opción de uso de las alternativas secundarias.','#send-btn','04'),
'C7.8':('Dos ideas de inicio y acceso directo al historial, ruta y notas; no hay un asistente secuencial obligatorio.','#starter-actions','01'),
'C7.10':('Reglas, ejemplos y versiones siguen accesibles. La recuperación sin apoyo es una práctica explícita y voluntaria, con opción de consultar.','#recall-banner','06'),
'C8.1':('La intención, la lectura y la producción propia ocupan el centro. La ruta permanece plegada inicialmente.','#main','01'),
'C8.2':('Cambios aceptados o conservados muestran estado en su tarjeta y confirmación junto al compositor; las versiones anteriores no se borran.','#composer-notice','04'),
'C8.3':('El indicador siempre visible muestra Etapa actual de cuatro. La ruta distingue Actual, Aporte guardado y Sin aporte aún. Cambiar de actividad actualiza la etapa; abrirla no registra una producción ni certifica dominio.','#stagebar','11'),
'C8.5':('Las opciones nombran el resultado: Comparar dos peticiones, Ver significado ahora y Probar sin definición.','[data-action="definition"]','05'),
'C8.6':('Confirmaciones y decisiones usan verbos concretos, incluida la acción de deshacer o usar una versión.','[data-action="undo-correction"]','04'),
'C8.7':('Las rutas responden a comparar registro, inferir, contrastar, recuperar y transferir expresiones del HTA seleccionado.','#learning-plan','06'),
'C8.10':('El cierre es una acción explícita en Mi aprendizaje: resume actividad, permite descargar notas y dejar una duda para retomar. No declara una tarea dominada por navegar hasta el final.','[data-action="finish"]','07'),
}
OTHER={
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
'C6.1':('Aplicado','Cuerpo a 16 px y etiquetas regulares a 14 px. Metadatos breves pueden ser menores; se verificó ausencia de desbordamiento a 320, 390 y 1440 px. La comodidad lectora requiere usuarios.','body'),
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
CAPTURES={'01':'01_inicio.png','02':'02_sugerencia.png','03':'03_comparar.png','04':'04_revision.png','05':'05_vocabulario.png','06':'06_recuperar.png','07':'07_aprendizaje.png','08':'08_historial.png','11':'11_etapas.png'}
INTRO='''La guía conserva los 71 principios y sus nombres de la matriz original. La columna de origen mantiene su clasificación binaria (44 cumplen y 27 no cumplen). El estado actual se revisa contra el prototipo conversacional: aplicado significa una decisión de diseño inspeccionable, no aprobación docente ni validación experimental. Parcial, pendiente, excluido y no aplica explican límites distintos; ninguno se cuenta como cumplimiento total.

Los originales anteriores al rediseño se conservan en docs/originales/principios-anterior/. El PDF y DOCX de la matriz de entrada permanecen intactos. Las capturas actuales se generan con tools/generate_screenshots.py; los recorridos completos están en guia.md y la correspondencia con el HTA en docs/REVISION_HTA_Y_TRAZABILIDAD.md.'''

def get_rows():
 rows=[]
 for item in json.loads((BASE/'docs/principios-base.json').read_text()):
  code=item['id']
  if code in APPLIED:
   reason,selector,picture=APPLIED[code];status='Aplicado'
  else:
   status,reason,selector=OTHER[code];picture=None
  rows.append({**item,'status':status,'reason':reason,'selector':selector,'picture':picture})
 assert len(rows)==71 and len(APPLIED)==44
 return rows

def main():
 rows=get_rows();counts=Counter(r['status'] for r in rows)
 md=['# Guía de principios IHC · interfaz conversacional','', 'Revisión técnica: 25/11/2026 · Correo y vocabulario · Prototipo local','',INTRO,'','## Resultado de la revisión','', '| Estado actual | Cantidad |','|---|---:|']+[f'| {k} | {v} |' for k,v in counts.items()]
 md+=['','Se mantienen los 44 principios aplicados de la matriz original, con evidencia nueva. Algunas reglas antes no cumplidas se aplican ahora. Las pruebas funcionales no acreditan comprensión, accesibilidad completa ni reducción de prompts.','','## Recorrido para revisar','', '1. Abre index.html y escribe una intención de correo: revisa la sugerencia opcional, edítala o descártala.','2. En Explorar ejemplos prepara el correo de revisión: compara Gramática/Tono, aplica y deshaz; recupera el original desde Mi aprendizaje.','3. Prepara el ejemplo léxico: escribe una hipótesis, contrástala, guarda/retira una palabra e intenta recuperarla sin definición.','4. Abre Mi aprendizaje y Conversaciones: comprueba notas, ayuda consultada y versiones. Retoma después desde el mismo navegador.','5. Consulta guia.md para los mensajes exactos y los límites de cada escenario.','','## Catálogo de los 71 principios','']
 chapters=['La percepción es sesgada','La visión está optimizada para ver estructura','Buscamos y usamos estructura visual','La visión del color es limitada','La visión periférica es pobre','Leer no es natural','La atención es limitada; la memoria es imperfecta','Los límites de la atención moldean pensamiento y acción']
 blocks=[]
 for c,title in enumerate(chapters,1):
  md+= [f'### C{c} · {title}','']
  blocks.append(f'<h2 id="chapter-{c}">C{c} · {html.escape(title)}</h2>')
  for r in rows:
   if not r['id'].startswith(f'C{c}.'):continue
   md += [f"#### {r['id']} · {r['title']}",f"- Matriz original: **{r['baseline']}**. Estado actual: **{r['status']}**.",f"- Evidencia / razón: {r['reason']}",f"- Localización real: `{r['selector']}`."]
   pic=f"docs/screenshots/actual/{CAPTURES[r['picture']]}" if r['picture'] else None
   if pic:md.append(f"- Captura del escenario: [{CAPTURES[r['picture']]}]({pic}).")
   md.append('')
   blocks.append(f'<article id="{r["id"]}"><h3>{r["id"]} · {html.escape(r["title"])}</h3><p class="status">Matriz original: {r["baseline"]} · <strong>{r["status"]}</strong></p><p>{html.escape(r["reason"])}</p><p>Localización: <code>{html.escape(r["selector"])}</code></p>{f"<a href={pic}>Ver captura de escenario</a>" if pic else ""}</article>')
 md+=['## Evidencias visuales actuales','']
 for code,name in CAPTURES.items():md+=[f'![Escenario actual {code}](docs/screenshots/actual/{name})','']
 md+=['## Límites de la evaluación','','Las fichas, escenarios y reglas son material de demostración, no consultas a una IA o diccionario en vivo. Las fechas de aportes son registros locales; la adquisición de conocimiento debe evaluarse mediante explicaciones, transferencia y recuperación posterior con usuarios. No se declara una mejora medida de consultas, tiempo, tokens ni aprendizaje.']
 (BASE/'GUIA_PRINCIPIOS_IHC.md').write_text('\n'.join(md)+'\n')
 nav=''.join(f'<a href="#chapter-{c}">C{c} · {html.escape(t)}</a>' for c,t in enumerate(chapters,1))
 gallery=''.join(f'<figure><img loading="lazy" src="docs/screenshots/actual/{n}" alt="Escenario actual {i}"><figcaption>{html.escape(n)}</figcaption></figure>' for i,n in CAPTURES.items())
 doc='<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Guía de principios · Lingua IA</title><style>body{font:16px/1.7 system-ui;color:#202c2c;max-width:1040px;margin:auto;padding:32px}h1,h2,h3{line-height:1.35}h1{font-size:2rem}h2{border-bottom:1px solid #ccc;padding-top:24px}article{border:1px solid #d2ddda;border-radius:12px;padding:20px;margin:18px 0;break-inside:avoid}article p{margin:10px 0}a{color:#0b665d}nav{display:flex;flex-wrap:wrap;gap:12px}code{font-size:.9em;overflow-wrap:anywhere}.status{color:#0b665d}img{width:100%;height:auto}figure{margin:24px 0}figcaption{font-size:14px;color:#596968}button{padding:10px 16px;font:inherit}table{border-collapse:collapse}td,th{border:1px solid #ccd8d3;padding:8px 16px}@media print{nav,button{display:none}body{padding:0}figure{break-inside:avoid}}</style><header><h1>Guía de principios IHC</h1><p>Lingua IA · Interfaz conversacional · Revisión técnica 25/11/2026</p><button onclick="window.print()">Imprimir o guardar como PDF</button><p><a href="index.html">Abrir prototipo</a> · <a href="guia.md">Guía de demostración</a></p></header>'
 doc+=''.join('<p>'+html.escape(p)+'</p>' for p in INTRO.split('\n\n'))+'<table><tr><th>Estado</th><th>Cantidad</th></tr>'+''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k,v in counts.items())+'</table><p>Se mantienen los 44 aplicados de la matriz original, con evidencia nueva. No se afirma validación experimental.</p><nav>'+nav+'</nav>'+''.join(blocks)+'<h2>Evidencias visuales actuales</h2>'+gallery+'</html>'
 (BASE/'GUIA_PRINCIPIOS_IHC.html').write_text(doc)
 (BASE/'guia.html').write_text(doc)
 print('Guías actualizadas:',dict(counts))
if __name__=='__main__':main()
