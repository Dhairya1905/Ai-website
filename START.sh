#!/bin/bash

echo "🚀 Starting AI Website Generator..."

# Start backend server
echo "📦 Starting FastAPI backend..."
cd backend
source venv/bin/activate 2>/dev/null || python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python database.py  # Initialize database
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Start frontend server
echo "🎨 Starting Next.js frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Servers started!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for interrupt
trap "echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
