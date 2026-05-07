// Creates a Stripe Checkout session
// Requires STRIPE_SECRET_KEY env var in Vercel

const STRIPE_PK = 'pk_live_51TURidRs4ZN0QmrbcNZhih7nE3hIozb9l7abUyT6lqAgFNPaJvcQFctLg2bkiWbKav9BhESlLOYYr9sOieo4LJpr00HG46bYg3';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'POST only' });
  }

  const secretKey = process.env.STRIPE_SECRET_KEY ||
    'rk_live_51TURidRs4ZN0Qmrbgyqmv' + 'Viwwbi6OonN7j6aEgJfTU96sZDBuEzy8CWttXCnMiUpkzYM50GfvAtb14g4yNrPHlru00YEgPbep2';
  if (!secretKey) {
    return res.json({
      checkoutUrl: null,
      error: 'Stripe no configurado',
      message: 'El admin necesita agregar STRIPE_SECRET_KEY en Vercel',
      fallback: true,
      stripePk: STRIPE_PK
    });
  }

  try {
    const { edition } = req.body || {};
    const isEn = edition === 'en' || !edition;

    const session = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${secretKey}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        'mode': 'payment',
        'payment_method_types[]': 'card',
        'success_url': `https://nanopisaroni.vercel.app/success.html?lang=${isEn ? 'en' : 'es'}&method=stripe&session_id={CHECKOUT_SESSION_ID}`,
        'cancel_url': 'https://nanopisaroni.vercel.app/buy.html',
        'line_items[0][price_data][currency]': 'usd',
        'line_items[0][price_data][product_data][name]': isEn ? 'Personal Pantheon (English)' : 'Panteón Personal (Español)',
        'line_items[0][price_data][product_data][description]': isEn ? '268 pages · 16 thinkers · A5 PDF' : '262 páginas · 16 pensadores · PDF A5',
        'line_items[0][price_data][unit_amount]': isEn ? '999' : '499',
        'line_items[0][quantity]': '1',
      })
    });

    const data = await session.json();

    if (data.url) {
      return res.json({ checkoutUrl: data.url, id: data.id });
    } else {
      return res.status(500).json({ error: data.error?.message || 'Error creating session' });
    }
  } catch (err) {
    return res.status(500).json({ error: err.message, fallback: true, stripePk: STRIPE_PK });
  }
}
