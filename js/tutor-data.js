/* Material didáctico escrito para la demo. No procede de una consulta en vivo. */
window.TutorData = Object.freeze({
  tasks: { email: 'Correo en inglés', vocab: 'Vocabulario en contexto', general: 'Por explorar' },
  stages: {
    email: ['Comprender y comparar', 'Escribir y decidir', 'Recuperar sin modelo', 'Usar en otra situación'],
    vocab: ['Inferir en contexto', 'Contrastar y relacionar', 'Recordar sin definición', 'Usar en otro contexto']
  },
  starters: {
    email: 'Quiero aprender a hacer peticiones en inglés usando un correo',
    vocab: 'Quiero entender “dedicated” en esta frase: “A dedicated space helps you focus on your work.”'
  },
  examples: {
    email: 'Quiero aprender a pedir una prórroga a mi profesora en inglés. Compara una petición cercana con una más cortés y explícame la diferencia sin escribir todo el correo.',
    review: 'Revisa el tono de este correo a mi profesora y conserva el resto:\nDear Professor,\nI want you to send me the notes.\nI am agree with the deadline.\nBest regards,\nAlex',
    vocab: '¿Qué significa dedicated en “A dedicated space helps you focus on your work”? Quiero inferir su significado antes de ver la definición.',
    subject: 'Quiero aprender a expresar el asunto en inglés. Compara request for y question about para comprender qué significa cada expresión.',
    greeting: 'Quiero comparar Dear y Hi en saludos en inglés y explicar cuándo usar cada uno.',
    request: 'Quiero aprender cómo se construyen las peticiones con can y could en inglés.',
    reason: 'Quiero aprender a expresar una razón con because y una finalidad con to + verbo en inglés.',
    closing: 'Quiero comprender la diferencia entre Best regards y Thanks como cierre en inglés.',
    ambiguous: 'Quiero mejorar mi inglés'
  },
  emailLessons: {
    subject: {
      label: 'Expresar el asunto', title: 'Qué comunican request for y question about', hta: 'C1.1; C3.1',
      intro: 'El asunto permite practicar cómo expresar una solicitud o una duda en inglés. Compara el significado de estas expresiones y adapta una a tu intención.',
      examples: [
        ['Request for lecture notes', 'Request for introduce lo solicitado; lecture notes se refiere a los apuntes de clase.'],
        ['Request for an extension until Friday', 'Extension expresa una ampliación del plazo; until Friday indica hasta cuándo se pide tiempo. Friday es un dato del ejemplo.'],
        ['Question about the submission deadline', 'Question about introduce el tema de una duda; submission deadline es la fecha límite de entrega.']
      ],
      pattern: 'Request for + lo solicitado; question about + el tema de la duda. Estas expresiones no se vuelven formales solo por ser más largas.',
      prompt: 'Escribe tu propio asunto en inglés para pedir material o aclarar un plazo. Explica qué significa la expresión que elegiste; usa solo los datos que conoces.',
      recall: 'Sin mirar los ejemplos, escribe un asunto en inglés para solicitar material de clase. Explica qué estás pidiendo y qué expresión recordaste.',
      transfer: 'Ahora quieres aclarar la fecha de otra entrega. Escribe un asunto en inglés y explica cómo expresa una duda frente a una solicitud de material.'
    },
    greeting: {
      label: 'Comparar saludos', title: 'Cómo cambian Dear y Hi según la relación', hta: 'C1.2; C3.2',
      intro: 'En un saludo de correo, Dear es una fórmula de apertura; no exige traducirlo literalmente como una expresión de afecto. La relación y las convenciones del contexto orientan la elección.',
      examples: [
        ['Dear Professor Rivera,', 'Professor + apellido utiliza un tratamiento conocido. Úsalo cuando ese sea el tratamiento pertinente; Rivera es solo un ejemplo.'],
        ['Dear Alex Rivera,', 'Dear + nombre completo permite saludar sin atribuir un título o género no confirmado.'],
        ['Hi Alex,', 'Hi + nombre puede encajar con alguien de confianza y en contextos donde esa apertura es habitual. No es una regla universal para todos los compañeros.']
      ],
      pattern: 'Compara la apertura (Dear o Hi) y la forma de dirigirte a la persona (tratamiento y apellido, nombre completo o nombre). Si faltan datos, conserva la duda en vez de inventarlos.',
      prompt: 'Prueba un saludo en inglés y explica qué relación lo hace adecuado. Puedes usar un nombre ficticio indicando que es un ejemplo.',
      recall: 'Sin mirar el modelo, escribe un saludo en inglés para un docente cuyo apellido y tratamiento conoces. Explica la apertura que elegiste.',
      transfer: 'Ahora saludas a alguien de confianza. Produce otra apertura en inglés y explica qué cambió respecto al saludo anterior.'
    },
    request: {
      label: 'Construir una petición', title: 'Entender quién pide qué con can y could', hta: 'C2; C3.3',
      intro: 'Compara el significado, la estructura y el efecto de estas peticiones. Can y could pueden aparecer en peticiones gramaticales; la cortesía depende también de la situación.',
      examples: [
        ['Can you send me the notes?', 'Can + you + verbo en forma base: se pide a la otra persona que envíe los apuntes. Una petición directa puede encajar entre personas de confianza.'],
        ['Could you please send me the notes?', 'Se conserva la intención. Could y please ofrecen una alternativa más cortés; send permanece en forma base.'],
        ['Could I have an extension until Friday?', 'I identifica a quien solicita más tiempo; until Friday concreta hasta cuándo. Cambiar I por you cambia quién realiza la acción.'],
        ['Could you please confirm the submission deadline?', 'Confirm significa confirmar; se pide comprobar la fecha límite de entrega, no ampliar el plazo.']
      ],
      pattern: 'En estas preguntas: can/could + sujeto + verbo en forma base. Compara la persona (I/you), la acción (have/send/confirm) y el matiz de cortesía; no basta con sustituir palabras sin conservar la intención.',
      prompt: 'Escribe una petición propia en inglés. Explica quién solicita qué y una decisión de estructura o cortesía. Puedes practicar solo una frase.',
      recall: 'Sin mirar el modelo, pide más tiempo para una entrega en una frase en inglés. Explica quién recibe ese tiempo y la estructura que recuerdas.',
      transfer: 'Ahora pide material a una persona de confianza. Escribe otra petición en inglés y explica qué significado y qué matiz cambiaron.'
    },
    reason: {
      label: 'Expresar razón y finalidad', title: 'Distinguir because de to + verbo', hta: 'C3.4',
      intro: 'Una razón explica por qué necesitas algo; una finalidad dice para qué. Compara dos recursos del inglés dentro de la misma situación de práctica.',
      examples: [
        ['I need more time because I have two exams this week.', 'Because introduce una oración con sujeto y verbo: I have… Expresa la razón de necesitar tiempo. Es una situación de ejemplo.'],
        ['I need more time to review my essay.', 'To + verbo en forma base (review) expresa aquí la finalidad: para revisar el ensayo. No se añade otro sujeto después de to en esta construcción.']
      ],
      pattern: 'Because + oración para dar una razón; to + verbo en forma base para expresar una finalidad en estos ejemplos. Elige una razón real para tu caso o identifica claramente una situación ficticia de práctica.',
      prompt: 'Expresa en inglés una razón o una finalidad para tu petición. Explica por qué usaste because o to; evita copiar una razón que no corresponde a tu situación.',
      recall: 'Sin mirar los ejemplos, expresa una finalidad en inglés para pedir material de estudio. Explica qué construcción recordaste.',
      transfer: 'En otra situación, explica una razón para pedir aclaraciones sobre una entrega. Usa una oración en inglés y explica qué cambia entre expresar una razón y una finalidad.'
    },
    closing: {
      label: 'Comprender cierres', title: 'Qué expresan Best regards y Thanks', hta: 'C3.5',
      intro: 'Estas fórmulas tienen una función en el intercambio. Comprenderlas permite elegir y reutilizarlas con una razón, además de completar el final del correo.',
      examples: [
        ['Best regards,', 'Fórmula de despedida habitual en correspondencia académica o profesional. Se interpreta como una unidad, no como una traducción palabra por palabra.'],
        ['Thanks,', 'Expresa agradecimiento y puede funcionar como cierre breve cuando encaja con la relación y la petición. No es obligatorio usarlo para todo correo cercano.']
      ],
      pattern: 'Relaciona el significado de la fórmula con el saludo, la petición y el destinatario. Una frase de agradecimiento puede acompañar a otra despedida; las opciones no son etiquetas rígidas de formalidad.',
      prompt: 'Propón un cierre en inglés para tu situación. Explica su función y por qué resulta coherente con tu saludo y petición.',
      recall: 'Sin mirar el modelo, recupera una despedida en inglés para una petición académica. Explica su función.',
      transfer: 'Ahora cierras una petición breve a alguien de confianza. Escribe un cierre en inglés y justifica si mantienes o cambias la fórmula anterior.'
    }
  },
  words: {
    dedicated: {
      word: 'dedicated', context: 'A dedicated space helps you focus on your work.',
      translation: 'Un espacio reservado te ayuda a concentrarte en tu trabajo.',
      clue: 'Mira “space” y “focus on your work”: ¿hablan de una persona o de un espacio con una función?',
      meaning: 'Reservado para una finalidad concreta. En esta oración, el espacio se destina a trabajar.',
      other: '“A dedicated teacher” describe a una persona comprometida. Esa acepción cambia el sentido de “space”.',
      pattern: 'dedicated + sustantivo: a dedicated space / a dedicated desk. También: dedicated to + sustantivo o verbo en -ing.',
      example: 'The library has a dedicated room for group projects.',
      register: 'Estos ejemplos no bastan para etiquetar la palabra como formal o informal. La situación y la acepción importan.',
      transfer: 'Escribe a un compañero para proponer un espacio reservado para su proyecto. Usa dedicated solo si encaja con lo que quieres decir.',
      alternatives: [{
        context: 'She is a dedicated teacher.',
        translation: 'Ella es una profesora comprometida.',
        clue: 'Mira “she” y “teacher”: se describe a una persona. ¿Qué cualidad podría expresar dedicated?',
        meaning: 'Comprometida con su trabajo. Aquí dedicated describe la dedicación de una profesora.',
        other: 'En “a dedicated space” se habla de un espacio reservado para una finalidad. Esa acepción no describe el compromiso de una persona.',
        pattern: 'dedicated + persona o profesión: a dedicated teacher. También: dedicated to + sustantivo o verbo en -ing.',
        example: 'He is a dedicated teacher who cares about his students.',
        transfer: 'Escribe a un compañero sobre una persona comprometida con su trabajo. Usa dedicated y explica qué cualidad quieres destacar.'
      }]
    },
    productive: {
      word: 'productive', context: 'Short breaks help students stay productive during a long study session.',
      translation: 'Las pausas breves ayudan a los estudiantes a seguir trabajando con buenos resultados durante una sesión de estudio larga.',
      clue: 'Relaciona “short breaks” con el resultado de una sesión de estudio: ¿qué ayudan a mantener?',
      meaning: 'Que logra resultados o realiza trabajo útil; aquí se refiere a aprovechar el tiempo de estudio.',
      other: 'En “productive farmland”, se habla de tierras que producen abundantemente. No es el sentido de la sesión de estudio.',
      pattern: 'stay productive / a productive session / a productive meeting.',
      example: 'We had a productive meeting and agreed on the next steps.',
      register: 'Aquí no se atribuye formalidad a la palabra: el tono depende de la oración y de la relación entre las personas.',
      transfer: 'Escribe a tu grupo para proponer una reunión útil. Explica por qué productive expresa tu intención.'
    },
    deadline: {
      word: 'deadline', context: 'Set a deadline for each task so you know when to finish.',
      translation: 'Fija una fecha límite para cada tarea para saber cuándo terminar.',
      clue: 'Relaciona “each task” con “when to finish”: ¿qué límite se propone fijar para cada tarea?',
      meaning: 'Fecha u hora límite para terminar o entregar algo.',
      other: 'No equivale a la duración de la tarea: “three hours” dice cuánto dura; “Friday” fija el límite.',
      pattern: 'meet a deadline / miss a deadline / extend a deadline.',
      example: 'Could we extend the deadline to Monday?',
      register: 'Deadline aparece en contextos académicos y cotidianos. La cortesía de una petición depende de cómo se formule.',
      transfer: 'Pide a un compañero acordar una fecha límite para su proyecto. Usa deadline y explica el destinatario que elegiste.',
      alternatives: [{
        context: 'The deadline is Friday, so please submit your essay before then.',
        translation: 'La fecha límite es el viernes, así que entrega tu ensayo antes de entonces.',
        clue: 'Relaciona “Friday” con “submit your essay before then”: ¿qué límite establece la frase?'
      }]
    }
  },
  model: 'Dear Professor,\nCould I have an extension until Friday? I need more time to review my essay.\nThank you for considering my request.\nBest regards,\nAlex'
});
