/**
 * Application-wide constants and configuration
 */

// ============================================================================
// API CONFIGURATION
// ============================================================================

export const API_CONFIG = {
  // Backend base URL (will be configurable via env variables)
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  
  // Endpoints
  ENDPOINTS: {
    CHAT: '/api/chat',
    UPLOAD: '/api/upload',
    HISTORY: '/api/history',
    HEALTH: '/api/health',
  },
  
  // Timeouts
  TIMEOUT: 30000, // 30 seconds
  UPLOAD_TIMEOUT: 120000, // 2 minutes for file uploads
};

// ============================================================================
// FILE UPLOAD CONFIGURATION
// ============================================================================

export const FILE_CONFIG = {
  // Allowed file types per mode
  ALLOWED_TYPES: {
    document: [
      'application/pdf',
      'text/plain',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ],
    csv: ['text/csv', 'application/vnd.ms-excel'],
  },
  
  // Maximum file sizes (in bytes)
  MAX_SIZE: {
    document: 10 * 1024 * 1024, // 10 MB
    csv: 50 * 1024 * 1024, // 50 MB
  },
  
  // File extensions
  EXTENSIONS: {
    document: ['.pdf', '.txt', '.docx'],
    csv: ['.csv'],
  },
};

// ============================================================================
// UI CONFIGURATION
// ============================================================================

export const UI_CONFIG = {
  // Sidebar width
  SIDEBAR_WIDTH: 280,
  INSIGHT_PANEL_WIDTH: 320,
  
  // Animation durations (ms)
  ANIMATION: {
    MESSAGE_FADE: 300,
    TYPING_INDICATOR: 100,
    PANEL_SLIDE: 200,
  },
  
  // Typing effect
  TYPING_SPEED: 20, // Characters per second
  
  // Chat
  MAX_MESSAGE_LENGTH: 4000,
  MESSAGES_PER_PAGE: 50,
  
  // Auto-scroll threshold
  AUTO_SCROLL_THRESHOLD: 100,
};

// ============================================================================
// DEFAULT VALUES
// ============================================================================

export const DEFAULTS = {
  // Assistant settings
  MODEL_NAME: 'llama2',
  TEMPERATURE: 0.7,
  MAX_TOKENS: 2000,
  
  // UI preferences
  THEME: 'dark' as const,
  SHOW_INSIGHT_PANEL: true,
  SHOW_REASONING_STEPS: true,
  
  // Conversation
  CONVERSATION_TITLE: 'New Conversation',
};

// ============================================================================
// MODE CONFIGURATION
// ============================================================================

export const MODE_CONFIG = {
  chat: {
    title: 'General Chat',
    description: 'Have a conversation with the AI assistant',
    icon: '💬',
    color: 'blue',
    placeholder: 'Ask me anything...',
  },
  document: {
    title: 'Document Q&A',
    description: 'Upload documents and ask questions',
    icon: '📄',
    color: 'indigo',
    placeholder: 'Ask questions about your documents...',
  },
  csv: {
    title: 'CSV Analyzer',
    description: 'Analyze CSV data with natural language',
    icon: '📊',
    color: 'purple',
    placeholder: 'Ask questions about your data...',
  },
  agent: {
    title: 'Agent Tools',
    description: 'AI agent with calculator, date, and more',
    icon: '🤖',
    color: 'green',
    placeholder: 'Use tools: calculate, get date, etc...',
  },
};

// ============================================================================
// STORAGE KEYS
// ============================================================================

export const STORAGE_KEYS = {
  CONVERSATIONS: 'aevorix_conversations',
  CURRENT_CONVERSATION: 'aevorix_current_conversation',
  USER_SETTINGS: 'aevorix_user_settings',
  THEME: 'aevorix_theme',
};

// ============================================================================
// MESSAGES
// ============================================================================

export const MESSAGES = {
  WELCOME: `👋 Welcome to **Aevorix Assistant**!

I'm your intelligent work companion. Here's what I can do:

**💬 General Chat**: Have a conversation on any topic
**📄 Document Q&A**: Upload PDFs/documents and ask questions
**📊 CSV Analysis**: Analyze your data with natural language
**🤖 Agent Tools**: Use calculator, get current date, and more

Choose a mode from the sidebar to get started!`,

  ERROR: {
    GENERIC: 'Something went wrong. Please try again.',
    NETWORK: 'Network error. Please check your connection.',
    FILE_TOO_LARGE: 'File is too large. Please upload a smaller file.',
    FILE_TYPE: 'Invalid file type. Please upload a supported file.',
    UPLOAD_FAILED: 'File upload failed. Please try again.',
  },
  
  SUCCESS: {
    FILE_UPLOADED: 'File uploaded successfully!',
    CONVERSATION_SAVED: 'Conversation saved.',
  },
};

// ============================================================================
// PROMPT TEMPLATES
// ============================================================================

export const PROMPTS = {
  SYSTEM: {
    chat: 'You are Aevorix, a helpful and intelligent AI assistant.',
    document: 'You are a document analysis expert. Answer questions based on the provided context.',
    csv: 'You are a data analyst. Help analyze CSV data and answer questions about it.',
    agent: 'You are an AI agent with access to tools. Use them when needed.',
  },
};
