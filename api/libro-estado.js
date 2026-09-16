// /api/libro-estado — escribe Estado y Lista de un libro en la Google Sheet "Biblioteca Panteón"
// Autenticación: service account / refresh token en env vars.
// Body JSON: { id, estado?, lista? }
//   estado: "" | "quiero" | "tengo" | "leyendo" | "leído"
//   lista:  "" | "comprar" | "regalo"
//
// Env vars requeridas (Vercel → Settings → Environment Variables):
//   GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN, SHEET_ID

const SHEET_ID = process.env.SHEET_ID || '1OQDNlQ5_yAXCfTOxjuyi9XDogPuR4T__diRigTC_iUE';
const ESTADOS = ['', 'quiero', 'tengo', 'leyendo', 'leído'];
const LISTAS = ['', 'comprar', 'regalo'];

let cachedToken = null;
let tokenExpiry = 0;

async function getAccessToken() {
  if (cachedToken && Date.now() < tokenExpiry - 60000) return cachedToken;

  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: process.env.GOOGLE_CLIENT_ID,
      client_secret: process.env.GOOGLE_CLIENT_SECRET,
      refresh_token: process.env.GOOGLE_REFRESH_TOKEN,
      grant_type: 'refresh_token',
    }),
  });

  if (!res.ok) {
    const t = await res.text();
    throw new Error('Token refresh falló: ' + res.status + ' ' + t);
  }
  const j = await res.json();
  cachedToken = j.access_token;
  tokenExpiry = Date.now() + (j.expires_in || 3600) * 1000;
  return cachedToken;
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { return res.status(400).json({ error: 'JSON inválido' }); } }
  const { id, estado, lista } = body || {};
  if (!id) return res.status(400).json({ error: 'Falta id' });

  if (estado !== undefined && !ESTADOS.includes(estado))
    return res.status(400).json({ error: 'Estado inválido', validos: ESTADOS });
  if (lista !== undefined && !LISTAS.includes(lista))
    return res.status(400).json({ error: 'Lista inválida', validas: LISTAS });

  try {
    const token = await getAccessToken();
    const auth = { Authorization: `Bearer ${token}` };

    // 1. Buscar la fila por ID (columna A)
    const cols = 'A:H'; // A=ID ... H=Estado (col 8), I=Lista (col 9)
    const r = await fetch(
      `https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${encodeURIComponent('Biblioteca!A:I')}`,
      { headers: auth }
    );
    if (!r.ok) throw new Error('Lectura falló: ' + r.status + ' ' + await r.text());
    const data = await r.json();
    const rows = data.values || [];

    let rowIndex = -1;
    for (let i = 1; i < rows.length; i++) {
      if ((rows[i][0] || '').trim() === id) { rowIndex = i + 1; break; } // +1 → 1-indexed
    }
    if (rowIndex === -1) return res.status(404).json({ error: 'ID no encontrado: ' + id });

    // 2. Armar updates solo de las columnas presentes
    const updates = [];
    if (estado !== undefined) updates.push({ range: `Biblioteca!H${rowIndex}`, values: [[estado]] });
    if (lista !== undefined)  updates.push({ range: `Biblioteca!I${rowIndex}`, values: [[lista]] });

    if (updates.length) {
      const w = await fetch(
        `https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values:batchUpdate`,
        {
          method: 'POST',
          headers: { ...auth, 'Content-Type': 'application/json' },
          body: JSON.stringify({ valueInputOption: 'USER_ENTERED', data: updates }),
        }
      );
      if (!w.ok) throw new Error('Escritura falló: ' + w.status + ' ' + await w.text());
    }

    return res.status(200).json({
      ok: true, id, row: rowIndex,
      estado: estado !== undefined ? estado : (rows[rowIndex - 1]?.[7] ?? ''),
      lista:  lista  !== undefined ? lista  : (rows[rowIndex - 1]?.[8] ?? ''),
    });
  } catch (e) {
    console.error('[libro-estado]', e);
    return res.status(500).json({ error: String(e.message || e) });
  }
}
