# Quick Start Guide

Follow these steps to get the RAG Agent up and running in minutes!

## Quick Setup (5 minutes)

### 1. Backend Setup (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Create .env file for Google Gemini API
# Copy the example and add your key:
# GEMINI_API_KEY=your_key_here
# Get your API key from: https://makersuite.google.com/app/apikey

# Start the server
python main.py
```

You should see: `Uvicorn running on http://0.0.0.0:8000`

### 2. Frontend Setup (Terminal 2)

Open a NEW terminal window:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

You should see: `Local: http://localhost:5173/`

### 3. Use the Application

1. Open your browser to `http://localhost:5173`
2. Click "Upload Documents"
3. Select a PDF or TXT file
4. Wait for upload confirmation
5. Type a question and press Enter
6. See the answer with source citations!

## Testing Without Gemini API

The system works without a Gemini API key! It will use a simpler answer extraction method. For better answers, add your Gemini API key to `backend/.env`. Get your API key from: https://makersuite.google.com/app/apikey

## Common Issues

**Backend won't start:**
- Make sure Python 3.8+ is installed
- Check that virtual environment is activated
- Verify all dependencies installed: `pip list`

**Frontend won't start:**
- Make sure Node.js 16+ is installed
- Try deleting `node_modules` and running `npm install` again

**Can't upload files:**
- Make sure backend is running on port 8000
- Check browser console for errors
- Verify file is PDF or TXT format

**No answers generated:**
- Make sure documents are uploaded successfully
- Check backend terminal for error messages
- Verify you have documents loaded (should show count in header)

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize the embedding model in `backend/rag_service.py`
- Adjust chunk size and overlap for your documents
- Add more file type support

Enjoy your RAG Agent! 🚀

