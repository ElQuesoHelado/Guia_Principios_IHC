"""Prueba real del flujo en Firefox, sin bibliotecas Python adicionales."""
from pathlib import Path
from browser_capture import capture
import tempfile

SCRIPT = r'''
const results = [];
const check = (ok, name) => { if (!ok) throw Error(name); results.push(name); };
const click = (selector) => { const el = document.querySelector(selector); if (!el) throw Error('Falta '+selector); el.click(); };
const field = (key, value) => { const el = document.querySelector('[data-learning-field="'+key+'"]'); el.value = value; el.dispatchEvent(new Event('input', {bubbles:true})); };
try {
    check(document.querySelectorAll('#mode-nav [data-mode]').length === 3, 'Tres tareas principales');
    check(!document.querySelector('#learning-title') && document.querySelector('[data-doc]'), 'Acceso directo al correo sin actividad obligatoria');
    click('[data-action="correction-accept"][data-id="c1"]');
    click('[data-action="set-version"][data-version="original"]');
    check(document.querySelector('[data-doc]').textContent.includes('I am agree'), 'Original conservado tras aceptar');
    click('[data-action="set-version"][data-version="final"]');
    check(document.querySelector('[data-doc]').textContent.includes('I agree') && !document.querySelector('[data-doc]').textContent.includes('I am agree'), 'Versión actual incorpora solo cambios aceptados');
    click('[data-action="open-changes-view"]');
    click('[data-action="correction-undo"][data-id="c1"]');
    click('[data-action="open-learning-examples"]');
    check(document.querySelector('.learning-card details').open, 'Ejemplos accesibles sin requisitos');
    click('[data-action="toggle-learning"]');
    check(!document.querySelector('#learning-title') && document.querySelector('[data-doc]'), 'Ocultar apoyo conserva el correo');
    click('[data-action="toggle-learning"]');
    click('[data-action="learning-save"]');
    check(DemoState.get().completedStages.writing.length === 0, 'No completa sin evidencias');
    field('structure', 'Saludo, contexto, petición y cierre');field('purpose', 'Solicitar una prórroga a mi profesora');
    click('[data-action="learning-save"]');
    check(DemoState.get().completedStages.writing.includes(0), 'Guarda notas opcionales');
    field('purpose', 'Pedir prórroga hasta el viernes');
    check(!DemoState.get().completedStages.writing.includes(0), 'Editar requiere registrar de nuevo');
    click('[data-action="learning-save"]');
    click('[data-action="set-stage"][data-stage="1"]');
    check(!DemoState.get().completedStages.writing.includes(1), 'Navegar no acredita aprendizaje');
    field('draft', 'Dear Professor, Could you please give me more time?');field('doubt', 'Quiero añadir una fecha');
    document.querySelectorAll('.learning-check input').forEach(el => {el.checked=true;el.dispatchEvent(new Event('change',{bubbles:true}));});
    click('[data-action="learning-save"]');
    check(DemoState.get().completedStages.writing.includes(1), 'Borrador con autoevaluación');
    click('[data-action="set-mode"][data-mode="lessons"]');
    check(!document.querySelector('#learn-topic') && document.querySelector('.reading-card'), 'Lectura directa sin formulario obligatorio');
    click('[data-action="toggle-learning"]');
    field('topic','Trabajo remoto');field('inference','Dedicated: reservado para una función');
    click('[data-action="select-word"][data-word="dedicated"]');
    check(document.querySelector('.inline-word-detail').textContent.includes('reservado'), 'Significado contextual visible');
    click('[data-action="save-word"][data-word="dedicated"]');
    check(DemoState.get().savedWords.includes('dedicated'), 'Vocabulario se conserva');
    click('[data-action="set-mode"][data-mode="writing"]');
    check(DemoState.get().activeStage===1 && document.querySelector('#learn-draft').value.includes('Dear Professor'), 'Borrador y etapa conservados');
    click('[data-action="set-stage"][data-stage="2"]');
    click('[data-action="correction-accept"][data-id="c1"]');
    check(DemoState.get().statuses.c1==='accepted', 'Cambio localizado aceptado');
    click('[data-action="open-changes-view"]');
    click('[data-action="correction-undo"][data-id="c1"]');
    check(DemoState.get().statuses.c1==='pending', 'Decisión reversible');
    click('[data-action="set-stage"][data-stage="3"]');
    check(document.querySelector('#learn-transfer') && document.querySelector('.correction-card') && document.querySelector('[data-action="set-version"][data-version="original"]'), 'Cambios y original accesibles desde cualquier sugerencia');
    field('transfer','Dear Gallery, Could you please send me more information?');field('reflection','Aprendí a pedir de forma cortés');
    click('[data-action="learning-save"]');
    click('[data-action="open-progress-view"]');
    check(document.querySelector('#aside-content').textContent.includes('no acredita dominio'), 'Progreso diferencia actividad y dominio');
    click('[data-action="set-mode"][data-mode="conversation"]');
    click('[data-action="select-scenario"][data-scenario="cafe"]');
    check(DemoState.get().scenario==='cafe', 'Control del escenario escrito');
    click('[data-action="next-prompt"]');
    check(DemoState.get().messages.conversation.length===2, 'Turnos controlados por estudiante');
    click('[data-action="set-mode"][data-mode="lessons"]');
    check(document.querySelector('#learn-topic').value==='Trabajo remoto', 'Notas de lectura conservadas');
    click('[data-action="set-stage"][data-stage="3"]');
    field('transfer','A dedicated workspace helps me.');
    click('[data-action="learning-save"]');
    check(DemoState.get().completedStages.lessons.includes(3), 'Guarda una nota parcial sin exigir todos los campos');
    click('[data-action="set-stage"][data-stage="0"]');
    check(document.querySelector('#learn-topic').value==='Trabajo remoto', 'Retrocede sin perder notas');
    check(document.documentElement.scrollWidth <= window.innerWidth, 'Sin desbordamiento horizontal');
    dump('LINGUA_TEST_PASS '+results.length+'\n');
    document.body.innerHTML='<main style="padding:32px;color:#135c36;background:white;font:20px sans-serif"><h1>Verificación completada</h1>'+results.map(r=>'<p>✓ '+r+'</p>').join('')+'</main>';
} catch(e) {
    dump('LINGUA_TEST_FAIL '+e.stack+'\n');
    document.body.innerHTML='<pre style="background:white;color:red;font-size:24px">'+e.stack+'</pre>';
}
'''
if __name__ == '__main__':
    for width, height in [(1440,1000),(390,844)]:
        output=Path(tempfile.gettempdir()) / f'lingua-tests-{width}.png'
        log=capture(SCRIPT,output,width,height)
        lines=[line for line in log.splitlines() if 'LINGUA_TEST_' in line]
        print(width, '\n'.join(lines), output)
        assert any('LINGUA_TEST_PASS' in line for line in lines), log[-3000:]
