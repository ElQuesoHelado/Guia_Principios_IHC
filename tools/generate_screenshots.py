"""Genera evidencias actuales por selector real, sin coordenadas fijas de versiones previas."""
from pathlib import Path
import json
import subprocess
import tempfile
import sys
from browser_capture import BASE, capture

DOCS_DIR = BASE / 'docs/screenshots'
CAPTURE_SPECS = [
 ('01_header_nav.png', '', '.app-header'),
 ('02_stagebar.png', '', '#stagebar'),
 ('03_correction_card.png', '', '.correction-card'),
 ('04_type_badges.png', '', '.correction-card .badge-row'),
 ('05_help_levels.png', '', '#help-levels'),
 ('06_side_criteria.png', '', '#side-panel'),
 ('07_side_progress.png', "DemoState.set({tab:'progress'});", '#side-panel'),
 ('08_side_rules.png', "DemoState.set({tab:'rules',detailsLevel:1});", '#side-panel'),
 ('09_lessons_reading.png', "DemoState.set({mode:'lessons',activeStage:1,tab:'vocabulary',selectedWord:'productive'});", '.reading-card'),
 ('10_conversation_chat.png', "DemoState.set({mode:'conversation',activeStage:1,tab:'vocabulary'});", '.chat-context-note'),
 ('11_drawer_menu.png', "DemoState.set({historyOpen:true});", '#history-drawer'),
 ('12_history_drawer.png', "DemoState.set({historyOpen:true});", '#history-drawer'),
 ('13_modal_rule.png', "document.querySelector('[data-action=\"correction-rule\"]')?.click();", '#modal'),
 ('14_composer_hints.png', '', '.composer'),
]

def main():
 DOCS_DIR.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='lingua-captures-') as tmp:
  for name,code,selector in CAPTURE_SPECS:
   if sys.argv[1:] and name not in sys.argv[1:]: continue
   setup="DemoState.set({homeOpen:false,activeStage:2,detailsLevel:3,tab:'criteria'});"
   setup+=code
   setup+=f'''const el=document.querySelector({json.dumps(selector)});
   if (!el) throw Error('Selector de captura ausente');
   el.scrollIntoView({{block:'center'}});
   const r=el.getBoundingClientRect();
   dump('LINGUA_BOX '+JSON.stringify([Math.max(0,Math.floor(r.x)),Math.max(0,Math.floor(r.y)),Math.min(Math.ceil(r.width),1440),Math.min(Math.ceil(r.height),1000)])+'\\n');'''
   raw=Path(tmp)/'raw.png'
   log=capture(setup,raw)
   bounds=next((json.loads(line.split('LINGUA_BOX ')[1]) for line in log.splitlines() if line.startswith('LINGUA_BOX ')),None)
   if bounds is None:raise RuntimeError('No se obtuvo selector: '+selector+' '+log[-500:])
   x,y,w,h=bounds;w=min(w,1440-x);h=min(h,1000-y)
   subprocess.run(['magick',str(raw),'-crop',f'{w}x{h}+{x}+{y}','+repage',str(DOCS_DIR/name)],check=True)
   print('Actualizada',name,flush=True)
if __name__=='__main__':main()
