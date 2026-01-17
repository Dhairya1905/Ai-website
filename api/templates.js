// Vercel Serverless Function for Templates
export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const templates = [
    { id: 'portfolio', name: 'Portfolio', description: 'Perfect for artists and photographers' },
    { id: 'business', name: 'Business', description: 'Professional business website' },
    { id: 'ecommerce', name: 'E-commerce', description: 'Online store template' },
    { id: 'restaurant', name: 'Restaurant', description: 'Restaurant or cafe website' },
    { id: 'custom', name: 'Custom', description: 'Generate from scratch based on your prompt' }
  ];

  res.status(200).json({ templates });
}
