/* Seguimiento personal de lectura — lee/escribe la Google Sheet "Biblioteca Panteón".
   - GET  (gviz CSV, público) → estado + lista de cada libro
   - POST /api/libro-estado    → escribe un cambio                            */

const SHEET_ID = '1OQDNlQ5_yAXCfTOxjuyi9XDogPuR4T__diRigTC_iUE';
const GVIZ = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Biblioteca`;

// id -> {estado, lista}
export const TRACK = new Map();

export const ESTADO_LABEL = {
  '':        '',
  'quiero':  'Quiero',
  'tengo':   'Lo tengo',
  'leyendo': 'Leyendo',
  'leído':   'Leído',
};

export const ESTADO_SHORT = {
  'quiero':  'quiero',
  'tengo':   'tengo',
  'leyendo': 'leyendo',
  'leído':   'leído',
};

/* ---------- parser CSV (maneja comillas y comas embebidas) ---------- */
function parseCSV(text) {
  const rows = [];
  let row = [], cell = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"') {
        if (text[i + 1] === '"') { cell += '"'; i++; }
        else q = false;
      } else cell += c;
    } else {
      if (c === '"') q = true;
      else if (c === ',') { row.push(cell); cell = ''; }
      else if (c === '\n') { row.push(cell); rows.push(row); row = []; cell = ''; }
      else if (c === '\r') { /* ignorar */ }
      else cell += c;
    }
  }
  if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
  return rows;
}

/* ---------- carga inicial ---------- */
export async function loadTracking() {
  const res = await fetch(GVIZ, { cache: 'no-cache' });
  if (!res.ok) throw new Error('HTTP ' + res.status);
  const text = await res.text();
  const rows = parseCSV(text);

  TRACK.clear();
  const sep = ' ';
  for (let i = 1; i < rows.length; i++) {
    const r = rows[i];
    if (!r || !r[0]) continue;
    TRACK.set(r[0].trim(), {
      pensador: r[1] || '',
      titulo:   r[2] || '',
      estado:   (r[7] || '').trim(),
      lista:    (r[8] || '').trim(),
    });
  }
  return TRACK;
}

/* ---------- escritura ---------- */
export async function saveBook(id, patch, token) {
  const res = await fetch('/api/libro-estado', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id, ...patch, token }),
  });
  const j = await res.json().catch(() => ({}));
  if (!res.ok || !j.ok) throw new Error(j.error || ('HTTP ' + res.status));
  // actualizar cache local
  const cur = TRACK.get(id) || {};
  if (patch.estado !== undefined) cur.estado = patch.estado;
  if (patch.lista  !== undefined) cur.lista  = patch.lista;
  TRACK.set(id, cur);
  return cur;
}
