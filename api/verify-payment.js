// Vercel Serverless Function — verifies USDC payments on-chain
// Works with: Ethereum, Polygon, Arbitrum, Base, Optimism, Avalanche
// Auto-deploys via api/ directory on Vercel

const OUR_WALLET = '0x18C3886478DE8c945c086A4DDe8967Ab15A1862F'.toLowerCase();
const MIN_AMOUNT = BigInt('9990000'); // 9.99 USDC min (price is $10, $0.01 tolerance for fees)
const TRANSFER_EVENT = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef';

const CHAINS = {
  ethereum: {
    rpc: 'https://cloudflare-eth.com',
    usdc: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    name: 'Ethereum (ERC-20)'
  },
  polygon: {
    rpc: 'https://polygon-bor-rpc.publicnode.com',
    usdc: '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359',
    name: 'Polygon'
  },
  arbitrum: {
    rpc: 'https://arb1.arbitrum.io/rpc',
    usdc: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
    name: 'Arbitrum'
  },
  base: {
    rpc: 'https://mainnet.base.org',
    usdc: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    name: 'Base'
  },
  optimism: {
    rpc: 'https://mainnet.optimism.io',
    usdc: '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85',
    name: 'Optimism'
  },
  avalanche: {
    rpc: 'https://api.avax.network/ext/bc/C/rpc',
    usdc: '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
    name: 'Avalanche C-Chain'
  }
};

async function rpcCall(rpcUrl, method, params) {
  const resp = await fetch(rpcUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', method, params, id: 1 })
  });
  const data = await resp.json();
  if (data.error) throw new Error(`RPC error: ${data.error.message}`);
  return data.result;
}

export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'GET only' });

  const { tx, chain } = req.query;
  if (!tx) return res.status(400).json({ error: 'Missing tx parameter' });
  if (!/^0x[a-fA-F0-9]{64}$/.test(tx)) return res.status(400).json({ error: 'Invalid tx hash format' });

  const chainConfig = CHAINS[chain] || CHAINS['ethereum'];

  try {
    // Step 1: Get transaction receipt
    const receipt = await rpcCall(chainConfig.rpc, 'eth_getTransactionReceipt', [tx]);
    if (!receipt || !receipt.logs) {
      return res.json({ verified: false, reason: 'Transaction not found or still pending' });
    }

    // Step 2: Check confirmations (need at least 12 blocks for safety)
    const blockNumber = await rpcCall(chainConfig.rpc, 'eth_blockNumber', []);
    const currentBlock = BigInt(blockNumber);
    const txBlock = BigInt(receipt.blockNumber);
    const confirmations = currentBlock - txBlock + BigInt(1);

    if (confirmations < BigInt(12)) {
      return res.json({ verified: false, reason: `Waiting for confirmations (${confirmations.toString()}/12)` });
    }

    // Step 3: Decode Transfer events from logs
    const ourAddrPadded = '0x' + '0'.repeat(24) + OUR_WALLET.slice(2);
    
    for (const log of receipt.logs) {
      if (log.address.toLowerCase() !== chainConfig.usdc.toLowerCase()) continue;
      if (log.topics[0] !== TRANSFER_EVENT) continue;

      // topics[1] = from (padded), topics[2] = to (padded)
      const toAddr = '0x' + log.topics[2].slice(26).toLowerCase();
      if (toAddr !== OUR_WALLET) continue;

      // Decode amount (USDC has 6 decimals)
      const amount = BigInt(log.data);
      const amountFormatted = Number(amount) / 1_000_000;

      if (amount >= MIN_AMOUNT) {
        return res.json({
          verified: true,
          amount: amountFormatted,
          usdAmount: amountFormatted,
          chain: chainConfig.name,
          txHash: tx,
          confirmations: Number(confirmations),
          message: `✅ Verified! ${amountFormatted} USDC received.`
        });
      } else {
        return res.json({ verified: false, reason: `Amount too low: ${amountFormatted} USDC (min 9.99)` });
      }
    }

    return res.json({ verified: false, reason: 'No USDC transfer to our wallet found in this transaction' });

  } catch (err) {
    console.error('verify-payment error:', err);
    return res.status(500).json({ error: err.message });
  }
}
