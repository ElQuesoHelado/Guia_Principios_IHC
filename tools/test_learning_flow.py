"""Regresión de tareas y control del estudiante en Firefox real, sin dependencias."""
from pathlib import Path
from browser_capture import capture
import tempfile

SCRIPT = r'''
const results=[];
const check=(ok,name)=>{if(!ok)throw Error(name);results.push(name);};
const click=(selector)=>{const el=document.querySelector(selector);if(!el)throw Error('Falta '+selector);check(!el.disabled,'Control habilitado: '+selector);el.click();};
const last=(selector)=>{const els=document.querySelectorAll(selector);if(!els.length)throw Error('Falta '+selector);els[els.length-1].click();};
const type=(text)=>{const el=document.querySelector('#chat-input');el.value=text;el.dispatchEvent(new Event('input',{bubbles:true}));};
const send=(text)=>{type(text);click('#send-btn');};
const active=()=>{const st=Lingua.getState();return st.sessions.find(s=>s.id===st.active);};
const fits=()=>check(document.documentElement.scrollWidth<=innerWidth,'Sin desbordamiento horizontal');
try{
  Lingua.reset();
  check(!document.querySelector('form')&&document.querySelectorAll('textarea').length===1,'Un chat, sin fichas ni formularios por tarea');
  check(!document.querySelector('#welcome').hidden&&document.querySelector('#conversation').hidden,'Inicio vacío');
  check(Lingua.detect('¿Qué significa deadline en un correo?')==='vocab','Prioriza la duda de significado');
  check(Lingua.detect('Revisa el tono de este correo con deadline')==='email','Prioriza la revisión del correo');
  type('Quiero escribir un correo');
  check(!document.querySelector('#prompt-assist').hidden,'Sugerencia mientras escribe');
  check(document.querySelector('#prompt-assist').textContent.includes('destinatario'),'Sugerencia deriva de la relación');
  const before=document.querySelector('#chat-input').value;
  click('[data-action="dismiss-prompt"]');
  check(document.querySelector('#chat-input').value===before,'Descartar conserva la consulta');
  type('Quiero aprender a escribir un correo a mi profesora');
  click('[data-action="use-prompt"]');
  check(document.querySelector('#chat-input').value.includes('Compara dos formas'),'Acepta sugerencia sin enviar');
  check(Lingua.getState().sessions.length===0,'Añadir sugerencia no envía mensajes');
  click('[data-action="undo-prompt"]');
  check(document.querySelector('#chat-input').value==='Quiero aprender a escribir un correo a mi profesora','Sugerencia reversible');
  click('[data-action="edit-prompt"]');type(document.querySelector('#chat-input').value+' Quiero una explicación breve.');
  check(document.querySelector('#chat-input').value.endsWith('breve.'),'Sugerencia editable');
  click('#send-btn');
  check(active().task==='email','Clasifica y guarda en correo');
  check(active().evidence.length===0,'Enviar solicitud no acredita conocimiento');
  click('[data-action="compare"]');
  check(document.querySelector('.comparison').textContent.includes('Could you please'),'Misma intención, relación diferente');
  send('Could suaviza la petición a la profesora; con mi compañero hay más confianza.');
  check(active().evidence.some(e=>e.kind.includes('Justificación')),'Guarda explicación propia');
  click('[data-action="write"]');
  const original='Dear Professor,\nI want you to send me the notes.\nI am agree with the deadline.\nBest regards,\nAlex';
  send(original);click('[data-action="review"]');
  const corrections=()=>active().messages.filter(m=>m.kind==='correction');
  check(corrections().length===2,'Revisa solo construcciones conocidas del borrador');
  check(new Set(corrections().map(m=>m.category)).size===2,'Distingue gramática de elección de tono');
  const grammar=corrections().find(m=>m.category==='Gramática');
  click('[data-action="accept"][data-id="'+grammar.id+'"]');
  check(active().draft===original.replace('I am agree','I agree'),'Cambio exclusivamente en el fragmento');
  click('[data-action="undo-correction"][data-id="'+grammar.id+'"]');
  check(active().draft===original,'Deshacer recupera exactamente el texto');
  const tone=corrections().find(m=>m.category==='Tono');
  click('[data-action="reject"][data-id="'+tone.id+'"]');
  check(active().draft===original,'Rechazar no modifica la producción');
  click('[data-action="versions"]');
  check(document.querySelector('#workspace-dialog').open,'Versiones en panel accesible');
  const originalVersion=active().versions[0].id;
  click('[data-action="restore"][data-id="'+originalVersion+'"]');
  check(active().versions.length===4&&active().draft===original,'Recuperar conserva el historial');
  click('[data-action="close-dialog"]');
  check(document.querySelector('.correction-card').textContent.includes('versión anterior'),'No presenta sugerencias antiguas como aplicadas al texto recuperado');
  click('[data-action="notebook"]');click('[data-action="close-dialog"]');
  click('[data-action="change-task"]');check(!document.querySelector('#task-choice').hidden,'Ubicación corregible por el estudiante');
  document.querySelector('#task-choice').hidden=true;
  click('[data-action="stage"][data-stage="2"]');
  check(active().recall&&document.querySelector('.comparison').closest('.message').getAttribute('aria-hidden')==='true','Recuperación oculta material anterior y su lectura accesible');
  check([...document.querySelectorAll('.recall-hidden')].every(el=>getComputedStyle(el).display==='none'),'Oculta también mensajes e hipótesis propios anteriores');
  send('Could I have more time? Elijo un tono cortés para la profesora.');
  check(active().evidence.at(-1).kind==='Intento de recuperación'&&!active().evidence.at(-1).help,'Registra producción con material oculto sin calificar');
  click('[data-action="transfer"]');send('Hi Sam, can you send me the notes? Uso un tono más cercano con mi compañero.');
  check(active().evidence.at(-1).kind==='Producción en otra situación','Transferencia con otro destinatario');
  const emailId=active().id;
  type('Una duda sin enviar');click('[data-action="new"]');
  send('Quiero mejorar mi inglés');
  check(active().task==='general','No adivina tareas con contexto insuficiente');
  click('[data-action="assign"][data-task="vocab"]');
  check(active().task==='vocab','Elección explícita organiza el chat');
  click('[data-action="new"]');
  send(TutorData.examples.vocab);
  check(active().task==='vocab'&&active().pending.type==='inference','Vocabulario empieza con hipótesis opcional');
  check(!document.querySelector('.word-detail'),'No revela definición antes del contraste');
  send('Creo que significa reservado para trabajar, porque habla de space y focus.');
  check(document.querySelector('.word-detail').textContent.includes('Tu interpretación inicial'),'Conserva hipótesis junto a acepción');
  click('[data-action="save-word"]');check(active().words.includes('dedicated'),'Guarda palabra para otro momento');
  click('[data-action="save-word"]');check(active().words.length===0,'Guardado de palabra reversible');
  click('[data-action="save-word"]');
  click('[data-action="vocab-explain"]');send('En este caso dedicado a una función; no comprometido como una persona.');
  click('[data-action="recall"]');
  check(document.querySelector('#recall-banner').hidden===false,'Modo sin definición visible');
  click('[data-action="reveal-support"]');send('I have a dedicated desk for my homework.');
  check(active().evidence.at(-1).help===true,'Distingue consulta de apoyo durante el intento');
  click('[data-action="transfer"]');send('Hi Sam, we have a dedicated room for our project. Aquí es un lugar reservado.');
  const vocabId=active().id;
  click('[data-action="notebook"]');
  check(document.querySelector('#dialog-content').textContent.includes('no acredita dominio'),'Resumen no atribuye dominio');
  click('[data-action="repaso"]');
  check(active().recall&&active().word==='dedicated','Repaso retoma palabra guardada sin definición');
  send('Dedicated: reservado para una finalidad. A dedicated room for our project.');
  click('[data-action="notebook"]');click('[data-action="finish"]');
  check(active().closed&&document.querySelector('.finish-summary'),'Cierre explícito sin aprobar automáticamente');
  click('[data-action="reflection"]');send('Quiero comprobar otras acepciones en un diccionario.');
  check(active().evidence.at(-1).kind==='Duda para retomar','Continuidad de aprendizaje');
  click('[data-action="history"]');
  check(document.querySelectorAll('.history-group').length===3,'Orden estable de categorías');
  fits();
  click('[data-action="resume"][data-id="'+emailId+'"]');
  check(active().draft===original&&document.querySelector('#chat-input').value==='Una duda sin enviar','Retoma texto y mensaje pendiente por conversación');
  check(active().evidence.some(e=>e.kind==='Producción en otra situación'),'Retoma evidencias');
  const stored=JSON.parse(localStorage.getItem('lingua-tutor-v1'));
  check(stored.sessions.some(s=>s.id===vocabId&&s.words.includes('dedicated')),'Persistencia real de palabras y sesiones');
  click('[data-action="new"]');send('¿Qué significa dedicated en “She is a dedicated teacher”?');
  check(!document.querySelector('.word-detail')&&active().pending.type==='custom-inference','No asigna acepción de espacio a un contexto propio');
  send('Creo que describe a alguien comprometido.');
  click('[data-action="pick-word"][data-word="productive"]');
  click('[data-action="definition"]');
  check(document.querySelector('.word-detail').textContent.includes('productive'),'Permite saltar la hipótesis y consultar directamente');
  click('[data-action="new"]');send('<img src=x onerror="window.injected=true"> Quiero un correo');
  check(!window.injected&&!document.querySelector('#chat-messages img'),'Escapa el texto del usuario');
  type('Prueba');
  document.querySelector('#chat-input').dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',shiftKey:true,bubbles:true}));
  check(document.querySelector('#chat-input').value==='Prueba','Shift Enter no envía');
  document.querySelector('#chat-input').dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',isComposing:true,bubbles:true}));
  check(document.querySelector('#chat-input').value==='Prueba','No envía composición de teclado');
  fits();
  dump('LINGUA_TEST_PASS '+results.length+'\n');
}catch(e){dump('LINGUA_TEST_FAIL '+e.message+' '+e.stack+'\n');document.body.innerHTML='<pre style="white-space:pre-wrap;color:red">'+e.message+' '+e.stack+'</pre>';}
'''
if __name__=='__main__':
    for width,height in [(1440,1000),(390,844),(320,740)]:
        output=Path(tempfile.gettempdir())/f'lingua-tests-{width}.png'
        log=capture(SCRIPT,output,width,height)
        lines=[line for line in log.splitlines() if 'LINGUA_TEST_' in line]
        print(width,'\n'.join(lines),flush=True)
        assert any('LINGUA_TEST_PASS' in line for line in lines),log[-4000:]
