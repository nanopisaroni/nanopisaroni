// Admin Dashboard — Vercel Serverless Function
// Protected by Basic Auth. Username: nanopi, Password: from env ADMIN_PW
// Serves the admin dashboard page with sales stats

const ADMIN_USER = 'nanopi';
const ADMIN_PW = process.env.ADMIN_PW || 'panteon2026';
const SALES_FILE = '/tmp/sales.json';

export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (req.method === 'OPTIONS') return res.status(200).end();

  // Basic Auth
  const auth = req.headers.authorization;
  if (!auth || !auth.startsWith('Basic ')) {
    res.setHeader('WWW-Authenticate', 'Basic realm="Panteón Admin"');
    return res.status(401).json({ error: 'Login required' });
  }

  const decoded = Buffer.from(auth.split(' ')[1], 'base64').toString();
  const [user, pass] = decoded.split(':');
  if (user !== ADMIN_USER || pass !== ADMIN_PW) {
    return res.status(403).json({ error: 'Invalid credentials' });
  }

  // Handle different actions
  const { action } = req.query;

  if (action === 'data') {
    // Return sales data as JSON
    try {
      const fs = await import('fs/promises');
      const data = await fs.readFile(SALES_FILE, 'utf-8').catch(() => '{"sales":[],"totalRevenue":0,"totalSales":0}');
      return res.json(JSON.parse(data));
    } catch (e) {
      return res.json({ sales: [], totalRevenue: 0, totalSales: 0 });
    }
  }

  if (action === 'record') {
    // Record a new sale
    try {
      const { edition, amount, currency, method, txHash } = req.body || req.query;
      const sale = {
        id: Date.now().toString(36),
        edition: edition || 'unknown',
        amount: parseFloat(amount) || 9.99,
        currency: currency || 'USD',
        method: method || 'manual',
        txHash: txHash || '',
        timestamp: new Date().toISOString()
      };
      
      const fs = await import('fs/promises');
      let data = { sales: [], totalRevenue: 0, totalSales: 0 };
      try {
        const raw = await fs.readFile(SALES_FILE, 'utf-8');
        data = JSON.parse(raw);
      } catch {}
      
      data.sales.push(sale);
      data.totalSales = data.sales.length;
      data.totalRevenue = data.sales.reduce((sum, s) => sum + s.amount, 0);
      
      await fs.writeFile(SALES_FILE, JSON.stringify(data, null, 2));
      return res.json({ success: true, sale });
    } catch (e) {
      return res.status(500).json({ error: e.message });
    }
  }

  // Default: serve the admin HTML dashboard
  const html = getDashboardHTML();
  res.setHeader('Content-Type', 'text/html');
  return res.status(200).send(html);
}

function getDashboardHTML() {
  return `<!doctype html>
<html lang="es">
<head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin - Panteón Dashboard</title>
<style>
:root{--bg:#0a0a0a;--card:#1a1a1a;--text:#f0ede5;--muted:#666;--accent:#c9a23c;--green:#059669}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:system-ui,sans-serif;font-size:15px;line-height:1.5}
.site{width:min(100%-40px,800px);margin:0 auto;padding:32px 0}
h1{font-size:28px;font-weight:600;margin:0 0 4px;color:var(--accent)}
.sub{color:var(--muted);font-size:14px;margin-bottom:32px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:32px}
.card{background:var(--card);border:1px solid #333;border-radius:8px;padding:20px}
.card .label{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px}
.card .value{font-size:32px;font-weight:700}
.card .value.green{color:var(--green)}
.card .value.gold{color:var(--accent)}
table{width:100%;border-collapse:collapse;margin-top:8px;font-size:13px}
th{text-align:left;color:var(--muted);padding:8px 12px;border-bottom:1px solid #333}
td{padding:8px 12px;border-bottom:1px solid #222}
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600}
.badge.stripe{background:#635bff20;color:#635bff}
.badge.crypto{background:#f7931a20;color:#f7931a}
.badge.manual{background:#66620;color:#666}
.badge.freebook{background:#05966920;color:#059669}
.refresh{font-size:13px;color:var(--accent);text-decoration:none;float:right;margin-top:4px}
.refresh:hover{text-decoration:underline}
.empty{color:var(--muted);text-align:center;padding:40px;font-size:14px}
.tx{font-family:monospace;font-size:11px;color:var(--muted)}
</style>
</head>
<body>
<div class="site">
<h1>🔐 Admin Dashboard</h1>
<p class="sub">Panteón Personal · Personal Pantheon — Sales & Analytics</p>

<div class="grid">
  <div class="card">
    <div class="label">Total Sales</div>
    <div class="value gold" id="totalSales">—</div>
  </div>
  <div class="card">
    <div class="label">Revenue (USD)</div>
    <div class="value green" id="totalRevenue">—</div>
  </div>
  <div class="card">
    <div class="label">English Edition</div>
    <div class="value" id="enSales">—</div>
  </div>
  <div class="card">
    <div class="label">Spanish Edition</div>
    <div class="value" id="esSales">—</div>
  </div>
  <div class="card">
    <div class="label">Free Downloads 🆓</div>
    <div class="value" id="freeDownloads">—</div>
  </div>
</div>

<h2 style="font-size:18px;font-weight:600;margin:0 0 12px">Recent Sales <a href="javascript:loadData()" class="refresh">⟳ Refresh</a></h2>
<div id="salesTable"><p class="empty">Loading...</p></div>

<p style="margin-top:32px;font-size:12px;color:var(--muted)">Wallet: 0x18C3886478DE8c945c086A4DDe8967Ab15A1862F</p>
</div>

<script>
async function loadData() {
  try {
    const resp = await fetch('/api/admin?action=data');
    const data = await resp.json();
    const sales = data.sales || [];
    
    document.getElementById('totalSales').textContent = sales.length;
    document.getElementById('totalRevenue').textContent = '$' + (data.totalRevenue || 0).toFixed(2);
    
    const enSales = sales.filter(s => s.edition === 'en' || s.edition === 'english').length;
    const esSales = sales.filter(s => s.edition === 'es' || s.edition === 'spanish').length;
    document.getElementById('enSales').textContent = enSales;
    document.getElementById('esSales').textContent = esSales;

    const freeDls = sales.filter(s => s.method === 'freebook').length;
    document.getElementById('freeDownloads').textContent = freeDls;

    if (sales.length === 0) {
      document.getElementById('salesTable').innerHTML = '<p class="empty">No sales yet. Share the book!</p>';
      return;
    }

    let html = '<table><tr><th>Date</th><th>Edition</th><th>Amount</th><th>Method</th><th>TX</th></tr>';
    for (const s of sales.slice().reverse().slice(0, 50)) {
      const date = new Date(s.timestamp).toLocaleDateString();
      const edition = s.edition === 'en' ? '📗 EN' : s.edition === 'es' ? '📖 ES' : s.edition;
      const method = s.method;
      const badge = s.method === 'stripe' ? 'stripe' : s.method === 'crypto' ? 'crypto' : s.method === 'freebook' ? 'freebook' : 'manual';
      html += '<tr><td>' + date + '</td><td>' + edition + '</td><td>$' + s.amount.toFixed(2) + '</td><td><span class="badge ' + badge + '">' + (method === 'freebook' ? '🆓 freebook' : method) + '</span></td><td class="tx">' + (s.txHash || '').slice(0, 12) + '...</td></tr>';
    }
    html += '</table>';
    document.getElementById('salesTable').innerHTML = html;
  } catch (e) {
    document.getElementById('salesTable').innerHTML = '<p class="empty">Error loading data. Make sure you are logged in.</p>';
  }
}
loadData();
setInterval(loadData, 30000);
</script>
</body>
</html>`;
}
