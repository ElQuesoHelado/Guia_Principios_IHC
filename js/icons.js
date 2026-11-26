/* ============================================================
   Icons · SVG inline (trazo 2–2.4, mismo lenguaje que Main.dc.html)
   ============================================================ */
(function () {
    'use strict';

    const svg = (inner, size) =>
        `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${inner}</svg>`;

    window.Icons = {
        menu: (s = 18) => svg('<path d="M4 7h16M4 12h16M4 17h16"/>', s),
        settings: (s = 18) => svg('<path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/>', s),
        lightbulb: (s = 18) => svg('<path d="M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0012 3z"/>', s),
        check: (s = 16) => svg('<path d="M5 12.5l4.5 4.5L19 7.5"/>', s),
        chevronLeft: (s = 18) => svg('<path d="M15 6l-6 6 6 6"/>', s),
        chevronRight: (s = 18) => svg('<path d="M9 6l6 6-6 6"/>', s),
        chevronDown: (s = 16) => svg('<path d="M6 9l6 6 6-6"/>', s),
        close: (s = 18) => svg('<path d="M6 6l12 12M18 6L6 18"/>', s),
        send: (s = 20) => svg('<path d="m21 3-7 18-4-7-7-4 18-7ZM10 14 21 3"/>', s),
        doc: (s = 16) => svg('<path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>', s),
        scan: (s = 16) => svg('<path d="M4 8V6a2 2 0 012-2h2M16 4h2a2 2 0 012 2v2M20 16v2a2 2 0 01-2 2h-2M8 20H6a2 2 0 01-2-2v-2"/><path d="M8 10h8M8 14h5"/>', s),
        tag: (s = 16) => svg('<path d="M20 13l-7 7-9-9V4h7l9 9z"/><circle cx="8.5" cy="8.5" r="1.2"/>', s),
        sparkles: (s = 16) => svg('<path d="M12 3l1.6 4.4L18 9l-4.4 1.6L12 15l-1.6-4.4L6 9l4.4-1.6z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>', s),
        play: (s = 16) => svg('<path d="M8 5l11 7-11 7z"/>', s),
        undo: (s = 16) => svg('<path d="M9 7L4 12l5 5"/><path d="M4 12h9a6 6 0 010 12h-2"/>', s),
        export: (s = 16) => svg('<path d="M12 4v11M7 9l5-5 5 5M5 20h14"/>', s),
        copy: (s = 16) => svg('<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 012-2h9"/>', s),
        book: (s = 16) => svg('<path d="M4 5a2 2 0 012-2h5v18H6a2 2 0 01-2-2z"/><path d="M20 5a2 2 0 00-2-2h-5v18h5a2 2 0 002-2z"/>', s),
        user: (s = 16) => svg('<circle cx="12" cy="8" r="3.5"/><path d="M5 20a7 7 0 0114 0"/>', s),
        plus: (s = 16) => svg('<path d="M12 5v14M5 12h14"/>', s),
        search: (s = 16) => svg('<circle cx="11" cy="11" r="6"/><path d="M16 16l4 4"/>', s),
        eye: (s = 16) => svg('<path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="2.5"/>', s),
        alert: (s = 16) => svg('<path d="M12 3l9 17H3z"/><path d="M12 9v5M12 17h.01"/>', s),
        info: (s = 16) => svg('<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>', s),
        arrowRight: (s = 16) => svg('<path d="M5 12h14M13 6l6 6-6 6"/>', s),
        refresh: (s = 16) => svg('<path d="M20 11a8 8 0 10-2.3 5.7"/><path d="M20 4v7h-7"/>', s),
        lock: (s = 16) => svg('<rect x="4" y="10" width="16" height="10" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/>', s),
        layers: (s = 16) => svg('<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5M3 17l9 5 9-5"/>', s),
        message: (s = 16) => svg('<path d="M21 12a8 8 0 01-8 8H6l-3 2V12a8 8 0 018-8h2a8 8 0 018 8z"/>', s),
        clock: (s = 16) => svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>', s),
        monitor: (s = 14) => svg('<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>', s),
        phone: (s = 14) => svg('<rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/>', s),
        wand: (s = 16) => svg('<path d="M4 20L17 7M14 4l1 3 3 1-3 1-1 3-1-3-3-1 3-1z"/>', s),
        table: (s = 16) => svg('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 10v10"/>', s),
        shield: (s = 16) => svg('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>', s)
    };
})();
