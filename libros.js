/* Los libros del panteón — filtros interactivos, vanilla JS */

let DATA = [];
let state = { thinker: 'all', type: 'all', q: '' };

const $ = (id) => document.getElementById(id);

const TYPE_LABEL = {
  recomendado: 'Recomendado',
  citado: 'Citado',
  propio: 'Propio',
  influencia: 'Influencia'
};

const TYPE_ORDER = ['recomendado', 'citado', 'propio', 'influencia'];

/* ---------- normalización de tildes para búsqueda ---------- */
function norm(s) {
  return (s || '')
    .toString()
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

function esc(s) {
  const d = document.createElement('div');
  d.textContent = s == null ? '' : String(s);
  return d.innerHTML;
}

/* ---------- carga ---------- */
async function load() {
  try {
    const res = await fetch('libros-data.json', { cache: 'no-cache' });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    DATA = await res.json();
  } catch (e) {
    $('results').innerHTML =
      '<div class="empty">No se pudo cargar la biblioteca.<br><small>' +
      esc(e.message) + '</small></div>';
    $('count').textContent = '';
    return;
  }
  DATA.sort((a, b) => (a.num || 0) - (b.num || 0));
  buildChips();
  render();
}

/* ---------- chips ---------- */
function buildChips() {
  const tc = $('thinkerChips');
  const total = DATA.reduce((n, t) => n + (t.libros || []).length, 0);

  let html = `<button class="chip ${state.thinker === 'all' ? 'on' : ''}" data-th="all">Todos<span class="cnt">${total}</span></button>`;
  for (const t of DATA) {
    const n = (t.libros || []).length;
    html += `<button class="chip ${state.thinker === t.slug ? 'on' : ''}" data-th="${esc(t.slug)}">${esc(t.nombre)}<span class="cnt">${n}</span></button>`;
  }
  tc.innerHTML = html;

  // tipos presentes
  const present = new Set();
  DATA.forEach(t => (t.libros || []).forEach(b => present.add(b.tipo)));
  const ordered = TYPE_ORDER.filter(t => present.has(t));

  let th = `<button class="chip ${state.type === 'all' ? 'on' : ''}" data-ty="all">Todos los tipos</button>`;
  for (const ty of ordered) {
    th += `<button class="chip ${state.type === ty ? 'on' : ''}" data-ty="${esc(ty)}">${esc(TYPE_LABEL[ty] || ty)}</button>`;
  }
  $('typeChips').innerHTML = th;

  tc.onclick = (e) => {
    const b = e.target.closest('[data-th]');
    if (!b) return;
    state.thinker = b.dataset.th;
    syncChips();
    render();
  };
  $('typeChips').onclick = (e) => {
    const b = e.target.closest('[data-ty]');
    if (!b) return;
    state.type = b.dataset.ty;
    syncChips();
    render();
  };
}

function syncChips() {
  document.querySelectorAll('#thinkerChips .chip').forEach(c => {
    c.classList.toggle('on', c.dataset.th === state.thinker);
  });
  document.querySelectorAll('#typeChips .chip').forEach(c => {
    c.classList.toggle('on', c.dataset.ty === state.type);
  });
}

/* ---------- render ---------- */
function render() {
  const nq = norm(state.q);
  const out = [];
  let shown = 0;

  for (const t of DATA) {
    if (state.thinker !== 'all' && t.slug !== state.thinker) continue;

    const books = (t.libros || []).filter(b => {
      if (state.type !== 'all' && b.tipo !== state.type) return false;
      if (!nq) return true;
      return norm(b.titulo).includes(nq) ||
             norm(b.titulo_original).includes(nq) ||
             norm(b.autor).includes(nq);
    });

    if (!books.length) continue;
    shown += books.length;

    let cards = '';
    for (const b of books) {
      const orig = b.titulo_original && b.titulo_original !== b.titulo
        ? `<div class="b-orig">${esc(b.titulo_original)}</div>` : '';
      cards += `
        <article class="bcard" tabindex="0" role="button" aria-expanded="false">
          <div class="b-top">
            <div>
              <h3 class="b-title">${esc(b.titulo)}</h3>
              <div class="b-author">${esc(b.autor)}</div>
              ${orig}
            </div>
            <div class="b-year">${b.anio ? esc(b.anio) : ''}</div>
          </div>
          <span class="badge ${esc(b.tipo)}">${esc(TYPE_LABEL[b.tipo] || b.tipo)}</span>
          <div class="b-note">${esc(b.nota)}</div>
        </article>`;
    }

    out.push(`
      <section class="thinker-block">
        <div class="thinker-head">
          <span class="num">#${esc(t.num)}</span>
          <h2>${esc(t.nombre)}</h2>
          <span class="nbooks">${books.length} ${books.length === 1 ? 'libro' : 'libros'}</span>
        </div>
        <div class="grid">${cards}</div>
      </section>`);
  }

  $('results').innerHTML = out.length
    ? out.join('')
    : '<div class="empty">Ningún libro coincide con ese filtro.<br>Probá con otra palabra o limpiá los filtros.</div>';

  $('count').textContent = shown
    ? `Mostrando ${shown} ${shown === 1 ? 'libro' : 'libros'}`
    : 'Sin resultados';
  $('reset').hidden = (state.thinker === 'all' && state.type === 'all' && !state.q);

  // expandir / colapsar
  $('results').querySelectorAll('.bcard').forEach(card => {
    const toggle = () => {
      const open = card.classList.toggle('open');
      card.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    card.addEventListener('click', toggle);
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
  });
}

/* ---------- wiring ---------- */
$('q').addEventListener('input', (e) => { state.q = e.target.value; render(); });
$('reset').addEventListener('click', () => {
  state = { thinker: 'all', type: 'all', q: '' };
  $('q').value = '';
  syncChips();
  render();
});

/* deep-link: libros.html#borges */
function applyHash() {
  const h = decodeURIComponent(location.hash.replace(/^#/, '')).trim();
  if (h && DATA.some(t => t.slug === h)) {
    state.thinker = h;
    syncChips();
    render();
  }
}
window.addEventListener('hashchange', applyHash);

load().then(applyHash);
