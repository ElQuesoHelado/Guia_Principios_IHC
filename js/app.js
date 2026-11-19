/* ============================================================
   App · bootstrap, render global y acciones
   Demo mocking · sin backend · prioridad visual
   ============================================================ */
(function () {
    'use strict';

    const D = window.DemoData;
    const S = window.DemoState;
    const I = window.Icons;
    const Chat = window.Chat;
    const Panels = window.Panels;

    let modalOpen = false;
    let toastTimer = null;

    const $ = (sel, root = document) => root.querySelector(sel);
    const $$ = (sel, root = document) => Array.prototype.slice.call(root.querySelectorAll(sel));

    const escapeHtml = (str) => String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');

    /* ---------------- Render ---------------- */
    function renderHeader() {
        const st = S.get();
        const historyButton = $('[data-action="toggle-history"]');
        if (historyButton) {
            historyButton.setAttribute('aria-expanded', String(st.historyOpen));
            historyButton.setAttribute('aria-controls', 'history-drawer');
        }
        const pageTitle = $('#page-title');
        if (pageTitle) pageTitle.textContent = st.homeOpen ? 'Dudas rápidas' : `Tutor de inglés · ${D.modes[st.mode].title}`;
        $$('#mode-nav .mode-pill').forEach((btn) => {
            const active = btn.dataset.view === 'quickstart'
                ? st.homeOpen
                : !st.homeOpen && btn.dataset.mode === st.mode;
            btn.classList.toggle('is-active', active);
            if (active) btn.setAttribute('aria-current', 'true');
            else btn.removeAttribute('aria-current');
            btn.setAttribute('aria-pressed', String(active));
            btn.title = btn.dataset.view === 'quickstart'
                ? 'Inicio: escribe una consulta para elegir una actividad'
                : active ? `Actividad actual: ${D.modes[btn.dataset.mode].label}` : `Cambiar a ${D.modes[btn.dataset.mode].label}`;
        });

        const pop = $('#suggestions-popover');
        const btn = $('#suggestions-btn');
        if (pop) {
            pop.hidden = !st.suggestionsOpen;
            if (st.suggestionsOpen) pop.innerHTML = Panels.renderSuggestions();
        }
        if (btn) btn.setAttribute('aria-expanded', String(st.suggestionsOpen));

        const hint = $('#composer-mode-hint');
        if (hint) hint.textContent = D.modes[st.mode].modeHint;
        const input = $('#chat-input');
        if (input) input.placeholder = D.modes[st.mode].placeholder;
    }

    function renderStagebar() {
        const st = S.get();
        const mode = D.modes[st.mode];
        // El control superior abre directamente el progreso del modo activo.
        const detailAction = 'open-progress-view';
        const detailLabel = 'Ver progreso';
        const stages = mode.stages.map((label, index) => {
            const done = (st.completedStages[st.mode] || []).includes(index);
            const state = index === st.activeStage ? 'is-active' : done ? 'is-done' : '';
            return `
                <button class="stage ${state}" data-action="set-stage" data-stage="${index}">
                    <span class="stage-dot">${done ? I.check(13) : index + 1}</span>
                    <span>${label}</span>
                </button>
                ${index < mode.stages.length - 1 ? '<span class="stage-line" aria-hidden="true"></span>' : ''}
            `;
        }).join('');

        const el = $('#stagebar');
        if (!el) return;
        el.innerHTML = `
            <div class="stages" aria-label="Etapas de la tarea">${stages}</div>
            <div class="stage-actions">
                <button class="details-toggle" data-action="${detailAction}">${detailLabel}</button>
                <button class="mobile-support-toggle" data-action="open-mobile-support" aria-controls="side-panel" aria-expanded="${Boolean(st.supportOpen)}">${I.book(14)} Apoyo</button>
            </div>
        `;
    }

    function renderHelpLevels() {
        const st = S.get();
        const levels = [
            { id: 'pista', label: 'Pista' },
            { id: 'explicacion', label: 'Explicación' },
            { id: 'ejemplo', label: 'Ejemplo' },
            { id: 'reescritura', label: 'Reescritura completa' }
        ];
        const el = $('#help-levels');
        if (!el) return;
        el.innerHTML = `
            <span class="help-label">Nivel de ayuda</span>
            ${levels.map((l) => `<button class="help-pill ${st.help === l.id ? 'is-active' : ''}" data-action="set-help" data-help="${l.id}" aria-pressed="${st.help === l.id}">${l.label}</button>`).join('')}
        `;
    }


    function renderHistory() {
        const st = S.get();
        const drawer = $('#history-drawer');
        const overlay = $('#history-overlay');
        if (!drawer || !overlay) return;
        drawer.hidden = !st.historyOpen;
        overlay.hidden = !st.historyOpen;
        if (st.historyOpen) drawer.innerHTML = Panels.renderHistoryDrawer();
    }

    function renderQuickstart() {
        const feedback = $('#quickstart-feedback');
        const input = $('#quickstart-input');
        const st = S.get();
        if (feedback) {
            feedback.textContent = st.quickstartFeedback;
            feedback.hidden = !st.quickstartFeedback;
        }
        if (input && input.value !== st.quickstartDraft) input.value = st.quickstartDraft || '';
    }

    function renderAside() {
        const tabs = $('#aside-tabs');
        const content = $('#aside-content');
        if (tabs) tabs.innerHTML = Panels.renderTabs();
        if (content) content.innerHTML = Panels.renderAsideContent();
    }

    function renderAll() {
        const st = S.get();
        const detailLevel = st.detailsLevel;
        document.body.classList.toggle('quickstart-mode', Boolean(st.homeOpen));
        document.body.classList.toggle('learner-mode', detailLevel === 0);
        document.body.classList.toggle('overview-mode', detailLevel === 1);
        document.body.classList.toggle('research-menu-mode', detailLevel === 2);
        document.body.classList.toggle('research-mode', detailLevel >= 3);
        document.body.classList.toggle('mobile-support-open', Boolean(st.supportOpen));
        const supportOverlay = $('#mobile-support-overlay');
        if (supportOverlay) supportOverlay.hidden = !st.supportOpen;
        renderHeader();
        renderQuickstart();
        renderStagebar();
        const supportToggle = $('.mobile-support-toggle');
        if (supportToggle) supportToggle.setAttribute('aria-expanded', String(Boolean(st.supportOpen)));
        renderHelpLevels();
        renderHistory();
        renderAside();
        Chat.render();
    }

    /* ---------------- Toast / modal ---------------- */
    function toast(message) {
        const el = $('#toast');
        if (!el) return;
        el.textContent = message;
        el.hidden = false;
        el.classList.add('is-visible');
        window.clearTimeout(toastTimer);
        toastTimer = window.setTimeout(() => {
            el.classList.remove('is-visible');
            window.setTimeout(() => { el.hidden = true; }, 220);
        }, 2600);
        const live = $('#live-region');
        if (live) live.textContent = message;
    }

    function openModal(title, body, eyebrow) {
        const overlay = $('#modal-overlay');
        const modal = $('#modal');
        if (!overlay || !modal) return;
        modal.innerHTML = `
            <div class="modal-head">
                <div>
                    ${eyebrow ? `<p class="modal-eyebrow">${eyebrow}</p>` : ''}
                    <h3 id="modal-title">${title}</h3>
                </div>
                <button class="icon-btn" data-action="modal-close" aria-label="Cerrar">${I.close(18)}</button>
            </div>
            ${body}
        `;
        overlay.hidden = false;
        modalOpen = true;
        const closeBtn = $('[data-action="modal-close"]', modal);
        if (closeBtn) closeBtn.focus();
    }

    function closeModal() {
        const overlay = $('#modal-overlay');
        if (overlay) overlay.hidden = true;
        modalOpen = false;
    }

    /* ---------------- Acciones ---------------- */
    function setCorrection(id, status) {
        const st = S.get();
        const statuses = Object.assign({}, st.statuses, { [id]: status });
        const patch = { statuses, version: 'final' };
        S.set(patch);
        toast(status === 'accepted' ? 'Corrección aceptada · la reescritura se actualizó.' : status === 'rejected' ? 'Corrección rechazada · se mantiene tu versión.' : 'Corrección devuelta a pendiente.');
    }

    function openRule(id) {
        const rule = D.rules.find((r) => r.id === id);
        if (!rule) return;
        openModal(rule.title, `
            <div class="modal-body">
                <div class="badge-row"><span class="type-badge ${rule.kind}">${rule.label}</span></div>
                <p class="modal-text">${rule.body}</p>
                <div class="rule-example good"><span>Correcto</span>${rule.good}</div>
                <div class="rule-example bad"><span>Evitar</span>${rule.bad}</div>
                <div class="modal-note">${I.info(14)} La regla se muestra en lenguaje simple para que puedas decidir, no solo aceptar.</div>
                <div class="modal-actions">
                    <button class="btn btn-primary" data-action="modal-close">Entendido</button>
                    <button class="btn" data-action="open-synonyms">${I.search(14)} Buscar sinónimos</button>
                </div>
            </div>
        `, 'Regla y ejemplo');
    }

    function openVersionHistory() {
        const st = S.get();
        const rows = st.versionHistory.map((version) => `
            <div class="version-history-row ${st.version === version.id ? 'is-active' : ''}">
                <div class="version-history-copy">
                    <strong>${version.label}</strong>
                    <span>${version.time}</span>
                    <p>${version.detail}</p>
                </div>
                <button class="btn ${st.version === version.id ? 'btn-ghost' : ''}" data-action="reuse-version" data-version="${version.id}">${st.version === version.id ? 'En uso' : 'Reutilizar'}</button>
            </div>
        `).join('');
        openModal('Versiones del texto', `
            <div class="modal-body">
                <p class="modal-text">Retoma una versión sin borrar la actual. La vista principal se actualizará solo cuando elijas una opción.</p>
                <div class="version-history-list">${rows}</div>
                <div class="modal-actions"><button class="btn" data-action="modal-close">Cerrar</button></div>
            </div>
        `, 'Acompañamiento de escritura');
    }

    function openRefineResponse(index) {
        const options = [
            'Más formal',
            'Más sencillo',
            'Más conciso',
            'Ampliar idea',
            'Enfatizar lo importante',
            'Personalizar'
        ];
        openModal('Refinar respuesta', `
            <div class="modal-body">
                <p class="modal-text">Elige un ajuste para esta respuesta. No necesitas volver a redactar el prompt.</p>
                <div class="refine-options">
                    ${options.map((option) => `<button class="refine-option" data-action="apply-refinement" data-index="${index}" data-refine="${option}">${option}</button>`).join('')}
                </div>
                <div class="modal-actions"><button class="btn" data-action="modal-close">Cancelar</button></div>
            </div>
        `, 'Refinamiento rápido');
    }

    function applyRefinement(index, option) {
        const st = S.get();
        const message = st.messages[st.mode] && st.messages[st.mode][Number(index)];
        if (!message || message.role !== 'ai') return;
        message.refinement = option;
        closeModal();
        S.set({});
        toast(`Ajuste aplicado: ${option}.`);
    }

    function openSynonyms() {
        const groups = [
            { word: 'important', options: ['relevant', 'crucial', 'significant', 'demanding'] },
            { word: 'agree', options: ['accept', 'concur', 'be okay with'] },
            { word: 'help', options: ['support', 'assistance', 'guidance'] }
        ];
        openModal('Buscar sinónimos', `
            <div class="modal-body">
                <p class="modal-text">Elige una alternativa y añádela a tus criterios. La IA comprobará si encaja con el tono formal.</p>
                <div class="stack">
                    ${groups.map((g) => `
                        <div class="synonym-group">
                            <strong>${g.word}</strong>
                            <div class="chip-row">${g.options.map((o) => `<button class="chip" data-action="pick-synonym" data-word="${o}">${o}</button>`).join('')}</div>
                        </div>`).join('')}
                </div>
                <div class="modal-actions"><button class="btn" data-action="modal-close">Cerrar</button></div>
            </div>
        `, 'Sinónimos y alternativas');
    }

    function openLessonHint(word) {
        const w = D.article.words.find((x) => x.word === word);
        if (!w) return;
        openModal(w.word, `
            <div class="modal-body">
                <p class="modal-text"><b>Significado en el artículo:</b> ${w.meaning}</p>
                <div class="rule-example good"><span>En contexto</span>${w.example}</div>
                <p class="modal-text"><b>Cómo se usa:</b> ${w.use}</p>
                <div class="word-examples-modal">
                    <strong>Otros ejemplos para comparar</strong>
                    ${(w.examples || []).map((example) => `<div class="word-example-line">“${example}”</div>`).join('')}
                </div>
                <div class="modal-actions">
                    <button class="btn btn-primary" data-action="save-word" data-word="${w.word}">${I.plus(14)} Guardar palabra</button>
                    <button class="btn" data-action="modal-close">Cerrar</button>
                </div>
            </div>
        `, 'Vocabulario en contexto');
    }

    function openReadingModal() {
        const st = S.get();
        openModal('Usar mi lectura', `
            <div class="modal-body">
                <p class="modal-text">Pega el texto que estás leyendo y escribe la palabra que quieres entender.</p>
                <label for="custom-reading-input">Lectura</label>
                <textarea id="custom-reading-input" class="custom-reading-input" rows="8" placeholder="Pega aquí tu lectura">${escapeHtml(st.customReading || '')}</textarea>
                <label for="custom-reading-word">Palabra que quiero consultar</label>
                <input id="custom-reading-word" class="custom-reading-word" value="${escapeHtml(st.customWord || '')}" placeholder="Ej.: dedicated">
                <div class="modal-actions">
                    <button class="btn btn-primary" data-action="save-custom-reading">Usar esta lectura</button>
                    <button class="btn" data-action="modal-close">Cancelar</button>
                </div>
            </div>
        `, 'Lectura y vocabulario');
    }

    function classifyQuickPrompt(text) {
        const q = String(text || '').toLocaleLowerCase('es').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        if (/entrevista|conversacion|dialogo|practicar hablar|responder en ingles|speak|interview/.test(q)) return 'conversation';
        if (/vocabulario|palabra|significa|significado|lectura|leer|articulo|dedicated|productive|flexibility/.test(q)) return 'lessons';
        if (/redact|revis|corrig|correo|email|gramatica|tono|ensayo|frase|oracion|formal/.test(q)) return 'writing';
        return null;
    }

    function submitQuickPrompt(prompt) {
        const clean = String(prompt || '').trim();
        if (!clean) return;
        const target = classifyQuickPrompt(clean);
        if (!target) {
            S.set({ quickstartDraft: clean, quickstartFeedback: 'No identifiqué la actividad. Elige Redacción, Lecciones y repaso o Conversación; también puedes precisar tu consulta.' });
            return;
        }
        switchMode(target);
        S.set({ quickstartDraft: '', quickstartFeedback: '' });
        Chat.send(clean);
    }

    function nextPrompt() {
        const st = S.get();
        const scenario = D.scenarios.find((s) => s.id === st.scenario);
        const idx = ((st.promptIndex || 0) + 1) % scenario.prompts.length;
        st.promptIndex = idx;
        st.messages.conversation.push({
            role: 'ai',
            label: 'Tutor · conversación escrita',
            text: scenario.prompts[idx],
            chips: [{ icon: 'lightbulb', text: 'Pista: responde con una razón', kind: 'info' }]
        });
        S.set({});
        Chat.scrollToBottom();
    }

    function saveWord(word) {
        const st = S.get();
        if (!st.savedWords.includes(word)) {
            S.set({ savedWords: st.savedWords.concat(word) });
            toast(`“${word}” guardada para repaso.`);
        } else {
            toast(`“${word}” ya estaba guardada.`);
        }
    }

    function removeWord(word) {
        const st = S.get();
        if (!st.savedWords.includes(word)) return;
        S.set({ savedWords: st.savedWords.filter((saved) => saved !== word) });
        toast(`“${word}” quitada de palabras guardadas.`);
    }


    function saveCriteria() {
        const st = S.get();
        const inputs = $$('[data-criterion]');
        const updated = st.criteria.map((c) => {
            const input = inputs.find((i) => i.dataset.criterion === c.id);
            return Object.assign({}, c, { value: input ? input.value : c.value });
        });
        const changed = updated.some((c, i) => c.value !== st.criteria[i].value);
        if (!changed) { toast('No hay cambios en los criterios.'); return; }
        S.set({ criteria: updated, sideOpen: false });
        toast('Criterios guardados · la revisión queda lista para continuar.');
    }

    function switchMode(mode) {
        if (!D.modes[mode]) return;
        const m = D.modes[mode];
        const defaultAsideTab = {
            writing: 'criteria',
            conversation: 'vocabulary',
            lessons: 'vocabulary'
        }[mode] || m.tabs[0].id;
        S.set({
            mode,
            homeOpen: false,
            quickstartFeedback: '',
            quickstartDraft: '',
            activeStage: m.activeStage,
            tab: defaultAsideTab,
            supportOpen: false,
            suggestionsOpen: false,
            detailsLevel: 0,
            sideOpen: false,
            sideAnswer: null,
            typing: false
        });
        const input = $('#chat-input');
        if (input) input.value = '';
        Chat.scrollToTop();
    }

    /* ---------------- Delegación de eventos ---------------- */
    function handleAction(action, el) {
        const st = S.get();

        switch (action) {
            case 'open-quickstart': S.set({ homeOpen: true, quickstartFeedback: '', supportOpen: false, historyOpen: false }); break;
            case 'toggle-history': S.set({ historyOpen: !st.historyOpen, supportOpen: false }); break;
            case 'close-history': S.set({ historyOpen: false }); break;
            case 'open-mobile-support': S.set({ supportOpen: true, historyOpen: false }); break;
            case 'close-mobile-support': S.set({ supportOpen: false }); break;
            case 'toggle-suggestions': S.set({ suggestionsOpen: !st.suggestionsOpen }); break;
            case 'advance-details': {
                const next = st.detailsLevel === 0 ? 1 : st.detailsLevel === 1 ? 2 : st.detailsLevel === 2 ? 0 : 2;
                S.set({ detailsLevel: next, tab: next === 0 ? D.modes[st.mode].tabs[0].id : st.tab });
                break;
            }
            case 'open-progress-view': S.set({ detailsLevel: 0, tab: 'progress', supportOpen: true, historyOpen: false }); break;
            case 'open-changes-view': S.set({ detailsLevel: 0, tab: 'changes', supportOpen: true, historyOpen: false }); break;
            case 'open-aside-tools': S.set({ detailsLevel: 2 }); break;
            case 'open-detail-tab': {
                S.set({ detailsLevel: 3, tab: el.dataset.tab });
                break;
            }
            case 'set-mode': {
                switchMode(el.dataset.mode);
                S.set({ historyMode: el.dataset.mode });
                break;
            }
            case 'set-tab': S.set({ tab: el.dataset.tab }); break;
            case 'open-tab': S.set({ tab: el.dataset.tab }); break;
            case 'set-version': S.set({ version: el.dataset.version }); break;
            case 'set-help': {
                const help = el.dataset.help;
                S.set({ help, version: help === 'reescritura' ? 'suggested' : st.version === 'suggested' ? 'draft' : st.version });
                break;
            }
            case 'set-stage': {
                const index = Number(el.dataset.stage);
                const stages = D.modes[st.mode].stages;
                const completedStages = Object.assign({}, st.completedStages);
                const completed = new Set(completedStages[st.mode] || []);
                if (index > st.activeStage) completed.add(st.activeStage);
                if (index === st.activeStage && index === stages.length - 1) completed.add(index);
                completedStages[st.mode] = Array.from(completed).sort((a, b) => a - b);
                S.set({ activeStage: index, completedStages });
                const allDone = stages.every((_, i) => completed.has(i));
                const missing = stages.filter((_, i) => !completed.has(i)).length;
                if (allDone) toast(`Actividad terminada: ${D.modes[st.mode].label}. Tus cambios siguen disponibles en el panel de apoyo.`);
                else if (index === stages.length - 1) toast(`Etapa ${stages[index]} seleccionada. Quedan ${missing} etapa${missing === 1 ? '' : 's'} por completar.`);
                else toast(`Etapa: ${stages[index]}.`);
                break;
            }
            case 'scroll-sessions': {
                const track = $('#session-track');
                if (track) track.scrollBy({ left: Number(el.dataset.dir) * 260, behavior: 'smooth' });
                break;
            }
            case 'select-session': {
                const sessions = st.sessions.map((s) => Object.assign({}, s, { active: s.id === el.dataset.session }));
                const selected = st.sessions.find((s) => s.id === el.dataset.session);
                S.set({ sessions, historyOpen: false, historyMode: selected ? selected.mode : st.historyMode });
                if (selected && selected.mode) switchMode(selected.mode);
                toast('Sesión cargada.');
                break;
            }
            case 'select-scenario': {
                const scenario = D.scenarios.find((s) => s.id === el.dataset.scenario);
                const messages = st.messages.conversation.slice(0, 1).map((m) => Object.assign({}, m, { text: scenario.prompts[0] }));
                S.set({ scenario: el.dataset.scenario, messages: Object.assign({}, st.messages, { conversation: messages }), promptIndex: 0 });
                toast(`Escenario: ${scenario.name}.`);
                break;
            }
            case 'next-prompt': nextPrompt(); break;
            case 'select-word': S.set({ selectedWord: el.dataset.word }); break;
            case 'save-word': saveWord(el.dataset.word); break;
            case 'hint-word': openLessonHint(st.selectedWord || 'productive'); break;
            case 'open-word-examples': openLessonHint(el.dataset.word || st.selectedWord || 'productive'); break;
            case 'open-reading-modal': openReadingModal(); break;
            case 'save-custom-reading': {
                const reading = ($('#custom-reading-input')?.value || '').trim();
                const word = ($('#custom-reading-word')?.value || '').trim();
                if (!reading || !word) { toast('Pega la lectura y escribe una palabra para continuar.'); break; }
                S.set({ customReading: reading, customWord: word, selectedWord: null, tab: 'vocabulary' });
                closeModal();
                toast(`Lectura cargada. Ahora puedes consultar “${word}”.`);
                break;
            }
            case 'ask-about-reading': {
                const word = st.customWord || el.dataset.word || '';
                Chat.send(`En la lectura que pegué, ¿qué significa “${word}”? Dame dos ejemplos en inglés y explícame cuándo se usa.`);
                break;
            }
            case 'submit-quick-prompt': submitQuickPrompt($('#quickstart-input')?.value || ''); break;
            case 'focus-composer': {
                const input = $('#chat-input');
                if (input) input.focus();
                break;
            }
            case 'quick-question': Chat.send(el.dataset.text); break;

            /* Correcciones */
            case 'correction-accept': setCorrection(el.dataset.id, 'accepted'); break;
            case 'correction-reject': setCorrection(el.dataset.id, 'rejected'); break;
            case 'correction-undo': setCorrection(el.dataset.id, 'pending'); break;
            case 'correction-explain': S.set({ help: 'explicacion', version: st.version === 'suggested' ? 'draft' : st.version }); break;
            case 'correction-rule': {
                const c = D.corrections.find((x) => x.id === el.dataset.id);
                if (c) openRule(c.ruleId);
                break;
            }
            case 'correction-confused': {
                const c = D.corrections.find((x) => x.id === el.dataset.id);
                S.set({ help: 'explicacion', version: st.version === 'suggested' ? 'draft' : st.version });
                toast('Te muestro la explicación paso a paso.');
                const card = document.querySelector(`[data-card="${c ? c.id : ''}"]`);
                if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                break;
            }
            case 'correction-ask': {
                const c = D.corrections.find((x) => x.id === el.dataset.id);
                S.set({ sideOpen: true, sidePrefill: c ? `¿Por qué “${c.before}” → “${c.after}”?` : '' });
                break;
            }
            /* Plan / criterios */
            case 'edit-plan': S.set({ tab: 'plan' }); break;
            case 'open-criteria': S.set({ tab: 'criteria' }); break;
            case 'save-criteria': saveCriteria(); break;
            case 'discard-criteria': renderAside(); toast('Cambios descartados.'); break;
            case 'add-criterion': {
                const criteria = st.criteria.concat({ id: `custom-${st.criteria.length}`, icon: 'tag', label: 'Supuesto nuevo', value: 'Escribe un criterio' });
                S.set({ criteria });
                break;
            }
            case 'regenerate-plan': toast('El plan de esta demostración no se regenera automáticamente. Puedes editar sus pasos aquí.'); break;
            case 'open-vocabulary': S.set({ tab: 'vocabulary' }); break;
            case 'remove-word': removeWord(el.dataset.word); break;

            /* Paneles / modales */
            case 'open-version-history': openVersionHistory(); break;
            case 'reuse-version': {
                S.set({ version: el.dataset.version });
                closeModal();
                toast('Versión retomada. Puedes continuar desde este punto.');
                break;
            }
            case 'open-refine-response': openRefineResponse(el.dataset.index); break;
            case 'apply-refinement': applyRefinement(el.dataset.index, el.dataset.refine); break;
            case 'open-synonyms': openSynonyms(); break;
            case 'open-rule': openRule(el.dataset.id); break;
            case 'modal-close': closeModal(); break;
            case 'pick-synonym': closeModal(); toast(`Alternativa seleccionada: “${el.dataset.word}”.`); break;

            /* Side query */
            case 'close-side-query': S.set({ sideOpen: false, sideAnswer: null }); break;
            case 'side-example': S.set({ sidePrefill: el.dataset.text }); {
                const input = $('#side-input');
                if (input) { input.value = el.dataset.text; input.focus(); }
                break;
            }
            case 'side-add-criterion': {
                const criteria = st.criteria.concat({ id: `side-${st.criteria.length}`, icon: 'message', label: 'Desde consulta lateral', value: st.sidePrefill || 'Supuesto añadido' });
                S.set({ criteria });
                toast('Añadido a criterios · consulta lateral.');
                break;
            }
            case 'side-insert': toast('La inserción automática no está disponible en esta demostración.'); break;

            default: {
                if (action.indexOf('open-rule-') === 0) openRule(action.replace('open-rule-', ''));
                else if (action.indexOf('save-word-') === 0) saveWord(action.replace('save-word-', ''));
                else if (action === 'create-exercise') {
                    st.messages[st.mode].push({ role: 'ai', label: 'TUTOR IA · EJERCICIO', text: 'Completa: “I ______ (agree) with the deadline.” Escribe tu respuesta y te doy feedback.', chips: [] });
                    S.set({});
                }
                break;
            }
        }
    }

    /* ---------------- Eventos ---------------- */
    function bindEvents() {
        document.addEventListener('click', (e) => {
            const el = e.target.closest('[data-action]');
            if (el) {
                e.preventDefault();
                handleAction(el.dataset.action, el);
                return;
            }
            if (modalOpen && !e.target.closest('.modal')) closeModal();
        });

        document.addEventListener('change', (e) => {
            const planCheck = e.target.closest('[data-plan-check]');
            if (planCheck) {
                const st = S.get();
                const plan = st.plan.map((p) => p.id === planCheck.dataset.planCheck ? Object.assign({}, p, { done: planCheck.checked }) : p);
                S.set({ plan });
                return;
            }
            const planText = e.target.closest('[data-plan]');
            if (planText) {
                const st = S.get();
                const plan = st.plan.map((p) => p.id === planText.dataset.plan ? Object.assign({}, p, { text: planText.value }) : p);
                S.set({ plan });
            }
        });

        const form = $('#chat-form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const input = $('#chat-input');
                if (!input) return;
                const text = input.value;
                if (!text.trim()) return;
                input.value = '';
                input.style.height = '44px';
                Chat.send(text);
            });
        }

        const quickstartForm = $('#quickstart-form');
        if (quickstartForm) {
            quickstartForm.addEventListener('submit', (e) => {
                e.preventDefault();
                submitQuickPrompt($('#quickstart-input')?.value || '');
            });
        }

        const input = $('#chat-input');
        if (input) {
            input.addEventListener('input', () => {
                input.style.height = 'auto';
                input.style.height = Math.min(input.scrollHeight, 96) + 'px';
            });
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    const formEl = $('#chat-form');
                    if (formEl) formEl.dispatchEvent(new Event('submit', { cancelable: true }));
                }
            });
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                if (modalOpen) closeModal();
                else if (S.get().historyOpen) S.set({ historyOpen: false });
                else if (S.get().supportOpen) S.set({ supportOpen: false });
                else if (S.get().sideOpen) S.set({ sideOpen: false, sideAnswer: null });
                else if (S.get().suggestionsOpen) S.set({ suggestionsOpen: false });
            }
        });

        document.addEventListener('mouseover', (e) => {
            const node = e.target.closest('.graph-node[data-corr]');
            $$('.correction-card').forEach((card) => card.classList.remove('is-highlighted'));
            if (node) {
                const card = document.querySelector(`[data-card="${node.dataset.corr}"]`);
                if (card) card.classList.add('is-highlighted');
            }
        });
    }

    /* ---------------- Init ---------------- */
    document.addEventListener('DOMContentLoaded', () => {
        S.subscribe(renderAll);
        bindEvents();
        renderAll();
    });
})();
