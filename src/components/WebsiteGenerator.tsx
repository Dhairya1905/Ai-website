'use client';

import { useState } from 'react';

interface GeneratedWebsite {
  id: string;
  html: string;
  metadata: {
    prompt: string;
    template?: string;
    style: string;
    created_at: string;
  };
}

function TemplateSelector({ selectedTemplate, onTemplateChange }: { selectedTemplate: string; onTemplateChange: (template: string) => void }) {
  const templates = [
    { id: 'custom', name: 'Custom', description: 'Generate from scratch based on your prompt' },
    { id: 'portfolio', name: 'Portfolio', description: 'Perfect for artists and photographers' },
    { id: 'business', name: 'Business', description: 'Professional business website' },
    { id: 'ecommerce', name: 'E-commerce', description: 'Online store template' },
    { id: 'restaurant', name: 'Restaurant', description: 'Restaurant or cafe website' },
  ];

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Choose a template (optional)
      </label>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {templates.map((template) => (
          <button
            key={template.id}
            onClick={() => onTemplateChange(template.id)}
            className={`p-3 rounded-lg border-2 transition-all text-left ${
              selectedTemplate === template.id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="font-medium text-gray-900">{template.name}</div>
            <div className="text-sm text-gray-500 mt-1">{template.description}</div>
          </button>
        ))}
      </div>
    </div>
  );
}

function WebsitePreview({ website }: { website: GeneratedWebsite }) {
  return (
    <div className="space-y-4">
      <div className="border-2 border-gray-300 rounded-lg overflow-hidden shadow-lg">
        <iframe
          srcDoc={website.html}
          className="w-full bg-white"
          style={{ height: '500px' }}
          title="Website Preview"
          sandbox="allow-scripts allow-same-origin"
        />
      </div>
      
      <div className="text-sm text-gray-600 space-y-1">
        <p><strong>Template:</strong> {website.metadata.template || 'Custom'}</p>
        <p><strong>Style:</strong> {website.metadata.style}</p>
        <p><strong>Generated:</strong> {new Date(website.metadata.created_at).toLocaleString()}</p>
      </div>
    </div>
  );
}

export function WebsiteGenerator() {
  const [prompt, setPrompt] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState('custom');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedWebsite, setGeneratedWebsite] = useState<GeneratedWebsite | null>(null);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a description for your website');
      return;
    }

    setIsGenerating(true);
    setError('');

    try {
      const response = await fetch('/api/generate-website', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt,
          template: selectedTemplate === 'custom' ? null : selectedTemplate,
          style: 'modern'
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate website');
      }

      const website = await response.json();
      setGeneratedWebsite(website);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Generation error:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExport = () => {
    if (!generatedWebsite) return;

    try {
      const cssRegex = /<style[^>]*>([\s\S]*?)<\/style>/i;
      const jsRegex = /<script[^>]*>([\s\S]*?)<\/script>/i;
      
      const cssMatch = generatedWebsite.html.match(cssRegex);
      const css = cssMatch ? cssMatch[1].trim() : '';

      const jsMatch = generatedWebsite.html.match(jsRegex);
      const js = jsMatch ? jsMatch[1].trim() : '';

      let cleanHtml = generatedWebsite.html;
      if (css) {
        cleanHtml = cleanHtml.replace(cssRegex, '<link rel="stylesheet" href="styles.css">');
      }
      if (js) {
        cleanHtml = cleanHtml.replace(jsRegex, '<script src="script.js"></script>');
      }

      downloadFile('index.html', cleanHtml);

      if (css) {
        downloadFile('styles.css', css);
      }

      if (js) {
        downloadFile('script.js', js);
      }

      downloadFile('website-complete.html', generatedWebsite.html);

      const readme = `# Generated Website

Generated on: ${new Date(generatedWebsite.metadata.created_at).toLocaleString()}
Template: ${generatedWebsite.metadata.template || 'Custom'}
Style: ${generatedWebsite.metadata.style}
Prompt: ${generatedWebsite.metadata.prompt}

## Files Included:

1. website-complete.html - Complete website in a single file
2. index.html - Main HTML file
3. styles.css - Stylesheet (if CSS was extracted)
4. script.js - JavaScript file (if JS was extracted)

## How to Use:

### Option 1: Single File
- Open website-complete.html in your browser

### Option 2: Multiple Files
- Make sure all files are in the same folder
- Open index.html in your browser

## Deployment:

### Vercel:
1. Install Vercel CLI: npm i -g vercel
2. Run: vercel

### Netlify:
1. Drag and drop your folder to netlify.com/drop

### GitHub Pages:
1. Create a new repository
2. Upload all files
3. Enable GitHub Pages in Settings

Enjoy your new website!
`;
      downloadFile('README.md', readme);

    } catch (err) {
      setError('Failed to export website files');
      console.error('Export error:', err);
    }
  };

  const downloadFile = (filename: string, content: string) => {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-900">Describe Your Website</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  What kind of website do you want to create?
                </label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="e.g., Create a portfolio website for a photographer with a gallery, about section, and contact form..."
                  className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-gray-900 placeholder-gray-500 bg-white"
                />
              </div>

              <TemplateSelector
                selectedTemplate={selectedTemplate}
                onTemplateChange={setSelectedTemplate}
              />

              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                  {error}
                </div>
              )}

              <button
                onClick={handleGenerate}
                disabled={isGenerating}
                className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isGenerating ? 'Generating...' : 'Generate Website'}
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-3 text-gray-900">Example Prompts</h3>
            <div className="space-y-2">
              {[
                "Create a portfolio website for a photographer",
                "Build an e-commerce site for handmade jewelry",
                "Design a restaurant website with menu and reservations",
                "Make a business consulting website with services"
              ].map((example, index) => (
                <button
                  key={index}
                  onClick={() => setPrompt(example)}
                  className="block w-full text-left p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-sm text-gray-700"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="lg:sticky lg:top-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-semibold text-gray-900">Preview</h2>
              {generatedWebsite && (
                <button
                  onClick={handleExport}
                  className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors"
                >
                  Export Files
                </button>
              )}
            </div>
            
            {generatedWebsite ? (
              <WebsitePreview website={generatedWebsite} />
            ) : (
              <div className="h-96 bg-gray-50 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
                <p className="text-gray-500 text-center px-4">
                  {isGenerating ? (
                    <span className="flex flex-col items-center gap-2">
                      <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Generating your website...
                    </span>
                  ) : (
                    'Your generated website will appear here'
                  )}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}