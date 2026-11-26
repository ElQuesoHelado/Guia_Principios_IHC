/* Actividades de construcción de conocimiento. Evidencias locales, sin evaluación automática. */
(function () {
    'use strict';
    const S = window.DemoState;
    const esc = (v) => String(v || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    const tasks = {
        writing: {
            goal: 'Aprender a organizar un correo formal, justificar tus decisiones y usar las expresiones en una nueva situación.',
            steps: [
                { title: 'Reconoce cómo se construye una petición formal', prompt: 'Compara “Give me more time” con “Could you please give me more time?”. ¿Cuál usarías con una docente y por qué?', model: 'Subject: Request for a meeting\nDear Professor Ramos,\nI am a student in your English course. Could we arrange a meeting on Friday to discuss my project?\nThank you for your time.\nBest regards,\nAlex', fields: [['structure', 'Identifica saludo, contexto, petición y cierre del modelo.'], ['purpose', 'Planifica tu correo: destinatario, solicitud, motivo y fecha.']] },
                { title: 'Escribe y autoevalúa tu primer correo', prompt: 'Pide una prórroga para entregar un ensayo. Conserva tus ideas y escribe con el inglés que ya conoces antes de pedir ayuda.', fields: [['draft', 'Tu borrador en inglés'], ['doubt', '¿Qué frase te genera dudas y cómo intentarías mejorarla?']], checks: [['structureCheck', 'Incluí asunto, saludo, contexto, solicitud, cierre y firma.'], ['meaningCheck', 'Mi petición es clara, cortés e incluye una fecha.']] },
                { title: 'Compara, explica y decide', prompt: 'Las cuatro sugerencias siguientes pertenecen al correo de práctica. Compáralas con tus dudas: aceptar un cambio es una decisión, explicar por qué ayuda a comprenderlo.', fields: [['reason', 'Explica un cambio y su efecto. ¿Qué mantendrías y por qué?'], ['revised', 'Revisa tu propio borrador usando los criterios y las reglas.']] },
                { title: 'Usa lo aprendido con menos ayuda', prompt: 'Ahora escribe a una galería para pedir información sobre una exposición. Cambia destinatario y propósito; usa una petición cortés sin copiar el correo anterior.', fields: [['transfer', 'Nuevo correo en inglés'], ['reflection', 'Anota tres expresiones útiles, un error que evitarás y qué mejoró respecto al primer correo.']] }
            ]
        },
        conversation: {
            goal: 'Aprender a responder, pedir aclaraciones y reformular ideas en una conversación escrita.',
            steps: [
                { title: 'Prepara tus recursos para conversar', prompt: 'Elige un escenario abajo. Observa este intercambio: “Could you clarify what you mean?” → “Of course. Can you give an example of your experience?”. La aclaración permite continuar sin adivinar.', fields: [['goal', '¿Qué quieres practicar y qué vocabulario necesitas?'], ['preparation', 'Prepara una respuesta y una frase para pedir aclaración.']] },
                { title: 'Construye tus respuestas por escrito', prompt: 'Responde en el chat con tus propias ideas. Puedes pedir una pista o una aclaración; tú decides cuándo pasar a la siguiente pregunta.', fields: [['strategy', 'Anota una expresión que hayas usado para aclarar o ampliar una respuesta.']] },
                { title: 'Revisa una respuesta concreta', prompt: 'Relee una respuesta del chat y compárala con tu objetivo. Las respuestas del tutor son ejemplos de apoyo; no califican tu inglés.', fields: [['original', 'Copia una respuesta tuya que quieras mejorar.'], ['revision', 'Reformúlala y explica qué mejora en claridad, vocabulario o estructura.']] },
                { title: 'Transfiere una estrategia', prompt: 'Imagina que hablas por chat con una nueva compañera de clase. Preséntate, pregunta por su proyecto y pide una aclaración.', fields: [['transfer', 'Escribe un diálogo breve en inglés.'], ['reflection', '¿Qué estrategia pudiste reutilizar y qué practicarás después?']] }
            ]
        },
        lessons: {
            goal: 'Inferir el significado de palabras en contexto y recuperarlas en una producción propia.',
            steps: [
                { title: 'Comprende antes de consultar', prompt: 'Lee el artículo de abajo. Identifica el tema general y elige una palabra; intenta inferir su sentido a partir de la oración antes de abrir su significado.', fields: [['topic', '¿De qué trata el artículo?'], ['inference', 'Palabra elegida, oración original e hipótesis de significado.']] },
                { title: 'Contrasta tu hipótesis con ejemplos', prompt: 'Selecciona una palabra en el artículo y consulta su significado y uso. ¿Qué pistas del texto apoyan esa acepción?', fields: [['comparison', 'Compara tu hipótesis con el significado contextual. ¿Qué cambió y por qué?']] },
                { title: 'Registra para recordar', prompt: 'Guarda una palabra con el botón del artículo y completa una nota propia. Guardar una palabra prepara el repaso; comprueba después si puedes usarla.', fields: [['record', 'Palabra, significado en este contexto, oración del artículo y una nota de uso.']] },
                { title: 'Recupera y aplica el vocabulario', prompt: 'Escribe una oración nueva con la palabra que elegiste antes de volver a consultar los ejemplos. Después compara el sentido y el uso.', fields: [['transfer', 'Oración propia en inglés'], ['reflection', '¿Encaja con el significado contextual? ¿Qué estrategia te ayudó y qué necesitas repasar?']] }
            ]
        }
    };
    function render() {
        const st = S.get();
        const task = tasks[st.mode];
        const step = task.steps[st.activeStage];
        const values = st.learning[st.mode];
        const done = (st.completedStages[st.mode] || []).includes(st.activeStage);
        if (!st.learningOpen[st.mode]) {
            return `<section class="learning-suggestion" aria-label="Apoyo opcional para aprender">
                <div><strong>Aprende a tu ritmo</strong><p>Puedes consultar ejemplos, escribir o practicar cuando quieras.</p></div>
                <button class="btn" data-action="toggle-learning" aria-expanded="false" aria-controls="learning-content">Ver sugerencias de aprendizaje</button>
                ${st.mode === 'writing' ? '<button class="text-btn" data-action="open-learning-examples">Ver ejemplos de correo</button>' : ''}
            </section>`;
        }
        return `<section id="learning-content" class="learning-card" aria-labelledby="learning-title">
            <p class="learning-eyebrow">Actividad ${ {writing: 1, conversation: 2, lessons: 3}[st.mode]} · Sugerencia opcional</p>
            <div class="learning-actions"><button class="text-btn" data-action="toggle-learning" aria-expanded="true" aria-controls="learning-content">Ocultar sugerencias</button>${st.mode === 'writing' ? '<button class="text-btn" data-action="open-learning-examples">Volver a los ejemplos de correo</button>' : ''}</div>
            <h2 id="learning-title">${step.title}</h2>
            <p class="learning-goal"><strong>Meta de aprendizaje:</strong> ${task.goal}</p>
            <p>${step.prompt}</p>
            ${step.model ? `<details><summary>Ver modelo de correo</summary><pre class="learning-model" lang="en">${step.model}</pre></details>` : ''}
            ${step.fields.map(([key, label]) => `<label class="learning-field" for="learn-${key}">${label}<textarea id="learn-${key}" data-learning-field="${key}" rows="3">${esc(values[key])}</textarea></label>`).join('')}
            ${(step.checks || []).map(([key, label]) => `<label class="learning-check"><input type="checkbox" data-learning-field="${key}" ${values[key] ? 'checked' : ''}>${label}</label>`).join('')}
            <div class="learning-actions"><button class="btn btn-primary" data-action="learning-save">Guardar mis notas</button>${st.activeStage < 3 ? `<button class="btn" data-action="set-stage" data-stage="${st.activeStage + 1}">Ver otra sugerencia</button>` : ''}<span id="learning-status" role="status">${done ? 'Notas guardadas en esta sesión.' : 'Estas propuestas son opcionales. Puedes saltarlas o volver a ellas sin perder tus notas.'}</span></div>
        </section>`;
    }
    function capture(el) {
        const st = S.get();
        // No emitir durante la escritura: preserva foco, cursor y selección.
        st.learning[st.mode][el.dataset.learningField] = el.type === 'checkbox' ? el.checked : el.value;
        const completed = st.completedStages[st.mode] || [];
        st.completedStages[st.mode] = completed.filter(i => i !== st.activeStage);
        const status = document.getElementById('learning-status');
        if (status) status.textContent = 'Notas modificadas en esta sesión. Puedes guardar lo que quieras conservar.';
    }
    function save() {
        const st = S.get();
        const step = tasks[st.mode].steps[st.activeStage];
        const values = st.learning[st.mode];
        const hasNotes = step.fields.some(([key]) => String(values[key] || '').trim());
        if (!hasNotes) {
            document.getElementById('learning-status').textContent = 'Puedes escribir una nota, consultar otra sugerencia o continuar practicando.';
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
    window.Learning = { render, capture, save, evidenceSummary };
})();
