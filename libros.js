/* Los libros del panteón — filtros interactivos + red de vínculos, vanilla JS */

let DATA = [];
let state = { thinker: 'all', type: 'all', q: '', sharedOnly: false, view: 'lista' };
let LINKS = new Map();   // key normalizada -> [{thinker, nombre, slug, tipo, nota, lib}]
let PAIRS = [];          // pares de pensadores con lecturas compartidas

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
    .replace(/[\u0300-\u036f]/g, '')
    .trim();
}

/* clave canónica de un libro: título normalizado + primer apellido del autor */
function bookKey(b) {
  return norm(b.titulo);
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
  buildIndex();
  buildChips();
  render();
}

/* ---------- índice de vínculos ---------- */
function buildIndex() {
  LINKS = new Map();
  const pairCount = new Map();

  for (const t of DATA) {
    for (const b of (t.libros || [])) {
      const k = bookKey(b);
      if (!LINKS.has(k)) LINKS.set(k, []);
      LINKS.get(k).push({
        thinker: t.slug, nombre: t.nombre, num: t.num,
        tipo: b.tipo, nota: b.nota, lib: b
      });
    }
  }

  // sólo las claves con más de un pensador distinto cuentan como vínculo
  for (const [k, arr] of LINKS) {
    const slugs = new Set(arr.map(x => x.thinker));
    if (slugs.size < 2) continue;
    const list = [...slugs];
    for (let i = 0; i < list.length; i++) {
      for (let j = i + 1; j < list.length; j++) {
        const pk = [list[i], list[j]].sort().join('|');
        if (!pairCount.has(pk)) pairCount.set(pk, new Set());
        pairCount.get(pk).add(k);
      }
    }
  }

  const nameOf = {};
  DATA.forEach(t => nameOf[t.slug] = { nombre: t.nombre, num: t.num });

  PAIRS = [...pairCount.entries()].map(([pk, keys]) => {
    const [a, b2] = pk.split('|');
    return {
      a, b: b2, count: keys.size,
      keys: [...keys],
      nombreA: nameOf[a].nombre, nombreB: nameOf[b2].nombre,
      numA: nameOf[a].num, numB: nameOf[b2].num
    };
  }).sort((x, y) => y.count - x.count || x.nombreA.localeCompare(y.nombreA));

  // cuántos libros comparte cada pensador (grado)
  const deg = {};
  for (const [k, arr] of LINKS) {
    const slugs = new Set(arr.map(x => x.thinker));
    if (slugs.size < 2) continue;
    for (const s of slugs) deg[s] = (deg[s] || 0) + 1;
  }
  window.__DEG = deg;
}

function sharedWith(slug) {
  // devuelve [{slug, nombre, num, libros:[...]}] de los que comparten algo con slug
  const out = new Map();
  for (const [k, arr] of LINKS) {
    const mine = arr.filter(x => x.thinker === slug);
    if (!mine.length) continue;
    const otros = arr.filter(x => x.thinker !== slug);
    if (!otros.length) continue;
    for (const o of otros) {
      if (!out.has(o.thinker)) out.set(o.thinker, { slug: o.thinker, nombre: o.nombre, num: o.num, libros: [] });
      out.get(o.thinker).libros.push({ k, lib: mine[0].lib });
    }
  }
  return [...out.values()].sort((a, b) => b.libros.length - a.libros.length);
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
  const v = $('viewChips');
  if (v) v.querySelectorAll('.chip').forEach(c => c.classList.toggle('on', c.dataset.vw === state.view));
  const so = $('sharedOnly');
  if (so) so.checked = state.sharedOnly;
}

/* ---------- vista VÍNCULOS ---------- */
function renderLinks() {
  const nq = norm(state.q);
  const deg = window.__DEG || {};

  // pares ordenados por afinidad
  const maxPairs = 24;
  let pairs = PAIRS.filter(p => {
    if (state.thinker !== 'all' && p.a !== state.thinker && p.b !== state.thinker) return false;
    if (!nq) return true;
    return norm(p.nombreA).includes(nq) || norm(p.nombreB).includes(nq);
  });

  let pHtml = '';
  for (const p of pairs.slice(0, maxPairs)) {
    const titles = p.keys.map(k => LINKS.get(k)[0].lib.titulo);
    const more = titles.length > 4 ? `<span class="more">+${titles.length - 4} más</span>` : '';
    pHtml += `
      <article class="pair-card" data-a="${esc(p.a)}" data-b="${esc(p.b)}" tabindex="0" role="button" aria-expanded="false">
        <div class="pair-head">
          <span class="pair-names">
            <strong>${esc(p.nombreA)}</strong>
            <span class="pair-x">↔</span>
            <strong>${esc(p.nombreB)}</strong>
          </span>
          <span class="pair-count">${p.count} ${p.count === 1 ? 'libro' : 'libros'}</span>
        </div>
        <div class="pair-titles">
          ${titles.slice(0, 4).map(t => `<span class="ptitle">${esc(t)}</span>`).join('')}
          ${more}
        </div>
      </article>`;
  }
  if (!pHtml) pHtml = '<div class="empty">No hay pares que coincidan con ese filtro.</div>';

  // pensadores más conectados (grado)
  const ranked = DATA.map(t => ({ ...t, deg: deg[t.slug] || 0 }))
    .filter(t => t.deg > 0)
    .sort((a, b) => b.deg - a.deg);

  const maxDeg = ranked.length ? ranked[0].deg : 1;
  let gHtml = '';
  for (const t of ranked) {
    const w = Math.max(6, Math.round((t.deg / maxDeg) * 100));
    gHtml += `
      <button class="degree-row" data-th="${esc(t.slug)}">
        <span class="deg-name">${esc(t.nombre)}</span>
        <span class="deg-bar"><span style="width:${w}%"></span></span>
        <span class="deg-num">${t.deg}</span>
      </button>`;
  }

  $('results').innerHTML = `
    <section class="links-block">
      <div class="thinker-head">
        <span class="num">★</span>
        <h2>Pares con lecturas compartidas</h2>
        <span class="nbooks">${pairs.length} pares</span>
      </div>
      <p class="links-help">Dos pensadores aparecen juntos cuando el mismo título figura en la lista de ambos — sea porque uno recomienda lo que el otro escribió, o porque los dos lo citan.</p>
      <div class="pair-grid">${pHtml}</div>
    </section>
    <section class="links-block">
      <div class="thinker-head">
        <span class="num">◆</span>
        <h2>Quiénes son el nudo de la red</h2>
        <span class="nbooks">libros compartidos con otros</span>
      </div>
      <div class="degree-list">${gHtml}</div>
    </section>`;

  $('results').querySelectorAll('.pair-card').forEach(card => {
    const toggle = () => {
      const open = card.classList.toggle('open');
      card.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open && !card.dataset.filled) {
        card.dataset.filled = '1';
        const a = card.dataset.a, b = card.dataset.b;
        const keys = PAIRS.find(p => p.a === a && p.b === b).keys;
        const body = document.createElement('div');
        body.className = 'pair-body';
        body.innerHTML = keys.map(k => {
          const arr = LINKS.get(k);
          const entries = arr.filter(x => x.thinker === a || x.thinker === b);
          return `<div class="pair-row">
            <div class="pr-title">${esc(entries[0].lib.titulo)}</div>
            <div class="pr-who">${entries.map(e =>
              `<span class="mini-badge ${esc(e.tipo)}">${esc(e.nombre)} · ${esc(TYPE_LABEL[e.tipo] || e.tipo)}</span>`
            ).join('')}</div>
          </div>`;
        }).join('');
        card.appendChild(body);
      }
    };
    card.addEventListener('click', toggle);
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
  });

  $('results').querySelectorAll('.degree-row').forEach(row => {
    row.addEventListener('click', () => {
      state.thinker = row.dataset.th;
      state.view = 'lista';
      syncChips();
      render();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });

  $('count').textContent = `${pairs.length} pares · ${PAIRS.length} en total`;
}

/* ---------- render LISTA ---------- */
function render() {
  if (state.view === 'vinculos') { renderLinks(); $('reset').hidden = false; return; }

  const nq = norm(state.q);
  const out = [];
  let shown = 0;

  for (const t of DATA) {
    if (state.thinker !== 'all' && t.slug !== state.thinker) continue;

    const books = (t.libros || []).filter(b => {
      if (state.type !== 'all' && b.tipo !== state.type) return false;
      if (state.sharedOnly) {
        const arr = LINKS.get(bookKey(b)) || [];
        if (new Set(arr.map(x => x.thinker)).size < 2) return false;
      }
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

      // vínculos: otros pensadores con el mismo título
      const arr = LINKS.get(bookKey(b)) || [];
      const otros = arr.filter(x => x.thinker !== t.slug);
      const seen = new Set();
      const uniq = otros.filter(x => { if (seen.has(x.thinker)) return false; seen.add(x.thinker); return true; });
      const linkHtml = uniq.length
        ? `<div class="b-links">
             <span class="link-label">También en</span>
             ${uniq.map(o =>
               `<button class="link-chip" data-goto="${esc(o.thinker)}">${esc(o.nombre)}<span class="mini ${esc(o.tipo)}">${esc(TYPE_LABEL[o.tipo] || o.tipo)}</span></button>`
             ).join('')}
           </div>`
        : '';

      cards += `
        <article class="bcard${uniq.length ? ' has-links' : ''}" tabindex="0" role="button" aria-expanded="false">
          <div class="b-top">
            <div>
              <h3 class="b-title">${esc(b.titulo)}</h3>
              <div class="b-author">${esc(b.autor)}</div>
              ${orig}
            </div>
            <div class="b-year">${b.anio ? esc(b.anio) : ''}</div>
          </div>
          <span class="badge ${esc(b.tipo)}">${esc(TYPE_LABEL[b.tipo] || b.tipo)}</span>
          ${linkHtml}
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
    ? `Mostrando ${shown} ${shown === 1 ? 'libro' : 'libros'}` + (state.sharedOnly ? ' compartidos' : '')
    : 'Sin resultados';
  $('reset').hidden = (state.thinker === 'all' && state.type === 'all' && !state.q && !state.sharedOnly);

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

  // saltar al pensador vinculado
  $('results').querySelectorAll('.link-chip').forEach(chip => {
    chip.addEventListener('click', (e) => {
      e.stopPropagation();
      state.thinker = chip.dataset.goto;
      state.view = 'lista';
      syncChips();
      render();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });
}

/* ---------- wiring ---------- */
$('q').addEventListener('input', (e) => { state.q = e.target.value; render(); });
$('reset').addEventListener('click', () => {
  state = { thinker: 'all', type: 'all', q: '', sharedOnly: false, view: state.view };
  $('q').value = '';
  syncChips();
  render();
});
$('sharedOnly').addEventListener('change', (e) => { state.sharedOnly = e.target.checked; render(); });
$('viewChips').addEventListener('click', (e) => {
  const b = e.target.closest('[data-vw]');
  if (!b) return;
  state.view = b.dataset.vw;
  syncChips();
  render();
});

/* deep-link: libros.html#borges */
function applyHash() {
  const h = decodeURIComponent(location.hash.replace(/^#/, '')).trim();
  if (h === 'vinculos') { state.view = 'vinculos'; syncChips(); render(); return; }
  if (h && DATA.some(t => t.slug === h)) {
    state.thinker = h;
    state.view = 'lista';
    syncChips();
    render();
  }
}
window.addEventListener('hashchange', applyHash);

load().then(applyHash);
