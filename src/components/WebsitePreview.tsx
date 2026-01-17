'use client';

import { useEffect, useRef } from 'react';

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

interface WebsitePreviewProps {
  website: GeneratedWebsite;
}

export function WebsitePreview({ website }: WebsitePreviewProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    if (iframeRef.current && website.html) {
      const iframe = iframeRef.current;
      const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;
      
      if (iframeDoc) {
        iframeDoc.open();
        iframeDoc.write(website.html);
        iframeDoc.close();
      }
    }
  }, [website.html]);

  return (
    <div className="space-y-4">
      <div className="border border-gray-200 rounded-lg overflow-hidden">
        <iframe
          ref={iframeRef}
          className="w-full h-96 bg-white"
          title="Website Preview"
          sandbox="allow-scripts allow-same-origin"
          loading="lazy"
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
