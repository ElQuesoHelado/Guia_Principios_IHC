/* Actividades de construcción de conocimiento. Evidencias locales, sin evaluación automática. */
(function () {
    'use strict';
    const S = window.DemoState;
    const esc = (v) => String(v || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    const tasks = {
        writing: {
            goal: 'Aprender a organizar un correo formal, justificar tus decisiones y usar las expresiones en una nueva situación.',
            steps: [
                { title: 'Prepara tu correo', prompt: 'Compara “Give me more time” y “Could you please give me more time?”. ¿Cuál usarías con una docente?', model: 'Subject: Request for a meeting\nDear Professor Ramos,\nI am a student in your English course. Could we arrange a meeting on Friday to discuss my project?\nThank you for your time.\nBest regards,\nAlex', fields: [['structure', '¿Qué hace que el modelo sea una petición cortés?']] },
                { title: 'Escribe tu correo', prompt: 'Pide una prórroga para entregar un ensayo. Este texto es tuyo; las correcciones de abajo pertenecen al correo de ejemplo.', fields: [['draft', 'Mi correo · escritura libre, sin corrección automática']] },
                { title: 'Revisa un cambio', prompt: 'Compara una sugerencia con el correo de práctica. Decide si la conservarías y explica por qué.', fields: [['reason', 'Explica una decisión que tomaste en las correcciones']] },
                { title: 'Prueba con otro correo', prompt: 'Escribe a una galería para pedir información sobre una exposición. Usa una petición cortés.', fields: [['transfer', 'Nuevo correo en inglés'], ['reflection', '¿Qué expresión reutilizaste?']] }
            ]
        },
        conversation: {
            goal: 'Aprender a responder, pedir aclaraciones y reformular ideas en una conversación escrita.',
            steps: [
                { title: 'Prepara una respuesta', prompt: 'Elige un escenario. Para pedir una aclaración puedes usar “Could you clarify what you mean?”.', fields: [] },
                { title: 'Responde en el chat', prompt: 'Responde en inglés. Si necesitas ayuda, pide una pista en el chat.', fields: [] },
                { title: 'Mejora una respuesta', prompt: 'Mejora una respuesta de tu conversación. Los ejemplos del tutor no califican tu inglés.', fields: [['revision', 'Una versión mejorada y qué cambiaste']] },
                { title: 'Prueba otro diálogo', prompt: 'Escribe un diálogo con una compañera: preséntate, pregunta por su proyecto y pide una aclaración.', fields: [['transfer', 'Escribe un diálogo breve en inglés.'], ['reflection', '¿Qué expresión pudiste reutilizar?']] }
            ]
        },
        lessons: {
            goal: 'Inferir el significado de palabras en contexto y recuperarlas en una producción propia.',
            steps: [
                { title: 'Lee y elige una palabra', prompt: 'Lee el artículo e intenta deducir una palabra antes de consultar su significado.', fields: [['inference', 'Antes de consultar: palabra y significado que imaginas']] },
                { title: 'Comprueba el significado', prompt: 'Elige una palabra de la lista y compara su significado con lo que imaginabas.', fields: [] },
                { title: 'Guarda una palabra', prompt: 'Selecciona una palabra y pulsa “Guardar palabra” para repasarla después.', fields: [] },
                { title: 'Usa la palabra', prompt: 'Escribe una oración con la palabra elegida. Después compárala con los ejemplos.', fields: [['transfer', 'Oración propia en inglés'], ['reflection', '¿Usaste la palabra con el mismo significado?']] }
            ]
        }
    };
    // Cada orientación lleva al único lugar donde se realiza la acción.
    const destinations = {
        writing: [
            { target: 'criteria', label: 'Ver criterios del correo' },
            { target: 'practice', label: 'Escribir mi correo' },
            { target: 'corrections', label: 'Ir a las correcciones del ejemplo' },
            { target: 'practice', label: 'Escribir otro correo' }
        ],
        conversation: [
            { target: 'scenario', label: 'Elegir escenario' },
            { target: 'chat', label: 'Responder en el chat' },
            { target: 'practice', label: 'Revisar una respuesta propia' },
            { target: 'practice', label: 'Escribir otro diálogo' }
        ],
        lessons: [
            { target: 'practice', label: 'Anotar el significado que imagino' },
            { target: 'words', label: 'Explorar palabras de la lectura' },
            { target: 'words', label: 'Elegir una palabra para guardar' },
            { target: 'practice', label: 'Escribir una oración propia' }
        ]
    };
    function actionButton(destination) {
        return `<button class="btn" data-action="learning-go" data-target="${destination.target}">${destination.label}</button>`;
    }
    function render() {
        const st = S.get();
        const step = tasks[st.mode].steps[st.activeStage];
        const destination = destinations[st.mode][st.activeStage];
        const values = st.learning[st.mode];
        const done = (st.completedStages[st.mode] || []).includes(st.activeStage);
        const hasFields = step.fields.length > 0;
        if (!st.learningOpen[st.mode]) {
            return `<section class="learning-suggestion" aria-label="Apoyo opcional para aprender">
                ${hasFields ? '<button class="text-btn" data-action="toggle-learning" aria-expanded="false" aria-controls="learning-content">Abrir mis notas opcionales</button>' : actionButton(destination)}
                ${st.mode === 'writing' ? '<button class="text-btn" data-action="open-learning-examples">Ver ejemplos de correo</button>' : ''}
            </section>`;
        }
        const lastReply = st.mode === 'conversation' && st.activeStage === 2
            ? st.messages.conversation.filter(message => message.role === 'user').slice(-1)[0] : null;
        return `<section id="learning-content" class="learning-card" aria-labelledby="learning-title">
            <p class="learning-eyebrow">${hasFields ? 'Notas opcionales' : 'Orientación'} · ${window.DemoData.modes[st.mode].stages[st.activeStage]}</p>
            <div class="learning-actions"><button class="text-btn" data-action="toggle-learning" aria-expanded="true" aria-controls="learning-content">Cerrar apoyo</button></div>
            <h2 id="learning-title">${step.title}</h2>
            <p>${step.prompt}</p>
            ${destination.target !== 'practice' ? actionButton(destination) : ''}
            ${st.mode === 'lessons' && st.activeStage === 2 ? actionButton({ target: 'saved', label: 'Ver palabras guardadas' }) : ''}
            ${step.model ? `<details><summary>Ver modelo de correo</summary><pre class="learning-model" lang="en">${step.model}</pre></details>` : ''}
            ${st.mode === 'conversation' && st.activeStage === 2 ? (lastReply
                ? `<div class="learning-source"><strong>Tu última respuesta</strong><p>${esc(lastReply.text)}</p></div>`
                : '<p>Responde primero en el chat para tener un ejemplo propio.</p>') : ''}
            ${step.fields.map(([key, label]) => `<label class="learning-field" for="learn-${key}">${label}<textarea id="learn-${key}" data-learning-field="${key}" rows="3">${esc(values[key])}</textarea></label>`).join('')}
            <div class="learning-actions">${hasFields ? '<button class="btn btn-primary" data-action="learning-save">Guardar mis notas</button>' : ''}${st.activeStage < 3 ? `<button class="btn" data-action="set-stage" data-stage="${st.activeStage + 1}">Siguiente etapa</button>` : ''}${hasFields ? `<span id="learning-status" role="status">${done ? 'Notas guardadas en esta sesión.' : 'Notas opcionales · solo en esta sesión.'}</span>` : ''}</div>
        </section>`;
    }
    function capture(el) {
        const st = S.get();
        // No emitir durante la escritura: preserva foco, cursor y selección.
        st.learning[st.mode][el.dataset.learningField] = el.type === 'checkbox' ? el.checked : el.value;
        const completed = st.completedStages[st.mode] || [];
        st.completedStages[st.mode] = completed.filter(i => i !== st.activeStage);
        const status = document.getElementById('learning-status');
        if (status) status.textContent = 'Tienes cambios sin registrar.';
    }
    function save() {
        const st = S.get();
        const step = tasks[st.mode].steps[st.activeStage];
        const values = st.learning[st.mode];
        if (!step.fields.length) return;
        const hasNotes = step.fields.some(([key]) => String(values[key] || '').trim());
        if (!hasNotes) {
            document.getElementById('learning-status').textContent = 'Escribe una nota para guardarla.';
            return;
        }
        const completed = new Set(st.completedStages[st.mode]);
        completed.add(st.activeStage);
        S.set({ completedStages: Object.assign({}, st.completedStages, { [st.mode]: [...completed].sort() }) });
    }
    function evidenceSummary(mode) {
        const values = S.get().learning[mode];
        return `${Object.values(values).filter(v => typeof v === 'string' && v.trim()).length} notas de aprendizaje escritas. Las sugerencias y sus notas son opcionales.`;
    }
    function currentTip() {
        const st = S.get();
        const step = tasks[st.mode].steps[st.activeStage];
        return { title: step.title, text: step.prompt, destination: destinations[st.mode][st.activeStage] };
    }
    window.Learning = { render, capture, save, evidenceSummary, currentTip };
})();
