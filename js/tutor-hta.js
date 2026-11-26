/* Recorridos didácticos de la v8. Ejemplos preparados, sin servicios externos. */
window.TutorHTA = (() => {
  'use strict';
  let A;
  const copy = x => JSON.parse(JSON.stringify(x));
  const norm = t => String(t || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const cases = {
    notes: {name:'Solicitar apuntes o material', subject:'Request for lecture notes', near:'Can you send me the notes?', polite:'Could you please send me the notes?', reason:'I need the notes to review the lesson.', need:'Qué material necesitas y de qué clase o tema.'},
    extension: {name:'Pedir una prórroga', subject:'Request for an extension', near:'Can I have an extension until [fecha propuesta]?' , polite:'Could I have an extension until [fecha propuesta]?', reason:'I need more time to review my essay.', need:'Qué entrega es, cuál es el plazo vigente y qué fecha quieres proponer.'},
    clarify: {name:'Aclarar una entrega', subject:'Question about the submission deadline', near:'Can you confirm the submission deadline?', polite:'Could you please confirm the submission deadline?', reason:'I want to make sure I submit my work on time.', need:'Qué fecha o forma de presentación necesitas aclarar.'}
  };
  const resourceNames = {model:'Diccionario o modelo',translation:'Traducción',ai:'IA existente',person:'Docente o compañero'};
  function init(api) { A=api; }
  function prepare(s) {
    if (!s.hta) s.hta={email:{cases:[],relation:'unknown',name:'',title:'',facts:{},doubts:[]},entries:[],returns:[],queries:[],productions:[],pendingNotes:[],rootStates:{},originTask:s.task,status:'En práctica'};
    const h=s.hta;
    s.stage=Number.isInteger(s.stage)?Math.max(0,Math.min(3,s.stage)):0;s.stageEvidence=Array.isArray(s.stageEvidence)?s.stageEvidence:[];
    s.word=typeof s.word==='string'?s.word:'';s.context=typeof s.context==='string'?s.context:'';s.inputDraft ||= '';
    h.email ||= {cases:[],relation:'unknown',name:'',title:'',facts:{},doubts:[]};
    h.email.facts ||= {};h.email.doubts ||= [];
    for(const key of ['entries','returns','queries','productions','pendingNotes'])h[key] ||= [];
    h.rootStates ||= {};h.originTask ||= s.task;
    // Conserva las palabras v1, incluso si solo tenían una acepción por nombre.
    for(const word of s.words || []) {
      const context=s.savedContexts?.[word] || (s.word===word && s.context) || A.D.words[word]?.context || '';
      const e=entry(s,word,context);e.saved=true;
    }
    return h;
  }
  function entry(s,word=s.word,context=s.context) {
    const h=s.hta; const key=norm(word)+'|'+A.contextKey(context);
    let e=h.entries.find(e=>e.key===key);
    if(!e){e={id:A.id(),key,word,context,hypothesis:'',interpretation:'',note:'',sources:[],productions:[],reviews:[],saved:false,doubts:[],created:new Date().toISOString()};h.entries.push(e);}
    return e;
  }
  function tracked(s) { return entry(s,s.word,s.context||A.D.words[s.word]?.context||''); }
  function bt(action,label,attrs='',primary=false) { return A.btn('hta-'+action,A.esc(label),attrs,primary); }
  function data(name,value) { return `data-${name}="${A.esc(value)}"`; }
  function wordData(e) { return `${data('entry',e.id)} ${data('word',e.word)} ${data('context',e.context)}`; }
  function chooseEntry(s,el) {
    const e=s.hta.entries.find(e=>e.id===el.dataset.entry);
    if(e){s.word=e.word;s.context=e.context;}return e||tracked(s);
  }
  function ask(s,purpose,text,extra={}) {s.recall=false;s.pending={type:'hta',purpose,label:text,...extra};A.message(s,'text',text);}
  function post(s,view,extra={}) {return A.message(s,'hta','',{view,emailSnapshot:copy(s.hta.email),...(s.task==='vocab'?{entryId:tracked(s).id}:{}),...extra});}
  function remember(s,kind,text,extra={}) {A.evidence(s,kind,text);Object.assign(s.evidence.at(-1),extra);}
  function observe(s,text) {
    prepare(s);if(s.task!=='email')return;
    const t=norm(text),e=s.hta.email;
    const selected=[];
    if(/apuntes|material|lecture notes|send me (the )?notes/.test(t))selected.push('notes');
    if(/prorroga|extension|mas tiempo|more time/.test(t))selected.push('extension');
    if(/aclar|confirm|forma de present|question about the submission/.test(t))selected.push('clarify');
    if(selected.length)e.cases=/combinar|ademas|tambien|ambas/.test(t)?[...new Set([...e.cases,...selected])]:selected;
    if(/relacion desconocida|no conozco|no se quien/.test(t))e.relation='unknown';
    else if(/profesor|docente|teacher|professor/.test(t))e.relation='teacher';
    else if(/companero|amigo|colega|friend/.test(t))e.relation='peer';
    const greeting=text.match(/^Dear\s+([^,\n]+),?/im)||text.match(/^Hi\s+([^,\n]+),?/im);
    const named=text.match(/(?:nombre(?: completo)?|destinatario)\s*:\s*([^\n;]+)/i);
    if(named)e.name=named[1].trim();
    const title=text.match(/tratamiento\s*:\s*([^\n;]+)/i);if(title)e.title=title[1].trim();
    if(greeting){e.name=greeting[1].replace(/^Professor\s+/i,'').trim();if(/^Professor\s+/i.test(greeting[1]))e.title='Professor';}
    for(const [key,re] of Object.entries({current:/fecha vigente\s*:\s*([^\n;]+)/i,proposed:/fecha propuesta\s*:\s*([^\n;]+)/i,material:/material\s*:\s*([^\n;]+)/i,reason:/motivo\s*:\s*([^\n;]+)/i})) {const m=text.match(re);if(m)e.facts[key]=m[1].trim();}
    const until=text.match(/(?:until|hasta)\s+(Friday|Monday|Tuesday|Wednesday|Thursday|Saturday|Sunday|viernes|lunes|martes|miercoles|jueves|sabado|domingo|\d{1,2}(?:[/-]\d{1,2})?)/i);
    if(until)e.facts.proposed=until[1];
  }
  function mainCase(s,m={}) {return m.emailSnapshot?.cases?.[0] || s.hta.email.cases[0] || 'notes';}
  function situation(s,m={}) {return m.emailSnapshot || s.hta.email;}
  function dateLabel(value) {return {lunes:'Monday',martes:'Tuesday',miercoles:'Wednesday',jueves:'Thursday',viernes:'Friday',sabado:'Saturday',domingo:'Sunday'}[norm(value)]||value;}
  function phrase(s,kind,m={}) {
    const c=cases[mainCase(s,m)],e=situation(s,m);
    return c[kind].replace('[fecha propuesta]',dateLabel(e.facts.proposed)||'[fecha propuesta]');
  }
  function meta(s,kind) {
    if(!s.hta)return {};
    if(['compare','model','recall','draft'].includes(kind))return {emailSnapshot:copy(s.hta.email),task:s.task};
    return {};
  }
  function emailStart(s) {prepare(s);if(!s.hta.email.cases.length||s.hta.email.relation==='unknown')post(s,'email-context');}
  function markHelp(s) {if(s.recall){s.helpUsed=true;const e=s.hta.entries.find(e=>e.id===s.hta.attemptEntry);if(e)e.helpUsed=true;}}
  function header(s) {
    const frame=s.hta?.returns.at(-1);
    return frame?`<div class="return-strip"><span>Consulta vinculada · tu ${frame.task==='email'?'correo':'práctica de vocabulario'} sigue guardado</span>${bt('return',frame.task==='email'?'Volver al correo':'Volver al vocabulario')}</div>`:'';
  }
  function intro(s) {return '<details class="rule"><summary>Otros apoyos para esta situación</summary>'+A.actions([bt('situation','Precisar mi situación'),bt('parts','Encontrar una expresión'),bt('resources','Resolver una duda')])+'</details>';}
  function comparison(s,m) {
    return `<p>Ejemplo preparado · misma intención: ${A.esc(cases[mainCase(s,m)].name.toLowerCase())}.</p><section class="card"><h2>La misma intención, otra relación</h2><div class="comparison"><div><span class="badge">Con confianza</span><blockquote lang="en">${A.esc(phrase(s,'near',m))}</blockquote><small>Puede encajar si la relación admite una petición directa.</small></div><div><span class="badge tone">Alternativa más cortés</span><blockquote lang="en">${A.esc(phrase(s,'polite',m))}</blockquote><small>Could suaviza la petición; please puede reforzar la cortesía.</small></div></div><p>Can y could son posibles construcciones gramaticales. La relación y el contexto orientan la elección; una frase más larga no es automáticamente más adecuada.</p>${A.actions([A.btn('write','Escribir mi petición','',true),A.btn('justify','Explicar la diferencia','data-stage="0"'),A.btn('model','Ver el correo completo'),bt('parts','Explorar asunto, saludo y cierre')])}</section>`;
  }
  function model(s,m) {
    const c=cases[mainCase(s,m)];
    const text=`Subject: ${c.subject}\nDear Professor Rivera,\n${c.polite.replace('[fecha propuesta]','Friday')} ${c.reason}\nThank you for your time.\nBest regards,\nAlex`;
    return `<section class="card"><p class="eyebrow">Modelo preparado · nombres y fechas ficticios · no es tu borrador</p><h2>${A.esc(c.name)}</h2><div class="doc-text" lang="en">${A.esc(text)}</div><p>El asunto anticipa la necesidad; el saludo identifica la relación; la petición expresa la intención; el motivo explica una razón pertinente y el cierre conserva un tono coherente. Can, could y please cambian el efecto de la petición, no sus datos.</p>${A.actions([A.btn('write','Probar con mis recursos','',true),bt('parts','Examinar una expresión'),A.btn('recall','Intentar sin el modelo'),bt('identify-model','Explicar la intención y las partes')])}</section>`;
  }
  function entryExtras(s,m) {const e=entry(s,m.word,m.context||A.D.words[m.word]?.context||'');return '<details class="rule"><summary>Explorar pistas, fuentes y producción propia</summary>'+A.actions([bt('lexical-tools','Pistas y patrones',wordData(e)),bt('lexical-note','Redactar mi nota',wordData(e)),bt('vocab-write','Probar una oración',wordData(e)),bt('resources','Contrastar con un recurso',wordData(e)),bt('word-status','Dejar una duda pendiente',wordData(e))])+'</details>';}
  function notebook(s) {
    const h=s.hta;
    return `<h3>Para continuar</h3><p>${A.esc(h.status||'En práctica')} · las dudas y los intentos no se califican automáticamente.</p>${A.actions([bt('resume-plan','Elegir qué retomar'),bt('productions','Comparar mis producciones')])}<h3>Palabras y contextos para repasar</h3>${h.entries.filter(e=>e.saved).map(e=>`<section class="evidence"><strong>${A.esc(e.word)}</strong><p>${A.esc(e.context)}</p>${A.actions([bt('entry-recall','Repasar esta entrada',wordData(e)),bt('unsave-entry','Quitar esta entrada',wordData(e))])}</section>`).join('')||'<p class="small">Puedes guardar cada acepción por separado.</p>'}<h3>Dudas pendientes</h3>${h.pendingNotes.map(n=>`<p>${A.esc(n.text)} <small>· ${A.esc(n.task==='email'?'Correo':'Vocabulario')}</small></p>`).join('')||'<p class="small">Sin dudas registradas todavía.</p>'}`;
  }
  function suspend(s) {return copy({task:s.task,emailTopic:s.emailTopic,stage:s.stage,pending:s.pending,recall:s.recall,recallStart:s.recallStart,helpUsed:s.helpUsed,word:s.word,context:s.context,inputDraft:A.input.value,draft:s.draft,email:s.hta.email,reviewFragment:s.hta.reviewFragment,reviewScope:s.hta.reviewScope,stageEvidence:s.stageEvidence});}
  function beginLink(s,task,origin={}) {
    markHelp(s);const frame={...(s.hta.consultOrigin||suspend(s)),id:A.id(),origin,created:new Date().toISOString()};
    delete s.hta.consultOrigin;s.hta.returns.push(frame);s.hta.reviewFragment=origin.fragment||'';s.hta.reviewScope=null;s.task=task;s.stage=0;s.pending=null;s.recall=false;s.stageEvidence=[];A.input.value='';s.inputDraft='';return frame;
  }
  function back(s) {
    const frame=s.hta.returns.pop();if(!frame){A.message(s,'text','No hay una consulta vinculada a la que volver. Puedes continuar esta práctica o abrir otra desde el historial.');return;}
    const e=s.task==='vocab'?tracked(s):null;
    const result=e ? (e.interpretation||e.note||e.hypothesis||e.reference?.meaning||'Duda pendiente: no hay una interpretación explicada.') : frame.result||s.draft||'Producción pendiente.';
    s.hta.queries.push({id:A.id(),origin:frame.origin,result,entry:e?copy(e):null,date:new Date().toISOString(),partial:e?!(e.interpretation||e.note):!frame.result});
    const draft=s.draft;
    Object.assign(s,{task:frame.task,emailTopic:frame.emailTopic,stage:frame.stage,pending:frame.pending,recall:false,word:frame.word,context:frame.context,helpUsed:frame.helpUsed,stageEvidence:frame.stageEvidence});
    s.hta.email=frame.email;s.hta.reviewFragment=frame.reviewFragment;s.hta.reviewScope=frame.reviewScope;s.draft=frame.draft;s.inputDraft=frame.inputDraft;A.restoreInput(frame.inputDraft);
    if(draft!==frame.draft && s.task==='email')s.versions.push({id:A.id(),label:'Retorno al correo de origen',text:s.draft,date:new Date().toISOString()});
    if(s.task==='email'&&s.draft)A.publishDraft(s);
    post(s,'return-result',{result,origin:frame.origin,entryId:e?.id,entryData:e?copy(e):null,pending:e?!(e.interpretation||e.note):!frame.result});
    A.notice('Retomaste el punto de origen. El resultado de la consulta no modifica tu producción.');
  }
  function consult(s,fragment,versionId) {
    const version=s.versions.find(v=>v.id===versionId)||s.versions.at(-1);
    const text=version?.text||s.draft;
    if(text&&!text.includes(fragment)){ask(s,'fragment','Ese fragmento no coincide con la versión elegida. Copia una frase exacta del correo para conservar su contexto.',{versionId});return;}
    const sentence=text.split(/\n/).find(line=>line.includes(fragment))||fragment;
    const word=Object.keys(A.D.words).find(w=>new RegExp('\\b'+w+'\\b','i').test(fragment));
    if(!word){s.hta.consultSpec={fragment,context:sentence,versionId:version?.id};post(s,'doubt-kind',{fragment,context:sentence});return;}
    beginLink(s,'vocab',{fragment,context:sentence,versionId:version?.id,point:'C4.1'});
    s.word=word;s.context=sentence;
    post(s,'consultation',{fragment,context:sentence});
    if(word){tracked(s);A.clue(s);}else ask(s,'target-word','¿Qué palabra de esta oración quieres contrastar? Escríbela sin cambiar la oración.');
  }
  function selection(el) {
    const selected=window.getSelection();
    if(!selected || selected.isCollapsed)return '';
    const box=el.closest('.card')?.querySelector('.doc-text');
    return box && box.contains(selected.anchorNode) && box.contains(selected.focusNode)?selected.toString().trim():'';
  }
  function render(s,m) {
    const h=s.hta,e=m.emailSnapshot||h.email,c=cases[mainCase(s,m)],esc=A.esc;
    const explain=label=>bt('explain',label,data('topic',label));
    switch(m.view){
      case 'range':return `<section class="card"><h2>¿Qué aparición quieres revisar?</h2>${A.actions(m.hits.map((r,i)=>bt('review-range',`${i+1}. ${r.label}`,`data-start="${r.start}" data-end="${r.end}"`)))}</section>`;
      case 'email-context':return `<section class="card"><h2>Tu intención y lo que falta precisar</h2><p>${e.cases.length?e.cases.map(k=>esc(cases[k].name)).join(' · '):'Puedes contar tu necesidad o explorar un caso.'}</p><p>Relación: ${esc({teacher:'docente',peer:'persona de confianza',unknown:'por comprobar'}[e.relation])}. Nombre: ${esc(e.name||'no indicado')}. Tratamiento: ${esc(e.title||'sin confirmar')}.</p><p>${esc(e.cases.length?c.need:'Elige solo las solicitudes que de verdad necesitas comunicar.')}</p>${A.actions(Object.entries(cases).map(([key,c])=>bt('case',c.name,data('case',key))))}<details class="rule"><summary>Datos aportados y por confirmar</summary>${Object.entries({material:'Material',current:'Fecha vigente',proposed:'Fecha propuesta',reason:'Motivo'}).map(([key,label])=>`<p><strong>${label}:</strong> ${esc(e.facts[key]||'no indicado')}</p>`).join('')}</details><details class="rule"><summary>Precisar relación, datos y dudas</summary>${A.actions([bt('relation','Docente','data-relation="teacher"'),bt('relation','Con confianza','data-relation="peer"'),bt('relation','Relación desconocida','data-relation="unknown"'),bt('facts','Aportar los datos que conozco'),bt('known','Recordar una expresión y señalar mi duda'),bt('combine','Combinar solicitudes necesarias')])}<p>No se deduce un título a partir de un nombre. Puedes conservar datos desconocidos como dudas.</p></details></section>`;
      case 'parts':return `<section class="card"><h2>Encontrar mis expresiones</h2><p>Trabajamos ${esc(c.name.toLowerCase())}. Puedes escribir tu elección en el chat y justificarla.</p>${['subject','greeting','request','reason','closing'].map(key=>`<details class="rule"><summary>${{subject:'Asunto',greeting:'Saludo',request:'Petición',reason:'Motivo',closing:'Cierre'}[key]}</summary>${parts(s,key,m)}${A.actions([bt('try-part','Probar mi expresión',data('part',key)),explain('Cómo elegir '+{subject:'el asunto',greeting:'el saludo',request:'la petición',reason:'el motivo',closing:'el cierre'}[key])])}</details>`).join('')}${A.actions([A.btn('write','Escribir mi correo','',true),A.btn('compare','Comparar dos peticiones'),bt('resources','Resolver una duda')])}</section>`;
      case 'resources':return `<section class="card"><h2>Contrastar una duda concreta</h2><blockquote>${esc(m.fragment||s.context||s.draft||'Puedes indicar tu fragmento en el chat.')}</blockquote><p>Estas vías muestran ejemplos didácticos preparados. También puedes registrar una consulta realizada fuera de la aplicación.</p>${A.actions(Object.entries(resourceNames).map(([key,name])=>bt('resource',name,data('resource',key))))}${A.actions([bt('external','Registrar una respuesta externa'),bt('refine','Precisar la duda que sigue abierta'),bt('pending','Conservar la duda pendiente')])}</section>`;
      case 'resource':return `<section class="card"><p class="eyebrow">Ejemplo preparado · no es una consulta en vivo ni una respuesta real de otra persona</p><h2>${esc(resourceNames[m.resource])}</h2><p>${esc(m.example)}</p>${A.actions([bt('resource-compare','Explicar qué aclara y qué falta'),bt('resources','Contrastar otra vía'),bt('external','Añadir una consulta externa')])}</section>`;
      case 'doubt-kind':return `<section class="card"><h2>¿Qué necesitas comprender?</h2><blockquote>${esc(m.context)}</blockquote>${A.actions([bt('doubt','El significado','data-kind="meaning"'),bt('doubt','La construcción gramatical','data-kind="grammar"'),bt('doubt','El registro o tono','data-kind="register"')])}</section>`;
      case 'consultation':return `<section class="card"><h2>Una duda sin perder el correo</h2><blockquote>${esc(m.context)}</blockquote><p>Fragmento: ${esc(m.fragment)}. El correo y la actividad de origen siguen guardados. Puedes volver aunque la duda quede pendiente.</p>${A.actions([bt('resources','Elegir un recurso'),bt('return','Volver al correo')])}</section>`;
      case 'return-result':return `<section class="card"><h2>Retomamos tu producción</h2><blockquote>${esc(m.origin.context||m.origin.fragment||'Producción de origen')}</blockquote><p>${esc(m.result)}</p>${m.entryData?`<details class="rule"><summary>Contexto, patrón y dudas de la consulta</summary><p>${esc(m.entryData.context)}</p><p>${esc(m.entryData.reference?.pattern||'Patrón pendiente de contraste.')}</p><p>${esc(m.entryData.doubts.join(' · ')||'No se registró otra duda.')}</p>${m.entryData.sources.map(source=>`<p class="small">${esc(source.kind==='prepared'?'Ejemplo preparado':source.reference||'Aporte externo no verificado')}</p>`).join('')}</details>`:''}<p class="note">${m.pending?'Consulta parcial: contrasta el resultado antes de usarlo.':'Explicación propia registrada: comprueba si conserva tu intención.'}</p>${A.actions([bt('resource-compare','Explicar cómo afecta a mi expresión'),A.btn('write','Reformular con mis palabras'),bt('pending','Dejar lo incierto para después')])}</section>`;
      case 'lexical-tools':return lexicalTools(s,m);
      case 'note-result':return `<section class="card"><h2>${esc(m.title)}</h2><p>${esc(m.text)}</p>${A.actions([bt('resources','Contrastar otra fuente'),bt('productions','Comparar mis producciones'),bt('pending','Anotar una duda')])}</section>`;
      case 'vocab-production':return `<section class="card"><h2>Tu oración y sus decisiones</h2><blockquote lang="en">${esc(m.text)}</blockquote><p>Contrasta referente, acepción, combinación gramatical y situación. La demo no califica tu frase.</p>${A.actions([bt('production-keep','Conservar y justificar',data('production',m.production)+' '+data('entry',m.entryId||h.productions.find(p=>p.id===m.production)?.entryId||'')),bt('production-rewrite','Reformular el patrón',data('production',m.production)+' '+data('entry',m.entryId||h.productions.find(p=>p.id===m.production)?.entryId||'')),bt('production-replace','Elegir otra palabra',data('production',m.production)+' '+data('entry',m.entryId||h.productions.find(p=>p.id===m.production)?.entryId||'')),bt('transfer-email','Usarla en un correo',data('production',m.production)+' '+data('entry',m.entryId||h.productions.find(p=>p.id===m.production)?.entryId||'')),bt('lexical-tools','Consultar pistas y patrones')])}</section>`;
      case 'meaning-contrast':return `<section class="card"><p class="eyebrow">Ejemplo preparado para detectar cambios de datos o intención</p><h2>¿Conserva lo que querías decir?</h2><div class="comparison"><div><small>Origen</small><blockquote>${esc(m.before)}</blockquote></div><div><small>Alternativa para contrastar</small><blockquote>${esc(m.after)}</blockquote></div></div><p>${esc(m.notice)}</p>${A.actions([bt('meaning-keep','Mantener el origen'),bt('meaning-explain','Explicar la diferencia'),bt('candidate','Contrastar mi propia alternativa')])}</section>`;
      case 'productions':return productions(s);
      case 'resume':return `<section class="card"><h2>Un punto para retomar</h2><p>Retomas ${esc(s.task==='email'?cases[mainCase(s)].name.toLowerCase():s.word||'una duda de vocabulario')}. Última etapa: ${esc(A.D.stages[s.task]?.[s.stage]||'por precisar')}.</p><p>${esc(s.recall?'El apoyo anterior está oculto. Puedes intentar recuperar o mostrar dónde quedaste.':h.pendingNotes.at(-1)?.text||'Puedes recuperar una expresión antes de volver al apoyo.')}</p>${A.actions([A.btn('recall',s.task==='email'?'Intentar sin modelo':'Intentar sin definición','',true),bt('continue','Mostrar dónde quedé'),bt('resources','Retomar una duda'),bt(s.task==='email'?'parts':'lexical-tools','Revisar una elección'),bt('pending','Mantener la práctica pendiente')])}</section>`;
      default:return '';
    }
  }
  function parts(s,key,m={}) {
    const e=situation(s,m),c=cases[mainCase(s,m)],esc=A.esc;
    const samples={subject:[c.subject+(mainCase(s,m)==='extension'?' until '+(dateLabel(e.facts.proposed)||'[fecha propuesta]'):'')],greeting:['Dear Professor Rivera, — solo si tratamiento y apellido están confirmados.','Dear Alex Rivera, — si conoces el nombre completo sin atribuir título o género.','Hi Alex, — cuando la cercanía y el uso habitual lo permiten.'],request:[phrase(s,'near',m),phrase(s,'polite',m)],reason:[c.reason,'because + una razón pertinente y verdadera'],closing:['Best regards, — correspondencia académica o profesional.','Thanks, — cuando encaja un agradecimiento breve como cierre.']};
    return samples[key].map(t=>`<p lang="en">${esc(t)}</p>`).join('')+`<p class="small">${key==='greeting'?'Nombres de ejemplo. Si no conoces nombre o tratamiento, compruébalos o conserva esa duda.':key==='reason'?'No añadas una razón ficticia. Comprueba que motivo y petición no se contradigan; incluye la razón solo si es pertinente.':key==='subject'?'El asunto debe prometer lo mismo que el cuerpo. Las fechas desconocidas se mantienen como pendientes.':'Son alternativas de práctica; elige según significado, relación y contexto.'}</p>`;
  }
  function lexicalTools(s,m) {
    const e=s.hta.entries.find(e=>e.id===m.entryId)||tracked(s),w=A.wordEntry(e.word,e.context),esc=A.esc;
    return `<section class="card"><h2>Pistas, acepciones y uso</h2><blockquote>${esc(e.context)}</blockquote><details class="rule"><summary>Examinar una pista y su límite</summary><p>${esc(w?.clue||'La demo no confirma una pista para esta oración. Amplía el contexto o registra que no puedes inferir.')}</p><p>En “a dedicated space”, dedicated modifica space. Una combinación conocida orienta una hipótesis, pero no la demuestra.</p><p>Ejemplo adicional preparado: “She is a dedicated teacher: she cares deeply about her students.” La segunda parte ofrece una reformulación explícita. Esa pista no está necesariamente en tu oración.</p>${A.actions([bt('infer','Explicar mi pista',wordData(e)),bt('context','Ampliar el contexto',wordData(e))])}</details><details class="rule"><summary>Contrastar significado y patrón</summary><p>${esc(w?.other||'Mantén abiertas varias interpretaciones hasta tener una fuente suficiente.')}</p><p>${esc(w?.pattern||'Busca ejemplos que respalden un patrón antes de generalizarlo.')}</p><p lang="en">${esc(w?.example||'Compara solo ejemplos que correspondan a la acepción elegida.')}</p>${A.actions([bt('interpret','Reformular mi interpretación',wordData(e)),bt('resources','Elegir una fuente',wordData(e))])}</details><details class="rule"><summary>Registro y situación de uso</summary><p>${esc(w?.register||'Sin una nota fiable no se atribuye formalidad.')}</p><p>Significado y registro son aspectos distintos. Una diferencia entre persona comprometida y espacio reservado cambia la acepción; no demuestra formalidad.</p>${A.actions([bt('register-note','Registrar una etiqueta de mi fuente',wordData(e)),bt('register-unknown','Dejar el registro sin determinar',wordData(e)),bt('usage','Justificar una situación y destinatario',wordData(e))])}</details>${A.actions([bt('lexical-note','Redactar mi nota',wordData(e)),bt('vocab-write','Escribir una oración propia',wordData(e)),bt('pending','Anotar una duda',wordData(e))])}</section>`;
  }
  function productions(s) {
    const ps=s.hta.productions;
    return `<section class="card"><h2>Comparar mis producciones</h2><p>Observa intención, significado, registro y ayuda. Puedes explicar qué conservaste y qué cambió; las producciones se muestran sin calificarlas.</p>${ps.map(p=>`<section class="evidence"><strong>${A.esc(p.kind)}</strong><small>${new Date(p.date).toLocaleString('es-PE')} · ${p.help?'con apoyo consultado':'sin apoyo registrado'}</small><p class="doc-text">${A.esc(p.text)}</p>${p.context?`<p class="small">Origen: ${A.esc(p.context)}</p>`:''}</section>`).join('')||'<p>Todavía no hay producciones propias para comparar.</p>'}${A.actions([bt('compare-own','Explicar coincidencias y diferencias'),bt('pending','Priorizar una duda'),A.btn('recall','Volver a intentar sin apoyo')])}</section>`;
  }
  function rootSwitch(s,task) {
    prepare(s);if(s.hta.returns.at(-1)?.task===task){back(s);return;}s.hta.rootStates[s.task]=suspend(s);
    const old=s.hta.rootStates[task];
    if(old)Object.assign(s,{stage:old.stage,pending:old.pending,word:old.word,context:old.context,stageEvidence:old.stageEvidence});if(old){s.hta.reviewFragment=old.reviewFragment;s.hta.reviewScope=old.reviewScope;}
    else Object.assign(s,{stage:0,pending:null,stageEvidence:[]});
    s.task=task;s.hta.originTask=task;s.recall=false;
  }
  function recordProduction(s,text,kind) {
    prepare(s);const p={id:A.id(),text,kind,task:s.task,context:s.task==='vocab'?s.context:cases[mainCase(s)].name,date:new Date().toISOString(),help:s.helpUsed};
    s.hta.productions.push(p);if(s.task==='vocab'){p.entryId=tracked(s).id;tracked(s).productions.push(p);}return p;
  }

  function promptSuggestion(text,task,s) {
    if(task!=='email')return null;
    const t=norm(text),relation=/profesor|docente|amig|companero|destinatario|colega|teacher/.test(t)||s?.hta.email.relation&&s.hta.email.relation!=='unknown';
    if(!relation)return null;
    if(/saludo/.test(t)&&!/dear|hi alex|contrastar.*saludo/.test(t))return {key:'greeting-options',add:'Quiero contrastar los ejemplos “Dear Professor [apellido confirmado],” y “Dear [nombre completo],” para elegir mi saludo; si falta el tratamiento, déjalo pendiente.',why:'El saludo depende de lo que sabes de la relación y del nombre, sin inventar títulos.'};
    if(/cierre|despedida/.test(t)&&!/best regards|thanks|contrastar.*cierre/.test(t))return {key:'closing-options',add:'Quiero contrastar “Best regards,” y “Thanks,” para elegir un cierre coherente con mi saludo y petición.',why:'Comparar expresiones concretas ayuda a justificar el registro.'};
    const key=/prorroga|extension|mas tiempo/.test(t)?'extension':/aclar|confirm/.test(t)?'clarify':/apuntes|material/.test(t)?'notes':s?.hta.email.cases[0];
    if(key&&/asunto/.test(t)&&!/request for|question about/.test(t))return {key:'subject-'+key,add:`Ayúdame a contrastar el asunto de ejemplo “${cases[key].subject}” con mi petición; quiero comprobar que dicen lo mismo, conservando mis datos.`,why:'El asunto debe expresar la misma intención que el cuerpo.'};
    if(key&&!/compar|asunto|explic|conserv/.test(t))return {key:'case-'+key,add:`Quiero comparar cómo ${cases[key].name.toLowerCase()} en inglés y elegir asunto y petición, conservando los datos que aporte y dejando lo desconocido pendiente.`,why:'La comparación se centra en tu intención antes de redactar.'};
    return null;
  }
  function natural(s,text) {
    const t=norm(text).trim();
    if(/^[¿?\s]*(?:que significa|que quiere decir|what does|meaning of)\b/.test(t)) {
      const quote=[...text.matchAll(/[“"]([^”"]+)[”"]/g)].map(m=>m[1]).find(q=>q.includes(' '));
      const word=Object.keys(A.D.words).find(w=>new RegExp('\\b'+w+'\\b','i').test(text));
      if(quote&&word){A.input.value='';if(s.task!=='vocab')beginLink(s,'vocab',{fragment:word,context:quote,point:'C4.1',source:'Oración aportada en la consulta'});s.word=word;s.context=quote;tracked(s);A.clue(s);return true;}
    }
    const commands=[[/^(?:volver|regresar|retomar) al correo\b/,'return'],[/^(?:volver|regresar) al vocabulario\b/,'return'],[/^(?:dame|quiero|necesito) (?:otra |una )explicacion\b/,'explain'],[/^(?:quiero )?(?:consultar|resolver) (?:una|esta|la) (?:duda|expresion|palabra)\b/,'consult'],[/^(?:quiero )?(?:ver|elegir|probar) (?:un |el )?(?:asunto|saludo|cierre|motivo)\b/,'parts'],[/^(?:quiero )?comparar mis (?:correos|producciones|oraciones)\b/,'productions'],[/^(?:quiero )?revisar (?:mi |el )?(?:correo|borrador|frase)\b/,'review']];
    const found=commands.find(([re])=>re.test(t));
    if(found){A.input.value='';if(found[1]==='review'){if(s.task==='general')rootSwitch(s,'email');A.review(s);}else action(s,'hta-'+found[1],{dataset:{},closest:()=>null});return true;}
    return false;
  }
  function answer(s,text) {
    const p=s.pending;if(!p||p.type!=='hta')return false;s.pending=null;
    const e=p.entryId?s.hta.entries.find(e=>e.id===p.entryId):s.task==='vocab'?tracked(s):null;
    const purpose=p.purpose;
    if(purpose==='resource-compare'&&s.hta.returns.length)s.hta.returns.at(-1).result=text;
    if(purpose==='review-fragment'){reviewFragment(s,text);return true;}
    if(purpose==='fragment'){consult(s,text,p.versionId);return true;}
    if(purpose==='target-word'){s.word=text.trim();if(!new RegExp('\\b'+text.trim().replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\b','i').test(s.context)){ask(s,'target-word','Esa palabra no aparece en la oración conservada. Indica la palabra exacta o deja la duda pendiente.');return true;}tracked(s);A.clue(s);return true;}
    if(purpose==='facts'){observe(s,text);s.hta.email.providedDetails=text;remember(s,'Contexto y datos aportados',text);post(s,'email-context');return true;}
    if(purpose==='combine'){observe(s,text);remember(s,'Solicitudes necesarias',text);post(s,'email-context');return true;}
    if(purpose==='context') {const before=e.context;e.context=text;e.key=norm(e.word)+'|'+A.contextKey(text);s.context=text;remember(s,'Contexto ampliado',text,{originalContext:before});A.clue(s);return true;}
    if(purpose==='external-ref'){s.hta.external={id:A.id(),reference:text,task:s.task,entryId:e?.id,status:'Pendiente de respuesta',date:new Date().toISOString()};s.hta.queries.push(copy(s.hta.external));ask(s,'external-answer','Comparte la explicación o el ejemplo recibido. Se conservará como aporte externo no verificado.',{entryId:e?.id});return true;}
    if(purpose==='external-answer'){const source={...s.hta.external,answer:text,verified:false,date:new Date().toISOString()};if(e){e.sources.push(source);e.definitionSeen=true;}const previous=s.hta.queries.find(q=>q.id===source.id);if(previous)Object.assign(previous,source,{status:'Respuesta aportada, sin verificar'});else s.hta.queries.push(source);delete s.hta.external;remember(s,'Consulta externa no verificada',source.reference+'\n'+text);ask(s,'resource-compare','¿Qué aclara respecto a tu oración y qué queda incierto?',{entryId:e?.id});return true;}
    if(purpose==='candidate'){const before=p.fragment||s.hta.reviewFragment||s.draft;if(p.sourceText!==s.draft){A.message(s,'text','El borrador cambió mientras preparabas la alternativa. Tu propuesta queda conservada como mensaje; selecciona de nuevo el fragmento antes de aplicarla.');return true;}post(s,'meaning-contrast',{before,after:text,notice:'Contrasta intención, fechas, material y relación. La demo señala diferencias para que tú las expliques; no valida cualquier alternativa.'});s.hta.candidate={before,after:text};const scoped=p.range&&p.range.text===s.draft&&s.draft.slice(p.range.start,p.range.end)===before;const start=scoped?p.range.start:s.draft.indexOf(before);if(start>=0&&(scoped||s.draft.indexOf(before,start+1)===-1))A.message(s,'correction','',{before,after:text,category:'Significado / datos',reason:'Es tu alternativa para contrastar. Comprueba intención, datos y construcción antes de decidir; no se ha validado automáticamente.',status:'pending',start,end:start+before.length,versionId:s.versions.at(-1)?.id});else A.message(s,'text','Para aplicar esta alternativa, elige primero una aparición única del fragmento.');return true;}
    if(purpose==='vocab-write'){const production=recordProduction(s,text,'Oración propia');remember(s,'Producción propia de vocabulario',text);post(s,'vocab-production',{text,production:production.id});return true;}
    if(purpose==='rewrite'||purpose==='replace'){const production=recordProduction(s,text,purpose==='replace'?'Otra palabra para conservar la intención':'Oración reformulada');remember(s,'Reformulación léxica',text);post(s,'vocab-production',{text,production:production.id});return true;}
    if(purpose==='interpret'){e.interpretation=text;remember(s,'Interpretación reformulada',text,{entryId:e.id});}
    else if(purpose==='infer'){remember(s,inferenceKind(s,text),text,{entryId:e.id});A.definition(s,text);return true;}
    else if(purpose==='lexical-note'){e.note=text;remember(s,'Nota de significado, contexto y uso',text,{entryId:e.id});}
    else if(purpose==='register-note'){e.register={label:text,verified:false};remember(s,'Etiqueta aportada de una fuente, por verificar',text,{entryId:e.id});}
    else if(purpose==='pending'){s.hta.pendingNotes.push({id:A.id(),text,task:s.task,entryId:e?.id,date:new Date().toISOString()});if(e)e.doubts.push(text);s.hta.status='Pendiente de continuar';remember(s,'Duda para retomar',text);}
    else if(purpose==='part'){s.hta.email[p.part]=text;remember(s,'Elección propia: '+p.part,text);}
    else {remember(s,{known:'Expresión conocida y duda inicial',usage:'Situación y destinatario del uso',compare:'Comparación de producciones',decision:'Razón para conservar o reformular',refine:'Duda reformulada', 'resource-compare':'Contraste de la consulta'}[purpose]||'Explicación propia',text,{decisionId:p.decisionId});if(e&&purpose==='resource-compare')e.interpretation=text;}
    if(e&&p.productionId)e.reviews.push({productionId:p.productionId,decision:purpose,text,date:new Date().toISOString()});
    post(s,'note-result',{title:purpose==='pending'?'Un pendiente para continuar':'Tu explicación quedó guardada',text:'Puedes contrastarla, reformularla o volver al punto de origen. Guardarla no certifica que sea correcta.'});return true;
  }
  function action(s,action,el) {
    if(!action.startsWith('hta-'))return false;
    if(!s)return true;prepare(s);markHelp(s);
    if(document.querySelector('#workspace-dialog').open)A.closeDialog();
    const key=action.slice(4),h=s.hta;
    if(!el.dataset.entry){const owner=s.messages.find(m=>m.id===el.closest?.('[data-message]')?.dataset.message);if(owner?.entryId)el={...el,dataset:{...el.dataset,entry:owner.entryId}};}
    const e=el.dataset.entry?chooseEntry(s,el):s.task==='vocab'?tracked(s):null;
    switch(key){
      case 'situation':post(s,'email-context');break;
      case 'case':h.email.cases=[el.dataset.case];s.stage=0;post(s,'email-context');break;
      case 'combine':ask(s,'combine','Indica cuáles de estas solicitudes necesitas combinar y por qué: apuntes, prórroga o aclaración.');break;
      case 'relation':h.email.relation=el.dataset.relation;post(s,'email-context');break;
      case 'facts':ask(s,'facts','Escribe los datos que conozcas. Puedes indicar nombre, tratamiento, material, fecha vigente, fecha propuesta y motivo. Deja explícito lo desconocido.');break;
      case 'known':ask(s,'known','Recuerda una expresión que ya conozcas y señala qué no sabes expresar: asunto, saludo, petición, motivo o cierre.');break;
      case 'parts':post(s,'parts');break;
      case 'try-part':ask(s,'part','Escribe tu expresión de '+{subject:'asunto',greeting:'saludo',request:'petición',reason:'motivo',closing:'cierre'}[el.dataset.part]+' y explica por qué conserva tu intención.',{part:el.dataset.part});break;
      case 'explain':A.message(s,'text','Podemos distinguir significado, construcción y efecto en el destinatario. Can y could permiten pedir; could suele suavizar. Please expresa cortesía, pero no corrige por sí solo una fecha o intención distinta. Una razón con because debe explicar la necesidad real.');post(s,s.task==='email'?'parts':'lexical-tools');break;
      case 'resources':post(s,'resources',{fragment:h.reviewFragment||s.context||s.draft});break;
      case 'resource':{
        const w=s.task==='vocab'?A.wordEntry(s.word,s.context):null;
        const examples={model:w?`Material de práctica: ${w.meaning} Otra acepción o contraste: ${w.other} Ejemplo: ${w.example} Contrasta las acepciones con la oración, no con una traducción aislada.`:'Compara el fragmento con el modelo del mismo caso: identifica petición, motivo, plazo y relación. Un modelo no sustituye comprobar tus datos.',translation:'Ejemplo de contraste: “I want you to send me the notes” puede traducirse como “Quiero que me envíes los apuntes”. La traducción conserva una idea, pero no demuestra que el tono sea adecuado. Comprueba quién pide qué y qué datos permanecen.',ai:'Ejemplo de consulta para editar: “Explica este fragmento dentro de su oración. Compara significado y tono, conserva los datos y no reescribas el resto. Si faltan datos, indícalo”. No se envía a una IA.',person:'Ejemplo de pregunta a otra persona: “¿Qué efecto tiene esta expresión en este destinatario y qué alternativa de igual intención propondrías?”. Una respuesta útil explica un fragmento y ofrece un ejemplo; este material no proviene de un docente real.'};
        if(w&&el.dataset.resource==='model')tracked(s).definitionSeen=true;
        if(s.task==='vocab')tracked(s).sources.push({kind:'prepared',resource:el.dataset.resource,verified:false,text:examples[el.dataset.resource]});
        if(s.task==='vocab'&&el.dataset.resource==='translation')examples.translation=w?`Oración: ${s.context} Traducción preparada: ${w.translation} Comprueba referente, finalidad y datos; una traducción aislada no confirma la acepción fuera de esta oración.`:'No hay una traducción preparada para esta oración. Puedes registrar una traducción externa y contrastar qué datos o relaciones conserva; no se trasladará una traducción de otro contexto.';
        if(el.dataset.resource==='ai')examples.ai=`Consulta de ejemplo, editable fuera de la demo: Explica el fragmento «${h.reviewFragment||s.word||'expresión por precisar'}» dentro de «${s.context||s.draft||'contexto por aportar'}». Distingue significado, construcción y registro, conserva los datos y explica las dudas. No reescribas el resto. Esta consulta no se envía a un servicio.`;
        if(s.task==='vocab'&&el.dataset.resource==='person')examples.person=w?`Ejemplo didáctico de explicación, no respuesta de una persona real: ${w.meaning} Para comprobarlo, compara la oración «${s.context}» con «${w.example}». Una persona consultada podría proponer otros ejemplos; registra su respuesta y lo que sigue incierto.`:'Pregunta de ejemplo: ¿qué interpretaciones admite esta oración y qué evidencia faltaría para elegir? No hay una respuesta preparada para este contexto; puedes registrar la de una persona consultada fuera.';
        h.queries.push({id:A.id(),resource:el.dataset.resource,kind:'prepared',text:examples[el.dataset.resource],word:s.word,context:s.context});post(s,'resource',{resource:el.dataset.resource,example:examples[el.dataset.resource]});break;}
      case 'external':ask(s,'external-ref','Indica el recurso consultado y su referencia, si la tienes: diccionario, traductor, IA, docente o compañero. No hace falta incluir datos personales.',{entryId:e?.id});break;
      case 'resource-compare':ask(s,'resource-compare','Explica qué aporta la consulta a la intención o acepción y qué sigue incierto.',{entryId:e?.id});break;
      case 'refine':ask(s,'refine','Reformula solo la duda abierta: añade contexto, pide otro ejemplo de igual intención o precisa qué significado falta.');break;
      case 'pending':case 'word-status':ask(s,'pending','¿Qué duda quieres retomar y qué necesitarías comprobar?',{entryId:e?.id});break;
      case 'doubt':{
        const spec=h.consultSpec;if(!spec){A.notice('Selecciona primero una expresión.');break;}delete h.consultSpec;
        beginLink(s,el.dataset.kind==='meaning'?'vocab':'email',{...spec,point:'C4.1',kind:el.dataset.kind});
        if(el.dataset.kind==='meaning'){s.word='';s.context=spec.context;ask(s,'target-word','¿Qué palabra exacta de la oración quieres contrastar?');}
        else {h.reviewFragment=spec.fragment;post(s,'resources',{fragment:spec.fragment});}break;}
      case 'review-fragment':{
        const version=s.versions.find(v=>v.id===el.dataset.version);if(version&&version.text!==s.draft){A.notice('Esa tarjeta es de otra versión. Abre la versión actual antes de revisar el fragmento.');break;}
        const fragment=selection(el);if(fragment)reviewFragment(s,fragment);else ask(s,'review-fragment','Copia el fragmento exacto que deseas revisar. Si se repite, podrás elegir la aparición.');break;}
      case 'identify-model':ask(s,'identify-model','Identifica en el modelo qué se pide, qué dato concreta el material o plazo y qué frase explica el motivo.');break;
      case 'review-range':{
        const range=h.reviewRange;if(!range||range.text!==s.draft){A.notice('La versión cambió. Elige de nuevo el fragmento.');break;}
        h.reviewFragment=range.fragment;A.review(s,{start:Number(el.dataset.start),end:Number(el.dataset.end)});break;}
      case 'consult':{h.consultOrigin=suspend(s);const fragment=selection(el);const versionId=el.dataset.version;if(fragment)consult(s,fragment,versionId);else ask(s,'fragment','Copia la expresión exacta que quieres consultar. Mantendremos su oración y el correo de origen.',{versionId});break;}
      case 'return':back(s);break;
      case 'lexical-tools':post(s,'lexical-tools',{entryId:e?.id});break;
      case 'infer':ask(s,'infer','Propón una hipótesis y señala qué pista real del texto la sostiene; puedes decir que no pudiste inferir.',{entryId:e.id});break;
      case 'context':ask(s,'context','Comparte la oración completa o amplía su entorno, conservando la palabra que consultas.',{entryId:e.id});break;
      case 'interpret':ask(s,'interpret','Compara tu hipótesis con las acepciones y reformula tu interpretación; explica por qué descartas otra.',{entryId:e.id});break;
      case 'register-note':ask(s,'register-note','Anota la etiqueta de uso, su acepción y la referencia que la presenta. Se guardará como aporte por verificar.',{entryId:e.id});break;
      case 'register-unknown':e.register={label:'Sin determinar',verified:false};remember(s,'Registro sin determinar','No hay una etiqueta fiable para esta acepción.');post(s,'lexical-tools',{entryId:e.id});break;
      case 'usage':ask(s,'usage','Elige una situación y destinatario. Justifica la acepción y el patrón, sin confundir registro con significado.',{entryId:e.id});break;
      case 'lexical-note':ask(s,'lexical-note','Escribe tu nota: significado, oración de origen, patrón, situación de uso y duda pendiente. Usa tus palabras.',{entryId:e.id});break;
      case 'vocab-write':ask(s,'vocab-write','Elige una idea propia y escribe una oración. Después contrastaremos referente, acepción y patrón.',{entryId:e.id});s.stage=1;break;
      case 'production-keep':ask(s,'decision','Explica una coincidencia entre tu oración y un ejemplo de la misma acepción.',{entryId:e?.id,productionId:el.dataset.production});break;
      case 'production-rewrite':ask(s,'rewrite','Conserva tu idea y reformula la construcción. Después compara la nueva frase con el mismo ejemplo.',{entryId:e?.id,productionId:el.dataset.production});break;
      case 'production-replace':ask(s,'replace','Elige otra palabra si la acepción no expresa tu intención. Escribe la nueva frase y explica qué conserva.',{entryId:e?.id,productionId:el.dataset.production});break;
      case 'transfer-email':{
        const p=h.productions.find(p=>p.id===el.dataset.production)||h.productions.filter(p=>p.task==='vocab').at(-1);
        beginLink(s,'email',{point:'V6',context:s.context,productionId:p?.id,fragment:p?.text});h.email={cases:[],relation:'unknown',name:'',title:'',facts:{},doubts:[]};s.stage=1;
        ask(s,'transfer-draft','Compón un correo con esta idea para otro destinatario. Conserva la acepción y explica la relación; puedes cambiar la palabra si no encaja.');if(p)A.message(s,'text','Tu idea de origen: '+p.text);break;}
      case 'entry-recall':h.attemptEntry=e.id;A.recall(s);break;
      case 'unsave-entry':e.saved=false;syncWords(s);A.notice('Entrada retirada del repaso. Sus notas y producciones se conservan.');A.notebook();break;
      case 'review-choice':post(s,'meaning-contrast',{before:h.reviewFragment||s.draft||'Could I have an extension until Friday?',after:(h.reviewFragment||s.draft||'Could I have an extension until Friday?').includes('Friday')?(h.reviewFragment||s.draft||'Could I have an extension until Friday?').replace('Friday','Monday'):'Could I have permission to leave?',notice:'Comprueba si cambió una fecha o lo que se solicita. Este ejemplo no es una mejora recomendada.'});break;
      case 'candidate':ask(s,'candidate','Escribe una alternativa para el fragmento conservado. Contrastaremos los datos y el sentido antes de decidir.',{sourceText:s.draft,fragment:h.reviewFragment||s.draft,range:copy(h.reviewScope||null)});break;
      case 'meaning-keep':remember(s,'Decisión sobre significado','Conservo el origen: la alternativa puede cambiar datos o intención.');ask(s,'decision','Explica qué dato o intención debes conservar y por qué.');break;
      case 'meaning-explain':ask(s,'decision','Explica si cambió el significado, la fecha o el material solicitado.');break;
      case 'productions':post(s,'productions');break;
      case 'compare-own':ask(s,'compare','Compara dos producciones: intención conservada, cambio de tono o patrón, destinatario y apoyo necesario.');break;
      case 'resume-plan':post(s,'resume');break;
      case 'continue':s.recall=false;s.helpUsed=true;A.notice('Apoyo anterior visible. Se registra la consulta durante el intento.');break;
      case 'reading-note':ask(s,'reading','Relaciona el título con una experiencia, anticipa el tema según fuente y destinatario y resume la idea general.');break;
      case 'priority':ask(s,'priority','¿La expresión impide comprender la idea, cambia la petición o será útil para una producción? Explica si la consultas ahora o la dejas para después.');break;
      default:return false;
    }
    return true;
  }

  function reviewFragment(s,text) {
    const hits=[];let offset=0;
    while(text && (offset=s.draft.indexOf(text,offset))!==-1){hits.push(offset);offset+=text.length;}
    if(!hits.length){ask(s,'review-fragment','Ese fragmento no está en el borrador actual. Copia una frase exacta para revisarla.');return;}
    if(hits.length===1){A.review(s,{start:hits[0],end:hits[0]+text.length});return;}
    s.hta.reviewRange={text:s.draft,fragment:text};
    A.message(s,'hta','',{view:'range',fragment:text,hits:hits.map(start=>({start,end:start+text.length,label:s.draft.slice(Math.max(0,start-30),start+text.length+30)}))});
  }
  function reviewSaved(s) {
    prepare(s);const entries=s.hta.entries.filter(e=>e.saved);
    if(entries.length>1){A.openDialog('Elige qué palabra y contexto repasar',entries.map(e=>`<section class="evidence"><strong>${A.esc(e.word)}</strong><p>${A.esc(e.context)}</p>${bt('entry-recall','Intentar sin definición',wordData(e))}</section>`).join(''),'review');return true;}
    if(document.querySelector('#workspace-dialog').open)A.closeDialog();
    if(entries.length){s.word=entries[0].word;s.context=entries[0].context;s.hta.attemptEntry=entries[0].id;A.recall(s);}else A.message(s,'text','Guarda una palabra y su contexto antes de elegir un repaso.');
    return false;
  }
  function finish(s) {
    prepare(s);s.hta.status=s.hta.productions.length && s.evidence.some(e=>/explicaci|justificaci|interpretaci/i.test(e.kind))?'Práctica registrada; decisión de continuidad pendiente':'Práctica parcial: producción o explicación pendiente';
    s.hta.closedAt=new Date().toISOString();
  }
  function resume(s) {prepare(s);s.closed=false;s.hta.resumeHidden=true;s.recall=true;s.recallStart=s.messages.length;post(s,'resume');}
  function isSaved(s,m) {return entry(s,m.word,m.context||A.D.words[m.word]?.context||'').saved;}
  function syncWords(s) {s.words=[...new Set(s.hta.entries.filter(e=>e.saved).map(e=>e.word))];s.savedContexts=Object.fromEntries(s.hta.entries.filter(e=>e.saved).map(e=>[e.word,e.context]));}
  function saveEntry(s,word,context) {const e=entry(s,word,context);e.saved=!e.saved;syncWords(s);return e.saved;}
  function pendingDraft(s,text) {if(s.pending?.type==='hta'&&s.pending.purpose==='transfer-draft'){s.pending=null;A.saveDraft(s,text);return true;}return false;}
  function inferenceKind(s,text) {
    const e=tracked(s);
    if(e.definitionSeen)return 'Interpretación después del contraste';
    return /^(?:no (?:puedo|se|pude)|ya (?:conozco|se)|prefiero consultar)/.test(norm(text))?'Punto de partida sin hipótesis':'Hipótesis y pista contextual';
  }
  function onDefinition(s,hypothesis) {
    const e=tracked(s);
    if(hypothesis){
      if(e.definitionSeen)e.interpretation=hypothesis;
      else if(inferenceKind(s,hypothesis)==='Punto de partida sin hipótesis')e.startingPoint=hypothesis;
      else e.hypothesis=hypothesis;
    }else if(!e.hypothesis&&!e.startingPoint)e.startingPoint='Consulta directa sin hipótesis';
    const w=A.wordEntry(s.word,s.context||A.D.words[s.word]?.context);if(w)e.reference={meaning:w.meaning,pattern:w.pattern,example:w.example,register:w.register,source:'Material preparado de la demo'};
    e.definitionSeen=true;return e.hypothesis;
  }
  function updateInterpretation(s,text) {const e=tracked(s);e.interpretation=text;}
  return {init,prepare,observe,meta,emailStart,header,intro,comparison,model,render,entryExtras,notebook,markHelp,rootSwitch,recordProduction,natural,answer,action,saveEntry,pendingDraft,onDefinition,updateInterpretation,inferenceKind,promptSuggestion,tracked,cases,resume,finish,reviewSaved,isSaved};
})();
