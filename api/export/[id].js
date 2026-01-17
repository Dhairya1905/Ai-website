// Vercel Serverless Function for Export
export default async function handler(req, res) {
  const { id } = req.query;
  
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Mock export response
    const mockFiles = {
      'index.html': `<!DOCTYPE html><html><head><title>Exported Website</title></head><body><h1>Website ID: ${id}</h1></body></html>`,
      'style.css': 'body { margin: 0; font-family: Arial; }',
      'script.js': '// Generated JavaScript'
    };

    res.status(200).json({
      id,
      files: mockFiles,
      metadata: {
        prompt: 'Mock prompt',
        template: 'custom',
        style: 'modern',
        created_at: new Date().toISOString()
      }
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to export website' });
  }
}
