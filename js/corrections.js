/* ============================================================
   Corrections · tarjetas de verificación + progreso + descomposición
   Papers: Yang (WoZ), WaitGPT (granularidad), LightVA (descomposición)
   ============================================================ */
(function () {
    'use strict';

    const D = window.DemoData;
    const S = window.DemoState;
    const I = window.Icons;

    const helpLabels = {
        pista: 'Pista',
        explicacion: 'Explicación',
        ejemplo: 'Ejemplo',
        reescritura: 'Reescritura completa'
    };

    function helpsFor(c) {
        const help = S.get().help;
        const parts = [];
        if (help === 'pista') {
            parts.push(`<div class="hint-box"><strong>Pista:</strong> ${c.hint}</div>
                <button class="text-btn mt-8" data-action="correction-explain" data-id="${c.id}">Mostrar explicación</button>`);
            return parts.join('');
        }
        parts.push(`<div class="hint-box"><strong>Pista:</strong> ${c.hint}</div>`);
        if (help === 'explicacion' || help === 'ejemplo' || help === 'reescritura') {
            parts.push(`<p class="why"><strong>Por qué:</strong> ${c.why}</p>`);
        }
        if (help === 'ejemplo' || help === 'reescritura') {
            parts.push(`<div class="example-box"><span class="example-label">Ejemplo</span>${c.example}</div>`);
        }
        return parts.join('');
    }

    function renderCard(c) {
        const st = S.get();
        const simple = st.detailsLevel !== 3;
        const status = st.statuses[c.id] || 'pending';
        const isAccepted = status === 'accepted';
        const isRejected = status === 'rejected';

        const diff = S.get().help === 'pista'
            ? ''
            : `<div class="diff-line">
                    <span class="diff-before">${c.before}</span>
                    <span class="diff-arrow" aria-hidden="true">→</span>
                    <span class="diff-after">${c.after}</span>
               </div>`;

        const actions = status === 'pending' && simple
            ? `
                <button class="btn btn-primary" data-action="correction-accept" data-id="${c.id}">Usar esta sugerencia</button>
                <button class="btn" data-action="correction-reject" data-id="${c.id}">Mantener mi frase</button>
                <button class="text-btn" data-action="correction-confused" data-id="${c.id}">Explícamelo de otra forma</button>
              `
            : status === 'pending'
            ? `
                <button class="btn btn-primary" data-action="correction-accept" data-id="${c.id}">Aceptar</button>
                <button class="btn" data-action="correction-reject" data-id="${c.id}">Rechazar</button>
                <button class="btn" data-action="correction-confused" data-id="${c.id}">No entiendo</button>
                <span class="actions-spacer"></span>
                <button class="text-btn" data-action="correction-rule" data-id="${c.id}">${I.book(14)} Ver regla y ejemplo</button>
                <button class="text-btn" data-action="correction-ask" data-id="${c.id}">${I.message(14)} Preguntar</button>
              `
            : `
                <span class="resolved-note">${isAccepted ? 'Aceptada: la reescritura ya incorpora este cambio.' : 'Rechazada: se mantiene tu versión original.'}</span>
                <span class="actions-spacer"></span>
                <button class="text-btn" data-action="correction-undo" data-id="${c.id}">${I.undo(14)} Deshacer</button>
              `;

        return `
            <article class="correction-card kind-${c.kind} status-${status}" data-card="${c.id}" ${status === 'accepted' ? 'data-accepted="true"' : ''}>
                <div class="correction-head">
                    <div class="badge-row">
                        <span class="type-badge ${c.kind}">${c.label}</span>
                    </div>
                    <span class="correction-count">${simple ? 'Paso' : 'Corrección'} ${c.correctionNo} de 4</span>
                </div>

                <div class="correction-title-row">
                    <h4>${c.title}</h4>
                    <span class="status-pill ${status}">${status === 'pending' ? 'Pendiente' : status === 'accepted' ? 'Aceptada' : 'Rechazada'}</span>
                </div>

                ${diff}
                ${helpsFor(c)}

                <div class="correction-actions">${actions}</div>
            </article>
        `;
    }

    window.Corrections = {
        renderAnalysis() {
            const st = S.get();
            const current = D.corrections.find((c) => (st.statuses[c.id] || 'pending') === 'pending') || D.corrections[D.corrections.length - 1];
            return renderCard(current);
        },
        renderCard,
        helpLabels
    };
})();
