// Record Sale — Vercel Serverless Function (no auth required)
// Called from success.html client-side to log purchases

const SALES_FILE = '/tmp/sales.json';
const PRICE_CENTS = 1000; // $10 default

export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'GET only' });

  const { edition, amount, method, txHash } = req.query;

  const sale = {
    id: Date.now().toString(36),
    edition: edition || 'unknown',
    amount: parseFloat(amount) || 9.99,
    currency: 'USD',
    method: method || 'manual',
    txHash: txHash || '',
    timestamp: new Date().toISOString()
  };

  try {
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
