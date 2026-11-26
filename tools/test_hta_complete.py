"""Escenarios ilustrativos: alternativas, retorno, revisión y producción propia.
No acreditan cobertura completa del HTA general ni aprendizaje.
"""
from pathlib import Path
import json
import re
import subprocess
import tempfile
from browser_capture import BASE, capture

SCRIPT = r'''
const checks=[],covered=new Set();
const check=(ok,name)=>{if(!ok)throw Error(name);checks.push(name);};
const cover=(ids,ok,name)=>{check(ok,name);ids.split(' ').forEach(id=>covered.add(id));};
const activate=e=>{if(!e)throw Error('Control inexistente');for(let p=e.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;e.scrollIntoView({block:'center'});check(e.getBoundingClientRect().height>0,'Control visible: '+(e.dataset.action||e.tagName));e.click();};
const click=q=>{const e=document.querySelector(q);if(!e)throw Error('Falta '+q);activate(e);};
const last=q=>{const es=document.querySelectorAll(q);if(!es.length)throw Error('Falta '+q);activate(es[es.length-1]);};
const type=t=>{const e=document.querySelector('#chat-input');e.value=t;e.dispatchEvent(new Event('input',{bubbles:true}));};
const send=t=>{type(t);click('#send-btn');};
const active=()=>{const st=Lingua.getState();return st.sessions.find(s=>s.id===st.active);};
const lastText=()=>document.querySelector('#chat-messages').lastElementChild.textContent;
try {
 Lingua.reset();
 type('Quiero un saludo para un correo a mi profesora');
 check(document.querySelector('#prompt-assist').textContent.includes('Dear Professor'),'Sugiere expresiones concretas mientras se escribe');
 click('[data-action="use-prompt"]');check(Lingua.getState().sessions.length===0,'El apoyo de expresión no envía ni fabrica datos');
 click('[data-action="undo-prompt"]');
 type('Quiero un asunto para pedir una prórroga a mi profesora');
 check(document.querySelector('#prompt-assist').textContent.includes('Request for an extension'),'Sugiere asunto de la misma intención');
 type('Quiero una despedida para un correo a mi profesora');
 check(document.querySelector('#prompt-assist').textContent.includes('Best regards'),'Sugiere cierres para contrastar');
 send('Quiero escribir un correo para pedir apuntes a mi profesora.');
 cover('C1 C1.1 C1.1.1',active().hta.email.cases[0]==='notes','Identifica material sin cambiar la intención');
 click('[data-action="hta-situation"]');last('[data-action="hta-facts"]');send('nombre: Alex Rivera; tratamiento: Professor; material: apuntes de la clase del lunes; fecha vigente: Thursday; fecha propuesta: Friday; motivo: preparar mi examen');
 cover('C1.2 C1.3',active().hta.email.name==='Alex Rivera'&&active().hta.email.facts.material.includes('lunes'),'Conserva los datos aportados y su procedencia');
 last('[data-action="hta-known"]');send('Conozco can, pero dudo cómo escribir el asunto y el saludo.');
 check(active().evidence.at(-1).kind.includes('Expresión conocida'),'Registra expresión previa y duda');
 for(const [key,subject,polite,id] of [['notes','Request for lecture notes','Could you please send me the notes?','C3.1.1'],['extension','Request for an extension','Could I have an extension until Friday?','C3.1.2'],['clarify','Question about the submission deadline','Could you please confirm the submission deadline?','C3.1.3']]){
  click('[data-action="hta-case"][data-case="'+key+'"]');
  click('[data-action="model"]');
  check(lastText().includes(subject)&&lastText().includes('Modelo preparado'),'Modelo del mismo caso, datos de ejemplo identificados');
  click('[data-action="compare"]');
  check(lastText().includes(polite),'Comparación conserva la intención de '+key);
  send('Could suaviza, please añade cortesía. El motivo explica la necesidad; el dato identifica material o plazo.');
  click('[data-action="hta-parts"]');
  cover(id,lastText().includes(subject),'Asunto pertinente de '+key);
 }
 cover('C1.1.2 C1.1.3 C2 C2.1 C2.2 C2.3 C3 C3.1',active().hta.email.facts.current==='Thursday'&&active().hta.email.facts.proposed==='Friday','Distingue fechas y tres intenciones; explica el modelo');
 last('[data-action="hta-relation"][data-relation="unknown"]');
 click('[data-action="hta-parts"]');
 const parts=lastText();
 cover('C3.2 C3.2.1 C3.2.2 C3.2.3 C3.2.4',parts.includes('Dear Professor Rivera')&&parts.includes('Dear Alex Rivera')&&parts.includes('Hi Alex')&&parts.includes('compruébalos'),'Alternativas de saludo y tratamiento desconocido');
 cover('C3.3 C3.3.1 C3.3.2 C3.3.3 C3.3.4',checks.filter(t=>t.startsWith('Comparación conserva')).length===3,'Peticiones de material, plazo y aclaración');
 cover('C3.4 C3.5 C3.5.1 C3.5.2',parts.includes('because')&&parts.includes('Best regards')&&parts.includes('Thanks'),'Motivo y dos cierres contextualizados');
 last('[data-action="hta-try-part"][data-part="subject"]');send('Question about the submission deadline: debo aclarar la fecha, no pedir una prórroga.');
 check(active().evidence.at(-1).kind.startsWith('Elección propia'),'Guarda expresión y explicación');
 click('[data-action="hta-situation"]');last('[data-action="hta-combine"]');send('Necesito combinar apuntes y una prórroga porque son dos solicitudes necesarias.');
 check(active().hta.email.cases.includes('notes')&&active().hta.email.cases.includes('extension'),'Combina solicitudes solo al declararlas');
 click('[data-action="write"]');
 const original='Subject: Study space\nDear Professor Rivera,\nA dedicated space helps you focus on your work.\nI am agree.\nSend me the notes.\nSend me the notes.\nBest regards,\nAlex';
 send(original);
 cover('C5 C5.1',active().draft===original,'Conserva la producción antes de revisarla');
 last('[data-action="hta-review-fragment"]');send('Send me the notes.');
 const ranges=[...document.querySelectorAll('[data-action="hta-review-range"]')];
 check(ranges.length===2,'Distingue dos apariciones del mismo fragmento');activate(ranges[1]);
 const correction=active().messages.filter(m=>m.kind==='correction'&&m.status==='pending').at(-1);
 click('[data-action="accept"][data-id="'+correction.id+'"]');
 const expected=original.slice(0,correction.start)+'Could you please send me the notes?'+original.slice(correction.end);
 cover('C5.2 C5.2.2 C5.3 C5.3.1',active().draft===expected&&!active().draft.includes('?.'),'Cambia solo la segunda aparición y conserva puntuación');
 click('[data-action="justify"][data-id="'+correction.id+'"]');send('Mantengo lo que pido y suavizo el tono porque me dirijo a una profesora.');
 cover('C5.4',active().evidence.at(-1).before==='Send me the notes.'&&active().evidence.at(-1).after.includes('Could'),'Registra antes, después y razón');
 click('[data-action="review"]');
 const grammar=active().messages.find(m=>m.kind==='correction'&&m.category==='Gramática'&&m.status==='pending');
 check(Boolean(grammar),'Regla de I am agree');click('[data-action="reject"][data-id="'+grammar.id+'"]');
 cover('C5.2.1 C5.3.2',active().draft.includes('I am agree'),'Conservar no modifica la producción');
 last('[data-action="hta-explain"]');
 cover('C5.3.3',lastText().includes('Encontrar mis expresiones'),'Otra explicación abre el apoyo y permite volver');
 click('[data-action="hta-review-choice"]');
 cover('C5.2.3',lastText().includes('no es una mejora recomendada'),'Contrasta cambio de intención como ejemplo adverso');
 last('[data-action="hta-meaning-explain"]');send('Cambiar apuntes por permiso altera lo que necesito del destinatario.');
 // Entrada real C4 -> V0: se guardan versión, pending y texto todavía no enviado.
 click('[data-action="write"]');const preserved=active().draft;
 type('Una parte de mi próximo correo sin enviar');
 last('[data-action="hta-consult"]');send('A dedicated space helps you focus on your work.');
 cover('C4 C4.1 V1.3',active().task==='vocab'&&active().hta.returns.length===1&&active().context==='A dedicated space helps you focus on your work.','Consulta conserva oración y origen');
 check(active().hta.returns[0].pending.type==='draft','Conserva la tarea de producción pendiente');
 dump('HTA_SNAPSHOT '+JSON.stringify(Lingua.getState())+'\n');
 send('Creo que es reservado para una finalidad, por space y focus on your work.');
 cover('V2.3',document.querySelector('.word-detail').textContent.includes('Tu interpretación inicial'),'Hipótesis registrada antes de consultar');
 click('[data-action="hta-resources"]');
 for(const resource of ['model','translation','ai','person']){
  last('[data-action="hta-resource"][data-resource="'+resource+'"]');
  check(lastText().includes('Ejemplo preparado')&&lastText().includes('no es una consulta en vivo'),'Identifica procedencia de '+resource);
  click('[data-action="hta-resources"]');
 }
 cover('C4.2 C4.2.1 C4.2.2 C4.2.3 C4.2.4 V3.1 V3.1.1 V3.1.2 V3.1.3 V3.1.4',active().hta.queries.filter(q=>q.kind==='prepared').length===4,'Cuatro rutas no acumulativas');
 last('[data-action="hta-external"]');send('Diccionario consultado por mí, nota de clase de hoy.');send('En esta oración dedicado significa reservado para una finalidad.');send('Space indica un lugar; no se trata de compromiso de una persona.');
 cover('C4.3 V3.2',active().hta.entries.some(e=>e.sources.some(x=>x.verified===false&&x.reference?.includes('Diccionario consultado'))),'Preserva fuente externa sin fingir verificación');
 click('[data-action="hta-resources"]');last('[data-action="hta-refine"]');send('¿Qué cambia si dedicated modifica teacher? Necesito otro ejemplo de igual acepción.');
 cover('C4.4',active().evidence.at(-1).text.includes('teacher'),'Reformula solo la duda abierta');
 click('[data-action="hta-lexical-tools"]');
 const tools=lastText();
 cover('V2 V2.1 V2.2 V2.2.1 V2.2.2 V2.2.3',tools.includes('modifica space')&&tools.includes('reformulación explícita')&&tools.includes('no la demuestra'),'Pistas y límites del indicio sin inventar su presencia');
 last('[data-action="hta-infer"]');send('Creo que es reservado, por space y focus on your work.');
 check(active().evidence.at(-1).kind==='Interpretación después del contraste','Una explicación posterior no sustituye la hipótesis inicial');
 last('[data-action="hta-lexical-tools"]');last('[data-action="hta-interpret"]');send('Reservado para una finalidad, porque modifica un espacio; descarto comprometida como una persona.');
 cover('V3 V3.3 V3.3.1 V3.4',active().hta.entries.some(e=>e.interpretation.includes('descarto')),'Interpretación reformulada con acepción descartada');
 click('[data-action="hta-return"]');
 cover('C0 V0',active().task==='email'&&active().draft===preserved&&active().pending.type==='draft'&&document.querySelector('#chat-input').value==='Una parte de mi próximo correo sin enviar','Retorna sin perder borrador, pendiente ni mensaje sin enviar');
 check(lastText().includes('Reservado'),'Devuelve interpretación al punto de origen');
 click('[data-action="recall"]');
 check([...document.querySelectorAll('.recall-hidden')].every(e=>getComputedStyle(e).display==='none'),'Material anterior oculto durante recuperación');
 send('Could you please send me the notes? Elijo cortesía sin alterar lo que solicito.');
 click('[data-action="transfer"]');send('Hi Alex, can you send me the notes? Thanks, Sam. Tengo confianza con mi compañero.');
 click('[data-action="hta-productions"]');
 cover('C6 C6.1 C6.2 C6.3 C6.4',lastText().includes('Could you please send me')&&lastText().includes('Hi Alex'),'Conserva y compara recuperación y nueva producción');
 last('[data-action="hta-compare-own"]');send('La intención se conserva; can y Hi son más cercanos. Necesité apoyo para el cierre.');
 click('[data-action="notebook"]');click('[data-action="finish"]');click('[data-action="reflection"]');send('Quiero revisar si puedo recuperar el asunto sin mirar el modelo.');
 click('[data-action="notebook"]');click('[data-action="hta-resume-plan"]');click('[data-action="recall"]');click('[data-action="notebook"]');
 check(active().helpUsed,'Abrir notas durante recuperación registra apoyo');click('[data-action="close-dialog"]');
 send('Request for lecture notes. Consulté el apoyo para comparar el asunto.');
 cover('C7 C7.1 C7.2 C7.3 C7.4',active().evidence.at(-1).help&&lastText().toLowerCase().includes('no se ha calificado'),'Continuidad y ayuda diferenciadas de dominio');
 // Las dos acepciones, la lectura y las alternativas léxicas.
 click('[data-action="new"]');send('¿Qué significa dedicated en “She is a dedicated teacher”?');
 last('[data-action="definition"]');
 cover('V3.3.2',document.querySelector('.word-detail .proposal').textContent.includes('Comprometida'),'Acepción de persona');
 click('[data-action="save-word"]');click('[data-action="reading"]');
 click('[data-action="hta-reading-note"]');send('El título me recuerda mi lugar de estudio; la nota está dirigida a estudiantes y trata de organizar el trabajo.');
 cover('V1 V1.1',active().evidence.at(-1).text.includes('estudiantes'),'Conocimientos previos, fuente y resumen propios');
 click('[data-action="hta-priority"]');send('Dedicated es relevante para describir mi espacio; puedo dejar otras palabras para después.');
 cover('V1.2',active().evidence.at(-1).text.includes('relevante'),'Decide relevancia sin obligar a consultar todas las palabras');
 click('[data-action="pick-word"][data-word="dedicated"]');last('[data-action="definition"]');last('[data-action="save-word"][data-context="A dedicated space helps you focus on your work."]');
 check(active().hta.entries.filter(e=>e.word==='dedicated'&&e.saved).length===2,'Guarda dos acepciones de la misma palabra');
 last('[data-action="hta-lexical-tools"]');
 cover('V4 V4.1 V4.3',lastText().includes('dedicated + sustantivo'),'Patrón y ejemplos para comparar significado con registro');
 last('[data-action="hta-register-note"]');send('Mi fuente marca un uso neutro; acepción de espacio reservado. Referencia anotada, pendiente de verificar.');
 cover('V4.2 V4.2.1',active().hta.entries.some(e=>e.register?.verified===false),'Etiqueta aportada conserva su procedencia sin atribuir verificación');
 click('[data-action="hta-lexical-tools"]');last('[data-action="hta-register-unknown"]');
 cover('V4.2.2',active().hta.entries.some(e=>e.register?.label==='Sin determinar'),'Ausencia de etiqueta explícita');
 last('[data-action="hta-lexical-note"]');send('Dedicated: reservado para una finalidad. Origen: A dedicated space helps you focus on your work. Patrón: dedicated + sustantivo. Lo usaré para proponer un lugar de estudio; debo contrastar otros usos.');
 cover('V4.4',active().hta.entries.some(e=>e.note.includes('Patrón')),'Nota propia conecta significado, contexto, patrón y duda');
 click('[data-action="hta-lexical-tools"]');last('[data-action="hta-vocab-write"]');send('I have a dedicated desk for my homework.');
 cover('V5 V5.1 V5.2',lastText().includes('referente, acepción, combinación gramatical'),'Producción y criterios de contraste');
 last('[data-action="hta-production-keep"]');send('Desk es un espacio reservado; coincide con el ejemplo dedicated room.');
 cover('V5.3 V5.3.1',active().hta.entries.some(e=>e.reviews.some(r=>r.decision==='decision')),'Conserva y justifica la coincidencia');
 click('[data-action="hta-lexical-tools"]');last('[data-action="hta-vocab-write"]');send('This desk is dedicated for studying.');last('[data-action="hta-production-rewrite"]');send('This desk is dedicated to studying.');
 cover('V5.3.2',active().hta.productions.some(p=>p.kind==='Oración reformulada'),'Reformula el patrón conservando la producción previa');
 last('[data-action="hta-production-replace"]');send('I have a quiet desk. Quiero decir silencioso, no reservado.');
 cover('V5.3.3',active().hta.productions.some(p=>p.kind==='Otra palabra para conservar la intención'),'Permite otra palabra sin forzar la acepción');
 last('[data-action="hta-transfer-email"]');
 check(active().task==='email'&&active().hta.returns.length===1,'Transferencia abre correo vinculado');
 send('Hi Alex, we have a dedicated room for our project. Thanks, Sam.');
 click('[data-action="review"]');click('[data-action="hta-return"]');
 cover('V6 V6.2 V6.3',active().task==='vocab'&&lastText().includes('dedicated room'),'Correo de transferencia regresa al vocabulario');
 click('[data-action="recall"]');send('Dedicated significa reservado para una finalidad. We have a dedicated room.');
 cover('V6.1',active().evidence.at(-1).kind==='Intento de recuperación','Recuperación propia sin definición');
 click('[data-action="hta-productions"]');last('[data-action="hta-compare-own"]');send('En el correo propuse un lugar para un proyecto; la acepción es la misma. El patrón dedicado a me requirió apoyo.');
 cover('V6.4',active().evidence.at(-1).text.includes('patrón'),'Compara nuevo uso, origen y ayuda');
 click('[data-action="notebook"]');click('[data-action="repaso"]');
 const reviewOptions=[...document.querySelectorAll('#dialog-content [data-action="hta-entry-recall"]')];
 check(reviewOptions.length===2,'Elige qué acepción repasar');
 activate(reviewOptions.find(e=>e.dataset.context.includes('teacher')));
 check(active().word==='dedicated'&&active().context.includes('teacher'),'Repasa la acepción elegida, no la primera');
 send('Una persona comprometida. She is a dedicated teacher.');
 click('[data-action="hta-pending"]');send('Quiero contrastar el patrón dedicated to en otra sesión.');
 click('[data-action="notebook"]');click('[data-action="hta-resume-plan"]');
 cover('V7 V7.1 V7.2 V7.3 V7.4',active().hta.pendingNotes.length>0&&lastText().includes('Retomar una duda'),'Registro, fecha, ayuda y decisión de continuación sin falsa retención');
 click('[data-action="new"]');send('¿Qué significa dedicated en “He dedicated the book to his mother”?');
 click('[data-action="stage"][data-stage="1"]');
 cover('V3.3.3',!document.querySelector('.word-detail'),'Contexto no preparado conserva incertidumbre');

 // Entrar con borrador, corregir varios rangos y contrastar una alternativa propia.
 click('[data-action="new"]');
 const direct='Dear Professor,\nI am agree.\nSend me the notes.\nBest regards,\nAlex';send(direct);
 check(active().task==='email','Entrada directa con borrador sin selector previo');
 const cs=active().messages.filter(m=>m.kind==='correction'&&m.status==='pending');
 for(const c of cs)click('[data-action="accept"][data-id="'+c.id+'"]');
 check(active().draft.includes('I agree.')&&active().draft.includes('Could you please send me the notes?')&&!active().draft.includes('?.'),'Dos cambios no solapados actualizan sus posiciones');
 click('[data-action="write"]');send('Dear Professor,\nCould I have an extension until Friday?\nBest regards,\nAlex');
 const beforeData=active().draft;last('[data-action="hta-review-choice"]');
 check(lastText().includes('Friday')&&lastText().includes('Monday'),'El ejemplo de datos hace visible el cambio de fecha');
 last('[data-action="hta-meaning-keep"]');send('Friday es mi fecha propuesta; Monday cambiaría mi solicitud.');
 check(active().draft===beforeData,'Rechazar diferencia semántica conserva la fecha');
 last('[data-action="hta-review-fragment"]');send('Could I have an extension until Friday?');
 click('[data-action="hta-candidate"]');send('Could you please give me an extension until Friday?');
 const own=active().messages.filter(m=>m.kind==='correction'&&m.category==='Significado / datos').at(-1);
 click('[data-action="accept"][data-id="'+own.id+'"]');
 check(active().draft===beforeData.replace('Could I have an extension until Friday?',own.after),'La alternativa propia cambia solo el rango conservado');
 // Una consulta gramatical conserva el origen sin inventar una acepción léxica.
 last('[data-action="hta-consult"]');send('Could you please give me an extension until Friday?');
 click('[data-action="hta-doubt"][data-kind="grammar"]');
 check(active().task==='email'&&active().hta.returns.length===1,'Consulta gramatical mantiene su punto de retorno');
 last('[data-action="hta-resource"][data-resource="person"]');last('[data-action="hta-resource-compare"]');send('La construcción sigue siendo una petición y la fecha no cambia.');
 click('[data-action="hta-return"]');check(lastText().includes('La construcción sigue siendo'),'El retorno gramatical devuelve la explicación, no otro borrador');
 // Una orden explícita se atiende aunque hubiera una producción pendiente.
 click('[data-action="write"]');send('¿Qué significa dedicated en “She is a dedicated teacher”?');
 check(active().task==='vocab'&&active().hta.returns.length===1,'Pregunta de significado interrumpe de forma recuperable una producción');
 send('No puedo inferir todavía.');
 check(active().evidence.at(-1).kind==='Punto de partida sin hipótesis','No poder inferir no se transforma en una hipótesis inventada');
 last('[data-action="hta-lexical-tools"]');last('[data-action="hta-infer"]');send('Ahora comprendo que describe a una persona comprometida.');
 check(active().evidence.at(-1).kind==='Interpretación después del contraste','No reconstruye una hipótesis inicial después de consultar');
 send('volver al correo');check(active().task==='email'&&active().pending.type==='draft','La orden de retorno conserva la tarea pendiente');
 check(document.documentElement.scrollWidth<=innerWidth,'Sin desbordamiento horizontal');
 dump('LINGUA_HTA_PASS '+checks.length+' '+JSON.stringify([...covered].sort())+'\n');
} catch(e) {dump('LINGUA_HTA_FAIL '+e.message+' '+e.stack+'\n');}
'''


def run():
    catalog=json.loads((BASE/'docs/hta-v8-coverage.json').read_text())
    expected=set(catalog['scenario_node_ids'])
    assert expected<={row['id'] for row in catalog['nodes']}
    snapshot=None
    for width,height in [(1440,1000),(390,844),(320,740)]:
        log=capture(SCRIPT,Path(tempfile.gettempdir())/f'lingua-hta-complete-{width}.png',width,height)
        line=next((line for line in log.splitlines() if line.startswith('LINGUA_HTA_PASS ')),None)
        failure=next((line for line in log.splitlines() if line.startswith('LINGUA_HTA_FAIL ')),None)
        print(width,line.split(' [')[0] if line else failure or log[-2000:],flush=True)
        assert line, failure or log[-3000:]
        found=set(json.loads(line[line.index('['):]))
        assert expected<=found, f'Nodos sin prueba: {sorted(expected-found)}'
        assert 'JavaScript error:' not in log,log[-2000:]
        snapshot_line=next(line for line in log.splitlines() if line.startswith('HTA_SNAPSHOT '))
        snapshot=json.loads(snapshot_line[len('HTA_SNAPSHOT '):])
    # Recarga real del estado intermedio de una consulta vinculada en otro perfil de navegador.
    before='localStorage.setItem("lingua-tutor-v2",'+json.dumps(json.dumps(snapshot))+');'
    script=r'''
try {
 const click=q=>document.querySelector(q).click();
 const check=(ok,t)=>{if(!ok)throw Error(t);};
 const prior=JSON.parse(localStorage.getItem('lingua-tutor-v2'));
 const session=prior.sessions.find(s=>s.hta.returns.length),frame=session.hta.returns.at(-1);
 click('[data-action="history"]');click('[data-action="resume"][data-id="'+session.id+'"]');
 check(document.querySelector('#context-return').textContent.includes('Volver al correo'),'Retorno sigue disponible tras recargar');
 check([...document.querySelectorAll('.recall-hidden')].every(e=>getComputedStyle(e).display==='none'),'No muestra primero la definición al retomar');
 click('[data-action="hta-return"]');
 const state=Lingua.getState(),s=state.sessions.find(s=>s.id===state.active);
 check(s.draft===frame.draft&&s.pending.type===frame.pending.type,'Borrador y actividad pendientes se conservan');
 check(document.querySelector('#chat-input').value===frame.inputDraft,'Mensaje sin enviar se conserva');
 check(s.hta.returns.length===0,'Retorno consumido una vez');
 dump('LINGUA_HTA_RELOAD_PASS\n');
} catch(e){dump('LINGUA_HTA_RELOAD_FAIL '+e.message+'\n');}
'''
    log=capture(script,Path(tempfile.gettempdir())/'lingua-hta-reload.png',before_script=before)
    print('\n'.join(line for line in log.splitlines() if line.startswith('LINGUA_HTA_RELOAD_')),flush=True)
    assert 'LINGUA_HTA_RELOAD_PASS' in log,log[-2000:]


if __name__=='__main__':run()
