'use client';

import { useState } from 'react';
import { WebsiteGenerator } from '@/components/WebsiteGenerator';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI Website Generator
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Create beautiful, functional websites instantly with AI. Just describe what you want, and we'll build it for you.
          </p>
        </header>
        
        <WebsiteGenerator />
      </div>
    </div>
  );
}
