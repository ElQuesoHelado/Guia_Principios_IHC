# Análisis de Usuarios y Especificación de Tareas · Lingua IA

Este documento formaliza el **Análisis de Usuarios Objetivo** y el **Análisis Jerárquico de Tareas (HTA)** para el prototipo interactivo **Lingua IA**, en el marco de la disciplina de **Interacción Humano-Computador (IHC)** y fundamentado en los principios cognitivos de *Designing with the Mind in Mind* (Jeff Johnson).

---

## 1. Análisis de Potenciales Grupos de Usuarios (Usuarios Objetivo)

Para garantizar un diseño centrado en el usuario (UCD), se identifican y caracterizan dos perfiles representativos: un **Grupo Primario**, sobre el cual se calibran todas las decisiones de interacción, densidad de información y soporte cognitivo; y un **Grupo Secundario**, que representa un escenario de uso avanzado y extensión del sistema.

```
                    ┌────────────────────────────────────────────────────────┐
                    │               UNIVERSO DE APRENDICES                   │
                    └──────────────────────────┬─────────────────────────────┘
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       ▼                                               ▼
     ┌───────────────────────────────────┐           ┌───────────────────────────────────┐
     │  GRUPO 1: USUARIO PRIMARIO (CORE) │           │  GRUPO 2: USUARIO SECUNDARIO      │
     │  Estudiante universitario B1–B2   │           │  Estudiante avanzado / B2+ a C1   │
     │  • Sesiones cortas e itinerantes  │           │  • Refinamiento de tono y estilo  │
     │  • Práctica escrita y por chat    │           │  • Preparación profesional alta   │
     │  • Foco: Reducción de ansiedad    │           │  • Foco: Precisión pragmática     │
     └───────────────────────────────────┘           └───────────────────────────────────┘
```

---

### Grupo 1: Estudiante Universitario de Nivel Intermedio (B1–B2)
> **Perfil:** Usuario Primario (Core User / Persona Central de Diseño).

* **a) Rango de edades, cultura y lenguaje:**
  * **Edad:** 18 a 25 años.
  * **Perfil cultural:** Nativo digital, inmerso en entornos universitarios latinoamericanos e hispanohablantes.
  * **Idioma nativo (L1):** Español.
  * **Idioma objetivo (L2):** Inglés intermedio (estratos B1–B2 según el MCER).

* **b) Educación y antecedentes formativos:**
  * Estudiante de pregrado en curso (diversas facultades: ingeniería, humanidades, ciencias sociales, negocios, ciencias de la salud, etc.).
  * Alfabetización completa, alta competencia lectora y dominio de la producción escrita académica en su lengua materna.
  * Formación previa en inglés escolar o institutos básicos; posee nociones de sintaxis y reglas generales, pero carece de práctica autónoma estructurada y continua.

* **c) Conocimientos específicos y competencias en el dominio:**
  * Domina las estructuras gramaticales básicas e intermedias (tiempos verbales simples y continuos, conectores elementales).
  * Manifiesta inseguridad y vacilación al momento de redactar textos formales (correos institucionales, solicitudes académicas, cartas de presentación).
  * Su vocabulario activo es reducido respecto a su vocabulario pasivo: reconoce términos al leerlos en un artículo, pero le cuesta evocarlos espontáneamente al componer un mensaje (*principio de reconocimiento frente a recuerdo*).
  * Experimenta una notable ansiedad comunicativa (*filtro afectivo* de Krashen) frente a la interacción en tiempo real; prefiere componer mensajes mediante turnos controlados de texto antes que exponerse a la conversación oral directa.

* **d) Limitaciones físicas, sensoriales y cognitivas:**
  * **Físicas y sensoriales:** Sin discapacidades motrices ni sensoriales severas. Requiere interfaces con tipografía legible, jerarquía visual definida y contrastes normalizados (WCAG AA) para evitar la fatiga visual durante sesiones de estudio nocturnas o frente a pantallas pequeñas.
  * **Cognitivas:** Memoria de trabajo limitada ante tareas complejas de doble procesamiento cognitivo (generar el contenido de la idea y simultáneamente traducir/adecuar la sintaxis al inglés). Es altamente vulnerable a la sobrecarga cognitiva cuando una herramienta le presenta listas extensas y descontextualizadas de errores.

* **e) Experiencia con la tecnología y herramientas habituales:**
  * **Competencia digital:** Muy alta. Uso diario e intensivo de laptops, tabletas y teléfonos inteligentes.
  * **Ecosistema habitual:** Procesadores de texto (Google Docs, Word), aplicaciones de mensajería instantánea (WhatsApp, Telegram, Discord), traductores automáticos contextuales (DeepL, Google Translate) y diccionarios digitales (WordReference, Cambridge Dictionary).
  * **Comportamiento tecnológico:** Familiarizado con interfaces reactivas, patrones de chat conversacional, navegación ágil por pestañas y retroalimentación interactiva inmediata.

* **f) Motivación, metas y actitud frente al sistema:**
  * **Motivación extrínseca:** Requisitos de graduación universitaria, postulación a intercambios académicos, pasantías profesionales o mejora de su perfil de empleabilidad.
  * **Motivación intrínseca:** Superar la barrera de timidez idiomática, redactar con fluidez y naturalidad, y prescindir gradualmente de los traductores automáticos de copiar y pegar.
  * **Actitud y tolerancia al error:** Actitud proactiva pero cautelosa. Tolera el error como parte del aprendizaje, pero se frustra ante explicaciones abstractas, confusas o correcciones automáticas que no justifican el motivo ("alucinaciones" o respuestas opacas de la IA). Requiere explicaciones claras, situadas y verificables donde él o ella mantenga siempre la decisión final.

* **g) Experiencia en el dominio del aprendizaje autónomo:**
  * Aprendiz en proceso de consolidación. Rara vez tiene oportunidad de interactuar con angloparlantes nativos en su rutina; su práctica es solitaria, asíncrona y depende fuertemente de aplicaciones digitales.
  * Tiende a estudiar de manera fragmentada y se beneficia enormemente del andamiaje (*scaffolding*) pedagógico que descompone las tareas en pasos acotados y manejables.

* **h) Ambiente de trabajo y contexto socio-físico:**
  * **Contexto de uso:** Práctica fragmentada en micro-sesiones (10 a 25 minutos) entre clases, en bibliotecas universitarias, salas de estudio, transporte público o en casa.
  * **Multidispositivo:** Emplea la laptop para sesiones de redacción extendida y el smartphone para lecturas ágiles, consulta rápida de términos y práctica conversacional interactiva por chat.
  * **Condición acústica ambiental:** Frecuenta espacios públicos o compartidos de silencio estricto (bibliotecas y salas de cómputo) o entornos con ruido moderado (transporte, cafeterías) donde hablar en voz alta o utilizar audios/micrófono resulta inviable, molesto o motivo de vergüenza. La interacción conversacional basada exclusivamente en texto se adapta de manera idónea a esta realidad física y social.

* **i) Relaciones y patrones de comunicación:**
  * Mantiene comunicación académica asíncrona con profesores y tutores vía correo electrónico, enfrentando a menudo demoras prolongadas para recibir correcciones.
  * Al no contar con un interlocutor de habla inglesa accesible para practicar, percibe a la IA interactiva como un acompañante seguro, paciente, disponible bajo demanda y libre del temor al juicio o la vergüenza social.

---

### Grupo 2: Estudiante Universitario Avanzado o Egresado (B2+ a C1)
> **Perfil:** Usuario Secundario (Advanced Learner / Perfil de Extensión).

* **a) Rango de edades, cultura y lenguaje:**
  * **Edad:** 21 a 35 años.
  * **Perfil cultural:** Estudiantes de últimos semestres universitarios, tesistas, postulantes a posgrados o profesionales junior en proceso de inserción laboral internacional.
  * **Idioma nativo (L1):** Español.
  * **Idioma objetivo (L2):** Inglés avanzado (B2+ a C1 según el MCER).

* **b) Educación y antecedentes formativos:**
  * Estudios de pregrado culminados o en fase de titulación. Experiencia en redacción técnica, lectura de bibliografía especializada en inglés y preparación de exámenes estandarizados (TOEFL iBT, IELTS, Cambridge Advanced).

* **c) Conocimientos específicos y competencias en el dominio:**
  * Gramática estructural consolidada y vocabulario general fluido.
  * Sus necesidades formativas se enfocan en la naturalidad discursiva, el dominio de colocaciones precisas (*collocations*), verbos compuestos (*phrasal verbs*), modismos contextuales y, en especial, la calibración fina del tono formal y corporativo.
  * Busca eliminar calcos del español ("spanglish" conceptual) y afinar la sutileza pragmática de sus argumentos escritos.

* **d) Limitaciones físicas, sensoriales y cognitivas:**
  * Sin limitaciones físicas ni cognitivas significativas. Posee mayor resistencia a la fatiga lectora y mayor capacidad de memoria de trabajo, pero rechaza tajantemente la fricción de interfaces poco directas, con demasiados clics o con pasos protocolarios que no agreguen valor.

* **e) Experiencia con la tecnología:**
  * Muy alta. Usuario intensivo de plataformas colaborativas, gestores de tareas, suites ofimáticas en la nube y modelos de lenguaje para propósitos específicos. Exige transparencia algorítmica, rapidez de respuesta y control explícito de cambios.

* **f) Motivación, metas y actitud frente al sistema:**
  * **Metas concretas:** Redactar propuestas de investigación (*abstracts*), cartas de motivación de alta competitividad (*Statements of Purpose*), correos a comités evaluadores y simular entrevistas de trabajo para compañías multinacionales.
  * **Actitud frente a la IA:** Crítica y exigente. Tiene tolerancia mínima a correcciones triviales de nivel elemental; busca un editor de estilo que justifique matices pragmáticos y le permita decidir sobre cada sugerencia mediante comparaciones directas.

* **g) Experiencia en el aprendizaje autónomo:**
  * Alta autonomía. Consume fuentes originales complejas (artículos académicos, podcasts de industria, noticias globales). Utiliza la herramienta como un entorno de pulido y verificación puntual.

* **h) Ambiente de trabajo y contexto socio-físico:**
  * Entornos profesionales, laboratorios o despachos de estudio. Sesiones de trabajo más largas y focalizadas en computadora de escritorio o portátil, complementadas con revisiones móviles.

* **i) Relaciones y patrones de comunicación:**
  * Interacciones formales con docentes internacionales, comités de becas o clientes remotos. Utiliza la simulación conversacional por texto para entrenar la agilidad argumentativa y el uso de terminología técnica en turnos dinámicos de intercambio.

---

### Cuadro Comparativo de Grupos de Usuarios

| Dimensión de Análisis | Grupo 1: Intermedio B1–B2 (Usuario Primario) | Grupo 2: Avanzado B2+–C1 (Usuario Secundario) |
|---|---|---|
| **Meta Principal** | Superar bloqueos, corregir errores gramaticales y ganar confianza. | Refinar tono, naturalidad idiomática y precisión pragmática. |
| **Principal Obstáculo** | Ansiedad comunicativa, vocabulario activo escaso y dudas de sintaxis. | Uso no idiomático del lenguaje (calcos del español) y calibración del registro formal. |
| **Rol de Lingua IA** | Tutor pedagógico paciente, con andamiaje estructurado y pistas graduales. | Asistente de edición avanzada y *sparring* para simulaciones interactivas. |
| **Interacción Conversacional** | Chat interactivo por turnos breves, con pistas contextuales y sin voz. | Chat técnico/profesional simulado para agilidad de argumentación escrita. |
| **Tolerancia a Explicaciones** | Requiere explicaciones directas, reglas concisas y ejemplos contrastados. | Valora justificaciones lingüísticas profundas y alternativas de estilo. |

---

## 2. Análisis Jerárquico de Tareas (HTA - Hierarchical Task Analysis)

En correspondencia con el alcance funcional y arquitectónico de **Lingua IA** establecido en `agents.md`, el sistema modela tres actividades clave para la práctica deliberada y autónoma del idioma. A continuación se detalla cada tarea bajo estándares formales de IHC:

```
                            ┌──────────────────────────────────────────────┐
                            │          TAREAS NÚCLEO EN LINGUA IA          │
                            └──────────────────────┬───────────────────────┘
                                                   │
           ┌───────────────────────────────────────┼───────────────────────────────────────┐
           ▼                                       ▼                                       ▼
 ┌───────────────────────────┐           ┌───────────────────────────┐           ┌───────────────────────────┐
 │   TAREA 1: REDACCIÓN      │           │   TAREA 2: CONVERSACIÓN   │           │    TAREA 3: LECCIONES     │
 │        ASISTIDA           │           │   INTERACTIVA POR TEXTO   │           │       Y VOCABULARIO       │
 │ Modo: 'writing'           │           │ Modo: 'conversation'      │           │ Modo: 'lessons'           │
 │ • Correo formal           │           │ • Chat en turnos breves   │           │ • Lectura de artículo     │
 │ • Tarjetas de diff        │           │ • Pistas graduales        │           │ • Popover contextual      │
 │ • Aceptar / Rechazar      │           │ • Sin voz / Baja ansiedad │           │ • Glosario en sesión      │
 └───────────────────────────┘           └───────────────────────────┘           └───────────────────────────┘
```

---

### Tarea 1: Redactar y Revisar un Correo Electrónico Formal de Solicitud
* **Identificador de Sistema:** `T1` | **Modo de Interfaz:** `writing` (Redacción asistida)
* **Objetivo del Usuario:** Producir y validar un correo electrónico formal en inglés (ej. solicitud de prórroga académica, postulación a una beca o petición de reunión con un docente o autoridad), garantizando que el mensaje cumpla con las normas de cortesía, corrección sintáctica, claridad y registro apropiado mediante la inspección y decisión sobre sugerencias asistidas por IA.
* **Precondiciones:**
  1. El usuario tiene definido el propósito comunicativo, la petición concreta y el destinatario (o cargo institucional).
  2. Dispone de un borrador preliminar (o selecciona el caso guiado del sistema).
  3. La interfaz `writing` se encuentra activa, con el editor de texto y el panel de criterios sincronizados.

#### Descomposición Jerárquica de Subtareas:

```
0. Redactar y revisar correo formal de solicitud
   1.0 Planificar la estructura y parámetros del mensaje
       1.1 Determinar el destinatario y establecer el nivel de formalidad (formal vs. semi-formal)
       1.2 Delimitar el propósito central y los argumentos de respaldo necesarios
       1.3 Formular una línea de asunto (Subject) concisa y representativa
   2.0 Redactar el borrador inicial
       2.1 Redactar el saludo formal protocolar (ej. "Dear Professor...", "Dear Admissions Committee")
       2.2 Redactar el cuerpo del mensaje (presentación personal, justificación y solicitud explícita)
       2.3 Incluir fecha límite o detalles logísticos requeridos
       2.4 Redactar la fórmula de cortesía de cierre y firma protocolar
   3.0 Revisar asistidamente con el soporte de Lingua IA
       3.1 Inspeccionar la tarjeta de sugerencia activa presentada junto al texto (enfoque unificado)
       3.2 Comparar el fragmento original contra la propuesta mediante la visualización de diferencias (diff)
       3.3 Consultar la categoría del cambio (Gramática, Vocabulario, Tono o Claridad) y la justificación breve
       3.4 Evaluar la sugerencia: aceptar el cambio (actualizando el texto) o rechazarlo (conservando el original)
       3.5 Navegar a la siguiente corrección manteniendo la visibilidad del avance global
   4.0 Validar y transferir el resultado final
       4.1 Efectuar una lectura integral de verificación del texto definitivo en el editor
       4.2 Constatar el estado de las metas en el panel de criterios y progreso
       4.3 Copiar el contenido final al cliente de correo institucional para su envío
```

* **Postcondiciones:**
  * El texto del correo está libre de errores sintácticos y léxicos críticos, cuenta con un tono formal homogéneo y el usuario ha comprendido el porqué de cada modificación adoptada.
* **Puntos de Dolor y Manejo de Excepciones (IHC):**
  * *Excepción 1.1: El usuario desconoce la fórmula de tratamiento adecuada para una autoridad académica.*  
    **Mitigación en interfaz:** El panel lateral de reglas y criterios provee plantillas de apertura formal verificadas.
  * *Excepción 1.2: La IA propone un cambio que altera el significado pretendido o vuelve el texto frío/impersonal.*  
    **Mitigación en interfaz:** Principio de agencia y control (*human-in-the-loop*); el usuario rechaza la propuesta con un solo clic (`data-action="reject-correction"`), sin penalización ni degradación del texto original.
  * *Excepción 1.3: Fatiga por sobrecarga informativa o exceso de correcciones simultáneas.*  
    **Mitigación en interfaz:** Presentación atencional secuenciada (una corrección a la vez, con colores e iconos distintivos por categoría: rojo para gramática, azul para vocabulario, gris para tono y amarillo para claridad).
* **Restricciones y Frecuencia de Uso:**
  * **Ambiente:** Requiere atención visual focalizada y conexión a la interfaz web.
  * **Frecuencia:** Semanal o quincenal, vinculada a hitos académicos y laborales.

---

### Tarea 2: Participar en una Simulación Conversacional Interactiva Basada en Texto
* **Identificador de Sistema:** `T2` | **Modo de Interfaz:** `conversation` (Conversación escrita)
* **Objetivo del Usuario:** Desarrollar soltura discursiva, velocidad de formulación en inglés y adecuación contextual mediante un diálogo interactivo guiado por turnos breves en un entorno simulado de baja ansiedad (ej. entrevista de trabajo técnica, interacción de atención profesional o *networking*), gestionando la formulación mediante mensajes de texto y apoyo de pistas graduales sin recurrir a audio ni voz.
* **Justificación de Diseño e IHC (Interacción 100% Basada en Texto):**
  * **Eliminación del filtro afectivo y la ansiedad:** Hablar en voz alta en un idioma extranjero genera inhibición y estrés en estudiantes B1–B2. La interacción textual permite una pausa reflexiva para estructurar la sintaxis antes de emitir la respuesta.
  * **Compatibilidad ambiental real:** Los estudiantes practican en salas de lectura, bibliotecas o transporte; el uso de micrófono o altavoces es inviable o invasivo en dichos espacios. El texto permite una práctica discreta, autónoma y accesible en cualquier momento y lugar.
  * **Turnos breves y control del ritmo:** En lugar de demandar respuestas orales instantáneas, la interfaz de chat en turnos controlados sitúa al estudiante como dueño del tiempo de respuesta, permitiéndole solicitar pistas graduales si sufre un bloqueo léxico.
* **Precondiciones:**
  1. El usuario selecciona el escenario temático de interacción (ej. entrevista laboral para una pasantía internacional).
  2. Dispositivo con pantalla y teclado funcional (laptop o smartphone) con el módulo `conversation` activo.
  3. No se requiere micrófono, auriculares, grabación de audio ni aislamiento acústico ambiental.

#### Descomposición Jerárquica de Subtareas:

```
0. Simular conversación interactiva mediante turnos de texto
   1.0 Configurar e iniciar el escenario conversacional
       1.1 Seleccionar el escenario simulado en el menú (ej. "Job Interview: Software Intern")
       1.2 Leer la descripción del contexto, el rol del interlocutor virtual y la meta comunicativa
       1.3 Revisar la lista de expresiones clave y vocabulario de apoyo en el panel lateral
   2.0 Recibir e interpretar el turno del interlocutor virtual
       2.1 Leer el mensaje de apertura o pregunta formulada por el tutor virtual en la ventana de chat
       2.2 Analizar la intención pragmática del mensaje (ej. solicitud de describir un reto superado)
       2.3 Identificar conectores o términos relevantes presentes en el turno entrante
   3.0 Formular y redactar la respuesta escrita
       3.1 Activar el área de composición de texto (*chat composer*)
       3.2 Elaborar la respuesta por escrito manteniendo la coherencia discursiva con el turno previo
       3.3 (Opcional ante bloqueo léxico o duda estructural): Solicitar una pista gradual mediante
           el botón de ayuda contextual ("Pedir pista / Hint") para obtener un andamiaje sintáctico
       3.4 Efectuar una revisión rápida del mensaje escrito en el campo de entrada
       3.5 Presionar la acción de envío (tecla Enter o botón de enviar) para ceder el turno al sistema
   4.0 Analizar la retroalimentación y proseguir el diálogo
       4.1 Observar la respuesta contextual generada por el agente virtual que da continuidad al intercambio
       4.2 Verificar en el panel lateral el registro de expresiones empleadas y el contador de turnos
       4.3 Repetir el ciclo de lectura-formulación-envío durante los turnos previstos para la simulación
   5.0 Concluir la sesión y repasar el intercambio
       5.1 Finalizar la conversación al alcanzar el objetivo del escenario o completar los turnos pautados
       5.2 Revisar el historial consolidado de mensajes intercambiados en la sesión
       5.3 Contrastar el léxico utilizado con las recomendaciones y notas de aprendizaje del escenario
```

* **Postcondiciones:**
  * El estudiante completa satisfactoriamente el intercambio simulado de 4 a 6 turnos, habiendo formulado respuestas completas en inglés formal/profesional, superado eventuales bloqueos mediante pistas escritas y retenido expresiones clave sin la sobrecarga emocional de la evaluación oral.
* **Puntos de Dolor y Manejo de Excepciones (IHC):**
  * *Excepción 2.1: El estudiante sufre bloqueo léxico ("mente en blanco") y no sabe cómo iniciar la contestación.*  
    **Mitigación en interfaz:** Sistema de ayuda gradual (*scaffolding*). El botón de pistas ofrece en primer término un conector de apertura (ej. *"In my previous experience, I handled..."*); si insiste, sugiere una estructura completa de respuesta.
  * *Excepción 2.2: El estudiante no comprende el significado de un término dentro de la pregunta del agente virtual.*  
    **Mitigación en interfaz:** El estudiante puede realizar una consulta rápida escribiendo su duda directamente en el chat activo o consultar el panel lateral de expresiones del escenario sin abandonar la pantalla.
  * *Excepción 2.3: La IA responde de manera desalineada o excesivamente extensa.*  
    **Mitigación en interfaz:** En Lingua IA las respuestas de simulación están diseñadas en turnos concisos (máximo 2 a 3 oraciones), formulando preguntas claras para sostener el foco cognitivo (C1 y C3 de Johnson).
* **Restricciones y Frecuencia de Uso:**
  * **Ambiente:** Totalmente silencioso o ruidoso indiferentemente; se ejecuta en cualquier lugar al no requerir entrada/salida de audio.
  * **Frecuencia:** Sesiones ágiles de 10 a 15 minutos, 3 a 5 veces por semana.

---

### Tarea 3: Adquirir y Consolidar Vocabulario a Partir de un Artículo Corto
* **Identificador de Sistema:** `T3` | **Modo de Interfaz:** `lessons` (Lecciones y repaso)
* **Objetivo del Usuario:** Incorporar nuevo léxico académico y profesional en inglés mediante la lectura comprensiva de un artículo auténtico breve, accediendo a definiciones contextuales, ejemplos y notas de uso con interacción *in-situ* (un solo clic) y almacenando los términos en su glosario personal de sesión sin cambiar de ventana.
* **Precondiciones:**
  1. El usuario accede al módulo `lessons` de Lingua IA.
  2. Dispone del artículo de muestra precargado en la interfaz (o pega un texto de su interés en el espacio provisto).
  3. El panel lateral de vocabulario se encuentra disponible para registrar los términos seleccionados.

#### Descomposición Jerárquica de Subtareas:

```
0. Adquirir vocabulario en contexto a partir de lectura breve
   1.0 Realizar lectura comprensiva del artículo
       1.1 Efectuar una lectura exploratoria global del texto para captar la temática general
       1.2 Localizar términos resaltados o palabras de vocabulario avanzado en su contexto oracional
   2.0 Consultar el significado situado de la palabra (Inspección in-situ)
       2.1 Tocar o hacer clic directamente sobre el término resaltado en el cuerpo del texto
       2.2 Observar el despliegue del componente contextual flotante (*popover* / tarjeta de definición),
           ubicado inmediatamente adyacente a la palabra para no perder el punto de fijación ocular
       2.3 Leer la definición específica para la acepción en uso, la categoría gramatical y la traducción
       2.4 Examinar las oraciones de ejemplo contextual que ilustran colocaciones habituales
   3.0 Guardar y gestionar el término en el glosario personal
       3.1 Presionar la acción "Guardar palabra" (*Save word*) dentro del popover interactivo
       3.2 Constatar la confirmación visual inmediata: la palabra cambia a estado "guardada" en el texto
       3.3 Verificar que el término se agregue de manera reactiva a la lista del panel lateral de vocabulario
   4.0 Afianzar el léxico y evaluar el progreso
       4.1 Abrir el panel de vocabulario para repasar el conjunto de palabras capturadas en la sesión
       4.2 (Opcional): Utilizar el campo de consulta/práctica de la actividad para redactar una oración propia
       4.3 Comprobar el avance de la sesión mediante el indicador de progreso ("Palabras guardadas")
```

* **Postcondiciones:**
  * El usuario comprende el significado preciso del término en el contexto leído, lo almacena en su lista de estudio y refuerza su memoria a largo plazo mediante ejemplos contrastados, sin haber sufrido la distracción de alternar entre múltiples pestañas del navegador.
* **Puntos de Dolor y Manejo de Excepciones (IHC):**
  * *Excepción 3.1: Ruptura del flujo de lectura por necesidad de abrir traductores externos (efecto "alt-tab").*  
    **Mitigación en interfaz:** Cumplimiento estricto del Principio C1.1 y C5.1 (Jeff Johnson); la información se muestra adyacente al foco visual primario mediante un popover contextual ligero, suprimiendo la sobrecarga de navegación.
  * *Excepción 3.2: Confusión ante palabras polisémicas (con múltiples significados según el diccionario).*  
    **Mitigación en interfaz:** El sistema prioriza exclusivamente la acepción correspondiente al contexto de la lectura activa, evitando que el estudiante deba discernir entre docenas de definiciones irrelevantes.
  * *Excepción 3.3: Olvido de términos consultados durante la lectura.*  
    **Mitigación en interfaz:** Persistencia visual en el panel lateral (*principio de reconocimiento frente a recuerdo*, C4 de Johnson); la lista de palabras guardadas permanece visible y accesible en todo momento.
* **Restricciones y Frecuencia de Uso:**
  * **Ambiente:** Apto para lectura en pantallas de laptop o dispositivos móviles; textos breves (200–400 palabras) para evitar fatiga cognitiva.
  * **Frecuencia:** 2 a 4 veces por semana, en bloques de 15 a 20 minutos.

---

## 3. Matriz de Trazabilidad: Tareas, Módulos y Principios Cognitivos de IHC

La siguiente matriz sintetiza el vínculo directo entre las tareas descritas, los componentes de la interfaz de **Lingua IA** y los fundamentos cognitivos del libro *Designing with the Mind in Mind* (Jeff Johnson):

| Tarea Analizada | Modo Lingua IA | Componentes Clave en Interfaz | Principios IHC Aplicados (*Jeff Johnson*) |
|---|---|---|---|
| **T1: Redacción de Correo Formal** | `writing` | • Tarjeta de sugerencia (`.correction-card`)<br>• Visualización de diferencias (`.diff-line`)<br>• Selector de acciones Aceptar / Rechazar<br>• Barra de etapas (`#stagebar`) | • **C1.1 / C1.2:** Percepción estructurada e información visual situada.<br>• **C3.1–C3.4:** Reducción de carga en la memoria de trabajo.<br>• **C7.5 / C7.7:** El usuario retiene el control final sobre las acciones de la IA. |
| **T2: Simulación Conversacional por Texto** | `conversation` | • Ventana de chat interactivo (`#chat-messages`)<br>• Compositor con botón de pista (`#chat-composer`)<br>• Panel lateral de expresiones clave<br>• Contador de turnos y avance | • **C2.1 / C2.2:** Atención guiada y turnos secuenciales acotados.<br>• **C7.1 / C7.8:** Asistencia gradual (*hints*) ante bloqueos sin resolver la tarea completa.<br>• **Exclusión deliberada de voz:** Supresión de ansiedad afectiva y viabilidad en espacios públicos silenciosos. |
| **T3: Adquisición Contextual de Vocabulario** | `lessons` | • Texto enriquecido con palabras interactivas<br>• Popover flotante de definición in-situ<br>• Panel lateral de vocabulario guardado<br>• Pestaña de progreso contextual | • **C4.1 / C4.5:** Reconocimiento superior al recuerdo (términos visibles en lista).<br>• **C5.1 / C5.3:** Eliminación de cambios de contexto y distractores externos.<br>• **C6.2 / C6.6:** Diseño tipográfico optimizado para la lectura comprensiva fluida. |

---

## 4. Conclusión de la Evaluación de IHC

El análisis de usuarios y la descomposición jerárquica de tareas evidencian que **Lingua IA** resuelve de manera coherente las necesidades del estudiante universitario intermedio:
1. **Sustitución de la conversación oral por diálogo interactivo en texto:** Constituye una decisión de diseño deliberada y pedagógicamente fundada que democratiza la práctica autónoma en espacios académicos reales (bibliotecas y aulas), reduce radicalmente la ansiedad social y brinda el tiempo de procesamiento necesario para estructurar respuestas de calidad.
2. **Asistencia verificable y no invasiva:** Cada sugerencia de redacción y definición de vocabulario se expone de forma situada, permitiendo la comparación inmediata y otorgando siempre la última palabra al estudiante.
3. **Optimización atencional:** Al integrar la consulta de reglas, vocabulario y pistas en paneles contextuales sincronizados, el sistema evita la fragmentación provocada por aplicaciones externas, minimizando la carga en la memoria de trabajo y favoreciendo la retención a largo plazo.
