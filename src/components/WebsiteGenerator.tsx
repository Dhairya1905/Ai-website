'use client';

import { useState } from 'react';

interface GeneratedWebsite {
  id: string;
  html: string;
  css: string;
  js: string;
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
      <div className="border border-gray-200 rounded-lg overflow-hidden bg-white">
        <iframe
          srcDoc={`
            <!DOCTYPE html>
            <html>
              <head>
                <style>${website.css}</style>
              </head>
              <body>
                ${website.html}
                <script>${website.js}</script>
              </body>
            </html>
          `}
          className="w-full h-96 border-0"
          sandbox="allow-scripts"
          title="Website Preview"
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
      const response = await fetch('/api/generate', {
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
        throw new Error('Failed to generate website');
      }

      const website = await response.json();
      setGeneratedWebsite(website);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExport = async () => {
    if (!generatedWebsite) return;

    try {
      const response = await fetch(`/api/export/${generatedWebsite.id}`);
      
      if (!response.ok) {
        throw new Error('Failed to export website');
      }
      
      const data = await response.json();

      // Create and download files
      Object.entries(data.files).forEach(([filename, content]) => {
        const blob = new Blob([content as string], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });
    } catch (err) {
      setError('Failed to export website');
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Section */}
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

          {/* Examples */}
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

        {/* Preview Section */}
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
              <div className="h-96 bg-gray-50 rounded-lg flex items-center justify-center">
                <p className="text-gray-500 text-center">
                  Your generated website will appear here
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
