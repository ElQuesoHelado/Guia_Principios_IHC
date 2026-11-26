"""Integridad del HTA vigente, archivo histórico y compatibilidad de contextos v1."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import tempfile
from browser_capture import BASE, capture


def documents():
    text = subprocess.check_output(['pdftotext', '-layout', str(BASE/'HTA_correo_vocabulario_v8.pdf'), '-']).decode()
    nodes = set(re.findall(r'^\s*([CV]\d+(?:\.\d+)*)\s', text, re.M))
    parents = {node.rsplit('.', 1)[0] for node in nodes if '.' in node} | {'C0', 'V0'}
    plans = set(re.findall(r'^\s*Plan\s+([CV]\d+(?:\.\d+)*)\b', text, re.M))
    assert len(parents) == 29 and parents == plans, (parents-plans, plans-parents)
    assert 'C4.1' in text and 'V4.4' in text and 'C4.3' in text
    assert not re.search(r'conversación escrita|Tarea 2\.', text, re.I)
    archive = BASE/'docs/originales/previo-v8'
    entries = json.loads((archive/'manifest.json').read_text())
    assert len(entries) == 11
    for entry in entries:
        assert hashlib.sha256((archive/entry['archivo']).read_bytes()).hexdigest() == entry['sha256'], entry['archivo']
    paths = [BASE/name for name in ['README.md','agents.md','usuarios.md','plan.md','reference.md','guia.md','guiaPapers.md','docs/REVISION_HTA_Y_TRAZABILIDAD.md','GUIA_PRINCIPIOS_IHC.md','docs/HTA_V8_COBERTURA.md']]
    for path in paths:
        md = path.read_text()
        assert not re.search(r'conversación escrita|tres actividades|tres tareas|HTA_unificado_sin_IA_v7', md, re.I), path
        for target in re.findall(r'\[[^\]]+\]\((<[^>]+>|[^)\s]+)\)', md):
            target = target.strip('<>').split('#', 1)[0]
            if not target or '://' in target:
                continue
            assert (path.parent/target).exists(), (path, target)
    catalog=json.loads((BASE/'docs/hta-v8-coverage.json').read_text())
    assert {n['id'] for n in catalog['nodes']} == nodes
    assert {n['id'] for n in catalog['nodes'] if n['kind']=='plan'} == plans
    assert catalog['actions']==80
    print('HTA v8: 29 planes completos; 11 originales intactos; alcance y enlaces vigentes coherentes.', flush=True)


def compatibility():
    base = dict(task='vocab', title='Práctica anterior', created='2026-11-24T12:00:00Z', evidence=[], versions=[], words=['deadline'], draft='', inputDraft='Duda sin enviar', stage=0, pending=None, word='deadline', context='The deadline is Friday, so please submit your essay before then.', recall=False, recallStart=0, helpUsed=False, closed=False, promptUses=0, promptDismisses=0, stageEvidence=[])
    old = {**base, 'id':'old-deadline', 'messages':[dict(id='d1',kind='definition',word='deadline',context=base['context'])]}
    unknown = {**base, 'id':'old-unknown', 'word':'dedicated', 'words':[], 'context':'He dedicated the book to his mother.', 'messages':[dict(id='u1',kind='definition',word='dedicated',context='He dedicated the book to his mother.')]}
    state = dict(version=1, sessions=[old, unknown], active=None)
    seed = 'localStorage.setItem("lingua-tutor-v1",'+json.dumps(json.dumps(state))+');'
    script = r'''
try {
 const click=q=>document.querySelector(q).click();
 const check=(ok,name)=>{if(!ok)throw Error(name);};
 click('[data-action="history"]');click('[data-action="resume"][data-id="old-deadline"]');
 check(document.querySelector('#chat-input').value==='Duda sin enviar','Mensaje pendiente anterior');
 check(document.querySelector('.word-detail blockquote').textContent.includes('Friday'),'Oración anterior conservada');
 check(document.querySelector('.word-detail .proposal').textContent.includes('Fecha u hora límite'),'Acepción compatible anterior');
 click('[data-action="notebook"]');click('[data-action="repaso"]');
 check(document.querySelector('#recall-banner').hidden===false,'Repaso anterior sin savedContexts');
 const state=Lingua.getState();
 check(state.sessions.find(s=>s.id==='old-deadline').context.includes('Friday'),'El repaso conserva también la oración de la sesión anterior');
 click('[data-action="history"]');click('[data-action="resume"][data-id="old-unknown"]');
 check(!document.querySelector('.word-detail'),'No renderiza ficha antigua incompatible');
 click('[data-action="stage"][data-stage="1"]');
 check(!document.querySelector('.word-detail'),'La navegación tampoco revela una acepción ajena');
 check(Lingua.getState().sessions.length===2,'No pierde las prácticas anteriores');
 check(JSON.parse(localStorage.getItem('lingua-tutor-v1')).version===1,'Conserva la clave original v1');
 check(JSON.parse(localStorage.getItem('lingua-tutor-v2')).version===2,'Guarda el estado migrado v2');
 dump('LINGUA_COMPAT_PASS\n');
} catch(e) { dump('LINGUA_COMPAT_FAIL '+e.message+'\n'); }
'''
    log = capture(script, Path(tempfile.gettempdir())/'lingua-v8-compatibility.png', before_script=seed)
    print('\n'.join(line for line in log.splitlines() if line.startswith('LINGUA_COMPAT_')), flush=True)
    assert 'LINGUA_COMPAT_PASS' in log, log[-2500:]


if __name__ == '__main__':
    documents()
    compatibility()
