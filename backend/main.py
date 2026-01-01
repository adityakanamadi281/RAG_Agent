from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from rag_service import RAGService

load_dotenv()

app = FastAPI(title="RAG Agent API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = RAGService()

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    relevant_docs: List[dict]

@app.get("/")
async def root():
    return {"message": "RAG Agent API is running"}

@app.post("/upload", response_model=dict)
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload and process documents"""
    try:
        uploaded_files = []
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        for file in files:
            content = await file.read()
            file_path = os.path.join(upload_dir, file.filename)
            
            with open(file_path, "wb") as f:
                f.write(content)
            
            uploaded_files.append(file_path)
        
        # Process documents
        await rag_service.add_documents(uploaded_files)
        
        return {
            "message": f"Successfully uploaded {len(uploaded_files)} document(s)",
            "files": [f.filename for f in files]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the RAG system"""
    try:
        result = await rag_service.query(request.query, top_k=request.top_k)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents", response_model=List[str])
async def list_documents():
    """List all processed documents"""
    try:
        return await rag_service.list_documents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents")
async def clear_documents():
    """Clear all documents from the vector store"""
    try:
        await rag_service.clear_documents()
        return {"message": "All documents cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

