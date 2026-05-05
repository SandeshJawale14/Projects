# 🏗️ Aevorix Assistant - System Architecture

## 📋 Overview

Aevorix Assistant is a production-grade AI assistant that provides multiple intelligent capabilities:
- Document-based Q&A using RAG (Retrieval Augmented Generation)
- CSV data analysis with natural language
- Autonomous agent system with tools
- Conversation memory and context management

---

## 🎯 Design Principles

1. **Modularity**: Each capability is a separate, testable module
2. **Scalability**: Clean separation between frontend and backend
3. **User Experience**: ChatGPT-like interface, not a prototype
4. **Intelligence**: Smart routing based on user intent
5. **Production-Ready**: Error handling, loading states, proper state management

---

## 🏛️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Sidebar    │  │  Chat Area   │  │ Insight Panel│      │
│  │              │  │              │  │              │      │
│  │ • File Upload│  │ • Messages   │  │ • Sources    │      │
│  │ • History    │  │ • Input      │  │ • Tools Used │      │
│  │ • Mode Switch│  │ • Typing Anim│  │ • Reasoning  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕ REST API
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Query Router (Intent Detection)          │   │
│  └──────────────────────────────────────────────────────┘   │
│           │              │              │            │       │
│    ┌──────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐ ┌────▼────┐ │
│    │ RAG Engine │ │CSV Analyzer│ │   Agent   │ │Direct LLM│ │
│    └────────────┘ └───────────┘ └───────────┘ └─────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Shared Components                        │   │
│  │  • LLM Wrapper (Ollama)                              │   │
│  │  • Vector Store (Chroma/FAISS)                       │   │
│  │  • Memory Manager                                    │   │
│  │  • Document Processor                                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Frontend Architecture

### Component Hierarchy

```
App
├── Layout
│   ├── Sidebar
│   │   ├── ModeSelector
│   │   ├── FileUploader
│   │   ├── ChatHistoryList
│   │   └── SettingsPanel
│   ├── MainChatArea
│   │   ├── MessageList
│   │   │   ├── UserMessage
│   │   │   ├── AIMessage
│   │   │   └── TypingIndicator
│   │   └── ChatInput
│   └── InsightPanel (collapsible)
│       ├── SourcesDisplay
│       ├── ToolUsageLog
│       └── ReasoningSteps
├── Providers
│   ├── ChatProvider (state management)
│   ├── ThemeProvider
│   └── APIProvider
└── Services
    ├── apiService (backend communication)
    ├── fileService (upload handling)
    └── storageService (local persistence)
```

### State Management Strategy

- **React Context**: Global state (chat history, current mode, user settings)
- **Local State**: Component-specific UI state
- **Custom Hooks**: Reusable logic (useChat, useFileUpload, useTypingEffect)

### Key Features

1. **Responsive Design**: Mobile-first, works on all devices
2. **Real-time Updates**: WebSocket support (future phase)
3. **Optimistic UI**: Immediate feedback, update on response
4. **Error Boundaries**: Graceful error handling
5. **Accessibility**: ARIA labels, keyboard navigation

---

## ⚙️ Backend Architecture (FastAPI)

### Directory Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Configuration management
│   ├── core/
│   │   ├── llm.py             # LLM wrapper (Ollama)
│   │   ├── embeddings.py      # Embedding generation
│   │   ├── vectorstore.py     # Vector database operations
│   │   └── memory.py          # Conversation memory
│   ├── routers/
│   │   ├── chat.py            # Chat endpoints
│   │   ├── upload.py          # File upload
│   │   ├── history.py         # Chat history
│   │   └── health.py          # Health checks
│   ├── services/
│   │   ├── query_router.py    # Intent detection & routing
│   │   ├── rag_service.py     # RAG pipeline
│   │   ├── csv_service.py     # CSV analysis
│   │   ├── agent_service.py   # Agent system
│   │   └── direct_llm.py      # Simple LLM calls
│   ├── ingestion/
│   │   ├── pdf_processor.py   # PDF text extraction
│   │   ├── text_processor.py  # Text chunking
│   │   └── csv_processor.py   # CSV parsing
│   ├── agents/
│   │   ├── tools.py           # Agent tools
│   │   ├── executor.py        # Agent execution
│   │   └── prompts.py         # Agent prompts
│   ├── models/
│   │   ├── chat.py            # Pydantic models
│   │   └── document.py        # Document models
│   └── utils/
│       ├── logger.py          # Logging setup
│       └── exceptions.py      # Custom exceptions
├── tests/
├── requirements.txt
└── README.md
```

### Core Components

#### 1. Query Router
```
User Query → Intent Detection → Route to:
  - RAG: "What does the document say about..."
  - CSV: "Show me rows where..."
  - Agent: "Calculate...", "What's the date?"
  - Direct: General conversation
```

#### 2. RAG Engine
- Document chunking (recursive text splitter)
- Embedding generation (sentence-transformers)
- Vector similarity search
- Context retrieval + LLM generation
- Source citation

#### 3. CSV Analyzer
- Pandas DataFrame operations
- Natural language to SQL/Pandas
- Data visualization suggestions
- Summary statistics

#### 4. Agent System
Tools:
- Calculator: Math operations
- DateTime: Current date/time
- WebSearch: External API calls (future)
- CodeExecutor: Safe Python execution (sandboxed)

#### 5. Memory Manager
- Conversation history buffer
- Summary memory for long conversations
- Entity extraction and tracking

---

## 🔄 Data Flow

### Example: Document Q&A Flow

```
1. User uploads PDF
   Frontend → POST /api/upload → Backend processes & stores

2. User asks question
   Frontend → POST /api/chat
   
3. Backend processing:
   a. Query Router detects "document question" intent
   b. Routes to RAG Service
   c. RAG Service:
      - Converts query to embedding
      - Searches vector store
      - Retrieves top-k relevant chunks
      - Constructs prompt with context
      - Calls LLM (Ollama)
      - Returns response + sources
   
4. Frontend displays:
   - AI message in chat
   - Sources in insight panel
   - Updates chat history
```

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Custom (with Headless UI for accessibility)
- **State**: React Context + Custom Hooks
- **HTTP Client**: Axios
- **Animations**: Framer Motion

### Backend
- **Framework**: FastAPI
- **LLM**: Ollama (local inference)
- **Embeddings**: sentence-transformers
- **Vector DB**: ChromaDB (easy setup) or FAISS
- **CSV**: Pandas
- **PDF**: PyPDF2 / pdfplumber
- **Validation**: Pydantic

### Development
- **Code Quality**: ESLint, Prettier (frontend)
- **Type Safety**: TypeScript, Pydantic
- **Testing**: Vitest (frontend), Pytest (backend)

---

## 🚀 Deployment Strategy

### Development
- Frontend: `npm run dev` (Vite dev server)
- Backend: `uvicorn app.main:app --reload`

### Production (Future)
- Frontend: Static hosting (Vercel, Netlify)
- Backend: Docker container (FastAPI + Ollama)
- Reverse proxy: Nginx
- Database: PostgreSQL (for chat history persistence)

---

## 🎯 Key Differentiators from Basic Q&A Chatbot

| Feature | Basic Chatbot | Aevorix Assistant |
|---------|---------------|-------------------|
| UI | Simple Streamlit forms | ChatGPT-like interface |
| Capabilities | Only Q&A | Q&A + CSV + Agents + Memory |
| Architecture | Monolithic script | Modular FastAPI backend |
| Routing | None | Intelligent intent detection |
| Sources | Text output | Visual panel with citations |
| Memory | None | Conversation context tracking |
| Code Quality | Prototype | Production-ready |
| Error Handling | Basic | Comprehensive |
| Extensibility | Hard to extend | Plugin-based architecture |

---

## 📦 Project Structure (Frontend - Current Phase)

```
aevorix-assistant/
├── public/
│   └── images/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Layout.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── MainChatArea.tsx
│   │   │   └── InsightPanel.tsx
│   │   ├── chat/
│   │   │   ├── MessageList.tsx
│   │   │   ├── Message.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── TypingIndicator.tsx
│   │   ├── sidebar/
│   │   │   ├── ModeSelector.tsx
│   │   │   ├── FileUploader.tsx
│   │   │   └── ChatHistory.tsx
│   │   ├── insight/
│   │   │   ├── SourcesDisplay.tsx
│   │   │   ├── ToolUsage.tsx
│   │   │   └── ReasoningSteps.tsx
│   │   └── common/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       └── Card.tsx
│   ├── context/
│   │   ├── ChatContext.tsx
│   │   └── ThemeContext.tsx
│   ├── hooks/
│   │   ├── useChat.ts
│   │   ├── useFileUpload.ts
│   │   └── useTypingEffect.ts
│   ├── services/
│   │   ├── api.ts
│   │   └── storage.ts
│   ├── types/
│   │   ├── chat.ts
│   │   ├── message.ts
│   │   └── mode.ts
│   ├── utils/
│   │   ├── formatters.ts
│   │   └── validators.ts
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── package.json
├── tailwind.config.js
└── tsconfig.json
```

---

## 🎨 UI/UX Design Specifications

### Color Scheme
- Primary: Indigo/Blue (AI, technology)
- Secondary: Purple (intelligence, creativity)
- Accent: Green (success, sources found)
- Background: Dark mode primary, Light mode option
- Text: High contrast for accessibility

### Layout
```
┌─────────────────────────────────────────────────────┐
│  Aevorix Assistant                    🌙 Settings   │
├──────────┬──────────────────────────────┬───────────┤
│          │                               │           │
│ SIDEBAR  │      CHAT AREA               │ INSIGHTS  │
│ (280px)  │      (flex-grow)             │ (320px)   │
│          │                               │           │
│ Modes:   │  ┌─────────────────────┐     │ Sources:  │
│ • Chat   │  │ AI: Hello! I'm...  │     │ • doc.pdf │
│ • Docs   │  └─────────────────────┘     │   p.12    │
│ • CSV    │                               │           │
│ • Agent  │  ┌──────────────────┐        │ Tools:    │
│          │  │ User: Analyze... │        │ ✓ Calc    │
│ Upload:  │  └──────────────────┘        │           │
│ [Drop]   │                               │ Steps:    │
│          │  ┌─────────────────────┐     │ 1. Parse  │
│ History: │  │ AI: Here's the...  │     │ 2. Search │
│ • Chat 1 │  └─────────────────────┘     │ 3. Answer │
│ • Chat 2 │                               │           │
│          │  ┌──────────────────────┐    │           │
│          │  │ Type a message...    │    │           │
│          │  └──────────────────────┘    │           │
└──────────┴──────────────────────────────┴───────────┘
```

### Animations
- Message fade-in
- Typing dots animation
- Smooth scrolling
- Panel slide transitions
- File upload progress

---

## 🔐 Security Considerations

1. **File Upload**: Validate file types, size limits, sanitize filenames
2. **API Security**: CORS configuration, rate limiting
3. **Code Execution**: Sandboxed environment for agent tools
4. **Data Privacy**: Local storage, no external data leaks
5. **Input Sanitization**: Prevent injection attacks

---

## 📊 Performance Optimization

1. **Frontend**:
   - Lazy loading components
   - Virtual scrolling for long chat history
   - Debounced search
   - Optimistic UI updates

2. **Backend**:
   - Async operations
   - Caching (embeddings, vector searches)
   - Connection pooling
   - Batch processing

---

## 🧪 Testing Strategy

### Frontend
- Unit: Components, hooks, utilities
- Integration: User flows
- E2E: Critical paths

### Backend
- Unit: Individual services
- Integration: API endpoints
- Load: Concurrent users

---

## 📈 Future Enhancements (Post-MVP)

1. **Real-time Collaboration**: Multiple users, shared chats
2. **Voice Input/Output**: Speech-to-text, TTS
3. **Multi-modal**: Image understanding, chart generation
4. **Plugins**: External API integrations
5. **Fine-tuning**: Custom model training
6. **Analytics**: Usage tracking, insights

---

## ✅ Success Metrics

- Response time < 2s for simple queries
- Retrieval accuracy > 85%
- User satisfaction score > 4/5
- Zero security vulnerabilities
- 90%+ test coverage

---

## 🎓 Learning Outcomes

By building this, you'll master:
- Production React architecture
- FastAPI best practices
- RAG implementation
- Agent systems
- LLM integration
- Full-stack development

---

**Next Phase**: We'll implement the RAG system with document processing and vector search.
