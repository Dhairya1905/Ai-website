# API Documentation

## Overview

The AI Website Generator API provides endpoints for generating websites from natural language prompts, managing templates, and exporting generated code.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. In production, API keys or JWT tokens should be implemented.

## Endpoints

### 1. Generate Website

**POST** `/api/generate`

Generates a complete website from a natural language prompt.

**Request Body:**
```json
{
  "prompt": "Create a portfolio website for a photographer",
  "template": "portfolio",
  "style": "modern"
}
```

**Parameters:**
- `prompt` (string, required): Natural language description of the desired website
- `template` (string, optional): Template ID to use as base. Defaults to custom generation
- `style` (string, optional): Visual style preference. Defaults to "modern"

**Response:**
```json
{
  "id": "uuid-string",
  "html": "<!DOCTYPE html>...",
  "css": "* { margin: 0; ... }",
  "js": "// JavaScript code",
  "metadata": {
    "prompt": "Create a portfolio website for a photographer",
    "template": "portfolio",
    "style": "modern",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### 2. Get Templates

**GET** `/api/templates`

Retrieves available website templates.

**Response:**
```json
{
  "templates": [
    {
      "id": "portfolio",
      "name": "Portfolio",
      "description": "Perfect for artists and photographers"
    },
    {
      "id": "business",
      "name": "Business",
      "description": "Professional business website"
    }
  ]
}
```

### 3. Preview Website

**GET** `/api/preview/{website_id}`

Retrieves a generated website for preview.

**Path Parameters:**
- `website_id` (string): The UUID of the generated website

**Response:**
```json
{
  "id": "uuid-string",
  "prompt": "Create a portfolio website for a photographer",
  "template": "portfolio",
  "style": "modern",
  "html": "<!DOCTYPE html>...",
  "css": "* { margin: 0; ... }",
  "js": "// JavaScript code",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 4. Export Website

**GET** `/api/export/{website_id}`

Exports a website as downloadable files.

**Path Parameters:**
- `website_id` (string): The UUID of the generated website

**Response:**
```json
{
  "id": "uuid-string",
  "files": {
    "index.html": "<!DOCTYPE html>...",
    "style.css": "* { margin: 0; ... }",
    "script.js": "// JavaScript code"
  },
  "metadata": {
    "prompt": "Create a portfolio website for a photographer",
    "template": "portfolio",
    "style": "modern",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### 5. List Projects

**GET** `/api/projects`

Lists all generated projects.

**Response:**
```json
{
  "projects": [
    {
      "id": "uuid-string",
      "prompt": "Create a portfolio website for a photographer",
      "template": "portfolio",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Error Responses

The API returns standard HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found (website ID doesn't exist)
- `500`: Internal Server Error

Error response format:
```json
{
  "detail": "Error message description"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing:
- Requests per minute per IP
- Daily request limits per user
- Queue system for heavy processing

## Integration Examples

### JavaScript/TypeScript

```javascript
async function generateWebsite(prompt, template = null) {
  const response = await fetch('http://localhost:8000/api/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      prompt,
      template,
      style: 'modern'
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to generate website');
  }

  return await response.json();
}

// Usage
const website = await generateWebsite(
  'Create a portfolio website for a photographer',
  'portfolio'
);
```

### Python

```python
import requests

def generate_website(prompt, template=None):
    response = requests.post(
        'http://localhost:8000/api/generate',
        json={
            'prompt': prompt,
            'template': template,
            'style': 'modern'
        }
    )
    
    if response.status_code != 200:
        raise Exception('Failed to generate website')
    
    return response.json()

# Usage
website = generate_website(
    'Create a portfolio website for a photographer',
    'portfolio'
)
```

## Component Library

The API uses a component-based architecture with the following components:

### Core Components
- **navbar**: Navigation header with logo and menu items
- **hero**: Hero section with headline and call-to-action
- **about**: About section with company information
- **contact**: Contact form section

### Extended Components
- **gallery**: Image gallery for portfolios
- **services**: Services showcase for business sites
- **products**: Product grid for e-commerce
- **menu**: Restaurant menu display
- **testimonials**: Customer testimonials

Each component includes:
- HTML structure with placeholder variables
- CSS styling with responsive design
- JavaScript interactivity where applicable

## Template System

Templates are predefined combinations of components optimized for specific use cases:

1. **Portfolio**: navbar, hero, gallery, about, contact
2. **Business**: navbar, hero, services, about, testimonials, contact
3. **E-commerce**: navbar, hero, products, features, contact
4. **Restaurant**: navbar, hero, menu, about, reservations, contact

Templates can be customized by:
- Modifying component order
- Adding/removing components
- Adjusting styling parameters
- Customizing content placeholders
