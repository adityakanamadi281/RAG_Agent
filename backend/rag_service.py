import os
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from typing import List, Dict, Optional
import asyncio
import google.generativeai as genai

class RAGService:
    def __init__(self):
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB (persistent client)
        chroma_dir = "chroma_db"
        os.makedirs(chroma_dir, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents"
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Initialize Gemini client (optional, can use local LLM)
        self.gemini_model = None
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
    
    def _load_document(self, file_path: str) -> str:
        """Load document content based on file type"""
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            return "\n".join([doc.page_content for doc in documents])
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
            documents = loader.load()
            return documents[0].page_content
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
    
    async def add_documents(self, file_paths: List[str]):
        """Process and add documents to vector store"""
        all_texts = []
        all_metadatas = []
        all_ids = []
        
        for file_path in file_paths:
            try:
                # Load document
                text = self._load_document(file_path)
                
                # Split into chunks
                chunks = self.text_splitter.split_text(text)
                
                # Add chunks with metadata
                for i, chunk in enumerate(chunks):
                    doc_id = f"{os.path.basename(file_path)}_{i}"
                    all_texts.append(chunk)
                    all_metadatas.append({"source": file_path})
                    all_ids.append(doc_id)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        if all_texts:
            # Generate embeddings
            embeddings = self.embedding_model.encode(all_texts).tolist()
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=all_texts,
                metadatas=all_metadatas,
                ids=all_ids
            )
            
            # ChromaDB persistent client auto-saves, no need to call persist()
    
    async def query(self, query: str, top_k: int = 5) -> Dict:
        """Query the RAG system"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search similar documents
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Extract relevant documents
        relevant_docs = []
        sources = []
        
        if results['documents'] and len(results['documents'][0]) > 0:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                relevant_docs.append({
                    "content": doc,
                    "source": metadata.get("source", "Unknown"),
                    "score": 1 - results['distances'][0][i] if results['distances'] else 0
                })
                if metadata.get("source") not in sources:
                    sources.append(metadata.get("source"))
        
        # Generate answer using LLM
        context = "\n\n".join([doc["content"] for doc in relevant_docs])
        answer = await self._generate_answer(query, context)
        
        return {
            "answer": answer,
            "sources": sources,
            "relevant_docs": relevant_docs
        }
    
    async def _generate_answer(self, query: str, context: str) -> str:
        """Generate answer using LLM"""
        prompt = f"""You are a helpful assistant that answers questions based on provided context.

Context:
{context}

Question: {query}

Based on the context above, provide a clear and concise answer. If the answer is not in the context, say so."""
        
        if self.gemini_model:
            try:
                response = await asyncio.to_thread(
                    self.gemini_model.generate_content,
                    prompt
                )
                return response.text
            except Exception as e:
                print(f"Gemini API error: {e}")
                # Fallback to simple extraction
                return self._simple_answer(query, context)
        else:
            # Fallback: return most relevant chunk
            return self._simple_answer(query, context)
    
    def _simple_answer(self, query: str, context: str) -> str:
        """Simple answer extraction when LLM is not available"""
        if not context:
            return "No relevant documents found. Please upload documents first."
        
        # Return first chunk as answer (simple fallback)
        chunks = context.split("\n\n")
        return chunks[0] if chunks else "Unable to generate answer."
    
    async def list_documents(self) -> List[str]:
        """List all unique document sources"""
        results = self.collection.get()
        sources = set()
        if results['metadatas']:
            for metadata in results['metadatas']:
                if metadata.get('source'):
                    # Return just the filename for cleaner display
                    source_path = metadata['source']
                    filename = os.path.basename(source_path)
                    sources.add(filename)
        return list(sources)
    
    async def clear_documents(self):
        """Clear all documents from the vector store"""
        self.chroma_client.delete_collection(name="documents")
        self.collection = self.chroma_client.create_collection(
            name="documents"
        )

