(() => {
  'use strict';
  const D = window.TutorData;
  const H = window.TutorHTA;
  const $ = (q) => document.querySelector(q);
  const esc = (v = '') => String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const normalize = (t) => t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const id = () => (crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).slice(2));
  const KEY = 'lingua-tutor-v2';
  const LEGACY_KEY = 'lingua-tutor-v1';
  const clone = v => JSON.parse(JSON.stringify(v));
  let state = {version:2, sessions:[], active:null};
  let restoredInput = null;
  let chosenTask = null, dismissed = '', promptUndo = null, panel = '', returnFocus = null;
  const input = $('#chat-input');
  function current() { return state.sessions.find(s => s.id === state.active); }
  function warnStorage() { const el = $('#storage-status'); el.hidden = false; el.textContent = 'El navegador no permite guardar esta práctica. Puedes continuar y descargar tus notas desde Mi aprendizaje.'; }
  function load() {
    try {
      const parsed = JSON.parse(localStorage.getItem(KEY) || localStorage.getItem(LEGACY_KEY));
      if (parsed && [1,2].includes(parsed.version) && Array.isArray(parsed.sessions) && parsed.sessions.every(s => s && typeof s.id === 'string' && s.task in D.tasks && Array.isArray(s.messages) && Array.isArray(s.evidence) && Array.isArray(s.versions) && Array.isArray(s.words) && typeof s.draft === 'string')) {
        state = parsed;state.version=2;
        for (const s of state.sessions) {
          H.prepare(s);
          for(const m of s.messages.filter(m=>m.kind==='correction'&&m.status==='pending'))if(m.start===undefined)m.status='outdated';
          s.savedContexts = {...s.savedContexts};
          for (const word of s.words) {
            if (s.savedContexts[word]) continue;
            const previous = s.messages.filter(m => m.word === word && m.context).slice(-1)[0];
            s.savedContexts[word] = (s.word === word && s.context) || previous?.context || D.words[word]?.context || '';
          }
        }
      }
    } catch (_) { warnStorage(); }
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (_) { warnStorage(); } }
  function session(task, title) {
    const s = {id:id(),task,title:title.slice(0,70),created:new Date().toISOString(),messages:[],evidence:[],words:[],versions:[],draft:'',inputDraft:'',stage:0,pending:null,word:'dedicated',context:'',recall:false,recallStart:0,helpUsed:false,closed:false,promptUses:0,promptDismisses:0,stageEvidence:[]};
    H.prepare(s);state.sessions.push(s); state.active = s.id; return s;
  }
  function message(s, kind, text = '', extra = {}) { const m = {id:id(),kind,text,...H.meta(s,kind),...extra}; s.messages.push(m); return m; }
  function evidence(s, kind, text) { s.evidence.push({kind,text,date:new Date().toISOString(),stage:s.stage,help:s.helpUsed}); if (!s.stageEvidence.includes(s.stage)) s.stageEvidence.push(s.stage); }
  function detect(text) {
    const t = normalize(text);
    if(/^(?:Subject:|Dear\s|Hi [^,\n]+,)/im.test(text)&&!/^\s*(?:que significa|que quiere decir|meaning of)/.test(t))return 'email';
    const email = /\b(correo|email|e-mail|mail|saludo|despedida|prorroga|peticion)\b|dear\s|best regards|kind regards|pedir (?:apuntes|material)|solicitar (?:apuntes|material)/.test(t);
    const vocab = /\b(vocabulario|palabra|acepcion|signific\w*|word|meaning|dedicated|productive|deadline)\b|que quiere decir/.test(t);
    if (email && vocab) {
      if (/que significa|que quiere decir|meaning of|acepcion|vocabulario/.test(t)) return 'vocab';
      if (/redact|revisa|escribir|correo a|tono de/.test(t)) return 'email';
      return 'ambiguous';
    }
    return email ? 'email' : vocab ? 'vocab' : 'general';
  }
  function suggest(text, task) {
    const t = normalize(text);
    if (text.trim().length < 7 || /\nDear |^Dear /i.test(text)) return null;
    const contextual=H.promptSuggestion(text,task,current());if(contextual)return contextual;
    if (task === 'email') {
      if (!/profesor|teacher|amig|companer|jefe|destinatario|professor|colega|universidad/.test(t) && (!current()?.hta.email.relation||current().hta.email.relation==='unknown')) return {key:'recipient', add:'Ayúdame a comparar cómo cambiaría la petición según la confianza con el destinatario.', why:'El destinatario ayuda a elegir el saludo y la cortesía.'};
      if (!/compar|explic|por que|diferencia/.test(t)) return {key:'tone', add:'Compara dos formas de pedir lo mismo y explícame qué cambia en el tono; quiero elegir mi propia expresión.', why:'Comparar la misma intención permite comprender el registro antes de redactar.'};
      if (!/conserv|sin (cambiar|reescribir)|solo|unicamente/.test(t)) return {key:'preserve', add:'Si propongo un borrador, sugiere cambios solo en la frase que revisemos y conserva el resto.', why:'La revisión localizada permite comprobar cada cambio sin perder tu intención.'};
    }
    if (task === 'vocab') {
      if (!/[“"'«:]/.test(text) && !/en esta frase|en la oracion|contexto/.test(t)) return {key:'context', add:'Quiero ver cómo cambia su significado en una oración. Si falta contexto, pídemelo antes de elegir una acepción.', why:'Una palabra puede tener varias acepciones; la oración ayuda a elegir.'};
      if (!/infer|hipotes|antes|deduc|pista/.test(t)) return {key:'infer', add:'Primero dame una pista del contexto para que intente inferir el significado; después lo contrastamos.', why:'Una hipótesis propia permite contrastar y ajustar lo que entiendes.'};
      if (!/propia|reutil|otro contexto|recuper|sin definicion/.test(t)) return {key:'reuse', add:'Después quiero usar la palabra en una oración propia y probarla en otra situación.', why:'Usar y recuperar una expresión va más allá de recordar su traducción.'};
    }
    return null;
  }
  const contextKey = text => normalize(text).replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
  function wordEntry(word, context) {
    const base = D.words[word];
    if (!base || !context) return null;
    const entry = [base, ...(base.alternatives || [])].find(item => contextKey(item.context) === contextKey(context));
    return entry ? {...base, ...entry} : null;
  }
  function activeWord(s) { return wordEntry(s.word, s.context || D.words[s.word]?.context); }
  function wordAttrs(m) { return `data-word="${esc(m.word || '')}" data-context="${esc(m.context || D.words[m.word]?.context || '')}"`; }
  function unavailableWord(s) {
    message(s,'text','No hay una ficha preparada para esta palabra y oración. Conserva el contexto y contrasta tu interpretación con un diccionario; puedes elegir expresamente otro ejemplo de la lectura.');
    s.recall=false;s.pending={type:'custom-inference',label:'Tu hipótesis y la pista de tu oración, pendientes de contraste'};
  }
  function btn(action, label, attrs = '', primary = false) { return `<button data-action="${action}" ${attrs} class="${primary ? 'primary' : ''}">${label}</button>`; }
  function actions(items) { return `<div class="actions">${items.join('')}</div>`; }
  function textBlock(t) { return `<p>${esc(t).replace(/\n/g,'<br>')}</p>`; }
  function introActions(task) {
    return task === 'email' ? actions([btn('compare','Comparar dos peticiones','',true),btn('write','Probar mi propia frase'),btn('model','Ver un modelo')]) : actions([btn('clue','Dame una pista','',true),btn('definition','Ver significado ahora'),btn('reading','Ver otra lectura')]);
  }
  function correction(s,m) {
    const accepted = m.status === 'accepted', decided = m.status && m.status !== 'pending';
    if(m.status==='outdated') return `<section class="card correction-card"><span class="badge">Propuesta de una versión anterior</span><div class="diff-line"><small>Fragmento revisado entonces</small><p lang="en">${esc(m.before)}</p></div><p class="small">Recuperaste otro borrador. Puedes solicitar una nueva revisión de la versión actual.</p>${actions([btn('review','Revisar versión actual'),btn('versions','Ver versiones')])}</section>`;
    return `<section class="card correction-card" aria-label="Propuesta de revisión"><span class="badge ${m.category === 'Gramática' ? 'grammar' : 'tone'}">${m.category === 'Gramática' ? '△ ' : ''}${esc(m.category)}</span><h2 style="margin-top:12px">${m.category === 'Gramática' ? 'Revisemos esta estructura' : m.category === 'Tono' ? 'Una alternativa de cortesía' : 'Contrastar esta alternativa'}</h2><div class="diff-line"><small>Tu frase</small><p lang="en">${esc(m.before)}</p></div><div class="diff-line proposal"><small>Propuesta · tú decides</small><p lang="en">${esc(m.after)}</p></div><details class="rule"><summary>Por qué se propone este cambio</summary><p>${esc(m.reason)}</p></details><p class="inline-help" style="margin-top:12px">Solo se modifica este fragmento. El resto del correo se conserva.</p>${decided ? `<p class="note">${accepted ? 'Sugerencia aplicada' : 'Conservaste tu frase'} · puedes revisar las versiones.</p>${actions([btn('undo-correction','Deshacer decisión',`data-id="${m.id}"`),btn('justify','Explicar mi decisión',`data-stage="1" data-id="${m.id}"`)])}` : actions([btn('accept','Usar esta sugerencia',`data-id="${m.id}"`,true),btn('reject','Conservar mi frase',`data-id="${m.id}"`),btn('justify','Explicar antes de decidir',`data-stage="1" data-id="${m.id}"`),btn('hta-explain','Pedir otra explicación'),btn('hta-candidate','Proponer otra frase')])}</section>`;
  }
  function wordCard(s, m) {
    const w = wordEntry(m.word, m.context || D.words[m.word]?.context);
    if (!w) return `<section class="card"><p>Esta ficha anterior no tiene una acepción preparada para su contexto. Tu oración se conserva para contrastarla.</p><blockquote>${esc(m.context)}</blockquote></section>`;
    return `<section class="card word-detail"><p class="eyebrow">${esc(w.word)} · en esta oración</p><blockquote class="doc-text" lang="en">${esc(m.context || w.context)}</blockquote>${m.startingPoint ? `<p class="small">Punto de partida: ${esc(m.startingPoint)}</p>` : ''}${m.hypothesis ? `<div class="diff-line"><small>Tu interpretación inicial</small><p>${esc(m.hypothesis)}</p></div>` : ''}<div class="diff-line proposal"><small>Acepción del ejemplo</small><p>${esc(w.meaning)}</p></div><details class="rule"><summary>Contrastar acepciones, patrón y ejemplos</summary><p>${esc(w.other)}</p><p lang="en">${esc(w.example)}</p><p>${esc(w.pattern)}</p><p>${esc(w.register)}</p><p class="small">Ficha didáctica de la demo. Contrasta con un diccionario si la usas fuera de este ejemplo.</p></details>${actions([btn('vocab-explain','Explicar con mis palabras',wordAttrs(m),true),btn('save-word',H.isSaved(s,m)?'Quitar del repaso':'Guardar palabra',wordAttrs(m)),btn('recall','Probar sin definición',wordAttrs(m))])}${H.entryExtras(s,m)}</section>`;
  }
  function content(s,m) {
    if(m.kind==='hta')return H.render(s,m);
    switch (m.kind) {
      case 'text': return textBlock(m.text) + (m.start ? introActions(s.task)+(s.task==='email'?H.intro(s):'') : '');
      case 'choice': return textBlock(m.text) + actions([btn('assign','Aprender con un correo','data-task="email"'),btn('assign','Vocabulario en contexto','data-task="vocab"')]);
      case 'compare': return H.comparison(s,m);
      case 'model': return H.model(s,m);
      case 'draft': return `<section class="card"><p class="eyebrow">Tu producción · versión guardada</p><h2>Un punto de partida propio</h2><div class="doc-text" lang="en">${esc(m.text)}</div>${actions([btn('review','Revisar una frase','',true),btn('versions','Comparar versiones'),btn('write','Escribir otra versión'),btn('hta-consult','Consultar esta expresión',`data-version="${m.versionId||''}"`),btn('hta-review-fragment','Revisar un fragmento',`data-version="${m.versionId||''}"`),btn('hta-review-choice','Contrastar significado y datos')])}</section>`;
      case 'correction': return correction(s,m);
      case 'reading': return `<section class="card reading-card"><p class="eyebrow">Lectura de práctica · texto creado para la demo</p><h2>Making room for focused work</h2><p>Una nota para estudiantes sobre cómo organizar el estudio. Antes de consultar: ¿qué idea general encuentras?</p><p class="reading" lang="en">A <button class="word-chip" data-action="pick-word" data-word="dedicated">dedicated</button> space helps you focus on your work. Short breaks help students stay <button class="word-chip" data-action="pick-word" data-word="productive">productive</button> during a long study session. Set a <button class="word-chip" data-action="pick-word" data-word="deadline">deadline</button> for each task so you know when to finish.</p><p class="small">Puedes tocar una palabra o compartir tu interpretación en el chat.</p>${actions([btn('hta-reading-note','Relacionar la lectura con lo que sé'),btn('hta-priority','Decidir qué necesito consultar')])}</section>`;
      case 'clue': return `<section class="card"><p class="eyebrow">Antes de consultar · ${esc(m.word)}</p><blockquote class="doc-text" lang="en">${esc(m.context)}</blockquote><p>${esc(m.text)}</p><p>¿Cuál es tu hipótesis y qué parte de la oración te hizo pensar eso?</p>${actions([btn('definition','Prefiero ver el significado',wordAttrs(m)),btn('hta-priority','Decidir si consultar ahora'),btn('hta-lexical-tools','Explorar otras pistas',wordAttrs(m))])}</section>`;
      case 'definition': return wordCard(s,m);
      case 'recall': return textBlock(m.text) + actions([btn('reveal-support','Necesito consultar el apoyo')]);
      case 'practice-result': return textBlock(m.text) + `<p class="note">Tu intento quedó registrado${m.help ? ' con apoyo consultado' : ' con el material anterior oculto'}. No se ha calificado su corrección.</p>` + actions([btn((m.task||s.task)==='email'?'compare':'definition','Contrastar con el ejemplo',wordAttrs(m),true),btn('transfer','Probar en otra situación',wordAttrs(m)),btn('notebook','Ver mis aportes'),btn('hta-productions','Comparar mis producciones'),...((m.task||s.task)==='vocab'?[btn('hta-transfer-email','Trabajar esta idea en un correo')]:[])]);
      case 'finish': return `<section class="card finish-summary"><h2>Un punto para retomar</h2><p class="note">${esc(s.hta.status)}</p><p>Guardaste ${s.evidence.length} ${s.evidence.length===1?'aporte':'aportes'} y ${s.words.length} ${s.words.length===1?'palabra':'palabras'}. Puedes volver desde Conversaciones.</p><p>${esc(m.text)}</p>${actions([btn('reflection','Anotar una duda pendiente','',true),btn('export','Descargar mis notas'),btn('transfer','Seguir practicando')])}</section>`;
      default: return textBlock(m.text);
    }
  }
  function renderMessages() {
    const s = current();
    $('#chat-messages').innerHTML = !s ? '' : s.messages.map((m,i) => `<article class="message ${m.kind==='user'?'user':'assistant'} ${s.recall && i<s.recallStart?'recall-hidden':''}" data-message="${esc(m.id)}"${s.recall&&i<s.recallStart?' aria-hidden="true"':''}>${m.kind==='user'?`<div class="user-text">${esc(m.text)}</div>`:`<div class="assistant-label"><span aria-hidden="true">✦</span> Lingua IA</div><div class="message-content">${content(s,m)}</div>`}</article>`).join('');
    $('#recall-banner').hidden = !s?.recall;
    $('#recall-banner strong').textContent=s?.hta.resumeHidden?'Apoyo anterior oculto al retomar':'Un intento sin modelo';
  }
  function render() {
    const s = current(), active = Boolean(s);
    $('#main').className = active ? 'active-chat' : 'home';
    $('#welcome').hidden = active; $('#conversation').hidden = !active;
    $('#starter-actions').hidden = active; $('#notebook-button').hidden = !active;
    if (s) {
      $('#task-label').textContent = D.tasks[s.task]; $('#chat-title').textContent = s.task === 'email' ? 'Encontrar tus palabras para escribir' : s.task === 'vocab' ? 'Del contexto a tus propias palabras' : 'Busquemos un punto de partida';
      $('#learning-plan').hidden = s.task === 'general';
      const stages = D.stages[s.task] || [];
      $('#stage-position').textContent = stages.length ? `Etapa ${s.stage + 1} de ${stages.length} · ${stages[s.stage]}` : '';
      $('#stagebar').innerHTML = stages.map((title,i)=>`<button class="stage" data-action="stage" data-stage="${i}" ${i===s.stage?'aria-current="step"':''}>${title}<small>${i===s.stage?'Actual · ':''}${s.stageEvidence.includes(i)?'Aporte guardado':'Sin aporte aún'}</small></button>`).join('');
    }
    if(s)H.prepare(s);
    $('#context-return').innerHTML=s?H.header(s):'';
    renderMessages(); renderAssist(); save();
  }
  function renderAssist() {
    const text = input.value, s=current();
    const raw = detect(text), task = chosenTask || ((raw==='general'||raw==='ambiguous') ? s?.task : raw);
    const suggestion = suggest(text,task);
    const show = suggestion && dismissed !== `${task}:${suggestion.key}` && !s?.recall && !s?.pending;
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
    H.observe(s,text);
    if(s.task==='general') { message(s,'choice','¿Quieres aprender expresiones para un correo o comprender una palabra en contexto? Puedes elegir o contarme más; tu mensaje ya está guardado.'); return; }
    if(s.task==='email') {
      if(/dear\s|best regards|kind regards|i am agree|send me the/i.test(text)) { saveDraft(s,text.replace(/^.*?:\s*\n(?=Dear)/is,'')); review(s); return; }
      message(s,'text','Podemos trabajar la intención y el tono, y después probar una expresión propia. No hace falta completar una ficha: tu consulta es el punto de partida.',{start:true});H.emailStart(s);
    } else {
      const word = Object.keys(D.words).find(w=>new RegExp(`\\b${w}\\b`,'i').test(text));
      if(!word && !/vocabulario|lectura/i.test(text)) { s.word='';s.context=text;message(s,'text','Comparte la oración y la palabra que te genera duda. La demo ofrece fichas para dedicated, productive y deadline; para otras palabras registra tu hipótesis sin inventar una definición.'); message(s,'reading'); s.pending={type:'custom-context',label:'Comparte tu palabra y su oración'}; return; }
      s.word = word || 'dedicated';
      const quoted = [...text.matchAll(/[“"«]([^”"»]+)[”"»]/g)].map(m=>m[1]).find(t=>t.includes(' ')&&t.toLowerCase().includes(s.word)) || text.match(/(?:en (?:esta |la )?(?:frase|oraci[oó]n)|contexto)\s*:\s*([^\n]+)/i)?.[1];
      s.context = quoted || D.words[s.word].context;
      if(quoted && !wordEntry(s.word, quoted)) { message(s,'text',`Conservé tu oración con “${s.word}”. Para este contexto, formula una hipótesis y contrástala con un diccionario. Las fichas disponibles pertenecen a otros ejemplos de la demo; no confirman la acepción de tu oración.`);message(s,'reading');s.pending={type:'custom-inference',label:'Tu hipótesis y la pista de tu oración'};return; }
      if(!quoted)message(s,'text','Como no hay una oración completa entre comillas, propongo un ejemplo de práctica. Puedes compartir tu propia frase indicando: en esta frase: …');
      message(s,'text','Primero podemos buscar una pista; luego contrastar tu interpretación y usar la palabra en otra situación.',{start:true});
      clue(s);
    }
  }
  function saveDraft(s,text) {
    s.stage=1;
    H.observe(s,text);s.hta.reviewFragment='';s.hta.reviewScope=null;
    s.messages.filter(m=>m.kind==='correction'&&m.status==='pending').forEach(m=>m.status='outdated');
    s.draft=text; s.versions.push({id:id(),label:s.versions.length?'Nueva producción propia':'Original · producción propia',text,date:new Date().toISOString()});
    evidence(s,'Producción propia',text);H.recordProduction(s,text,'Correo propio');message(s,'draft',text,{versionId:s.versions.at(-1).id});s.stage=1;
  }
  function publishDraft(s) {message(s,'draft',s.draft,{versionId:s.versions.at(-1)?.id});}
  function review(s,scope=null) {
    H.markHelp(s);s.recall=false;s.pending=null;s.stage=1;
    if(!s.draft){message(s,'text','Comparte tu frase o correo en inglés. Revisaremos solo el fragmento pertinente y conservaremos el resto.');s.pending={type:'draft',label:'Escribe tu frase o correo en inglés'};return;}
    const source=scope?s.draft.slice(scope.start,scope.end):s.draft,offset=scope?.start||0;
    const rules=[
      {re:/\bI am agree\b/ig,after:'I agree',category:'Gramática',reason:'Agree ya es un verbo: “I agree”. No necesita am en esta estructura. El significado de estar de acuerdo se mantiene.'},
      {re:/\bI want you to send me ([^.!?\n]+)[.!?]?/ig,after:m=>`Could you please send me ${m[1]}?`,category:'Tono',reason:'“I want you to…” es gramatical, pero puede sonar exigente. Could you please ofrece otra opción de cortesía. La relación determina su conveniencia.'},
      {re:/^(Send me [^.!?\n]+)[.!?]?/img,after:m=>`Could you please ${m[1][0].toLowerCase()+m[1].slice(1)}?`,category:'Tono',reason:'El imperativo puede encajar con confianza. Could you please suaviza la petición conservando lo solicitado.'}
    ];
    let count=0;
    for(const r of rules)for(const match of source.matchAll(r.re)){
      const start=offset+match.index,before=match[0];
      if(s.messages.some(m=>m.kind==='correction'&&m.start===start&&m.before===before&&m.status==='pending'))continue;
      message(s,'correction','',{before,after:typeof r.after==='function'?r.after(match):r.after,category:r.category,reason:r.reason,status:'pending',start,end:start+before.length,versionId:s.versions.at(-1)?.id});count++;
    }
    if(!count)message(s,'text','No tengo una revisión automática fiable para este fragmento en la demo. Puedes contrastar una alternativa propia y explicar qué cambia. Tu texto sigue guardado.');
    s.hta.reviewFragment=source;s.hta.reviewScope={start:offset,end:offset+source.length,text:s.draft,fragment:source};
  }
  function clue(s) {const w=activeWord(s);if(!w){unavailableWord(s);return;}if(s.recall)s.helpUsed=true;s.recall=false;message(s,'clue',w.clue,{word:s.word,context:s.context||w.context});s.pending={type:'inference',label:'Tu hipótesis de significado y una pista del contexto'};s.stage=0;}
  function definition(s,hypothesis='') {const w=activeWord(s);if(!w){unavailableWord(s);return;}hypothesis=H.onDefinition(s,hypothesis);if(s.recall)s.helpUsed=true;s.recall=false;s.pending=null;s.stage=1;message(s,'definition','',{word:s.word,context:s.context||w.context,hypothesis,startingPoint:H.tracked(s).startingPoint});}
  function recall(s,transfer=false) {
    if(s.task==='general'){message(s,'choice','Elige primero si quieres practicar un correo o una palabra en contexto.');return;}
    s.hta.resumeHidden=false;const w=activeWord(s);if(s.task==='vocab'&&!w){unavailableWord(s);return;}
    s.pending={type:transfer?'transfer':'recall',label:transfer?'Tu intento en una situación diferente':'Tu intento sin el material anterior'};
    s.stage=transfer?3:2;s.recall=true;s.helpUsed=false;s.recallStart=s.messages.length;
    const text=transfer ? s.task==='email'?'Ahora le escribes a un compañero de confianza para pedir sus apuntes. Redacta un correo breve y explica qué cambiarías respecto al tono con una profesora.':w.transfer : s.task==='email'?'Sin mirar el modelo: pide más tiempo para una entrega en una frase en inglés. Después explica por qué elegirías ese tono.':`Sin mirar la definición: explica “${s.word}” con tus palabras y úsala en una oración propia.`;
    const emailText=s.task==='email'?(transfer?`Escribe otro correo para una relación distinta, conservando esta intención: ${H.cases[s.hta.email.cases[0]||'notes'].name.toLowerCase()}. Explica qué cambiarías.`:`Sin mirar el modelo: formula una petición para ${H.cases[s.hta.email.cases[0]||'notes'].name.toLowerCase()}. Explica su significado y tono.`):text;
    message(s,'recall',emailText);
  }
  function pendingAnswer(s,text) {
    if(H.pendingDraft(s,text)||H.answer(s,text))return;
    const pending=s.pending;s.pending=null;
    if(pending.type==='draft'){saveDraft(s,text);return;}
    if(pending.type==='inference'){evidence(s,H.inferenceKind(s,text),text);definition(s,text);return;}
    if(pending.type==='custom-context'){message(s,'text','Tu contexto quedó registrado. Propón un significado y señala una pista; puedes usar un diccionario para contrastarlo. No asignaré la acepción de un ejemplo diferente.');evidence(s,'Contexto propio por contrastar',text);s.pending={type:'custom-inference',label:'Tu hipótesis y una pista de la oración'};return;}
    if(pending.type==='custom-inference'){evidence(s,'Hipótesis propia por contrastar',text);message(s,'text','Guardé tu interpretación como hipótesis, pendiente de contraste. Para explorar una ficha preparada puedes tocar una palabra de la lectura de práctica.');message(s,'reading');return;}
    if(pending.type==='recall'||pending.type==='transfer'){
      evidence(s,pending.type==='transfer'?'Producción en otra situación':'Intento de recuperación',text);
      H.recordProduction(s,text,pending.type==='transfer'?'Producción en otra situación':'Intento de recuperación');
      message(s,'practice-result','Conservé tu producción. Contrasta ahora si expresa la intención que buscabas y qué diferencia encuentras frente al ejemplo.',{help:s.helpUsed,task:s.task,word:s.word,context:s.context});
      s.recall=false;return;
    }
    evidence(s,pending.type==='reflection'?'Duda para retomar':s.task==='vocab'?'Explicación de significado y uso':'Justificación de una elección',text);
    if(s.task==='vocab')H.updateInterpretation(s,text);
    if(pending.decisionId){const decision=s.messages.find(m=>m.id===pending.decisionId);Object.assign(s.evidence.at(-1),{decisionId:pending.decisionId,before:decision?.before,after:decision?.after,decision:decision?.status});}
    message(s,'text','Tu explicación quedó guardada con tus palabras. Puedes contrastarla con el ejemplo, reformular tu producción o probar otra situación.');
  }
  function send() {
    const text=input.value.trim();if(!text)return;restoredInput=null;
    let s=current();const inferred=detect(text), task=chosenTask || (inferred==='ambiguous'?'general':inferred);
    if(!s) {s=session(task,text);message(s,'user',text);startIntro(s,text);}
    else {
      message(s,'user',text);
      if(H.natural(s,text)){}
      else if(!['draft','recall','transfer','hta'].includes(s.pending?.type) && /^(?:Subject:|Dear\s|Hi [^,]+,)/im.test(text) && s.task==='email'){saveDraft(s,text);review(s);}
      else if(s.pending)pendingAnswer(s,text);
      else if(s.task==='general' && task!=='general'){s.task=task;startIntro(s,text);}
      else if(s.task==='email' && /dear\s|best regards|kind regards|i am agree|i want you to|^send me\b/i.test(text)){saveDraft(s,text);review(s);}
      else if(s.task==='vocab' && Object.keys(D.words).some(w=>new RegExp(`\\b${w}\\b`,'i').test(text))){startIntro(s,text);}
      else {evidence(s,'Nota o pregunta por revisar',text);message(s,'text','Guardé tu aporte para retomarlo. Puedes elegir el apoyo que necesitas; las respuestas de esta demo están preparadas para ejemplos concretos.',{start:s.task!=='general'});if(s.task==='general')message(s,'choice','¿Con qué actividad se relaciona tu idea?');}
    }
    chosenTask=null;dismissed='';promptUndo=null;s.inputDraft=restoredInput??'';input.value=s.inputDraft;restoredInput=null;sizeInput();notice('');s.closed=false;afterAction();
  }
  function newChat() { persistInput();state.active=null;chosenTask=null;dismissed='';promptUndo=null;input.value='';$('#task-choice').hidden=true;$('#learning-plan').open=false;notice('');render();sizeInput();input.focus(); }
  function openDialog(title,html,type) {
    const dialog=$('#workspace-dialog');if(!dialog.open)returnFocus=document.activeElement;
    dialog.classList.toggle('conversation-drawer', type === 'history');
    panel=type;$('#dialog-title').textContent=title;$('#dialog-content').innerHTML=html;
    if(!dialog.open)dialog.showModal();$('#dialog-content').scrollTop=0;
  }
  function history() {
    const html=['email','vocab','general'].map(task=>`<section class="history-group"><h3>${D.tasks[task]}</h3>${state.sessions.filter(s=>(s.hta?.originTask||s.task)===task).map(s=>`<button class="session-link" data-action="resume" data-id="${s.id}" aria-current="${s.id===state.active}">${esc(s.title)}<span class="sr-only"> · ${s.evidence.length} aportes</span></button>`).join('')||'<p class="small">Aún no hay conversaciones.</p>'}</section>`).join('');
    openDialog('Conversaciones',`<p class="small">Se guardan en este navegador. Retoma el contexto, tu borrador y tus notas.</p>${btn('new','Empezar otro chat')}${html}`,'history');$('[data-action="history"]').setAttribute('aria-expanded','true');
  }
  function notebook() {
    const s=current();if(!s)return;
    H.markHelp(s);
    openDialog('Mi aprendizaje',`<p>${D.tasks[s.task]} · guardado en este navegador</p><div class="metrics"><div><strong>${s.evidence.length}</strong><span>Aportes escritos</span></div><div><strong>${s.words.length}</strong><span>Palabras guardadas</span></div></div><p class="small">Actividad registrada; no acredita dominio. Las explicaciones y los intentos deben contrastarse. Las sugerencias añadidas (${s.promptUses}) no demuestran una reducción de consultas.</p>${actions([btn('export','Descargar mis notas'),btn('versions','Ver versiones del correo'),btn('finish','Cerrar esta práctica')])}${s.words.length?`<h3>Palabras para repasar</h3><p>${s.words.map(esc).join(' · ')}</p>${btn('repaso','Retomar un repaso sin definición')}`:''}${H.notebook(s)}<h3>Mis producciones y reflexiones</h3>${s.evidence.map(e=>`<section class="evidence"><strong>${esc(e.kind)}</strong><small>${new Date(e.date).toLocaleString('es-PE')}${/recuper|otra situaci/i.test(e.kind)?e.help?' · consultaste apoyo':' · material anterior oculto':''}</small><p>${esc(e.text)}</p></section>`).join('')||'<p class="empty-note">Todavía no escribiste un aporte propio. Abrir una etapa o guardar una palabra no acredita aprendizaje.</p>'}`,'notebook');
  }
  function versions() {const s=current();if(!s)return;H.markHelp(s);openDialog('Versiones de tu correo',`<p class="small">Recuperar crea una nueva versión; conserva las anteriores. El original sigue disponible.</p>${s.versions.map((v,i)=>`<details class="version-item" ${i===s.versions.length-1?'open':''}><summary>${i+1}. ${esc(v.label)}</summary><pre lang="en">${esc(v.text)}</pre>${btn('restore','Usar esta versión',`data-id="${v.id}"`)}</details>`).join('')||'<p>No hay un correo propio guardado todavía.</p>'}`,'versions');}
  function demo() {openDialog('Ideas para explorar',`<p>Estos ejemplos muestran las tareas. Se abren en un chat nuevo y puedes editar el mensaje antes de enviarlo.</p>${[['email','Comprender el tono','Compara una misma petición según la relación.'],['review','Revisar sin perder tu voz','Prueba gramática, cortesía, decisiones y versiones.'],['vocab','Del contexto a una oración propia','Infiere, contrasta y practica sin la definición.'],['ambiguous','Empezar sin saber la tarea','Comprueba cómo se pide contexto sin adivinar.']].map(([key,title,detail])=>`<section class="demo-card"><h3>${title}</h3><p>${detail}</p>${btn('load-demo','Preparar ejemplo',`data-example="${key}"`)}</section>`).join('')}<p class="small">No se envían correos ni se consulta una IA externa. Las fichas y respuestas son material preparado.</p>`,'demo');}
  function closeDialog() {$('#workspace-dialog').close();panel='';$('[data-action="history"]').setAttribute('aria-expanded','false');if(returnFocus?.isConnected)returnFocus.focus();}
  function exportNotes() {const s=current();if(!s)return;const text=`Lingua IA · ${D.tasks[s.task]}\n${s.title}\nActividad registrada; no acredita dominio. Respuestas de ejemplo.\n\n`+s.evidence.map(e=>`${e.kind} · ${e.date}\n${e.text}`).join('\n\n')+`\n\nEntradas y consultas de la práctica\n${JSON.stringify(s.hta,null,2)}\n\nPalabras guardadas: ${s.words.join(', ')||'ninguna'}\n\nVersiones\n`+s.versions.map(v=>`${v.label}\n${v.text}`).join('\n\n');const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='lingua-mis-notas.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  function handle(action,el) {
    let s=current();restoredInput=null;
    if(s){H.prepare(s);if(H.action(s,action,el)){afterAction();restoredInput=null;return;}}
    if(s && el.dataset.context && ['clue','definition','vocab-explain','save-word','recall','transfer'].includes(action)) {
      s.word=el.dataset.word;s.context=el.dataset.context;
    }
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
      case 'resume':persistInput();state.active=el.dataset.id;s=current();chosenTask=null;dismissed='';promptUndo=null;closeDialog();input.value=s.inputDraft||'';H.resume(s);notice('Retomaste tu práctica. El contexto y las notas siguen aquí.');afterAction();sizeInput();return;
      case 'use-prompt':case 'edit-prompt':{
        const raw=detect(input.value),task=chosenTask||((raw==='general'||raw==='ambiguous')?s?.task:raw),p=suggest(input.value,task);if(!p)return;
        promptUndo={before:input.value,after:input.value.trim()+' '+p.add};setInput(promptUndo.after);dismissed=`${task}:${p.key}`;if(s)s.promptUses++;notice(action==='edit-prompt'?'Sugerencia añadida para que la edites antes de enviar.':'Sugerencia añadida; puedes editarla o deshacer.',true);save();return;}
      case 'dismiss-prompt':{const raw=detect(input.value),task=chosenTask||((raw==='general'||raw==='ambiguous')?s?.task:raw),p=suggest(input.value,task);dismissed=`${task}:${p?.key}`;if(s)s.promptDismisses++;renderAssist();save();input.focus();return;}
      case 'undo-prompt':if(promptUndo&&input.value===promptUndo.after){setInput(promptUndo.before);promptUndo=null;notice('Sugerencia retirada. Tu mensaje anterior está intacto.');}else notice('Tu mensaje cambió después de añadir la sugerencia. Puedes editarla directamente para conservar lo que escribiste.');return;
      case 'change-task':$('#task-choice').hidden=!$('#task-choice').hidden;$('#task-choice').innerHTML=`<p>¿Dónde quieres continuar este chat?</p>${actions([btn('assign','Correo en inglés','data-task="email"'),btn('assign','Vocabulario en contexto','data-task="vocab"')])}`;return;
      case 'assign':if(!s)return;H.rootSwitch(s,el.dataset.task);$('#task-choice').hidden=true;message(s,'text',`Este chat se organizó en ${D.tasks[s.task].toLowerCase()}. Conservé los mensajes y tus aportes.`,{start:true});break;
      case 'compare':if(!s)return;s.recall=false;s.helpUsed=true;s.pending={type:'justify',label:'Explica qué cambia en el tono o prueba una comparación'};s.stage=0;message(s,'compare');break;
      case 'model':if(!s)return;s.recall=false;s.helpUsed=true;s.pending=null;s.stage=0;message(s,'model');break;
      case 'write':if(!s)return;s.pending={type:'draft',label:'Tu propia frase o correo en inglés'};s.stage=1;s.recall=false;message(s,'text','Escribe una petición o un correo con tus recursos. Puedes incluir a quién te diriges y explicar el tono; no tienes que completar apartados.');break;
      case 'review':if(!s)return;review(s);break;
      case 'accept':case 'reject':{
        if(!s)return;const m=s.messages.find(m=>m.id===el.dataset.id);if(!m||m.status!=='pending')return;
        if(action==='accept'){
          if(m.start===undefined || s.draft.slice(m.start,m.end)!==m.before){notice('Tu borrador cambió. Revisa la versión actual antes de aplicar esta propuesta.');return;}
          m.previous=s.draft;const delta=m.after.length-m.before.length;for(const other of s.messages.filter(x=>x.kind==='correction'&&x.status==='pending'&&x.id!==m.id)){if(other.start>=m.end){other.start+=delta;other.end+=delta;}else if(other.end>m.start)other.status='outdated';}s.draft=s.draft.slice(0,m.start)+m.after+s.draft.slice(m.end);m.applied=s.draft;s.versions.push({id:id(),label:`Cambio de ${m.category.toLowerCase()}`,text:s.draft,date:new Date().toISOString()});m.status='accepted';publishDraft(s);
        }else m.status='rejected';
        notice(action==='accept'?'Cambio aplicado solo en el fragmento elegido. El resto se conserva.':'Conservaste tu frase. Puedes explicar por qué encaja con tu intención.');break;}
      case 'undo-correction':{
        if(!s)return;const m=s.messages.find(m=>m.id===el.dataset.id);if(!m)return;
        if(m.status==='accepted'){
          if(s.draft!==m.applied){notice('Hay cambios posteriores. Recupera una versión para no perderlos.');versions();return;}
          const delta=m.before.length-m.after.length;for(const other of s.messages.filter(x=>x.kind==='correction'&&x.status==='pending'&&x.start>=m.start+m.after.length)){other.start+=delta;other.end+=delta;}s.draft=m.previous;s.versions.push({id:id(),label:'Decisión deshecha',text:s.draft,date:new Date().toISOString()});publishDraft(s);
        }m.status='pending';notice('Decisión deshecha; las versiones anteriores siguen disponibles.');break;}
      case 'restore':{if(!s)return;const v=s.versions.find(v=>v.id===el.dataset.id);if(!v)return;s.draft=v.text;s.versions.push({id:id(),label:'Recuperada de '+v.label,text:v.text,date:new Date().toISOString()});s.messages.filter(m=>m.kind==='correction').forEach(m=>m.status='outdated');publishDraft(s);renderMessages();save();versions();notice('Versión recuperada. Las anteriores se conservan.');return;}
      case 'justify':case 'vocab-explain':if(!s)return;if(s.recall)s.helpUsed=true;s.recall=false;s.stage=action==='vocab-explain'?1:Number(el.dataset.stage??s.stage);s.pending={type:'justify',decisionId:el.dataset.id,label:action==='justify'?'Tu explicación del cambio o del tono':'Tu explicación del significado y del contexto'};message(s,'text',action==='justify'?'¿Qué efecto tiene la expresión que elegiste en el significado o en el tono? Puedes mantener tu frase si encaja con tu intención.':'Explica con tus palabras qué acepción encaja y qué pista de la oración permite descartar la otra. Puedes añadir un patrón de uso que quieras recordar.');break;
      case 'reading':if(!s)return;if(s.task!=='vocab')H.rootSwitch(s,'vocab');s.stage=0;s.pending=null;s.recall=false;message(s,'reading');break;
      case 'pick-word':if(!s)return;s.word=el.dataset.word;s.context=D.words[s.word].context;clue(s);break;
      case 'clue':if(!s)return;clue(s);break;
      case 'definition':if(!s)return;if(s.recall)s.helpUsed=true;s.recall=false;definition(s);break;
      case 'save-word':if(!s)return;notice(H.saveEntry(s,el.dataset.word,s.context||D.words[el.dataset.word]?.context)?'Entrada guardada con su contexto para repasar.':'Entrada retirada del repaso; sus producciones se conservan.');break;
      case 'repaso':if(!s)return;if(H.reviewSaved(s))return;break;
      case 'recall':case 'transfer':if(!s)return;if($('#workspace-dialog').open)closeDialog();recall(s,action==='transfer');break;
      case 'reveal-support':if(!s)return;s.recall=false;s.helpUsed=true;notice('Apoyo visible. Se registrará que lo consultaste durante este intento.');break;
      case 'stage':if(!s)return;if(s.recall)s.helpUsed=true;s.recall=false;s.stage=Number(el.dataset.stage);if(s.stage>=2)recall(s,s.stage===3);else if(s.stage===0){if(s.task==='email'){message(s,'compare');s.pending={type:'justify',label:'Tu comparación del tono'};}else clue(s);}else{if(s.task==='email'){s.pending={type:'draft',label:'Tu propia frase o correo'};message(s,'text','Prueba tu propia petición. Después puedes contrastar una expresión.');}else definition(s);}break;
      case 'finish':if(!s)return;if($('#workspace-dialog').open)closeDialog();s.closed=true;s.recall=false;s.pending=null;H.finish(s);message(s,'finish',s.evidence.length?'Para la próxima práctica: intenta recuperar una expresión antes de volver a los ejemplos.':'Aún no hay producciones propias guardadas. Puedes retomar más adelante o dejar una duda pendiente.');break;
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
  H.init({D,id,esc,contextKey,wordEntry,btn,actions,input,message,evidence,clue,definition,recall,review,saveDraft,publishDraft,notice,notebook,closeDialog,openDialog,restoreInput(text){restoredInput=text;input.value=text;}});
  load();state.active=null;render();
  // API de inspección del prototipo usada por las pruebas del navegador.
  window.Lingua={getState:()=>clone(state),detect,suggest,reset(){state={version:2,sessions:[],active:null};try{localStorage.removeItem(KEY);localStorage.removeItem(LEGACY_KEY);}catch(_){}newChat();},send,openDemo:demo};
})();
