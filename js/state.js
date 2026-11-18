/* ============================================================
   State · store mínimo con suscripciones
   ============================================================ */
(function () {
    'use strict';

    const D = window.DemoData;
    const clone = (v) => JSON.parse(JSON.stringify(v));

    const initial = {
        mode: 'writing',
        help: 'pista',                 // pista | explicacion | ejemplo | reescritura
        tab: 'criteria',
        version: 'draft',              // original | draft | final
        statuses: { c1: 'pending', c2: 'pending', c3: 'pending', c4: 'pending' },
        sideOpen: false,
        sidePrefill: '',
        sideAnswer: null,
        typing: false,
        activeStage: 2,
        completedStages: { writing: [0, 1], conversation: [0], lessons: [0] },
        messages: clone(D.initialMessages),
        scenario: 'interview',
        selectedWord: null,
        savedWords: [],
        plan: clone(D.plan),
        criteria: clone(D.criteria),
        versionHistory: [
            { id: 'original', label: 'Versión original', time: 'Inicio', detail: 'Tu texto antes de revisar.' },
            { id: 'draft', label: 'Borrador revisado', time: 'Antes de aceptar', detail: 'Tu texto con las sugerencias pendientes.' },
            { id: 'final', label: 'Versión actual', time: 'Ahora', detail: 'Solo incorpora los cambios que aceptaste.' }
        ],
        sessions: clone(D.sessions),
        suggestionsOpen: false,
        drawerOpen: false,
        historyOpen: false,
        supportOpen: false,
        historyMode: null,
        // 0 = vista tutor, 1 = apoyo guiado, 2 = índice de herramientas, 3 = una herramienta abierta
        detailsLevel: 0,
        focusCorrection: null
    };

    let state = clone(initial);
    const subscribers = [];

    function emit() {
        subscribers.slice().forEach((fn) => fn(state));
    }

    window.DemoState = {
        get() {
            return state;
        },
        set(patch) {
            state = Object.assign({}, state, patch);
            emit();
            return state;
        },
        update(fn) {
            fn(state);
            emit();
            return state;
        },
        touch() {
            emit();
        },
        subscribe(fn) {
            subscribers.push(fn);
            return () => {
                const i = subscribers.indexOf(fn);
                if (i >= 0) subscribers.splice(i, 1);
            };
        },
        reset() {
            state = clone(initial);
            emit();
        },
        helpers: {
            correction(id) {
                return D.corrections.find((c) => c.id === id);
            },
            rule(id) {
                return D.rules.find((r) => r.id === id);
            },
            mode() {
                return D.modes[state.mode];
            },
            verifiedCount() {
                return Object.keys(state.statuses).filter((k) => state.statuses[k] !== 'pending').length;
            }
        }
    };
})();
