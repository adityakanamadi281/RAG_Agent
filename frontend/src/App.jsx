import { useState, useRef, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [documents, setDocuments] = useState([])
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)

  useEffect(() => {
    loadDocuments()
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadDocuments = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/documents`)
      setDocuments(response.data)
    } catch (error) {
      console.error('Error loading documents:', error)
    }
  }

  const handleFileUpload = async (event) => {
    const files = Array.from(event.target.files)
    if (files.length === 0) return

    setUploading(true)
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })

    try {
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      alert(response.data.message)
      await loadDocuments()
    } catch (error) {
      alert(`Upload failed: ${error.response?.data?.detail || error.message}`)
    } finally {
      setUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handleClearDocuments = async () => {
    if (!window.confirm('Are you sure you want to clear all documents?')) {
      return
    }

    try {
      await axios.delete(`${API_BASE_URL}/documents`)
      setDocuments([])
      setMessages([])
      alert('All documents cleared successfully')
    } catch (error) {
      alert(`Failed to clear documents: ${error.response?.data?.detail || error.message}`)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setLoading(true)

    try {
      const response = await axios.post(`${API_BASE_URL}/query`, {
        query: userMessage,
        top_k: 5
      })

      const answer = response.data.answer
      const sources = response.data.sources || []

      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: answer,
          sources: sources
        }
      ])
    } catch (error) {
      setMessages(prev => [
        ...prev,
        {
          role: 'error',
          content: `Error: ${error.response?.data?.detail || error.message}`
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-md px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">RAG Agent</h1>
          <div className="flex gap-4 items-center">
            <div className="text-sm text-gray-600">
              {documents.length} document(s) loaded
            </div>
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              multiple
              accept=".pdf,.txt"
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer transition-colors disabled:opacity-50"
            >
              {uploading ? 'Uploading...' : 'Upload Documents'}
            </label>
            {documents.length > 0 && (
              <button
                onClick={handleClearDocuments}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Clear All
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 mt-20">
              <div className="text-6xl mb-4">🤖</div>
              <h2 className="text-2xl font-semibold mb-2">Welcome to RAG Agent</h2>
              <p className="mb-4">Upload documents to get started, then ask questions about them.</p>
              {documents.length === 0 && (
                <p className="text-sm text-gray-400">No documents uploaded yet.</p>
              )}
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-3xl rounded-lg px-4 py-3 ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : message.role === 'error'
                      ? 'bg-red-100 text-red-800 border border-red-300'
                      : 'bg-white text-gray-800 shadow-md'
                  }`}
                >
                  <div className="whitespace-pre-wrap">{message.content}</div>
                  {message.sources && message.sources.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-gray-200">
                      <div className="text-xs font-semibold text-gray-500 mb-1">Sources:</div>
                      <div className="flex flex-wrap gap-2">
                        {message.sources.map((source, i) => (
                          <span
                            key={i}
                            className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded"
                          >
                            {source.split('/').pop()}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-white rounded-lg px-4 py-3 shadow-md">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Form */}
      <div className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="flex gap-4">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about your documents..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
            >
              Send
            </button>
          </form>
          {documents.length === 0 && (
            <p className="text-sm text-gray-500 mt-2 text-center">
              Upload documents to improve query results
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

export default App

