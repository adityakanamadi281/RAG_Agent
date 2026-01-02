# RAG Agent - Retrieval-Augmented Generation System

A full-stack RAG (Retrieval-Augmented Generation) application with a FastAPI backend and React frontend. Upload documents (PDF, TXT), query them using natural language, and get AI-powered answers with source citations.

## Features

- 📄 **Document Upload**: Upload PDF and TXT files
- 🔍 **Semantic Search**: Vector-based document retrieval using ChromaDB
- 🤖 **AI Answers**: Generate answers using Google Gemini (optional) or simple extraction
- 📊 **Source Citation**: See which documents were used to answer your query
- 💬 **Chat Interface**: Beautiful, modern UI built with React and Tailwind CSS
- 🔄 **Persistent Storage**: Documents are stored in a local vector database

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **ChromaDB**: Vector database for document storage and retrieval
- **Sentence Transformers**: For generating embeddings
- **LangChain**: Document processing and text splitting
- **Google Gemini API** : For generating answers

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Styling
- **Axios**: HTTP client

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Google Gemini API key for enhanced answer generation

## Installation & Setup

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   git clone https://github.com/adityakanamadi281/RAG_Agent.git
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Set up environment variables:
   Create a `.env` file in the `backend` directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   Note: If you don't provide a Gemini API key, the system will use a simple answer extraction method.
   Get your API key from: https://makersuite.google.com/app/apikey

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Step 1: Start the Backend Server

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate your virtual environment (if not already activated):
   ```bash
   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Start the FastAPI server:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend API will be available at: `http://localhost:8000`
   
   You can view the API documentation at: `http://localhost:8000/docs`

### Step 2: Start the Frontend Development Server

1. Open a new terminal window

2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at: `http://localhost:5173`

## Usage

1. **Upload Documents**:
   - Click the "Upload Documents" button in the header
   - Select one or more PDF or TXT files
   - Wait for the upload to complete

2. **Ask Questions**:
   - Type your question in the input field at the bottom
   - Press Enter or click "Send"
   - View the AI-generated answer with source citations

3. **View Documents**:
   - The header shows how many documents are currently loaded
   - Click "Clear All" to remove all documents and start fresh

## API Endpoints

- `GET /` - Health check
- `POST /upload` - Upload and process documents
- `POST /query` - Query the RAG system
- `GET /documents` - List all processed documents
- `DELETE /documents` - Clear all documents

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── rag_service.py       # RAG logic and vector store management
│   ├── requirements.txt     # Python dependencies
│   ├── chroma_db/          # Vector database storage (created automatically)
│   └── uploads/            # Uploaded files storage (created automatically)
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── main.jsx        # React entry point
│   │   └── index.css       # Global styles
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
└── README.md
```

## Configuration

### Backend Configuration

- **Port**: Default is 8000 (can be changed in `main.py`)
- **Embedding Model**: `all-MiniLM-L6-v2` (can be changed in `rag_service.py`)
- **Chunk Size**: 1000 characters (can be adjusted in `rag_service.py`)
- **Chunk Overlap**: 200 characters (can be adjusted in `rag_service.py`)

### Frontend Configuration

- **Port**: Default is 5173 (can be changed in `vite.config.js`)
- **API URL**: `http://localhost:8000` (can be changed in `src/App.jsx`)

## Troubleshooting

### Backend Issues

1. **Import errors**: Make sure all dependencies are installed and virtual environment is activated
2. **Port already in use**: Change the port in `main.py` or kill the process using port 8000
3. **ChromaDB errors**: Delete the `backend/chroma_db` directory and restart the server

### Frontend Issues

1. **Connection refused**: Make sure the backend server is running on port 8000
2. **CORS errors**: Check that the backend CORS settings include your frontend URL
3. **Build errors**: Delete `node_modules` and `package-lock.json`, then run `npm install` again

## Production Deployment

### Backend

For production, use a production ASGI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend

Build the frontend for production:

```bash
cd frontend
npm run build
```

The built files will be in the `dist` directory, which can be served by any static file server or CDN.

## License

MIT

## Contributing

Feel free to submit issues and enhancement requests!

