"""Comprueba geometría real al desplazar un chat largo y coherencia de etapas."""
from pathlib import Path
from browser_capture import capture
import tempfile

SCRIPT=r'''
const results=[];
const check=(ok,name)=>{if(!ok)throw Error(name);results.push(name);};
const click=q=>{const el=document.querySelector(q);if(!el)throw Error('Falta '+q);el.click();};
const send=t=>{const e=document.querySelector('#chat-input');e.value=t;e.dispatchEvent(new Event('input',{bubbles:true}));click('#send-btn');};
const active=()=>{const st=Lingua.getState();return st.sessions.find(s=>s.id===st.active);};
const visible=q=>{const e=document.querySelector(q),r=e.getBoundingClientRect();return r.top>=-1&&r.bottom<=innerHeight+1&&r.left>=-1&&r.right<=innerWidth+1&&getComputedStyle(e).display!=='none';};
const reachable=q=>{const e=document.querySelector(q),r=e.getBoundingClientRect();return visible(q)&&document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)?.closest('button,summary')===e;};
const stage=i=>{
 check(active().stage===i,'Etapa del estado: '+i);
 check(document.querySelector('#stage-position').textContent===`Etapa ${i+1} de 4 · ${TutorData.stages[active().task][i]}`,'Ubicación visible corresponde a actividad: '+i);
 check(document.querySelectorAll('[aria-current="step"]').length===1&&document.querySelector('[aria-current="step"]').dataset.stage===String(i),'Una única etapa actual: '+i);
};
try{
 Lingua.reset();
 check(document.querySelector('#conversation').hidden,'Inicio conserva chat vacío');
 send(TutorData.examples.review);stage(1);
 for(let i=0;i<14;i++)send('Nota de práctica '+i+': quiero comparar mi intención con el efecto de la petición. '.repeat(5));
 check(document.documentElement.scrollHeight>innerHeight*3,'Chat largo reproduce desplazamiento');
 for(const scroll of [0,document.documentElement.scrollHeight/2,document.documentElement.scrollHeight]){
  window.scrollTo(0,scroll);
  const header=document.querySelector('.app-header').getBoundingClientRect();
  const nav=document.querySelector('.task-navigation').getBoundingClientRect();
  check(Math.abs(header.top)<1,'Cabecera visible al desplazar '+scroll);
  check(nav.top>=header.bottom-1,'Etapas por debajo de cabecera '+scroll);
  check(reachable('[data-action="history"]'),'Menú accesible al desplazar '+scroll);
  check(reachable('[data-action="new"]'),'Nuevo chat accesible al desplazar '+scroll);
  check(reachable('#notebook-button'),'Aprendizaje accesible al desplazar '+scroll);
  check(reachable('#learning-plan summary'),'Etapa y desplegable accesibles al desplazar '+scroll);
 }
 click('[data-action="history"]');
 const drawer=document.querySelector('#workspace-dialog');
 check(drawer.open,'Menú abre al final del chat');
 const bounds=drawer.getBoundingClientRect();
 check(Math.abs(bounds.left)<1&&Math.abs(bounds.top)<1,'Conversaciones se ancla al lado izquierdo');
 check(Math.abs(bounds.height-innerHeight)<2,'Panel lateral ocupa el alto de la ventana');
 check(bounds.right<innerWidth&&bounds.width<=360,'Panel lateral conserva espacio junto al chat');
 check(document.activeElement.closest('#workspace-dialog')===drawer,'Foco dentro del panel de conversaciones');
 click('[data-action="close-dialog"]');
 check(document.querySelector('[data-action="history"]').getAttribute('aria-expanded')==='false','Cerrar restaura el estado del menú');
 click('#notebook-button');
 check(!drawer.classList.contains('conversation-drawer'),'Las notas conservan su presentación independiente');
 click('[data-action="close-dialog"]');
 click('#learning-plan summary');
 check(document.querySelector('#learning-plan').open,'Ruta opcional se despliega desde el final');
 const route=document.querySelector('.route-content').getBoundingClientRect();
 check(route.height<=innerHeight*.35+1,'Ruta desplegada acotada en altura');
 check(route.top>=document.querySelector('.app-header').getBoundingClientRect().bottom,'Ruta no tapa cabecera');
 check(document.documentElement.scrollWidth<=innerWidth,'Ruta sin desbordamiento horizontal');
 const count=active().evidence.length;
 click('[data-action="stage"][data-stage="2"]');stage(2);
 check(active().recall,'Recuperar activa intento sin modelo');
 click('[data-action="stage"][data-stage="0"]');stage(0);
 check(!active().recall&&document.querySelector('#recall-banner').hidden,'Volver a comprender sale de recuperación');
 check(!document.querySelector('.recall-hidden'),'Comparación ya no deja materiales ocultos');
 check(active().evidence.length===count,'Visitar etapas no registra una producción');
 click('[data-action="write"]');stage(1);
 click('[data-action="model"]');stage(0);
 click('[data-action="review"]');stage(1);
 click('[data-action="stage"][data-stage="3"]');stage(3);
 click('[data-action="stage"][data-stage="1"]');stage(1);
 check(!active().recall&&active().pending.type==='draft','Volver a escribir sustituye la actividad pendiente');
 click('[data-action="new"]');send(TutorData.examples.vocab);stage(0);
 send('Creo que es un espacio reservado por la pista focus.');stage(1);
 click('[data-action="recall"]');stage(2);
 click('[data-action="stage"][data-stage="1"]');stage(1);
 check(!active().recall&&!active().pending,'Contrastar deja de pedir recuperación');
 click('[data-action="stage"][data-stage="3"]');stage(3);
 click('[data-action="reading"]');stage(0);
 check(!active().recall,'Lectura vuelve a inferencia y muestra el contexto');
 click('[data-action="pick-word"][data-word="productive"]');stage(0);
 click('[data-action="definition"]');stage(1);
 const vocabId=active().id;
 click('[data-action="new"]');send(TutorData.examples.email);stage(0);
 click('[data-action="history"]');click('[data-action="resume"][data-id="'+vocabId+'"]');stage(1);
 check(active().task==='vocab','Retoma la etapa de su conversación');
 check(document.documentElement.scrollWidth<=innerWidth,'Sin desbordamiento horizontal');
 click('[data-action="new"]');send('Quiero escribir un correo a mi profesora');click('[data-action="write"]');
 send('Dear Professor,\nA dedicated space helps you focus on your work.\nBest regards,\nAlex');
 click('[data-action="hta-consult"]');send('A dedicated space helps you focus on your work.');
 for(let i=0;i<8;i++)send('Aporte de continuación '+i+': por ahora quiero contrastar mi interpretación. '.repeat(4));
 window.scrollTo(0,document.documentElement.scrollHeight);
 check(reachable('#context-return [data-action="hta-return"]'),'Retorno de consulta accesible al final del chat');
 check(reachable('[data-action="history"]'),'Menú sigue accesible con franja de retorno');
 check(document.documentElement.scrollWidth<=innerWidth,'Consulta vinculada sin desbordamiento horizontal');
 dump('LINGUA_NAV_PASS '+results.length+'\n');
}catch(e){dump('LINGUA_NAV_FAIL '+e.message+' '+e.stack+'\n');}
'''
if __name__=='__main__':
 for width,height in [(1440,1000),(390,844),(320,740)]:
  path=Path(tempfile.gettempdir())/f'lingua-navigation-{width}.png'
  log=capture(SCRIPT,path,width,height)
  lines=[l for l in log.splitlines() if 'LINGUA_NAV_' in l]
  print(width,'\n'.join(lines),flush=True)
  assert any('LINGUA_NAV_PASS' in l for l in lines),log[-3000:]
