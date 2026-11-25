"""Verifica catálogo, evidencias y selectores de la app cargada, sin código histórico."""
from pathlib import Path
import re,json,tempfile
from build_guides import BASE,get_rows,APPLIED
from browser_capture import capture

def static_checks():
    md=(BASE/'GUIA_PRINCIPIOS_IHC.md').read_text()
    html=(BASE/'GUIA_PRINCIPIOS_IHC.html').read_text()
    rows=get_rows()
    expected={f'C{c}.{i}' for c,n in enumerate([3,8,9,7,10,12,11,11],1) for i in range(1,n+1)}
    assert {r['id'] for r in rows}==expected
    assert len(re.findall(r'^#### C[1-8]\.\d+ ',md,re.M))==71
    assert all(f'id="{code}"' in html for code in expected)
    assert len(APPLIED)==44
    assert all(r['status']=='Aplicado' for r in rows if r['baseline']=='Cumple')
    for rel in re.findall(r'\]\((docs/screenshots/actual/[^)]+)\)',md):
        assert (BASE/rel).is_file(),rel
    for rel in re.findall(r'(?:src|href)="((?:js|css)/[^\"]+)"',(BASE/'index.html').read_text()):
        assert (BASE/rel).is_file(),rel
    print('71 reglas presentes; 44 aplicaciones originales conservadas; archivos actuales referenciados existen.',flush=True)
    return rows

def browser_checks(rows):
    selectors=sorted({r['selector'] for r in rows})
    script='const selectors='+json.dumps(selectors)+';'+r'''
const seen=new Set();
const scan=()=>selectors.forEach(s=>{if(document.querySelector(s))seen.add(s);});
const click=q=>{const e=document.querySelector(q);if(!e)throw Error(q);e.click();scan();};
const send=t=>{const e=document.querySelector('#chat-input');e.value=t;e.dispatchEvent(new Event('input',{bubbles:true}));scan();click('#send-btn');};
try{
 Lingua.reset();scan();
 send(TutorData.examples.email);click('[data-action="compare"]');click('[data-action="new"]');
 send(TutorData.examples.review);
 click('[data-action="accept"]');
 click('[data-action="undo-correction"]');
 click('[data-action="notebook"]');click('[data-action="close-dialog"]');
 click('[data-action="stage"][data-stage="2"]');
 scan();
 click('[data-action="new"]');send(TutorData.examples.vocab);
 send('Reservado para una función, por la pista space.');scan();
 click('[data-action="save-word"]');click('[data-action="reading"]');
 click('[data-action="history"]');
 const missing=selectors.filter(s=>!seen.has(s));
 if(missing.length)throw Error('Selectores sin evidencia: '+missing.join(', '));
 for(const el of document.querySelectorAll('[aria-controls]'))for(const target of el.getAttribute('aria-controls').split(' '))if(!document.getElementById(target))throw Error('aria-controls inexistente: '+target);
 dump('LINGUA_GUIDE_PASS '+seen.size+' selectores reales\n');
}catch(e){dump('LINGUA_GUIDE_FAIL '+e.message+' '+e.stack+'\n');}
'''
    log=capture(script,Path(tempfile.gettempdir())/'lingua-guide-check.png')
    lines=[l for l in log.splitlines() if 'LINGUA_GUIDE_' in l]
    print('\n'.join(lines),flush=True)
    assert any('LINGUA_GUIDE_PASS' in l for l in lines),log[-3000:]

if __name__=='__main__':browser_checks(static_checks())
