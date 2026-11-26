/* Material didáctico escrito para la demo. No procede de una consulta en vivo. */
window.TutorData = Object.freeze({
  tasks: { email: 'Correo en inglés', vocab: 'Vocabulario en contexto', general: 'Por explorar' },
  stages: {
    email: ['Comprender el tono', 'Escribir y decidir', 'Recuperar sin modelo', 'Usar en otro correo'],
    vocab: ['Inferir en contexto', 'Contrastar y relacionar', 'Recordar sin definición', 'Usar en otro contexto']
  },
  starters: {
    email: 'Quiero aprender a escribir un correo en inglés',
    vocab: 'Quiero entender “dedicated” en esta frase: “A dedicated space helps you focus on your work.”'
  },
  examples: {
    email: 'Quiero aprender a pedir una prórroga a mi profesora en inglés. Compara una petición cercana con una más cortés y explícame la diferencia sin escribir todo el correo.',
    review: 'Revisa el tono de este correo a mi profesora y conserva el resto:\nDear Professor,\nI want you to send me the notes.\nI am agree with the deadline.\nBest regards,\nAlex',
    vocab: '¿Qué significa dedicated en “A dedicated space helps you focus on your work”? Quiero inferir su significado antes de ver la definición.',
    ambiguous: 'Quiero mejorar mi inglés'
  },
  words: {
    dedicated: {
      word: 'dedicated', context: 'A dedicated space helps you focus on your work.',
      clue: 'Mira “space” y “focus on your work”: ¿hablan de una persona o de un espacio con una función?',
      meaning: 'Reservado para una finalidad concreta. En esta oración, el espacio se destina a trabajar.',
      other: '“A dedicated teacher” describe a una persona comprometida. Esa acepción cambia el sentido de “space”.',
      pattern: 'dedicated + sustantivo: a dedicated space / a dedicated desk. También: dedicated to + sustantivo o verbo en -ing.',
      example: 'The library has a dedicated room for group projects.',
      register: 'Estos ejemplos no bastan para etiquetar la palabra como formal o informal. La situación y la acepción importan.',
      transfer: 'Escribe a un compañero para proponer un espacio reservado para su proyecto. Usa dedicated solo si encaja con lo que quieres decir.'
    },
    productive: {
      word: 'productive', context: 'Short breaks help students stay productive during a long study session.',
      clue: 'Relaciona “short breaks” con el resultado de una sesión de estudio: ¿qué ayudan a mantener?',
      meaning: 'Que logra resultados o realiza trabajo útil; aquí se refiere a aprovechar el tiempo de estudio.',
      other: 'En “productive farmland”, se habla de tierras que producen abundantemente. No es el sentido de la sesión de estudio.',
      pattern: 'stay productive / a productive session / a productive meeting.',
      example: 'We had a productive meeting and agreed on the next steps.',
      register: 'Aquí no se atribuye formalidad a la palabra: el tono depende de la oración y de la relación entre las personas.',
      transfer: 'Escribe a tu grupo para proponer una reunión útil. Explica por qué productive expresa tu intención.'
    },
    deadline: {
      word: 'deadline', context: 'The deadline is Friday, so please submit your essay before then.',
      clue: 'Relaciona “Friday” con “submit your essay before then”: ¿qué límite establece la frase?',
      meaning: 'Fecha u hora límite para terminar o entregar algo.',
      other: 'No equivale a la duración de la tarea: “three hours” dice cuánto dura; “Friday” fija el límite.',
      pattern: 'meet a deadline / miss a deadline / extend a deadline.',
      example: 'Could we extend the deadline to Monday?',
      register: 'Deadline aparece en contextos académicos y cotidianos. La cortesía de una petición depende de cómo se formule.',
      transfer: 'Pide a un compañero acordar una fecha límite para su proyecto. Usa deadline y explica el destinatario que elegiste.'
    }
  },
  model: 'Dear Professor,\nCould I have an extension until Friday? I need more time to review my essay.\nThank you for considering my request.\nBest regards,\nAlex'
});
