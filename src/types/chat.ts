/**
 * Core type definitions for Aevorix Assistant
 * Defines the data structures used throughout the application
 */

// ============================================================================
// ENUMS
// ============================================================================

/**
 * Assistant modes - determines which capability to use
 */
export enum AssistantMode {
  CHAT = 'chat',           // General conversation
  DOCUMENT = 'document',   // Document Q&A (RAG)
  CSV = 'csv',            // CSV data analysis
  AGENT = 'agent'         // Agent with tools
}

/**
 * Message sender type
 */
export enum MessageRole {
  USER = 'user',
  ASSISTANT = 'assistant',
  SYSTEM = 'system'
}

/**
 * Message status for optimistic UI
 */
export enum MessageStatus {
  SENDING = 'sending',
  SENT = 'sent',
  ERROR = 'error'
}

/**
 * File upload status
 */
export enum UploadStatus {
  IDLE = 'idle',
  UPLOADING = 'uploading',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  ERROR = 'error'
}

// ============================================================================
// CORE INTERFACES
// ============================================================================

/**
 * Message source/citation
 */
export interface MessageSource {
  id: string;
  filename: string;
  page?: number;
  chunk?: number;
  content: string;
  relevanceScore?: number;
}

/**
 * Tool usage information (for agent mode)
 */
export interface ToolUsage {
  toolName: string;
  input: string;
  output: string;
  timestamp: Date;
}

/**
 * Reasoning step (for transparency)
 */
export interface ReasoningStep {
  step: number;
  description: string;
  result?: string;
}

/**
 * Message metadata
 */
export interface MessageMetadata {
  sources?: MessageSource[];
  toolsUsed?: ToolUsage[];
  reasoningSteps?: ReasoningStep[];
  model?: string;
  tokensUsed?: number;
  processingTime?: number;
}

/**
 * Core message structure
 */
export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  status?: MessageStatus;
  metadata?: MessageMetadata;
  mode?: AssistantMode;
}

/**
 * Chat conversation
 */
export interface Conversation {
  id: string;
  title: string;
  mode: AssistantMode;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
  uploadedFiles?: UploadedFile[];
}

/**
 * Uploaded file information
 */
export interface UploadedFile {
  id: string;
  filename: string;
  fileType: string;
  size: number;
  uploadedAt: Date;
  status: UploadStatus;
  mode: AssistantMode;
  processingError?: string;
}

/**
 * User settings
 */
export interface UserSettings {
  theme: 'light' | 'dark';
  modelName: string;
  temperature: number;
  maxTokens: number;
  showInsightPanel: boolean;
  showReasoningSteps: boolean;
}

// ============================================================================
// API REQUEST/RESPONSE TYPES
// ============================================================================

/**
 * Chat request to backend
 */
export interface ChatRequest {
  conversationId: string;
  message: string;
  mode: AssistantMode;
  history?: Message[];
}

/**
 * Chat response from backend
 */
export interface ChatResponse {
  messageId: string;
  content: string;
  metadata?: MessageMetadata;
  conversationId: string;
}

/**
 * File upload request
 */
export interface FileUploadRequest {
  file: File;
  mode: AssistantMode;
  conversationId?: string;
}

/**
 * File upload response
 */
export interface FileUploadResponse {
  fileId: string;
  filename: string;
  status: UploadStatus;
  message: string;
  chunksCreated?: number;
}

/**
 * Error response
 */
export interface ErrorResponse {
  error: string;
  message: string;
  details?: any;
}
