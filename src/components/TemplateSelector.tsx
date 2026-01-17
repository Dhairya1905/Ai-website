'use client';

interface TemplateSelectorProps {
  selectedTemplate: string;
  onTemplateChange: (template: string) => void;
}

export function TemplateSelector({ selectedTemplate, onTemplateChange }: TemplateSelectorProps) {
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
