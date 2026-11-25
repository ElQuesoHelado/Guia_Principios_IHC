"""Evidencias de la interfaz vigente en Firefox. Ejecutar sin otras capturas en paralelo."""
from pathlib import Path
from browser_capture import BASE, capture
import sys,json,subprocess

OUT=BASE/'docs/screenshots/actual'
SETUP=r'''
Lingua.reset();
const click=q=>document.querySelector(q).click();
const type=t=>{const e=document.querySelector('#chat-input');e.value=t;e.dispatchEvent(new Event('input',{bubbles:true}));};
const send=t=>{type(t);click('#send-btn');};
'''
VOCAB="send(TutorData.examples.vocab);send('Creo que significa reservado para trabajar, porque habla de space y focus.');"
SPECS=[
 ('01_inicio.png','',1440,1000),
 ('02_sugerencia.png',"type('Quiero aprender a escribir un correo a mi profesora');",1440,1000),
 ('03_comparar.png',"send(TutorData.examples.email);click('[data-action=compare]');",1440,1000),
 ('04_revision.png',"send(TutorData.examples.review);document.querySelector('.correction-card').scrollIntoView({block:'start'});window.scrollBy(0,-20);",1440,1000),
 ('05_vocabulario.png',VOCAB+"document.querySelector('.word-detail .rule').open=true;document.querySelector('.word-detail').scrollIntoView({block:'center'});",1440,1100),
 ('06_recuperar.png',VOCAB+"click('[data-action=recall]');",1440,1000),
 ('07_aprendizaje.png',VOCAB+"click('[data-action=save-word]');click('[data-action=notebook]');",1440,1000),
 ('08_historial.png',"send(TutorData.examples.email);click('[data-action=new]');"+VOCAB+"click('[data-action=history]');",1440,1000),
 ('09_inicio_movil.png','',390,844),
 ('10_sugerencia_movil.png',"type('Quiero aprender a escribir un correo a mi profesora');",390,844),
]
if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True)
 for name,script,width,height in SPECS:
  if sys.argv[1:] and name not in sys.argv[1:]:continue
  selectors={'03_comparar.png':'.comparison','04_revision.png':'.correction-card','05_vocabulario.png':'.word-detail'}
  crop=selectors.get(name)
  if crop:
   height=3400
   script+='window.scrollTo(0,0);const boxes=[...document.querySelectorAll('+json.dumps(crop)+')].map(e=>e.getBoundingClientRect());const left=Math.min(...boxes.map(b=>b.left)),top=Math.min(...boxes.map(b=>b.top)),right=Math.max(...boxes.map(b=>b.right)),bottom=Math.max(...boxes.map(b=>b.bottom));dump("LINGUA_BOX "+JSON.stringify([Math.floor(left),Math.floor(top),Math.ceil(right-left),Math.ceil(bottom-top)])+"\\n");'
  log=capture(SETUP+script,OUT/name,width,height)
  if crop:
   line=next(l for l in log.splitlines() if l.startswith('LINGUA_BOX '))
   x,y,w,h=json.loads(line.split('LINGUA_BOX ')[1])
   subprocess.run(['magick',str(OUT/name),'-crop',f'{w}x{h}+{x}+{y}','+repage',str(OUT/name)],check=True)
  assert 'JavaScript error:' not in log,log[-2000:]
  print('Captura actual:',name,flush=True)
