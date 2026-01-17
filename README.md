# AI-Powered Website Generator

An intelligent web application that generates functional websites from natural language descriptions using AI models.

## Features

- **Natural Language Input**: Describe your website in plain text
- **AI-Powered Generation**: Uses LLMs to generate HTML/CSS/JavaScript
- **Component Library**: Reusable UI components for consistent design
- **Live Preview**: Preview generated websites before downloading
- **Export Functionality**: Download generated code or deploy to subdomains
- **Responsive Design**: Mobile-first approach for all devices

## Technology Stack

- **Frontend**: Next.js 14 with TypeScript
- **Backend**: FastAPI with Python
- **AI Integration**: OpenAI API / Anthropic Claude
- **Database**: PostgreSQL with Prisma ORM
- **Styling**: Tailwind CSS
- **Deployment**: Render/Vercel

## Project Structure

```
ai-website-generator/
├── frontend/          # Next.js frontend application
├── backend/           # FastAPI backend API
├── components/        # Reusable UI components library
├── docs/             # Documentation
└── README.md         # This file
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL (optional for local development)

### Installation

1. Clone the repository
2. Install frontend dependencies:
   ```bash
   cd frontend && npm install
   ```
3. Install backend dependencies:
   ```bash
   cd backend && pip install -r requirements.txt
   ```
4. Set up environment variables (see `.env.example`)
5. Run the development servers:
   ```bash
   # Frontend
   cd frontend && npm run dev
   
   # Backend
   cd backend && uvicorn main:app --reload
   ```

## API Endpoints

- `POST /api/generate` - Generate website from prompt
- `GET /api/templates` - Get available templates
- `POST /api/export` - Export generated website
- `GET /api/preview/{id}` - Preview generated website

## Usage

1. Open the frontend application in your browser
2. Enter a description of the website you want to create
3. Choose a template or let AI generate from scratch
4. Preview the generated website
5. Export the code or deploy to a subdomain

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
