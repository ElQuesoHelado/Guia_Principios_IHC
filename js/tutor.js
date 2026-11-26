(() => {
  'use strict';
  const D = window.TutorData;
  const $ = (q) => document.querySelector(q);
  const esc = (v = '') => String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const normalize = (t) => t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const id = () => (crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).slice(2));
  const KEY = 'lingua-tutor-v1';
  const clone = v => JSON.parse(JSON.stringify(v));
  let state = {version:1, sessions:[], active:null};
  let chosenTask = null, dismissed = '', promptUndo = null, panel = '', returnFocus = null;
  const input = $('#chat-input');
  function current() { return state.sessions.find(s => s.id === state.active); }
  function warnStorage() { const el = $('#storage-status'); el.hidden = false; el.textContent = 'El navegador no permite guardar esta práctica. Puedes continuar y descargar tus notas desde Mi aprendizaje.'; }
  function load() {
    try {
      const parsed = JSON.parse(localStorage.getItem(KEY));
      if (parsed && parsed.version === 1 && Array.isArray(parsed.sessions) && parsed.sessions.every(s => s && typeof s.id === 'string' && s.task in D.tasks && Array.isArray(s.messages) && Array.isArray(s.evidence) && Array.isArray(s.versions) && Array.isArray(s.words) && typeof s.draft === 'string')) state = parsed;
    } catch (_) { warnStorage(); }
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (_) { warnStorage(); } }
  function session(task, title) {
    const s = {id:id(),task,title:title.slice(0,70),created:new Date().toISOString(),messages:[],evidence:[],words:[],versions:[],draft:'',inputDraft:'',stage:0,pending:null,word:'dedicated',context:'',recall:false,recallStart:0,helpUsed:false,closed:false,promptUses:0,promptDismisses:0,stageEvidence:[]};
    state.sessions.push(s); state.active = s.id; return s;
  }
  function message(s, kind, text = '', extra = {}) { const m = {id:id(),kind,text,...extra}; s.messages.push(m); return m; }
  function evidence(s, kind, text) { s.evidence.push({kind,text,date:new Date().toISOString(),stage:s.stage,help:s.helpUsed,topic:s.task==='email'?s.emailTopic:null}); if (!s.stageEvidence.includes(s.stage)) s.stageEvidence.push(s.stage); }
  function emailTopic(text) {
    const t=normalize(text);
    if (/\basunto\b|\bsubject\b|request for|question about/.test(t)) return 'subject';
    if (/salud[oa]|\bdear\b|\bhi\b|tratamiento/.test(t)) return 'greeting';
    if (/\bbecause\b|finalidad|motivo|conector|\brazon\b|to review/.test(t)) return 'reason';
    if (/despedida|\bcierre\b|best regards|\bthanks\b/.test(t)) return 'closing';
    if (/\bcan\b|\bcould\b|\buntil\b|peticion|solicitud|estructura|prorroga/.test(t)) return 'request';
    return null;
  }
  function lessonQuery(text) {
    return /^[¿\s]*(?:(?:quiero|puedes|podrias|me gustaria)\b.*\b(?:aprender|practicar|comprender|entender|compar\w*|explic\w*)\b|(?:compara|explica|ayudame|como|que significa|que diferencia)\b)/.test(normalize(text)) ? emailTopic(text) : null;
  }
  function pastedEmail(text) {
    const greeting=/^[ \t]*(?:Dear|Hi|Hello)\b[^\r\n]*\r?\n/im.exec(text);
    if(!greeting || !text.slice(greeting.index+greeting[0].length).trim())return null;
    const subject=/^[ \t]*(?:Subject|Asunto):[^\r\n]*/im.exec(text.slice(0,greeting.index));
    return text.slice(subject?subject.index:greeting.index).trim();
  }
  function detect(text) {
    const t = normalize(text);
    if(pastedEmail(text)&& !/que significa|que quiere decir|meaning of|acepcion|vocabulario/.test(t))return 'email';
    const email = Boolean(lessonQuery(text)) || /\b(correo|email|e-mail|mail|saludo|despedida|prorroga|peticion)\b|dear\s|best regards|kind regards/.test(t);
    const vocab = /\b(vocabulario|palabra|acepcion|signific\w*|word|meaning|dedicated|productive|deadline)\b|que quiere decir/.test(t);
    if (email && vocab) {
      if (lessonQuery(text)) return 'email';
      if (/que significa|que quiere decir|meaning of|acepcion|vocabulario/.test(t)) return 'vocab';
      if (/redact|revisa|escribir|correo a|tono de/.test(t)) return 'email';
      return 'ambiguous';
    }
    return email ? 'email' : vocab ? 'vocab' : 'general';
  }
  function suggest(text, task) {
    const t = normalize(text);
    if (text.trim().length < 7 || pastedEmail(text) || /\nDear |^Dear /i.test(text)) return null;
    if (task === 'email') {
      const topic=emailTopic(text), lesson=D.emailLessons[topic];
      if (lesson && !/con mis palabras|significado y|patron y|patron e/.test(t)) {
        const adds={
          subject:'Compara request for y question about; quiero explicar su significado con mis palabras y adaptar un asunto a mi intención.',
          greeting:'Compara Dear y Hi con ejemplos según la relación; quiero explicar su significado y elegir sin inventar un tratamiento.',
          request:'Compara can y could; explícame el patrón y quién pide qué para producir una petición con mis palabras.',
          reason:'Compara because + oración y to + verbo; quiero explicar con mis palabras la diferencia entre razón y finalidad.',
          closing:'Compara Best regards y Thanks; quiero explicar con mis palabras su función y cuándo usar cada cierre.'
        };
        return {key:`learn-${topic}`,add:adds[topic],why:'Comprender la expresión y probar una variante permite practicar inglés en esta situación.'};
      }
      if (!/profesor|teacher|amig|companer|jefe|destinatario|professor|colega|universidad/.test(t)) return {key:'recipient', add:'Ayúdame a comparar cómo cambiaría la petición según la confianza con el destinatario.', why:'El destinatario ayuda a elegir el saludo y la cortesía (correo 1.2 y 2).'};
      if (!/compar|explic|por que|diferencia/.test(t)) return {key:'tone', add:'Compara dos formas de pedir lo mismo y explícame qué cambia en el tono; quiero elegir mi propia expresión.', why:'Comparar la misma intención permite comprender el registro antes de redactar (correo 2.1–2.3).'};
      if (!/conserv|sin (cambiar|reescribir)|solo|unicamente/.test(t)) return {key:'preserve', add:'Si propongo un borrador, sugiere cambios solo en la frase que revisemos y conserva el resto.', why:'La revisión localizada permite comprobar cada cambio sin perder tu intención (correo 5).'};
    }
    if (task === 'vocab') {
      if (!/[“"'«:]/.test(text) && !/en esta frase|en la oracion|contexto/.test(t)) return {key:'context', add:'Quiero ver cómo cambia su significado en una oración. Si falta contexto, pídemelo antes de elegir una acepción.', why:'Una palabra puede tener varias acepciones; la oración ayuda a elegir (vocabulario 2 y 3).'};
      if (!/infer|hipotes|antes|deduc|pista/.test(t)) return {key:'infer', add:'Primero dame una pista del contexto para que intente inferir el significado; después lo contrastamos.', why:'Una hipótesis propia permite contrastar y ajustar lo que entiendes (vocabulario 2.3–3.4).'};
      if (!/propia|reutil|otro contexto|recuper|sin definicion/.test(t)) return {key:'reuse', add:'Después quiero usar la palabra en una oración propia y probarla en otra situación.', why:'Usar y recuperar una expresión va más allá de recordar su traducción (vocabulario 6 y 7).'};
    }
    return null;
  }
  function btn(action, label, attrs = '', primary = false) { return `<button data-action="${action}" ${attrs} class="${primary ? 'primary' : ''}">${label}</button>`; }
  function actions(items) { return `<div class="actions">${items.join('')}</div>`; }
  function textBlock(t) { return `<p>${esc(t).replace(/\n/g,'<br>')}</p>`; }
  function introActions(task) {
    return task === 'email' ? actions([btn('compare','Comparar dos peticiones','',true),btn('write','Probar mi propia frase'),btn('model','Ver un modelo')])+lessonChoices() : actions([btn('clue','Dame una pista','',true),btn('definition','Ver significado ahora'),btn('reading','Ver otra lectura')]);
  }
  function lessonChoices() {
    return `<details class="rule language-options"><summary>Explorar expresiones del inglés</summary><p>Elige lo que quieres comprender o pregúntalo en el chat. Puedes practicar una sola expresión.</p>${actions(Object.entries(D.emailLessons).map(([key,lesson])=>btn('email-lesson',lesson.label,`data-topic="${key}"`)))}</details>`;
  }
  function languageLesson(m) {
    const lesson=D.emailLessons[m.topic];
    if(!lesson)return textBlock('Este apoyo ya no está disponible. Puedes elegir otra expresión.');
    return `<section class="card language-lesson" data-topic="${m.topic}"><p class="eyebrow">Inglés en una situación de práctica</p><h2>${esc(lesson.title)}</h2><p>${esc(lesson.intro)}</p><div class="comparison">${lesson.examples.map(([example,meaning])=>`<div><blockquote lang="en">${esc(example)}</blockquote><p>${esc(meaning)}</p></div>`).join('')}</div><details class="rule"><summary>Relacionar significado y estructura</summary><p>${esc(lesson.pattern)}</p></details><p>${esc(lesson.prompt)}</p>${actions([btn('email-practice','Probar con mis palabras',`data-topic="${m.topic}"`,true),btn('recall','Intentar sin ejemplos',`data-topic="${m.topic}"`),btn('model','Ver en un correo'),...(m.topic==='request'?[btn('compare','Comparar dos peticiones')]:[])])}</section>${lessonChoices()}`;
  }
  function correction(s,m) {
    const accepted = m.status === 'accepted', decided = m.status && m.status !== 'pending';
    if(m.status==='outdated') return `<section class="card correction-card"><span class="badge">Propuesta de una versión anterior</span><div class="diff-line"><small>Fragmento revisado entonces</small><p lang="en">${esc(m.before)}</p></div><p class="small">Recuperaste otro borrador. Puedes solicitar una nueva revisión de la versión actual.</p>${actions([btn('review','Revisar versión actual'),btn('versions','Ver versiones')])}</section>`;
    return `<section class="card correction-card" aria-label="Propuesta de revisión"><span class="badge ${m.category === 'Gramática' ? 'grammar' : 'tone'}">${m.category === 'Gramática' ? '△ ' : ''}${esc(m.category)}</span><h2 style="margin-top:12px">${m.category === 'Gramática' ? 'Revisemos esta estructura' : 'Una alternativa de cortesía'}</h2><div class="diff-line"><small>Tu frase</small><p lang="en">${esc(m.before)}</p></div><div class="diff-line proposal"><small>Propuesta · tú decides</small><p lang="en">${esc(m.after)}</p></div><details class="rule"><summary>Por qué se propone este cambio</summary><p>${esc(m.reason)}</p></details><p class="inline-help" style="margin-top:12px">Solo se modifica este fragmento. El resto del correo se conserva.</p>${decided ? `<p class="note">${accepted ? 'Sugerencia aplicada' : 'Conservaste tu frase'} · puedes revisar las versiones.</p>${actions([btn('undo-correction','Deshacer decisión',`data-id="${m.id}"`),btn('justify','Explicar mi decisión','data-stage="1"')])}` : actions([btn('accept','Usar esta sugerencia',`data-id="${m.id}"`,true),btn('reject','Conservar mi frase',`data-id="${m.id}"`),btn('justify','Explicar antes de decidir','data-stage="1"')])}</section>`;
  }
  function wordCard(s, m) {
    const w = D.words[m.word];
    return `<section class="card word-detail"><p class="eyebrow">${esc(w.word)} · en esta oración</p><blockquote class="doc-text" lang="en">${esc(m.context || w.context)}</blockquote>${m.hypothesis ? `<div class="diff-line"><small>Tu interpretación inicial</small><p>${esc(m.hypothesis)}</p></div>` : ''}<div class="diff-line proposal"><small>Acepción del ejemplo</small><p>${esc(w.meaning)}</p></div><details class="rule"><summary>Contrastar acepciones, patrón y ejemplos</summary><p>${esc(w.other)}</p><p lang="en">${esc(w.example)}</p><p>${esc(w.pattern)}</p><p>${esc(w.register)}</p><p class="small">Ficha didáctica de la demo. Contrasta con un diccionario si la usas fuera de este ejemplo.</p></details>${actions([btn('vocab-explain','Explicar con mis palabras','',true),btn('save-word',s.words.includes(w.word)?'Quitar del repaso':'Guardar palabra',`data-word="${w.word}"`),btn('recall','Probar sin definición')])}</section>`;
  }
  function content(s,m) {
    switch (m.kind) {
      case 'email-lesson': return languageLesson(m);
      case 'language-attempt': return `<section class="card language-attempt"><p class="eyebrow">Tu práctica · ${esc(D.emailLessons[m.topic]?.label || 'Inglés')}</p><blockquote class="doc-text">${esc(m.text)}</blockquote><p>Quedó guardado tu intento y la explicación que incluiste. Contrasta el significado, la estructura y la adecuación con el ejemplo; puedes señalar una duda o reformular. La demo no califica esta producción.</p>${actions([btn('email-lesson','Contrastar con los ejemplos',`data-topic="${m.topic}"`,true),btn('email-practice','Reformular mi intento',`data-topic="${m.topic}"`),btn('recall','Intentar sin ejemplos',`data-topic="${m.topic}"`),btn('transfer','Usar en otra situación',`data-topic="${m.topic}"`),btn('write','Aplicar en mi correo')])}</section>`;
      case 'text': return textBlock(m.text) + (m.start ? introActions(s.task) : '');
      case 'choice': return textBlock(m.text) + actions([btn('assign','Aprender con un correo','data-task="email"'),btn('assign','Vocabulario en contexto','data-task="vocab"')]);
      case 'compare': return `<p>Las dos peticiones buscan lo mismo: recibir unos apuntes. Cambia la relación con quien los recibe.</p><section class="card"><h2>La misma intención, otra relación</h2><div class="comparison"><div><span class="badge">A un compañero</span><blockquote lang="en">Can you send me the notes?</blockquote><small>Cercanía; una petición directa puede encajar.</small></div><div><span class="badge tone">A una profesora</span><blockquote lang="en">Could you please send me the notes?</blockquote><small>Could y please suavizan la petición.</small></div></div><p>Las dos son gramaticales. La segunda ofrece una opción más cortés; usar palabras difíciles no la hace automáticamente más formal.</p><p>¿Qué cambiarías si le escribieras a alguien de confianza? Puedes explicarlo o probar tu frase.</p>${actions([btn('write','Escribir mi petición','',true),btn('justify','Explicar la diferencia','data-stage="0"'),btn('model','Ver el correo completo')])}</section>`;
      case 'model': return `<section class="card"><p class="eyebrow">Modelo de práctica · no es tu borrador</p><h2>Pedir más tiempo para una entrega</h2><div class="doc-text" lang="en">${esc(D.model)}</div><p>“Dear Professor” abre el mensaje con un tratamiento acorde a la relación; “Could I have…” formula una petición cortés; “until Friday” concreta el plazo. El motivo explica la necesidad y “Best regards” cierra el correo con un tono coherente.</p>${actions([btn('write','Probar con mis recursos','',true),btn('recall','Intentar sin el modelo')])}</section>`;
      case 'draft': return `<section class="card"><p class="eyebrow">Tu producción · versión guardada</p><h2>Un punto de partida propio</h2><div class="doc-text" lang="en">${esc(m.text)}</div>${actions([btn('review','Revisar una frase','',true),btn('versions','Comparar versiones'),btn('write','Escribir otra versión')])}</section>`;
      case 'correction': return correction(s,m);
      case 'reading': return `<section class="card reading-card"><p class="eyebrow">Lectura de práctica · texto creado para la demo</p><h2>Making room for focused work</h2><p>Una nota para estudiantes sobre cómo organizar el estudio. Antes de consultar: ¿qué idea general encuentras?</p><p class="reading" lang="en">A <button class="word-chip" data-action="pick-word" data-word="dedicated">dedicated</button> space helps you focus on your work. Short breaks help students stay <button class="word-chip" data-action="pick-word" data-word="productive">productive</button> during a long study session. Set a <button class="word-chip" data-action="pick-word" data-word="deadline">deadline</button> for each task so you know when to finish.</p><p class="small">Puedes tocar una palabra o compartir tu interpretación en el chat.</p></section>`;
      case 'clue': return `<section class="card"><p class="eyebrow">Antes de consultar · ${esc(m.word)}</p><blockquote class="doc-text" lang="en">${esc(m.context)}</blockquote><p>${esc(m.text)}</p><p>¿Cuál es tu hipótesis y qué parte de la oración te hizo pensar eso?</p>${actions([btn('definition','Prefiero ver el significado')])}</section>`;
      case 'definition': return wordCard(s,m);
      case 'recall': return textBlock(m.text) + actions([btn('reveal-support','Necesito consultar el apoyo')]);
      case 'practice-result': return textBlock(m.text) + `<p class="note">Tu intento quedó registrado${m.help ? ' con apoyo consultado' : ' con el material anterior oculto'}. No se ha calificado su corrección.</p>` + actions([btn(m.topic?'email-lesson':s.task==='email'?'compare':'definition','Contrastar con el ejemplo',m.topic?`data-topic="${m.topic}"`:'',true),btn('transfer','Probar en otra situación',m.topic?`data-topic="${m.topic}"`:''),btn('notebook','Ver mis aportes')]);
      case 'finish': return `<section class="card finish-summary"><h2>Un punto para retomar</h2><p>Guardaste ${s.evidence.length} ${s.evidence.length===1?'aporte':'aportes'} y ${s.words.length} ${s.words.length===1?'palabra':'palabras'}. Puedes volver desde Conversaciones.</p><p>${esc(m.text)}</p>${actions([btn('reflection','Anotar una duda pendiente','',true),btn('export','Descargar mis notas'),btn('transfer','Seguir practicando')])}</section>`;
      default: return textBlock(m.text);
    }
  }
  function renderMessages() {
    const s = current();
    $('#chat-messages').innerHTML = !s ? '' : s.messages.map((m,i) => `<article class="message ${m.kind==='user'?'user':'assistant'} ${s.recall && i<s.recallStart?'recall-hidden':''}" data-message="${esc(m.id)}"${s.recall&&i<s.recallStart?' aria-hidden="true"':''}>${m.kind==='user'?`<div class="user-text">${esc(m.text)}</div>`:`<div class="assistant-label"><span aria-hidden="true">✦</span> Lingua IA</div><div class="message-content">${content(s,m)}</div>`}</article>`).join('');
    $('#recall-banner').hidden = !s?.recall;
  }
  function render() {
    const s = current(), active = Boolean(s);
    $('#main').className = active ? 'active-chat' : 'home';
    $('#welcome').hidden = active; $('#conversation').hidden = !active;
    $('#starter-actions').hidden = active; $('#notebook-button').hidden = !active;
    if (s) {
      $('#task-label').textContent = D.tasks[s.task]; $('#chat-title').textContent = s.task === 'email' ? 'Aprender inglés con tus propias palabras' : s.task === 'vocab' ? 'Del contexto a tus propias palabras' : 'Busquemos un punto de partida';
      $('#learning-plan').hidden = s.task === 'general';
      const stages = D.stages[s.task] || [];
      $('#stage-position').textContent = stages.length ? `Etapa ${s.stage + 1} de ${stages.length} · ${stages[s.stage]}` : '';
      $('#stagebar').innerHTML = stages.map((title,i)=>`<button class="stage" data-action="stage" data-stage="${i}" ${i===s.stage?'aria-current="step"':''}>${title}<small>${i===s.stage?'Actual · ':''}${s.stageEvidence.includes(i)?'Aporte guardado':'Sin aporte aún'}</small></button>`).join('');
    }
    renderMessages(); renderAssist(); save();
  }
  function renderAssist() {
    const text = input.value, s=current();
    const raw = detect(text), task = chosenTask || ((raw==='general'||raw==='ambiguous') ? s?.task : raw);
    const suggestion = suggest(text,task);
    const show = suggestion && dismissed !== `${task}:${suggestion.key}` && !s?.recall && (!s?.pending || lessonQuery(text));
    $('#send-btn').disabled = !text.trim();
    $('#composer-mode-hint').textContent = s?.pending ? s.pending.label : task && task in D.tasks && task!=='general' ? `${D.tasks[task]} · puedes cambiar de tarea` : raw==='ambiguous'?'Correo o vocabulario · puedes decidir al enviar':'Tu punto de partida, en español o inglés';
    $('#prompt-assist').hidden = !show;
    if(show) $('#prompt-assist').innerHTML = `<div class="assist-label">${Icons.sparkles()} Sugerencia para tu consulta ${btn('dismiss-prompt','Descartar')}</div><span class="assist-suggestion">${esc(suggestion.add)}</span><p class="assist-reason">${esc(suggestion.why)}</p>${actions([btn('use-prompt','Añadir a mi mensaje','',true),btn('edit-prompt','Editar la sugerencia')])}`;
  }
  function notice(t,undo=false) { $('#composer-notice').innerHTML = `${esc(t)} ${undo?btn('undo-prompt','Deshacer'):''}`; $('#live-region').textContent = t; }
  function persistInput() { const s=current(); if(s){s.inputDraft=input.value;save();} }
  function sizeInput() { input.style.height='auto';input.style.height=Math.min(input.scrollHeight,220)+'px'; }
  function setInput(text) { input.value=text; sizeInput(); renderAssist(); persistInput();input.focus(); }
  function afterAction(scroll=true) { render(); if(scroll) window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'}); input.focus({preventScroll:true}); }
  function startIntro(s,text) {
    if(s.task==='general') { message(s,'choice','¿Quieres aprender expresiones para un correo o comprender una palabra en contexto? Puedes elegir o contarme más; tu mensaje ya está guardado.'); return; }
    if(s.task==='email') {
      const pasted=pastedEmail(text);
      if(pasted){saveDraft(s,pasted);review(s);return;}
      const topic=lessonQuery(text);
      if(topic){learnEnglish(s,topic);return;}
      if(/dear\s|best regards|kind regards|i am agree|send me the/i.test(text)) { saveDraft(s,text.replace(/^.*?:\s*\n(?=Dear)/is,'')); review(s); return; }
      message(s,'text','Usaremos el correo para aprender expresiones del inglés: qué significan, cómo se construyen y cuándo usarlas. Puedes comenzar con un intento propio, comparar ejemplos o preguntar por una expresión; no hace falta completar apartados.',{start:true});
    } else {
      const word = Object.keys(D.words).find(w=>new RegExp(`\\b${w}\\b`,'i').test(text));
      if(!word && !/vocabulario|lectura/i.test(text)) { message(s,'text','Comparte la oración y la palabra que te genera duda. La demo ofrece fichas para dedicated, productive y deadline; para otras palabras registra tu hipótesis sin inventar una definición.'); message(s,'reading'); s.pending={type:'custom-context',label:'Comparte tu palabra y su oración'}; return; }
      s.word = word || 'dedicated';
      const quoted = [...text.matchAll(/[“"«]([^”"»]+)[”"»]/g)].map(m=>m[1]).find(t=>t.includes(' ')&&t.toLowerCase().includes(s.word)) || text.match(/(?:en (?:esta |la )?(?:frase|oraci[oó]n)|contexto)\s*:\s*([^\n]+)/i)?.[1];
      s.context = quoted || D.words[s.word].context;
      if(quoted && normalize(quoted).replace(/[^\w]+/g,' ').trim()!==normalize(D.words[s.word].context).replace(/[^\w]+/g,' ').trim()) { message(s,'text',`Conservé tu oración con “${s.word}”. Para este contexto, formula una hipótesis y contrástala con un diccionario. La ficha disponible pertenece al ejemplo de la demo; no confirma la acepción de tu oración.`);message(s,'reading');s.pending={type:'custom-inference',label:'Tu hipótesis y la pista de tu oración'};return; }
      if(!quoted)message(s,'text','Como no hay una oración completa entre comillas, propongo un ejemplo de práctica. Puedes compartir tu propia frase indicando: en esta frase: …');
      message(s,'text','Primero podemos buscar una pista; luego contrastar tu interpretación y usar la palabra en otra situación.',{start:true});
      clue(s);
    }
  }
  function learnEnglish(s,topic) {
    if(!D.emailLessons[topic])return;
    if(s.recall)s.helpUsed=true;
    s.task='email';s.emailTopic=topic;s.recall=false;s.helpUsed=true;s.stage=0;
    s.pending={type:'language-practice',topic,label:'Tu expresión en inglés y lo que significa para esta situación'};
    message(s,'email-lesson','',{topic});
  }
  function saveDraft(s,text) {
    s.stage=1;
    s.messages.filter(m=>m.kind==='correction').forEach(m=>m.status='outdated');
    s.draft=text; s.versions.push({id:id(),label:s.versions.length?'Nueva producción propia':'Original · producción propia',text,date:new Date().toISOString()});
    evidence(s,'Producción propia',text);message(s,'draft',text);s.stage=1;
  }
  function review(s) {
    if (s.recall) s.helpUsed = true;
    s.recall=false;s.pending=null;s.stage=1;
    if(!s.draft){message(s,'text','Comparte tu frase o correo en inglés. Revisaremos solo el fragmento pertinente y conservaremos el resto.');s.pending={type:'draft',label:'Escribe tu frase o correo en inglés'};return;}
    const rules=[
      {re:/\bI am agree\b/i,after:'I agree',category:'Gramática',reason:'Agree ya es un verbo: “I agree”. No necesita am en esta estructura. El significado de estar de acuerdo se mantiene.'},
      {re:/\bI want you to send me ([^.!?\n]+)[.!?]?/i,after:m=>`Could you please send me ${m[1]}?`,category:'Tono',reason:'“I want you to…” es gramatical, pero puede sonar exigente. “Could you please…?” suaviza la petición. La conveniencia depende de la relación; no es un error gramatical.'},
      {re:/(?:^|\n)(Send me [^.!?\n]+)[.!?]?/i,group:1,after:m=>`Could you please ${m[1][0].toLowerCase()+m[1].slice(1)}?`,category:'Tono',reason:'El imperativo puede servir entre personas de confianza. Could you please ofrece otra opción de cortesía sin cambiar lo que se solicita.'}
    ];
    let count=0;
    for(const r of rules){const match=s.draft.match(r.re);if(!match)continue;const before=r.group?match[r.group]:match[0]; if(s.messages.some(m=>m.kind==='correction'&&m.before===before&&m.status==='pending'))continue;message(s,'correction','',{before,after:typeof r.after==='function'?r.after(match):r.after,category:r.category,reason:r.reason,status:'pending'});count++;}
    if(!count) message(s,'text','No tengo una revisión automática fiable para este fragmento en la demo. Puedes comparar la intención y la cortesía con los ejemplos, o explicar una elección que quieras contrastar. Tu texto sigue guardado.');
    s.stage=1;
  }
  function clue(s) {const w=D.words[s.word];if(s.recall)s.helpUsed=true;s.recall=false;message(s,'clue',w.clue,{word:s.word,context:s.context||w.context});s.pending={type:'inference',label:'Tu hipótesis de significado y una pista del contexto'};s.stage=0;}
  function definition(s,hypothesis='') {const w=D.words[s.word];if(s.recall)s.helpUsed=true;s.recall=false;s.pending=null;s.stage=1;message(s,'definition','',{word:s.word,context:s.context||w.context,hypothesis});}
  function recall(s,transfer=false) {
    const topic=s.task==='email'&&D.emailLessons[s.emailTopic]?s.emailTopic:null;
    s.pending={type:transfer?'transfer':'recall',topic,label:transfer?'Tu intento en una situación diferente':'Tu intento sin el material anterior'};
    s.stage=transfer?3:2;s.recall=true;s.helpUsed=false;s.recallStart=s.messages.length;
    const text=topic?D.emailLessons[topic][transfer?'transfer':'recall']:transfer ? s.task==='email'?'Ahora le escribes a un compañero de confianza para pedir sus apuntes. Redacta un correo breve y explica qué cambiarías respecto al tono con una profesora.':D.words[s.word].transfer : s.task==='email'?'Sin mirar el modelo: pide más tiempo para una entrega en una frase en inglés. Después explica por qué elegirías ese tono.':`Sin mirar la definición: explica “${s.word}” con tus palabras y úsala en una oración propia.`;
    message(s,'recall',text);
  }
  function pendingAnswer(s,text) {
    const pending=s.pending;s.pending=null;
    if(pending.type==='language-practice'){
      s.stage=1;s.emailTopic=pending.topic;
      evidence(s,'Práctica de inglés · '+D.emailLessons[pending.topic].label,text);
      message(s,'language-attempt',text,{topic:pending.topic});return;
    }
    if(pending.type==='draft'){saveDraft(s,text);return;}
    if(pending.type==='inference'){evidence(s,'Hipótesis y pista contextual',text);definition(s,text);return;}
    if(pending.type==='custom-context'){message(s,'text','Tu contexto quedó registrado. Propón un significado y señala una pista; puedes usar un diccionario para contrastarlo. No asignaré la acepción de un ejemplo diferente.');evidence(s,'Contexto propio por contrastar',text);s.pending={type:'custom-inference',label:'Tu hipótesis y una pista de la oración'};return;}
    if(pending.type==='custom-inference'){evidence(s,'Hipótesis propia por contrastar',text);message(s,'text','Guardé tu interpretación como hipótesis, pendiente de contraste. Para explorar una ficha preparada puedes tocar una palabra de la lectura de práctica.');message(s,'reading');return;}
    if(pending.type==='recall'||pending.type==='transfer'){
      evidence(s,pending.type==='transfer'?'Producción en otra situación':'Intento de recuperación',text);
      message(s,'practice-result','Conservé tu producción. Contrasta ahora si expresa la intención que buscabas y qué diferencia encuentras frente al ejemplo.',{help:s.helpUsed,topic:pending.topic});
      s.recall=false;return;
    }
    evidence(s,pending.type==='reflection'?'Duda para retomar':s.task==='vocab'?'Explicación de significado y uso':'Justificación de una elección',text);
    message(s,'text','Tu explicación quedó guardada con tus palabras. Puedes contrastarla con el ejemplo, reformular tu producción o probar otra situación.');
  }
  function send() {
    const text=input.value.trim();if(!text)return;
    let s=current();const inferred=detect(text), task=chosenTask || (inferred==='ambiguous'?'general':inferred);
    if(!s) {s=session(task,text);message(s,'user',text);startIntro(s,text);}
    else {
      message(s,'user',text);
      const topic=lessonQuery(text), pasted=pastedEmail(text);
      const instruction=pasted?text.slice(0,text.indexOf(pasted)):text;
      const explicitReview=/\b(revisa\w*|corrig\w*|correcci\w*|review|proofread)\b/.test(normalize(instruction));
      if(pasted && task==='email' && (explicitReview || !['recall','transfer'].includes(s.pending?.type))){
        if(s.task!=='email')s.stageEvidence=[];
        s.task='email';s.emailTopic=null;saveDraft(s,pasted);review(s);
      }
      else if(topic && (s.task==='email'||task==='email'))learnEnglish(s,topic);
      else if(s.pending)pendingAnswer(s,text);
      else if(s.task==='general' && task!=='general'){s.task=task;startIntro(s,text);}
      else if(s.task==='email' && /dear\s|best regards|kind regards|i am agree|i want you to|^send me\b/i.test(text)){saveDraft(s,text);review(s);}
      else if(s.task==='vocab' && Object.keys(D.words).some(w=>new RegExp(`\\b${w}\\b`,'i').test(text))){startIntro(s,text);}
      else {evidence(s,'Nota o pregunta por revisar',text);message(s,'text','Guardé tu aporte para retomarlo. Puedes elegir el apoyo que necesitas; las respuestas de esta demo están preparadas para ejemplos concretos.',{start:s.task!=='general'});if(s.task==='general')message(s,'choice','¿Con qué actividad se relaciona tu idea?');}
    }
    chosenTask=null;dismissed='';promptUndo=null;s.inputDraft='';input.value='';sizeInput();notice('');s.closed=false;afterAction();
  }
  function newChat() { persistInput();state.active=null;chosenTask=null;dismissed='';promptUndo=null;input.value='';$('#task-choice').hidden=true;$('#learning-plan').open=false;notice('');render();sizeInput();input.focus(); }
  function openDialog(title,html,type) {
    const dialog=$('#workspace-dialog');if(!dialog.open)returnFocus=document.activeElement;
    dialog.classList.toggle('conversation-drawer', type === 'history');
    panel=type;$('#dialog-title').textContent=title;$('#dialog-content').innerHTML=html;
    if(!dialog.open)dialog.showModal();$('#dialog-content').scrollTop=0;
  }
  function history() {
    const html=['email','vocab','general'].map(task=>`<section class="history-group"><h3>${D.tasks[task]}</h3>${state.sessions.filter(s=>s.task===task).map(s=>`<button class="session-link" data-action="resume" data-id="${s.id}" aria-current="${s.id===state.active}">${esc(s.title)}<span class="sr-only"> · ${s.evidence.length} aportes</span></button>`).join('')||'<p class="small">Aún no hay conversaciones.</p>'}</section>`).join('');
    openDialog('Conversaciones',`<p class="small">Se guardan en este navegador. Retoma el contexto, tu borrador y tus notas.</p>${btn('new','Empezar otro chat')}${html}`,'history');$('[data-action="history"]').setAttribute('aria-expanded','true');
  }
  function notebook() {
    const s=current();if(!s)return;
    openDialog('Mi aprendizaje',`<p>${D.tasks[s.task]} · guardado en este navegador</p><div class="metrics"><div><strong>${s.evidence.length}</strong><span>Aportes escritos</span></div><div><strong>${s.words.length}</strong><span>Palabras guardadas</span></div></div><p class="small">Actividad registrada; no acredita dominio. Las explicaciones y los intentos deben contrastarse. Las sugerencias añadidas (${s.promptUses}) no demuestran una reducción de consultas.</p>${actions([btn('export','Descargar mis notas'),btn('versions','Ver versiones del correo'),btn('finish','Cerrar esta práctica')])}${s.words.length?`<h3>Palabras para repasar</h3><p>${s.words.map(esc).join(' · ')}</p>${btn('repaso','Retomar un repaso sin definición')}`:''}<h3>Mis producciones y reflexiones</h3>${s.evidence.map(e=>`<section class="evidence"><strong>${esc(e.kind)}</strong>${e.topic&&D.emailLessons[e.topic]?`<span class="small"> · ${esc(D.emailLessons[e.topic].label)}</span>`:''}<small>${new Date(e.date).toLocaleString('es-PE')}${/recuper|otra situaci/i.test(e.kind)?e.help?' · consultaste apoyo':' · material anterior oculto':''}</small><p>${esc(e.text)}</p></section>`).join('')||'<p class="empty-note">Todavía no escribiste un aporte propio. Abrir una etapa o guardar una palabra no acredita aprendizaje.</p>'}`,'notebook');
  }
  function versions() {const s=current();if(!s)return;openDialog('Versiones de tu correo',`<p class="small">Recuperar crea una nueva versión; conserva las anteriores. El original sigue disponible.</p>${s.versions.map((v,i)=>`<details class="version-item" ${i===s.versions.length-1?'open':''}><summary>${i+1}. ${esc(v.label)}</summary><pre lang="en">${esc(v.text)}</pre>${btn('restore','Usar esta versión',`data-id="${v.id}"`)}</details>`).join('')||'<p>No hay un correo propio guardado todavía.</p>'}`,'versions');}
  function demo() {
    const groups=[
      ['email','Aprender inglés con un correo',[
        ['email','Comprender el tono','Compara una misma petición según la relación.'],
        ['subject','Comprender el asunto','Aprende request for y question about; adapta una expresión.'],
        ['greeting','Comprender saludos','Compara Dear y Hi según la relación.'],
        ['request','Construir peticiones','Relaciona can/could, sujeto y verbo con la intención.'],
        ['reason','Dar una razón o una finalidad','Compara because + oración y to + verbo.'],
        ['closing','Comprender cierres','Explica la función de Best regards y Thanks.'],
        ['review','Revisar un correo pegado','Compara gramática y cortesía; acepta, conserva o deshaz cada cambio.']
      ]],
      ['vocab','Aprender vocabulario en contexto',[
        ['vocab','Del contexto a una oración propia','Infiere un significado, contrasta acepciones y practica sin la definición.']
      ]],
      ['general','Por explorar',[
        ['ambiguous','Empezar sin saber la tarea','Comprueba cómo se pide contexto sin adivinar.']
      ]]
    ];
    const html=groups.map(([task,title,examples])=>`<section class="demo-group" data-example-group="${task}"><h3>${title}</h3>${examples.map(([key,label,detail])=>`<article class="demo-card"><h4>${label}</h4><p>${detail}</p>${btn('load-demo','Preparar ejemplo',`data-example="${key}"`)}</article>`).join('')}</section>`).join('');
    openDialog('Ideas para explorar',`<p>Los ejemplos de correo y vocabulario están separados. Cada uno prepara un mensaje editable en un chat nuevo; tú decides cuándo enviarlo.</p>${html}<p class="small">No se envían correos ni se consulta una IA externa. Las respuestas son material preparado.</p>`,'demo');
  }
  function closeDialog() {$('#workspace-dialog').close();panel='';$('[data-action="history"]').setAttribute('aria-expanded','false');if(returnFocus?.isConnected)returnFocus.focus();}
  function exportNotes() {const s=current();if(!s)return;const text=`Lingua IA · ${D.tasks[s.task]}\n${s.title}\nActividad registrada; no acredita dominio. Respuestas de ejemplo.\n\n`+s.evidence.map(e=>`${e.kind}${e.topic&&D.emailLessons[e.topic]?' · '+D.emailLessons[e.topic].label:''} · ${e.date}\n${e.text}`).join('\n\n')+`\n\nPalabras guardadas: ${s.words.join(', ')||'ninguna'}\n\nVersiones\n`+s.versions.map(v=>`${v.label}\n${v.text}`).join('\n\n');const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='lingua-mis-notas.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  function handle(action,el) {
    let s=current();
    switch(action){
      case 'send':send();return;
      case 'new':if($('#workspace-dialog').open)closeDialog();newChat();return;
      case 'history':history();return;
      case 'notebook':notebook();return;
      case 'versions':versions();return;
      case 'demo':demo();return;
      case 'export':exportNotes();return;
      case 'close-dialog':closeDialog();return;
      case 'starter':chosenTask=el.dataset.task;setInput(D.starters[chosenTask]);notice('Puedes editar o enviar esta idea.');return;
      case 'load-demo':closeDialog();newChat();setInput(D.examples[el.dataset.example]);return;
      case 'resume':persistInput();state.active=el.dataset.id;s=current();chosenTask=null;dismissed='';promptUndo=null;closeDialog();input.value=s.inputDraft||'';notice('Retomaste tu práctica. El contexto y las notas siguen aquí.');afterAction();sizeInput();return;
      case 'use-prompt':case 'edit-prompt':{
        const raw=detect(input.value),task=chosenTask||((raw==='general'||raw==='ambiguous')?s?.task:raw),p=suggest(input.value,task);if(!p)return;
        promptUndo={before:input.value,after:input.value.trim()+' '+p.add};setInput(promptUndo.after);dismissed=`${task}:${p.key}`;if(s)s.promptUses++;notice(action==='edit-prompt'?'Sugerencia añadida para que la edites antes de enviar.':'Sugerencia añadida; puedes editarla o deshacer.',true);save();return;}
      case 'dismiss-prompt':{const raw=detect(input.value),task=chosenTask||((raw==='general'||raw==='ambiguous')?s?.task:raw),p=suggest(input.value,task);dismissed=`${task}:${p?.key}`;if(s)s.promptDismisses++;renderAssist();save();input.focus();return;}
      case 'undo-prompt':if(promptUndo&&input.value===promptUndo.after){setInput(promptUndo.before);promptUndo=null;notice('Sugerencia retirada. Tu mensaje anterior está intacto.');}else notice('Tu mensaje cambió después de añadir la sugerencia. Puedes editarla directamente para conservar lo que escribiste.');return;
      case 'change-task':$('#task-choice').hidden=!$('#task-choice').hidden;$('#task-choice').innerHTML=`<p>¿Dónde quieres continuar este chat?</p>${actions([btn('assign','Correo en inglés','data-task="email"'),btn('assign','Vocabulario en contexto','data-task="vocab"')])}`;return;
      case 'assign':if(!s)return;s.task=el.dataset.task;s.emailTopic=null;s.pending=null;s.recall=false;s.stage=0;s.stageEvidence=[];$('#task-choice').hidden=true;message(s,'text',`Este chat se organizó en ${D.tasks[s.task].toLowerCase()}. Conservé los mensajes y tus aportes.`,{start:true});break;
      case 'email-lesson':if(!s)return;learnEnglish(s,el.dataset.topic);break;
      case 'email-practice':if(!s||!D.emailLessons[el.dataset.topic])return;s.emailTopic=el.dataset.topic;s.recall=false;s.stage=1;s.pending={type:'language-practice',topic:s.emailTopic,label:'Tu expresión en inglés y una explicación de significado o uso'};message(s,'text',D.emailLessons[s.emailTopic].prompt);break;
      case 'compare':if(!s)return;s.emailTopic=null;s.recall=false;s.helpUsed=true;s.pending={type:'justify',label:'Explica qué cambia en el tono o prueba una comparación'};s.stage=0;message(s,'compare');break;
      case 'model':if(!s)return;s.emailTopic=null;s.recall=false;s.helpUsed=true;s.pending=null;s.stage=0;message(s,'model');break;
      case 'write':if(!s)return;s.emailTopic=null;s.pending={type:'draft',label:'Tu propia frase o correo en inglés'};s.stage=1;s.recall=false;message(s,'text','Escribe una petición o un correo con tus recursos. Puedes incluir a quién te diriges y explicar el tono; no tienes que completar apartados.');break;
      case 'review':if(!s)return;review(s);break;
      case 'accept':case 'reject':{
        if(!s)return;const m=s.messages.find(m=>m.id===el.dataset.id);if(!m||m.status!=='pending')return;
        if(action==='accept'){
          if(!s.draft.includes(m.before)){notice('Tu borrador cambió. Revisa la versión actual antes de aplicar esta propuesta.');return;}
          m.previous=s.draft;s.draft=s.draft.replace(m.before,m.after);m.applied=s.draft;s.versions.push({id:id(),label:`Cambio de ${m.category.toLowerCase()}`,text:s.draft,date:new Date().toISOString()});m.status='accepted';
        }else m.status='rejected';
        notice(action==='accept'?'Cambio aplicado solo en el fragmento elegido. El resto se conserva.':'Conservaste tu frase. Puedes explicar por qué encaja con tu intención.');break;}
      case 'undo-correction':{
        if(!s)return;const m=s.messages.find(m=>m.id===el.dataset.id);if(!m)return;
        if(m.status==='accepted'){
          if(s.draft!==m.applied){notice('Hay cambios posteriores. Recupera una versión para no perderlos.');versions();return;}
          s.draft=m.previous;s.versions.push({id:id(),label:'Decisión deshecha',text:s.draft,date:new Date().toISOString()});
        }m.status='pending';notice('Decisión deshecha; las versiones anteriores siguen disponibles.');break;}
      case 'restore':{if(!s)return;const v=s.versions.find(v=>v.id===el.dataset.id);if(!v)return;s.draft=v.text;s.versions.push({id:id(),label:'Recuperada de '+v.label,text:v.text,date:new Date().toISOString()});s.messages.filter(m=>m.kind==='correction').forEach(m=>m.status='outdated');renderMessages();save();versions();notice('Versión recuperada. Las anteriores se conservan.');return;}
      case 'justify':case 'vocab-explain':if(!s)return;if(s.recall)s.helpUsed=true;s.recall=false;s.stage=action==='vocab-explain'?1:Number(el.dataset.stage??s.stage);s.pending={type:'justify',label:action==='justify'?'Tu explicación del cambio o del tono':'Tu explicación del significado y del contexto'};message(s,'text',action==='justify'?'¿Qué efecto tiene la expresión que elegiste en el significado o en el tono? Puedes mantener tu frase si encaja con tu intención.':'Explica con tus palabras qué acepción encaja y qué pista de la oración permite descartar la otra. Puedes añadir un patrón de uso que quieras recordar.');break;
      case 'reading':if(!s)return;s.task='vocab';s.stage=0;s.pending=null;s.recall=false;message(s,'reading');break;
      case 'pick-word':if(!s)return;s.word=el.dataset.word;s.context=D.words[s.word].context;clue(s);break;
      case 'clue':if(!s)return;clue(s);break;
      case 'definition':if(!s)return;if(s.recall)s.helpUsed=true;s.recall=false;definition(s);break;
      case 'save-word':if(!s)return;if(s.words.includes(el.dataset.word)){s.words=s.words.filter(w=>w!==el.dataset.word);notice('Palabra retirada del repaso. Tus producciones siguen guardadas.');}else{s.words.push(el.dataset.word);notice('Palabra guardada para repasar; guardarla no demuestra que ya la dominas.');}break;
      case 'recall':case 'transfer':case 'repaso':if(!s)return;if(D.emailLessons[el.dataset.topic])s.emailTopic=el.dataset.topic;if($('#workspace-dialog').open)closeDialog();if(action==='repaso'&&s.words.length){s.word=s.words[0];s.context=D.words[s.word].context;}recall(s,action==='transfer');break;
      case 'reveal-support':if(!s)return;s.recall=false;s.helpUsed=true;notice('Apoyo visible. Se registrará que lo consultaste durante este intento.');break;
      case 'stage':if(!s)return;if(s.recall)s.helpUsed=true;s.recall=false;s.stage=Number(el.dataset.stage);if(s.stage>=2)recall(s,s.stage===3);else if(s.stage===0){if(s.task==='email'){if(D.emailLessons[s.emailTopic])learnEnglish(s,s.emailTopic);else{message(s,'compare');s.pending={type:'justify',label:'Tu comparación del tono'};}}else clue(s);}else{if(s.task==='email'){if(D.emailLessons[s.emailTopic]){s.pending={type:'language-practice',topic:s.emailTopic,label:'Tu expresión en inglés y una explicación de significado o uso'};message(s,'text',D.emailLessons[s.emailTopic].prompt);}else{s.pending={type:'draft',label:'Tu propia frase o correo'};message(s,'text','Prueba tu propia petición. Después puedes contrastar una expresión.');}}else definition(s);}break;
      case 'finish':if(!s)return;if($('#workspace-dialog').open)closeDialog();s.closed=true;s.recall=false;s.pending=null;message(s,'finish',s.evidence.length?'Para la próxima práctica: intenta recuperar una expresión antes de volver a los ejemplos.':'Aún no hay producciones propias guardadas. Puedes retomar más adelante o dejar una duda pendiente.');break;
      case 'reflection':if(!s)return;s.pending={type:'reflection',label:'Una duda o una idea para tu próxima práctica'};message(s,'text','¿Qué quieres comprobar o intentar la próxima vez? Lo guardaremos junto a esta práctica.');break;
      default:return;
    }
    afterAction();
  }
  document.addEventListener('click',e=>{const el=e.target.closest('[data-action]');if(el&&!el.disabled)handle(el.dataset.action,el);});
  input.addEventListener('input',()=>{dismissed='';notice('');sizeInput();renderAssist();persistInput();});
  input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();send();}});
  $('#workspace-dialog').addEventListener('close',()=>{panel='';$('[data-action="history"]').setAttribute('aria-expanded','false');});
  $('#workspace-dialog').addEventListener('click',e=>{if(e.target===$('#workspace-dialog')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeDialog();}});
  document.querySelectorAll('[data-icon]').forEach(el=>{el.innerHTML=Icons[el.dataset.icon]();});
  load();state.active=null;render();
  // API de inspección del prototipo usada por las pruebas del navegador.
  window.Lingua={getState:()=>clone(state),detect,suggest,reset(){state={version:1,sessions:[],active:null};try{localStorage.removeItem(KEY);}catch(_){}newChat();},send,openDemo:demo};
})();
