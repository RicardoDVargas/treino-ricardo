const $ = (id) => document.getElementById(id);
const TZ = 'America/Sao_Paulo';
const fullDays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
const shortDays = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'];
const weekday = new Intl.DateTimeFormat('en-US', {weekday: 'short', timeZone: TZ}).format(new Date());
const today = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].indexOf(weekday);
const todayKey = new Intl.DateTimeFormat('en-CA', {timeZone: TZ}).format(new Date());
const staticMoves = {plank: ['Posição', 'Sustente'], sideplank: ['Posição', 'Sustente']};
const list = new Intl.ListFormat('pt-BR', {style: 'long', type: 'conjunction'});
const icons = {
  clock: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="13" r="7.5"/><path d="M12 9.5V13l2.5 1.5M9.5 3.5h5"/></svg>',
  check: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>'
};

let selected = today;
let workouts = [];
let timerState = null;
let ticker;
let done = loadDone();

const cap = (text) => text.charAt(0).toLocaleUpperCase('pt-BR') + text.slice(1);
const lower = (text) => text.charAt(0).toLocaleLowerCase('pt-BR') + text.slice(1);
const seriesOf = (exercise) => parseInt(exercise.sets, 10) || 0;

/* ---------- progresso da sessão (reinicia a cada dia) ---------- */
function loadDone() {
  try {
    const saved = JSON.parse(localStorage.getItem('ricardo-done'));
    if (saved && saved.date === todayKey && saved.days) return saved.days;
  } catch {}
  return {};
}
function saveDone() {
  try { localStorage.setItem('ricardo-done', JSON.stringify({date: todayKey, days: done})); } catch {}
}
function isDone(day, index) { return Array.isArray(done[day]) && done[day].includes(index); }
function toggleDone(day, index) {
  const current = new Set(done[day] || []);
  current.has(index) ? current.delete(index) : current.add(index);
  done[day] = [...current];
  saveDone();
}

/* ---------- cronômetro de descanso ---------- */
function saveTimer() {
  try {
    if (timerState) localStorage.setItem('ricardo-rest', JSON.stringify(timerState));
    else localStorage.removeItem('ricardo-rest');
  } catch {}
}
function remaining() {
  return timerState.paused ? timerState.remaining : Math.max(0, Math.ceil((timerState.end - Date.now()) / 1000));
}
function tick() {
  if (!timerState) return;
  const seconds = remaining();
  $('clock').textContent = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
  $('timer-label').textContent = seconds ? 'Descanso' : 'Pode voltar';
  $('pause').textContent = seconds ? (timerState.paused ? 'Continuar' : 'Pausar') : 'Concluir';
  const total = timerState.total || seconds || 1;
  $('timer-fill').style.transform = `scaleX(${Math.min(1, seconds / total)})`;
}
function startRest(seconds) {
  timerState = {end: Date.now() + seconds * 1000, remaining: seconds, total: seconds, paused: false};
  saveTimer();
  $('timer').hidden = false;
  clearInterval(ticker);
  tick();
  ticker = setInterval(tick, 250);
}
function closeTimer() {
  clearInterval(ticker);
  timerState = null;
  saveTimer();
  $('timer').hidden = true;
}
$('pause').addEventListener('click', () => {
  if (!timerState || remaining() === 0) return closeTimer();
  if (timerState.paused) {
    timerState.end = Date.now() + timerState.remaining * 1000;
    timerState.paused = false;
  } else {
    timerState.remaining = remaining();
    timerState.paused = true;
  }
  saveTimer();
  tick();
});
$('close-timer').addEventListener('click', closeTimer);

/* ---------- dados do treino ---------- */
// "Peito (3) + bíceps (2) + ombros (2)" -> blocos com início e quantidade de exercícios
function blocksOf(workout) {
  const parts = workout.groups.split(' + ').map((part) => {
    const match = part.match(/^(.+?)\s*\((\d+)\)$/);
    return {name: match ? match[1] : part, count: match ? Number(match[2]) : 0};
  });
  const total = parts.reduce((sum, part) => sum + part.count, 0);
  if (total !== workout.exercises.length) return [{name: workout.groups, count: workout.exercises.length, start: 0, main: true}];
  let start = 0;
  return parts.map((part, index) => { const block = {...part, start, main: index === 0}; start += part.count; return block; });
}

/* ---------- desenho da tela ---------- */
function renderDays() {
  $('days').replaceChildren(...workouts.map((day, index) => {
    const names = blocksOf(day).map((block) => block.name);
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'day' + (index === today ? ' is-today' : '');
    button.setAttribute('aria-pressed', String(index === selected));
    button.setAttribute('aria-label', `${day.name}${index === today ? ', hoje' : ''}: ${names.join(', ')}`);
    button.innerHTML = '<span class="node" aria-hidden="true"></span><span class="d-text"><span class="d-full"></span><span class="d-short"></span><span class="d-groups"></span></span>' + (index === today ? '<span class="d-today">hoje</span>' : '');
    button.querySelector('.d-full').textContent = fullDays[index];
    button.querySelector('.d-short').textContent = shortDays[index];
    button.querySelector('.d-groups').textContent = cap(names.map(lower).join(', '));
    button.onclick = () => { selected = index; render(); };
    return button;
  }));
}

function renderHero(workout, blocks) {
  const exercises = workout.exercises;
  const series = exercises.reduce((sum, exercise) => sum + seriesOf(exercise), 0);
  const finished = exercises.filter((_, index) => isDone(selected, index)).length;
  $('day-label').innerHTML = '';
  $('day-label').append(`${workout.name}${selected < 5 ? '-feira' : ''}`);
  if (selected === today) { const tag = document.createElement('i'); tag.textContent = 'hoje'; $('day-label').append(tag); }
  $('day-title').textContent = cap(blocks[0].name);
  const others = blocks.slice(1).map((block) => lower(block.name));
  $('day-sub').textContent = others.length ? `com ${list.format(others)}` : '';
  const circ = 2 * Math.PI * 32;
  const fraction = exercises.length ? finished / exercises.length : 0;
  $('progress').setAttribute('aria-label', `${finished} de ${exercises.length} exercícios concluídos`);
  $('progress').innerHTML = `<svg viewBox="0 0 74 74" aria-hidden="true"><defs><linearGradient id="ringg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#f2cf8a"/></linearGradient></defs><circle class="ring-bg" cx="37" cy="37" r="32"/><circle class="ring" cx="37" cy="37" r="32" stroke-dasharray="${circ.toFixed(1)}" stroke-dashoffset="${(circ * (1 - fraction)).toFixed(1)}"/></svg><div class="progress-text"><strong>${finished}/${exercises.length}</strong><small>concluídos</small></div>`;
  const chips = [
    `<b>${workout.time}</b>`,
    `<b>${exercises.length}</b> exercícios`,
    `<b>${series}</b> séries`,
    'Reserva de 2–3 repetições (3–4 nos blocos leves)'
  ];
  $('chips').innerHTML = chips.map((chip) => `<li>${chip}</li>`).join('');
  $('note').textContent = workout.note;
  $('note').hidden = !workout.note;
}

function renderCard(exercise, index) {
  const article = document.createElement('article');
  article.className = 'card';
  article.dataset.done = String(isDone(selected, index));
  const moves = staticMoves[exercise.image] || ['Início', 'Movimento'];
  article.innerHTML = `<div class="art"><img loading="lazy" width="480" height="222" alt=""><span class="cap cap-a"></span><span class="cap cap-b"></span><span class="idx"></span></div>
<div class="body"><h3 class="name"></h3><div class="row"><div class="sets"><small>Séries × repetições</small><strong></strong></div><div class="actions"><button type="button" class="btn rest">${icons.clock}<span></span></button><button type="button" class="btn check"></button></div></div></div>`;
  article.querySelector('.idx').textContent = index + 1;
  const image = article.querySelector('img');
  image.src = `images/${exercise.image}.svg`;
  image.alt = `Ilustração de ${exercise.name}: ${moves[0].toLowerCase()} e ${moves[1].toLowerCase()}, com o músculo trabalhado em destaque.`;
  article.querySelector('.cap-a').textContent = moves[0];
  article.querySelector('.cap-b').textContent = moves[1];
  article.querySelector('.name').textContent = exercise.name;
  article.querySelector('.sets strong').textContent = exercise.sets;
  const rest = article.querySelector('.rest');
  rest.querySelector('span').textContent = `${exercise.rest} s`;
  rest.setAttribute('aria-label', `Iniciar ${exercise.rest} segundos de descanso para ${exercise.name}`);
  rest.onclick = () => startRest(exercise.rest);
  const check = article.querySelector('.check');
  const setCheck = () => {
    const on = isDone(selected, index);
    check.innerHTML = icons.check;
    check.setAttribute('aria-pressed', String(on));
    check.setAttribute('aria-label', on ? `Desmarcar ${exercise.name} como concluído` : `Marcar ${exercise.name} como concluído`);
  };
  setCheck();
  check.onclick = () => { toggleDone(selected, index); render(); };
  return article;
}

function render() {
  const workout = workouts[selected];
  const blocks = blocksOf(workout);
  renderDays();
  renderHero(workout, blocks);
  $('exercises').replaceChildren(...blocks.map((block) => {
    const section = document.createElement('section');
    section.setAttribute('aria-label', cap(block.name));
    const items = workout.exercises.slice(block.start, block.start + block.count);
    const each = items.length ? seriesOf(items[0]) : 0;
    const head = document.createElement('div');
    head.className = 'block-head';
    head.innerHTML = '<h2></h2><p></p><span class="tag"></span>';
    head.querySelector('h2').textContent = cap(block.name);
    head.querySelector('p').textContent = `${items.length} ${items.length === 1 ? 'exercício' : 'exercícios'}${each ? `, ${each} séries cada` : ''}`;
    head.querySelector('.tag').textContent = block.main ? 'Bloco principal' : 'Complementar';
    const cards = document.createElement('div');
    cards.className = 'cards';
    cards.append(...items.map((exercise, offset) => renderCard(exercise, block.start + offset)));
    section.append(head, cards);
    return section;
  }));
}

/* ---------- diálogos ---------- */
function showInfo(html) { $('info-body').innerHTML = html; $('info').showModal(); }
$('install').onclick = () => showInfo('<p class="kick">Sempre à mão</p><h2>Seu treino na tela inicial</h2><ol><li>Abra este link no <strong>Safari do iPhone</strong>.</li><li>Toque em <strong>Compartilhar</strong>.</li><li>Escolha <strong>Adicionar à Tela de Início</strong> e confirme.</li></ol><p>No Android, use a opção de instalar ou adicionar à tela inicial no menu do navegador.</p>');
$('about').onclick = () => showInfo('<p class="kick">Sua rotina</p><h2>Treino da semana</h2><p>Peito e bíceps na segunda, quarta e sexta. Costas e tríceps na terça, quinta e sábado. Frente de perna na quarta e domingo, posterior na terça e sábado.</p><p>Planeje 8 min de aquecimento, cerca de 42–47 min nos sete exercícios (séries, pausas e trocas) e até 5 min de volta à calma. Os três primeiros exercícios recebem 3 séries, e os quatro complementares, 2 séries. Domingo é opcional, leve e com 2 séries em todos os exercícios. Não é necessário prolongar uma sessão que terminar antes. A duração real varia com o ritmo da sessão.</p><p>Toque no botão de descanso do exercício para iniciar a contagem e no botão de check para marcar o exercício como concluído. O progresso do dia fica salvo neste aparelho e reinicia no dia seguinte. As ilustrações são esquemáticas e destacam o músculo trabalhado.</p><p>App atualizado em 10/11/2026 com novo visual e sete exercícios por dia. A planilha vinculada não foi atualizada nesta revisão. Alterações no Sheets precisam ser trazidas para o app.</p><a href="https://docs.google.com/spreadsheets/d/12pOSf6pDS6xS-zVxyb9iKxJ5Zc8l8yaNhZL8vbFMoYk/edit" target="_blank" rel="noopener">Abrir minha planilha ↗</a>');
$('close-info').onclick = () => $('info').close();
$('info').addEventListener('click', (event) => {
  if (event.target === $('info')) {
    const box = $('info').getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) $('info').close();
  }
});

/* ---------- início ---------- */
try {
  const response = await fetch('./workouts.json');
  if (!response.ok) throw new Error('Falha ao carregar treino');
  workouts = await response.json();
  render();
  try {
    const saved = JSON.parse(localStorage.getItem('ricardo-rest'));
    if (saved && Number.isFinite(saved.end) && Number.isFinite(saved.remaining) && (saved.paused || saved.end > Date.now())) {
      timerState = saved;
      $('timer').hidden = false;
      tick();
      ticker = setInterval(tick, 250);
    }
  } catch {}
} catch {
  $('day-title').textContent = 'Não foi possível carregar o treino.';
  $('note').hidden = false;
  $('note').textContent = 'Verifique a conexão e recarregue a página.';
}
if ('serviceWorker' in navigator) navigator.serviceWorker.register('./sw.js').catch(() => {});
document.addEventListener('visibilitychange', () => { if (!document.hidden) tick(); });
