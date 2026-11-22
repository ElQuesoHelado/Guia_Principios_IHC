/* ============================================================
   Mock data · Todo el contenido de la demo (sin backend)
   ============================================================ */
(function () {
    'use strict';

    /* ---------- Texto de la sesión de redacción ---------- */
    const writingText = `Dear Professor Ramos,

I am agree with the course deadline, but I had two exams last week. The deadline is important for my final grade, and I also had to work on a project and I could not finish the essay on time. I want you give me more time.

Thank you for your help.
Best regards`;

    /* ---------- Correcciones plantadas ---------- */
    const corrections = [
        {
            id: 'c1',
            kind: 'grammar',
            label: 'Gramática',
            title: 'Concordancia verbal',
            correctionNo: 1,
            before: 'I am agree',
            after: 'I agree',
            hint: 'Mira “I am agree”. ¿Necesita “agree” el auxiliar “am” para funcionar?',
            why: 'En inglés, “agree” ya es un verbo. No necesita el auxiliar “am”: se dice “I agree with…”.',
            example: 'I agree with the course deadline. / She agrees with the plan.',
            ruleId: 'r1',
            control: 'lógica del sistema',
            risk: 'variabilidad',
            paper: 'Yang · WoZ',
            status: 'pending'
        },
        {
            id: 'c2',
            kind: 'vocab',
            label: 'Vocabulario',
            title: 'Una alternativa según la intención',
            correctionNo: 2,
            before: 'important',
            after: 'crucial',
            hint: '“Important” ya es correcto. ¿Quieres enfatizar que el plazo es decisivo o conservar una expresión más general?',
            why: '“Crucial” destaca que algo es decisivo. Es una alternativa de énfasis, no la corrección de un error: conserva “important” si ese era tu sentido.',
            example: 'Submitting on time is crucial for my final grade.',
            ruleId: 'r2',
            control: 'comunicación',
            risk: 'validez ecológica',
            paper: 'Yang · WoZ',
            status: 'pending'
        },
        {
            id: 'c3',
            kind: 'tone',
            label: 'Tono',
            title: 'Petición demasiado directa',
            correctionNo: 3,
            before: 'I want you give me more time',
            after: 'Could you please give me more time?',
            hint: 'Mira “I want you give me more time”. Para escribirle a una profesora, ¿suena lo bastante formal?',
            why: '“Could you please…?” es una petición cortés y adecuada para el contexto académico.',
            example: 'Could you please give me more time to submit the essay?',
            ruleId: 'r3',
            control: 'colaboración',
            risk: 'decepción',
            paper: 'Yang · WoZ',
            status: 'pending'
        },
        {
            id: 'c4',
            kind: 'clarity',
            label: 'Claridad',
            title: 'Oración demasiado larga',
            correctionNo: 4,
            before: 'I also had to work on a project and I could not finish the essay on time.',
            after: 'I also had to work on a project. As a result, I could not finish the essay on time.',
            hint: 'Esa oración encadena dos ideas con “and”. ¿Podrías separarlas para que se entienda mejor?',
            why: 'Separar la causa y la consecuencia hace que el argumento sea más fácil de seguir.',
            example: 'I had to work on a project. As a result, I could not finish the essay on time.',
            ruleId: 'r4',
            control: 'guion predefinido',
            risk: 'reproducibilidad',
            paper: 'Yang · WoZ',
            status: 'pending'
        }
    ];

    /* ---------- Reglas y ejemplos ---------- */
    const rules = [
        {
            id: 'r1', kind: 'grammar', label: 'Gramática', title: '“Agree” ya es un verbo',
            body: 'No uses “am / is / are” delante de “agree”. El verbo se conjuga solo.',
            good: 'I agree with the deadline.',
            bad: 'I am agree with the deadline.'
        },
        {
            id: 'r2', kind: 'vocab', label: 'Vocabulario', title: 'Important / crucial',
            body: '“Important” indica importancia; “crucial” añade un énfasis decisivo. Elige según tu intención: el original también puede ser correcto.',
            good: 'Submitting on time is crucial for my final grade.',
            bad: 'This deadline is important for my final grade.',
            goodLabel: 'Alternativa con más énfasis', badLabel: 'Original válido'
        },
        {
            id: 'r3', kind: 'tone', label: 'Tono', title: 'Peticiones formales',
            body: 'En contextos académicos, usa modales de cortesía: could, would, may. Evita “I want you to…”.',
            good: 'Could you please give me more time?',
            bad: 'I want you give me more time.'
        },
        {
            id: 'r4', kind: 'clarity', label: 'Claridad', title: 'Una idea por oración',
            body: 'Unir ideas con “and” puede ser correcto. Si la relación de causa y consecuencia no queda clara, puedes dividir la oración o usar un conector.',
            good: 'I had to work on a project. As a result, I could not finish on time.',
            bad: 'I had to work on a project and I could not finish on time.',
            goodLabel: 'Relación explícita', badLabel: 'También es gramatical'
        }
    ];

    /* ---------- Criterios / supuestos editables (Kazemitabaar) ---------- */
    const criteria = [
        { id: 'audience', icon: 'user', label: 'Destinataria', value: 'Profesora Ramos · universidad' },
        { id: 'level', icon: 'layers', label: 'Nivel objetivo', value: 'B1–B2' },
        { id: 'tone', icon: 'message', label: 'Tono', value: 'Formal y cordial' },
        { id: 'goal', icon: 'tag', label: 'Objetivo', value: 'Solicitar una prórroga' },
        { id: 'avoid', icon: 'shield', label: 'Evitar', value: 'Contracciones y órdenes directas' }
    ];

    /* ---------- Plan de escritura ---------- */
    const plan = [
        { id: 'p1', text: 'Saludo: Dear Professor Ramos,', done: true, optional: false },
        { id: 'p2', text: 'Presentar el motivo: prórroga para el ensayo', done: true, optional: false },
        { id: 'p3', text: 'Justificar con dos exámenes y un proyecto', done: false, optional: false },
        { id: 'p4', text: 'Hacer la petición en tono formal', done: false, optional: false },
        { id: 'p5', text: 'Cierre: Thank you for your consideration.', done: false, optional: true }
    ];

    /* ---------- Sugerencias del header (WoZ) ---------- */
    const suggestions = [
        { icon: 'lightbulb', title: 'Prueba antes de abrir la explicación', text: 'Lee la pista e intenta corregir la frase con tus propias palabras.' },
        { icon: 'book', title: 'Comprueba el significado en contexto', text: 'Compara la palabra con la oración completa y revisa otro ejemplo.' },
        { icon: 'check', title: 'Decide qué cambio conservar', text: 'Compara el texto original con la propuesta y acepta solo lo que entiendas.' }
    ];

    /* ---------- Sesiones recientes ---------- */
    const sessions = [
        { id: 's1', title: 'Correo: prórroga', device: 'monitor', meta: 'Hoy 19:40', mode: 'writing', active: true },
        { id: 's2', title: 'Conversación: entrevista', device: 'phone', meta: 'Ayer 18:05', mode: 'conversation', active: false },
        { id: 's3', title: 'Artículo: vocabulario', device: 'monitor', meta: 'Lun 12:30', mode: 'lessons', active: false },
        
    ];

    /* ---------- Modos ---------- */
    const modes = {
        writing: {
            label: 'Aprender a escribir correos',
            title: 'Aprender a escribir correos',
            subtitle: 'Correo · solicitud de prórroga',
            stages: ['Comprender', 'Escribir', 'Revisar', 'Transferir'],
            activeStage: 0,
            tabs: [
                { id: 'text', label: 'Tu texto', paper: 'WaitGPT · data lens' },
                { id: 'rules', label: 'Reglas', paper: 'Gu et al. · procedimiento' },
                { id: 'criteria', label: 'Criterios', paper: 'Kazemitabaar · supuestos' },
                { id: 'plan', label: 'Plan', paper: 'LightVA · plan' },
                { id: 'changes', label: 'Cambios', paper: 'WaitGPT · granular' },
                { id: 'progress', label: 'Progreso', paper: 'Seguimiento de esta tarea' }
            ],
            placeholder: 'Pregunta sobre tu texto, vocabulario o una regla…',
            modeHint: 'Actividad: Aprender a escribir correos'
        },
        conversation: {
            label: 'Conversación escrita',
            title: 'Conversación escrita',
            subtitle: 'Conversación por chat · entrevista de trabajo',
            stages: ['Preparar', 'Conversar', 'Revisar', 'Transferir'],
            activeStage: 0,
            tabs: [
                { id: 'scenario', label: 'Escenario', paper: 'Gu et al. · contexto' },
                { id: 'vocabulary', label: 'Vocabulario', paper: 'LightVA · insights' },
                { id: 'progress', label: 'Progreso', paper: 'WoZ · rigor' },
                { id: 'changes', label: 'Cambios', paper: 'WaitGPT · granular' }
            ],
            placeholder: 'Escribe tu respuesta en inglés o pide una pista…',
            modeHint: 'Modo: Conversación'
        },
        lessons: {
            label: 'Aprender vocabulario',
            title: 'Aprender vocabulario',
            subtitle: 'Artículo corto · vocabulario en contexto',
            stages: ['Leer', 'Descubrir', 'Registrar', 'Practicar'],
            activeStage: 0,
            tabs: [
                { id: 'article', label: 'Artículo', paper: 'LightVA · data lens' },
                { id: 'vocabulary', label: 'Vocabulario', paper: 'Kazemitabaar · side query' },
                { id: 'progress', label: 'Progreso', paper: 'WoZ · rigor' },
                { id: 'plan', label: 'Plan', paper: 'LightVA · plan' },
                { id: 'changes', label: 'Cambios', paper: 'WaitGPT · granular' }
            ],
            placeholder: 'Pega tu lectura y escribe la palabra que necesitas…',
            modeHint: 'Actividad: Aprender vocabulario'
        },

    };

    /* ---------- Mensajes iniciales por modo ---------- */
    const initialMessages = {
        writing: [
            {
                role: 'user',
                text: 'Quiero aprender a pedir una prórroga en inglés y entender cómo usar un tono formal.'
            },
            {
                role: 'ai',
                label: 'TUTOR IA · REDACCIÓN',
                text: 'Analiza el modelo y escribe tu propio borrador. En Revisar podrás comparar cuatro sugerencias sobre un correo de práctica; tu borrador se conserva aparte.',
                chips: [
                    { icon: 'alert', text: 'Gramática: 1', kind: 'grammar' },
                    { icon: 'book', text: 'Vocabulario: 1', kind: 'vocab' },
                    { icon: 'message', text: 'Tono: 1', kind: 'tone' },
                    { icon: 'sparkles', text: 'Claridad: 1', kind: 'clarity' }
                ]
            }
        ],
        conversation: [
            {
                role: 'ai',
                label: 'TUTOR IA · CONVERSACIÓN ESCRITA',
                text: 'Good morning! Thanks for coming. To start, could you tell me a little about yourself and why you are interested in this position?',
                chips: [
                    { icon: 'lightbulb', text: 'Pista: usa “I have experience in…”', kind: 'info' }
                ]
            }
        ],
        lessons: [
            {
                role: 'ai',
                label: 'Tutor · lecciones',
                text: 'Selecciona una palabra para ver su significado y ejemplos.'
            }
        ],

    };

    /* ---------- Escenarios de conversación ---------- */
    const scenarios = [
        {
            id: 'interview', name: 'Entrevista de trabajo', icon: 'user',
            goal: 'Practicar una entrevista breve con preguntas sobre tu experiencia y fortalezas.',
            prompts: [
                'Could you tell me a little about yourself?',
                'What are your main strengths for this position?',
                'Tell me about a challenge you solved.',
                'Where do you see yourself in three years?'
            ],
            vocab: ['experience', 'strengths', 'goals', 'position', 'challenge', 'teamwork']
        },
        {
            id: 'cafe', name: 'Café con un amigo', icon: 'message',
            goal: 'Mantener una conversación informal de 5 intercambios.',
            prompts: [
                'How was your weekend?',
                'What do you usually do to relax?',
                'Have you seen any good series lately?'
            ],
            vocab: ['weekend', 'recommend', 'favorite', 'relax', 'catch up']
        },
        {
            id: 'campus', name: 'Conversación universitaria', icon: 'layers',
            goal: 'Explicar una idea de clase y responder una pregunta.',
            prompts: [
                'What are you working on in class?',
                'What is one idea you found interesting?',
                'How would you explain it to a classmate?'
            ],
            vocab: ['introduce', 'objective', 'summary', 'results', 'team', 'impact']
        }
    ];

    /* ---------- Artículo de la lección ---------- */
    const article = {
        title: 'The future of remote work',
        source: 'Mini artículo · 120 palabras · B1–B2',
        paragraphs: [
            'Remote work has become a normal part of modern life. Many companies discovered that employees can be productive at home, and workers value the flexibility. However, remote work also creates challenges, such as isolation and difficulty separating work from personal time.',
            'Experts recommend creating a clear routine. A dedicated workspace, regular breaks, and short conversations with colleagues can help. The goal is not to work more, but to work better.'
        ],
        words: [
            {
                word: 'productive', meaning: 'que produce buenos resultados', example: 'Employees can be productive at home.',
                use: 'Se usa para describir a una persona, equipo o actividad que logra buenos resultados.',
                examples: ['A productive meeting ends with clear decisions.', 'She feels more productive in the morning.']
            },
            {
                word: 'flexibility', meaning: 'capacidad de adaptarse a distintos horarios', example: 'Workers value the flexibility.',
                use: 'Se usa para hablar de horarios, normas o formas de trabajo que pueden adaptarse.',
                examples: ['This job offers flexibility for students.', 'The flexibility of the schedule helps parents.']
            },
            {
                word: 'isolation', meaning: 'sensación de estar solo', example: 'Remote work can create isolation.',
                use: 'Se usa cuando una persona se siente separada de otras personas o de un grupo.',
                examples: ['Long periods of isolation can affect motivation.', 'The student experienced isolation during the first month.']
            },
            {
                word: 'dedicated', meaning: 'reservado para un uso concreto', example: 'A dedicated workspace helps you focus.',
                use: 'En este artículo significa “reservado exclusivamente para una función”.',
                examples: ['I use a dedicated notebook for new vocabulary.', 'The team has a dedicated room for meetings.']
            },
            {
                word: 'routine', meaning: 'secuencia habitual de actividades', example: 'Create a clear routine.',
                use: 'Se usa para hablar de actividades que se repiten de manera organizada.',
                examples: ['My morning routine starts with a short walk.', 'A regular routine can make studying easier.']
            }
        ]
    };


    /* ---------- Guía visual de modos secundarios ---------- */


    /* ---------- Respuestas mock del chat ---------- */
    const replies = {
        writing: [
            { match: /pista|ayuda|hint/i, text: 'Pista: fíjate primero en “I am agree”. En inglés, “agree” ya es un verbo, así que no necesita “am”. ¿Quieres ver la regla completa?', chips: [{ icon: 'book', text: 'Ver regla', action: 'open-rule-r1', kind: 'info' }] },
            { match: /sinónim|vocabul|important/i, text: 'Para “important” puedes usar “relevant” si hablas de pertinencia, o “demanding” si hablas de una tarea exigente. ¿Cuál encaja mejor con tu frase?', chips: [{ icon: 'search', text: 'Buscar sinónimos', action: 'open-synonyms', kind: 'info' }] },
            { match: /regla|por qué|porque/i, text: 'La regla es simple: “agree” no lleva auxiliar. Se conjuga como cualquier verbo: I agree, she agrees, we agreed. ¿Quieres un ejemplo en tu correo?', chips: [{ icon: 'book', text: 'Ver ejemplo', action: 'open-rule-r1', kind: 'info' }] },
                        { match: /tono|formal|profesor/i, text: 'Para una profesora, cambia “I want you to…” por “Could you please…?”. Mantiene tu petición, pero suena más cortés.', chips: [{ icon: 'message', text: 'Editar criterio de tono', action: 'open-criteria', kind: 'info' }] }
        ],
        conversation: [
            { match: /pista|ayuda|hint/i, text: 'Pista: empieza con una estructura segura. “I have experience in…” + un ejemplo concreto. No necesitas una respuesta perfecta, solo clara.', chips: [{ icon: 'book', text: 'Ver vocabulario', action: 'open-vocabulary', kind: 'info' }] },
            { match: /nervios|miedo|no sé/i, text: 'Puedes tomarte un momento y escribir una idea sencilla. Por ejemplo: “I have experience in…” Luego añade una razón o un ejemplo.', chips: [{ icon: 'lightbulb', text: 'Ver una estructura', action: 'open-vocabulary', kind: 'info' }] },
            { match: /.*/, text: 'Para revisar tu respuesta, intenta añadir una razón: “because I enjoy…” o “for example, in my last project…”. Así tu respuesta gana detalle.', chips: [{ icon: 'arrowRight', text: 'Siguiente pregunta', action: 'next-prompt', kind: 'info' }] }
        ],
        lessons: [
            { match: /productiv/i, text: '“Productive” significa que produces buenos resultados. En el artículo: “employees can be productive at home”. ¿Puedes escribir una oración con “productive”?', chips: [{ icon: 'plus', text: 'Guardar palabra', action: 'save-word-productive', kind: 'info' }] },
            { match: /flexib/i, text: '“Flexibility” es la capacidad de adaptarse. Se usa mucho para horarios: “flexible hours”. En español sería “flexibilidad”.', chips: [{ icon: 'plus', text: 'Guardar palabra', action: 'save-word-flexibility', kind: 'info' }] },
            { match: /.*/, text: 'Veamos el contexto. Para entender una palabra en contexto, mira la oración completa antes de traducirla. ¿Quieres que te dé una pista o el significado directo?', chips: [{ icon: 'lightbulb', text: 'Dame una pista', action: 'hint-word', kind: 'info' }] }
        ],

    };

    window.DemoData = {
        writingText,
        corrections,
        rules,
        criteria,
        plan,
        suggestions,
        sessions,
        modes,
        initialMessages,
        scenarios,
        article,
        replies
    };
})();
