// Vercel Serverless Function for Website Generation
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { prompt, template, style } = req.body;
    
    // Here you would integrate with OpenAI/Anthropic API
    // For now, return a mock response
    const mockWebsite = {
      id: Date.now().toString(),
      html: `<!DOCTYPE html>
<html>
<head><title>Generated Website</title></head>
<body>
  <h1>Generated from: ${prompt}</h1>
  <p>This is a mock website. In production, this would be AI-generated.</p>
</body>
</html>`,
      css: "body { font-family: Arial; margin: 40px; }",
      js: "// Generated JavaScript",
      metadata: {
        prompt,
        template: template || 'custom',
        style: style || 'modern',
        created_at: new Date().toISOString()
      }
    };

    res.status(200).json(mockWebsite);
  } catch (error) {
    res.status(500).json({ error: 'Failed to generate website' });
  }
}
