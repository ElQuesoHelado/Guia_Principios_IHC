/* ============================================================
   Panels · tabs de apoyo, historial y sugerencias
   Papers: Gu (workflows), Kazemitabaar (supuestos), LightVA (task flow)
   ============================================================ */
(function () {
    'use strict';

    const D = window.DemoData;
    const S = window.DemoState;
    const I = window.Icons;

    const escapeHtml = (str) => String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');

    const hlClass = { grammar: 'hl-grammar', vocab: 'hl-vocab', tone: 'hl-tone', clarity: 'hl-clarity' };

    const defaultAsideTabs = {
        writing: 'criteria',
        conversation: 'vocabulary',
        lessons: 'vocabulary'
    };

    const duplicateCentralTabs = {
        writing: ['text'],
        conversation: ['scenario'],
        lessons: ['article']
    };

    function supportTabs(modeKey) {
        const hidden = duplicateCentralTabs[modeKey] || [];
        return D.modes[modeKey].tabs.filter((tab) => !hidden.includes(tab.id));
    }

    /* ---------------- Texto de la sesión ---------------- */
    function textWithHighlights(version) {
        const st = S.get();
        let text = D.writingText;

        if (version === 'original') {
            return text.split('\n\n').map((p) => `<p>${escapeHtml(p).replace(/\n/g, '<br>')}</p>`).join('');
        }

        const ordered = D.corrections.slice().sort((a, b) => b.before.length - a.before.length);

        if (version === 'suggested') {
            ordered.forEach((c) => { text = text.split(c.before).join(c.after); });
            return text.split('\n\n').map((p) => `<p>${escapeHtml(p).replace(/\n/g, '<br>')}</p>`).join('');
        }

        if (version === 'final') {
            ordered.forEach((c) => {
                if (st.statuses[c.id] === 'accepted') {
                    text = text.split(c.before).join(c.after);
                }
            });
        }

        ordered.forEach((c) => {
            if (version === 'final' && st.statuses[c.id] === 'accepted') return;
            const cls = hlClass[c.kind];
            const status = st.statuses[c.id];
            text = text.split(c.before).join(
                `<span class="hl ${cls} status-${status}" data-corr="${c.id}" title="${escapeHtml(c.label)}: ${escapeHtml(c.title)}">${escapeHtml(c.before)}</span>`
            );
        });

        return text.split('\n\n').map((p) => `<p>${p.replace(/\n/g, '<br>')}</p>`).join('');
    }

    function legend() {
        return `
            <div class="legend">
                <span><i class="legend-mark grammar"></i>Gramática</span>
                <span><i class="legend-mark vocab"></i>Vocabulario</span>
                <span><i class="legend-mark tone"></i>Tono</span>
                <span><i class="legend-mark clarity"></i>Claridad</span>
            </div>`;
    }

    function renderWritingDraft() {
        const st = S.get();
        const decided = Object.values(st.statuses).filter((status) => status !== 'pending').length;
        const total = D.corrections.length;
        const version = st.version;
        const versions = [
            { id: 'original', label: 'Original' },
            { id: 'draft', label: 'Borrador' },
            { id: 'final', label: 'Versión actual' }
        ];
        if (st.help === 'reescritura') versions.push({ id: 'suggested', label: 'Propuesta completa' });
        const renderedVersion = st.help === 'reescritura' && version === 'draft' ? 'suggested' : version;
        return `
            <section class="writing-draft-preview" aria-label="Texto que se está revisando">
                <div class="writing-draft-head">
                    <div><h3>${renderedVersion === 'suggested' ? 'Reescritura completa propuesta' : 'Correo de práctica'}</h3><p>Ejemplo guiado · las sugerencias solo afectan este texto</p></div>
                    <div class="writing-draft-actions">
                        <button class="text-btn" data-action="open-version-history">Versiones</button>
                        <button class="btn" data-action="open-changes-view">Ver cambios <span>${decided}/${total}</span></button>
                    </div>
                </div>
                <div class="version-tabs" role="group" aria-label="Versiones del texto">
                    ${versions.map((item) => `<button class="version-tab ${renderedVersion === item.id ? 'is-active' : ''}" data-action="set-version" data-version="${item.id}">${item.label}</button>`).join('')}
                </div>
                <div class="text-box" data-doc>${textWithHighlights(renderedVersion)}</div>
                ${renderedVersion === 'suggested' ? '' : legend()}
            </section>
        `;
    }

    /* ---------------- Tabs del aside ---------------- */
    function renderTabs() {
        const st = S.get();
        const mode = D.modes[st.mode];
        const guidedTabs = {
            writing: ['criteria', 'rules', 'plan', 'progress'],
            conversation: ['vocabulary', 'progress'],
            lessons: ['vocabulary', 'progress']
        };
        const allowed = guidedTabs[st.mode] || [mode.tabs[0].id];
        const available = supportTabs(st.mode);
        const defaultTab = defaultAsideTabs[st.mode] || available[0]?.id;
        if (st.detailsLevel === 2) {
            return `<span class="aside-context-label">Recursos de aprendizaje</span><button class="aside-more" data-action="advance-details">Volver al tutor</button>`;
        }
        const tabs = st.detailsLevel === 0
            ? available.filter((tab) => tab.id === defaultTab || (['progress', 'changes'].includes(st.tab) && tab.id === st.tab))
            : st.detailsLevel === 1
                ? available.filter((tab) => allowed.includes(tab.id))
                : available.filter((tab) => tab.id === st.tab);
        return tabs.map((tab) => `
            <button class="aside-tab ${st.tab === tab.id ? 'is-active' : ''}" role="tab" aria-selected="${st.tab === tab.id}" data-action="set-tab" data-tab="${tab.id}">
                ${tab.label}${tab.id === 'changes' ? ` <span class="tab-count">${Object.values(st.statuses).filter((status) => status !== 'pending').length}</span>` : ''}
            </button>
        `).join('') + `<button class="aside-more" data-action="${st.detailsLevel === 3 ? 'open-aside-tools' : 'advance-details'}">${st.detailsLevel === 0 ? 'Más apoyo' : st.detailsLevel === 1 ? 'Más recursos' : 'Más vistas'}</button>`;
    }

    function advancedDescription(id) {
        const descriptions = {
            rules: 'Entender la regla y practicar con un ejemplo.',
            criteria: 'Ajustar lo que quieres lograr con la actividad.',
            plan: 'Revisar los pasos de la tarea.',
            changes: 'Consultar decisiones y comparar versiones.',
            scenario: 'Cambiar el contexto de la conversación.',
            vocabulary: 'Guardar y repasar palabras del contexto.',
            progress: 'Consultar tu avance de aprendizaje.',
            article: 'Leer el texto y explorar palabras.',
            answers: 'Revisar respuestas frecuentes.',
            sources: 'Consultar el origen de una explicación.'
        };
        return descriptions[id] || 'Abrir esta vista de apoyo.';
    }

    function renderAdvancedMenu() {
        const st = S.get();
        const options = supportTabs(st.mode);
        return `
            <div class="panel-head">
                <div><h3>Herramientas disponibles</h3><p>Abre solo la que necesites ahora</p></div>
            </div>
            <div class="advanced-menu-note">Estas vistas ayudan a revisar el proceso, pero no necesitas usarlas todas para aprender.</div>
            <div class="advanced-menu-list">
                ${options.map((tab) => `
                    <button class="advanced-option" data-action="open-detail-tab" data-tab="${tab.id}">
                        <span><strong>${tab.label}</strong><small>${advancedDescription(tab.id)}</small></span>
                        <span aria-hidden="true">${I.arrowRight(14)}</span>
                    </button>
                `).join('')}
            </div>
        `;
    }

    /* ---------------- Contenido por tab ---------------- */
    function renderTextPanel() {
        const st = S.get();
        const versions = [
            { id: 'original', label: 'Original' },
            { id: 'draft', label: 'Borrador' },
            { id: 'final', label: 'Versión final' }
        ];
        return `
            <div class="panel-head">
                <div>
                    <h3>Correo de práctica</h3>
                    <p>Correo · solicitud de prórroga</p>
                </div>
                <div class="panel-head-actions">
                    <button class="text-btn" data-action="open-version-history">Versiones</button>
                    
                </div>
            </div>
            <div class="version-tabs" role="group" aria-label="Versiones del texto">
                ${versions.map((v) => `<button class="version-tab ${st.version === v.id ? 'is-active' : ''}" data-action="set-version" data-version="${v.id}">${v.label}</button>`).join('')}
            </div>
            <div class="text-box" data-doc>
                ${textWithHighlights(st.version)}
            </div>
            ${legend()}
            <div class="panel-actions">
                <button class="btn btn-primary" data-action="open-synonyms">${I.search(14)} Buscar sinónimos</button>
            </div>
        `;
    }

    function renderRulesPanel() {
        return `
            <div class="panel-head">
                <div><h3>Reglas y ejemplos</h3><p>El criterio detrás de cada corrección</p></div>
                
            </div>
            <div class="stack">
                ${D.rules.map((r) => `
                    <article class="rule-card kind-${r.kind}">
                        <div class="badge-row">
                            <span class="type-badge ${r.kind}">${r.label}</span>
                        </div>
                        <h4>${r.title}</h4>
                        <p>${r.body}</p>
                        <div class="rule-example good"><span>${r.goodLabel || 'Correcto'}</span>${r.good}</div>
                        <div class="rule-example bad"><span>${r.badLabel || 'Evitar'}</span>${r.bad}</div>
                        <button class="text-btn" data-action="open-rule" data-id="${r.id}">${I.book(14)} Ver regla completa</button>
                    </article>
                `).join('')}
            </div>
        `;
    }

    function renderCriteriaPanel() {
        const st = S.get();
        return `
            <div class="panel-head">
                <div><h3>Criterios editables</h3><p>Criterios para tu autoevaluación</p></div>
                
            </div>
            <p class="panel-note">Edita un supuesto y vuelve a revisar el texto cuando estés listo. Tus versiones anteriores permanecen disponibles en “Versiones”.</p>
            <div class="stack">
                ${st.criteria.map((c) => `
                    <label class="criterion-card">
                        <span class="criterion-icon">${(I[c.icon] || I.tag)(16)}</span>
                        <span class="criterion-body">
                            <span class="criterion-label">${c.label}</span>
                            <input type="text" data-criterion="${c.id}" value="${escapeHtml(c.value)}">
                        </span>
                    </label>
                `).join('')}
            </div>
            <button class="btn btn-ghost full" data-action="add-criterion">${I.plus(14)} Añadir supuesto</button>
            <div class="panel-actions">
                <button class="btn btn-primary" data-action="save-criteria">Guardar cambios</button>
                <button class="btn" data-action="discard-criteria">Descartar</button>
            </div>
        `;
    }

    function renderPlanPanel() {
        const st = S.get();
        return `
            <div class="panel-head">
                <div><h3>Plan de escritura</h3><p>Pasos en lenguaje natural</p></div>
                
            </div>
            <p class="panel-note">Marca los pasos opcionales. La IA no avanza de etapa sin tu confirmación.</p>
            <div class="stack">
                ${st.plan.map((p) => `
                    <label class="plan-step ${p.done ? 'is-done' : ''}">
                        <input type="checkbox" data-plan-check="${p.id}" ${p.done ? 'checked' : ''}>
                        <span class="plan-index">${p.id.replace('p', '')}</span>
                        <input type="text" data-plan="${p.id}" value="${escapeHtml(p.text)}">
                        ${p.optional ? '<span class="optional-badge">opcional</span>' : ''}
                    </label>
                `).join('')}
            </div>
            <div class="panel-actions">
                <button class="btn btn-primary" data-action="regenerate-plan">${I.refresh(14)} Regenerar desde el plan</button>
            </div>
        `;
    }

    function renderChangesPanel() {
        const st = S.get();
        const decided = Object.values(st.statuses).filter((status) => status !== 'pending').length;
        return `
            <div class="panel-head">
                <div><h3>Cambios</h3><p>${decided} de ${D.corrections.length} revisados</p></div>
                
            </div>
            <div class="stack">
                ${D.corrections.map((c) => {
                    const s = st.statuses[c.id] || 'pending';
                    const label = { pending: 'Pendiente', accepted: 'Aceptada', rejected: 'Rechazada' }[s];
                    return `
                        <article class="change-row status-${s}">
                            <div class="change-top">
                                <span class="type-badge ${c.kind}">${c.label}</span>
                                <span class="status-pill ${s}">${label}</span>
                            </div>
                            <strong>${c.title}</strong>
                            <p class="mono small">${c.before} → ${c.after}</p>
                            <div class="change-actions">
                                ${s !== 'pending' ? `<button class="text-btn" data-action="correction-undo" data-id="${c.id}">${I.undo(12)} Deshacer</button>` : '<span class="muted-text">Sin decisión todavía.</span>'}
                            </div>
                        </article>`;
                }).join('')}
            </div>
        `;
    }

    function renderScenarioPanel() {
        const st = S.get();
        return `
            <div class="panel-head">
                <div><h3>Escenario</h3><p>Contexto de la conversación</p></div>
                
            </div>
            <div class="stack">
                ${D.scenarios.map((s) => `
                    <button class="scenario-card ${st.scenario === s.id ? 'is-active' : ''}" data-action="select-scenario" data-scenario="${s.id}">
                        <span class="scenario-icon">${(I[s.icon] || I.message)(18)}</span>
                        <span>
                            <strong>${s.name}</strong>
                            <span>${s.goal}</span>
                        </span>
                    </button>
                `).join('')}
            </div>
            <div class="panel-note">
                <strong>Plan de la sesión</strong>
                <p>${D.scenarios.find((s) => s.id === st.scenario).prompts.length} preguntas · 5–10 minutos · nivel B1–B2.</p>
            </div>
        `;
    }

    function renderVocabularyPanel() {
        const st = S.get();
        const scenario = D.scenarios.find((s) => s.id === st.scenario);
        const allWords = st.mode === 'lessons'
            ? D.article.words
            : scenario.vocab.map((w, i) => ({ word: w, meaning: ['experiencia', 'fortalezas', 'metas', 'puesto', 'reto', 'trabajo en equipo'][i] || 'palabra clave', example: '' }));
        const words = st.mode === 'lessons'
            ? allWords.filter((w) => st.savedWords.includes(w.word))
            : allWords;
        const isSavedWords = st.mode === 'lessons';

        return `
            <div class="panel-head">
                <div><h3>${isSavedWords ? 'Palabras guardadas' : 'Vocabulario'}</h3><p>${isSavedWords ? 'Acceso directo de esta tarea' : 'Palabras clave del contexto'}</p></div>
                
            </div>
            ${isSavedWords && !words.length ? `
                <div class="empty-support">
                    <strong>Aún no tienes palabras guardadas</strong>
                    <p>Selecciona una palabra en la lectura central y pulsa “Guardar palabra”. Aquí aparecerá directamente.</p>
                </div>
            ` : `<div class="stack">
                ${words.map((w) => `
                    <article class="word-card ${st.savedWords.includes(w.word) ? 'is-saved' : ''}">
                        <div class="word-top">
                            <strong>${w.word}</strong>
                            <button class="mini-btn" data-action="${st.savedWords.includes(w.word) ? 'remove-word' : 'save-word'}" data-word="${w.word}" aria-label="${st.savedWords.includes(w.word) ? 'Quitar' : 'Guardar'} ${w.word}">${st.savedWords.includes(w.word) ? I.check(13) : I.plus(13)}</button>
                        </div>
                        <p>${w.meaning}</p>
                        ${w.example ? `<p class="muted-text italic">“${w.example}”</p>` : ''}
                    </article>
                `).join('')}
            </div>`}
            ${isSavedWords ? `<p class="panel-note">${st.savedWords.length || 'Ninguna'} palabra${st.savedWords.length === 1 ? '' : 's'} guardada${st.savedWords.length === 1 ? '' : 's'}.</p>` : ''}
        `;
    }

    function renderProgressPanel() {
        const st = S.get();
        const mode = st.mode;
        const stages = D.modes[mode].stages;
        const stageIndex = Math.max(0, Math.min(st.activeStage, stages.length - 1));
        const completedCount = (st.completedStages[mode] || []).length;
        const saved = st.savedWords.length;
        let metricLabel = 'Palabras guardadas';
        let metricValue = String(saved);
        let note = `Guardaste ${saved} palabra${saved === 1 ? '' : 's'} en esta sesión.`;
        if (mode === 'writing') {
            const statuses = Object.values(st.statuses);
            const decided = statuses.filter((status) => status !== 'pending').length;
            const accepted = statuses.filter((status) => status === 'accepted').length;
            const pending = statuses.filter((status) => status === 'pending').length;
            metricLabel = 'Sugerencias revisadas';
            metricValue = `${decided}/${statuses.length}`;
            note = `${accepted} aceptadas · ${pending} pendientes. Puedes volver a comparar cada cambio con tu texto.`;
        } else if (mode === 'conversation') {
            const replies = (st.messages.conversation || []).filter((message) => message.role === 'user').length;
            metricLabel = 'Respuestas escritas';
            metricValue = String(replies);
            note = `Tienes ${saved} palabra${saved === 1 ? '' : 's'} guardada${saved === 1 ? '' : 's'} para repasar.`;
        } else if (st.selectedWord) {
            note = `Estás revisando “${st.selectedWord}”. Puedes consultar ejemplos y guardarla para repasar.`;
        }
        return `
            <div class="panel-head">
                <div><h3>Tu progreso</h3><p>${D.modes[mode].label}</p></div>
            </div>
            <div class="stat-grid">
                <div class="stat-card"><strong>${completedCount}/${stages.length}</strong><span>Etapas con notas guardadas</span></div>
                <div class="stat-card"><strong>${escapeHtml(metricValue)}</strong><span>${escapeHtml(metricLabel)}</span></div>
            </div>
            <p class="panel-note">Etapa actual: ${escapeHtml(stages[stageIndex])}. ${escapeHtml(note)}</p>
            <p class="panel-note">${Learning.evidenceSummary(mode)} La actividad registrada no acredita dominio del inglés.</p>
        `;
    }

    function renderArticlePanel() {
        const st = S.get();
        const selected = st.selectedWord ? D.article.words.find((w) => w.word === st.selectedWord) : null;
        return `
            <div class="panel-head">
                <div><h3>${D.article.title}</h3><p>${D.article.source}</p></div>
                
            </div>
            <div class="article-box">
                ${D.article.paragraphs.map((p, pi) => `<p>${pi === 0 ? p : p}</p>`).join('')}
            </div>
            <p class="panel-note">Selecciona una palabra del artículo para ver su significado en contexto.</p>
            <div class="word-picker">
                ${D.article.words.map((w) => `<button class="word-chip ${st.selectedWord === w.word ? 'is-active' : ''}" data-action="select-word" data-word="${w.word}">${w.word}</button>`).join('')}
            </div>
            ${selected ? `
                <div class="word-detail">
                    <div class="word-detail-head"><strong>${selected.word}</strong><span>Significado en este artículo</span></div>
                    <p><b>Significado:</b> ${selected.meaning}</p>
                    <div class="word-example featured"><span>En el artículo</span>“${selected.example}”</div>
                    <div class="word-extra-example"><span>Otro ejemplo</span>“${selected.examples[0]}”</div>
                    <p class="word-use"><b>Cómo se usa:</b> ${selected.use}</p>
                    <div class="word-detail-actions">
                        <button class="btn btn-primary" data-action="open-word-examples" data-word="${selected.word}">Ver más ejemplos</button>
                        <button class="btn" data-action="save-word" data-word="${selected.word}">${I.plus(14)} Guardar palabra</button>
                    </div>
                </div>
            ` : ''}
        `;
    }

    function renderAnswersPanel() {
        return `
            <div class="panel-head">
                <div><h3>Respuestas rápidas</h3><p>Explicaciones cortas y ejemplos</p></div>
                
            </div>
            <div class="stack">
                <article class="qa-card"><strong>¿Cuándo uso “agree” sin “am”?</strong><p>“Agree” ya es un verbo: I agree, she agrees. Nunca “I am agree”.</p></article>
                <article class="qa-card"><strong>¿Important o relevant?</strong><p>“Important” es valor general; “relevant” es pertinencia. Para un plazo que afecta tu nota, “relevant”.</p></article>
                <article class="qa-card"><strong>¿Cómo suena “comfortable”?</strong><p>/ˈkʌmftəbl/, tres sílabas. Evita “com-for-ta-ble”.</p></article>
            </div>
            <button class="btn btn-ghost full" data-action="focus-composer">${I.message(14)} Hacer otra pregunta</button>
        `;
    }

    function renderSourcesPanel() {
        return `
            <div class="panel-head">
                <div><h3>Fuentes</h3><p>De dónde sale cada respuesta</p></div>
                
            </div>
            <div class="stack">
                <div class="source-card"><strong>Cambridge Grammar</strong><span>Uso de “agree” y verbos estativos.</span><span class="source-tag">verificado</span></div>
                <div class="source-card"><strong>Longman Dictionary</strong><span>Matices entre “important” y “relevant”.</span><span class="source-tag">verificado</span></div>
            </div>
        `;
    }

    function renderAsideContent() {
        const state = S.get();
        const tab = state.tab;
        const mode = state.mode;
        if (S.get().detailsLevel === 2) return renderAdvancedMenu();
        const map = {
            text: renderTextPanel,
            rules: renderRulesPanel,
            criteria: renderCriteriaPanel,
            plan: renderPlanPanel,
            changes: renderChangesPanel,
            scenario: renderScenarioPanel,
            vocabulary: renderVocabularyPanel,
            progress: renderProgressPanel,
            article: renderArticlePanel,
            answers: renderAnswersPanel,
            sources: renderSourcesPanel
        };
        const available = supportTabs(mode);
        const activeTab = available.some((item) => item.id === tab)
            ? tab
            : (defaultAsideTabs[mode] || available[0]?.id);
        return (map[activeTab] || renderVocabularyPanel)();
    }

    /* ---------------- Historial y sugerencias ---------------- */
    function renderHistoryDrawer() {
        const st = S.get();
        const groups = [
            { mode: 'writing', label: 'Redacción y escritura', icon: 'doc' },
            { mode: 'conversation', label: 'Conversación escrita', icon: 'message' },
            { mode: 'lessons', label: 'Lectura y vocabulario', icon: 'book' }
        ];
        const currentMode = st.historyMode || st.mode;
        return `
            <div class="history-head">
                <div><strong>Tus chats</strong><small>Elige una actividad para continuar</small></div>
                <button class="icon-btn" data-action="close-history" aria-label="Cerrar chats">${I.close(18)}</button>
            </div>
            <div class="history-groups">
                ${groups.map((group) => {
                    const sessions = st.sessions.filter((s) => s.mode === group.mode);
                    if (!sessions.length) return '';
                    return `
                        <section class="history-group ${group.mode === currentMode ? 'is-current' : ''}">
                            <h3>${(I[group.icon] || I.doc)(14)} ${group.label}</h3>
                            <div class="history-list">
                                ${sessions.map((s) => `
                                    <button class="history-item ${s.active ? 'is-active' : ''}" data-action="select-session" data-session="${s.id}">
                                        <span class="history-item-main"><strong>${s.title}</strong><small>${s.meta}</small></span>
                                        <span class="history-item-device">${(I[s.device] || I.monitor)(13)} ${s.device === 'phone' ? 'Celular' : 'Laptop'}</span>
                                    </button>
                                `).join('')}
                            </div>
                        </section>`;
                }).join('')}
            </div>
        `;
    }

    function renderSuggestions() {
        const st = S.get();
        if (st.detailsLevel < 3) {
            return `
                <div class="popover-head">
                    <h4>Una forma de avanzar</h4>
                    <button class="icon-btn tiny" data-action="toggle-suggestions" aria-label="Cerrar ayuda">${I.close(15)}</button>
                </div>
                <div class="learner-tip">
                    <span class="suggestion-icon">${I.lightbulb(16)}</span>
                    <div><strong>Piensa antes de aceptar.</strong><p>Lee la pista, intenta explicar el cambio con tus propias palabras y luego decide.</p></div>
                </div>
                <button class="btn btn-ghost full" data-action="set-help" data-help="explicacion">Mostrar explicación</button>
            `;
        }
        return `
            <div class="popover-head">
                
                <button class="icon-btn tiny" data-action="toggle-suggestions" aria-label="Cerrar sugerencias">${I.close(15)}</button>
            </div>
            <h4>Sugerencias para este paso</h4>
            <div class="suggestions-list">
                ${D.suggestions.map((s) => `
                    <div class="suggestion-item">
                        <span class="suggestion-icon">${(I[s.icon] || I.info)(16)}</span>
                        <div><strong>${s.title}</strong><p>${s.text}</p></div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    window.Panels = {
        renderTabs,
        renderAsideContent,
        renderWritingDraft,
        renderHistoryDrawer,
        renderSuggestions
    };
})();
