import { useState, useRef, useEffect } from 'react';
import { Brain, Menu, X, Sparkles, Code, BookOpen, Lightbulb, MessageCircle, Plus, Trash2 } from 'lucide-react';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import TypingIndicator from './components/TypingIndicator';
import { sendMessage } from './services/gemini';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
}

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([
    {
      id: '1',
      title: 'New Chat',
      messages: []
    }
  ]);
  const [currentConversationId, setCurrentConversationId] = useState('1');
  const [isLoading, setIsLoading] = useState(false);
  const [showSidebar, setShowSidebar] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const currentConversation = conversations.find(c => c.id === currentConversationId);
  const messages = currentConversation?.messages || [];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (content: string) => {
    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content
    };
    
    setConversations(prev => prev.map(conv => 
      conv.id === currentConversationId
        ? { 
            ...conv, 
            messages: [...conv.messages, userMessage],
            title: conv.messages.length === 0 ? content.slice(0, 30) + '...' : conv.title
          }
        : conv
    ));
    setIsLoading(true);

    try {
      // Send to AI
      const response = await sendMessage(content);

      // Add AI response
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.error || response.content
      };

      setConversations(prev => prev.map(conv => 
        conv.id === currentConversationId
          ? { ...conv, messages: [...conv.messages, aiMessage] }
          : conv
      ));
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '❌ Sorry, something went wrong. Please try again.'
      };
      setConversations(prev => prev.map(conv => 
        conv.id === currentConversationId
          ? { ...conv, messages: [...conv.messages, errorMessage] }
          : conv
      ));
    } finally {
      setIsLoading(false);
    }
  };

  const createNewChat = () => {
    const newConv: Conversation = {
      id: Date.now().toString(),
      title: 'New Chat',
      messages: []
    };
    setConversations(prev => [newConv, ...prev]);
    setCurrentConversationId(newConv.id);
  };

  const deleteConversation = (id: string) => {
    if (conversations.length === 1) return;
    setConversations(prev => prev.filter(c => c.id !== id));
    if (currentConversationId === id) {
      setCurrentConversationId(conversations[0].id);
    }
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      {/* Sidebar */}
      <div className={`
        fixed md:relative z-50 h-full w-80 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700
        transition-transform duration-300 ease-in-out
        ${showSidebar ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
      `}>
        <div className="flex flex-col h-full">
          {/* Sidebar Header */}
          <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-xl flex items-center justify-center shadow-lg">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-lg font-bold text-gray-900 dark:text-white">
                    Aevorix
                  </h1>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    Your Assistant
                  </p>
                </div>
              </div>
              <button
                onClick={() => setShowSidebar(false)}
                className="md:hidden p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <button
              onClick={createNewChat}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl"
            >
              <Plus className="w-5 h-5" />
              <span className="font-semibold">New Chat</span>
            </button>
          </div>

          {/* Quick Actions */}
          <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <div className="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-3">
              QUICK ACTIONS
            </div>
            <div className="grid grid-cols-2 gap-2">
              <button className="p-3 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors flex flex-col items-center gap-1">
                <Code className="w-5 h-5" />
                <span className="text-xs font-medium">Debug Code</span>
              </button>
              <button className="p-3 bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400 rounded-lg hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-colors flex flex-col items-center gap-1">
                <BookOpen className="w-5 h-5" />
                <span className="text-xs font-medium">Explain</span>
              </button>
              <button className="p-3 bg-pink-50 dark:bg-pink-900/20 text-pink-600 dark:text-pink-400 rounded-lg hover:bg-pink-100 dark:hover:bg-pink-900/30 transition-colors flex flex-col items-center gap-1">
                <Lightbulb className="w-5 h-5" />
                <span className="text-xs font-medium">Brainstorm</span>
              </button>
              <button className="p-3 bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 rounded-lg hover:bg-green-100 dark:hover:bg-green-900/30 transition-colors flex flex-col items-center gap-1">
                <MessageCircle className="w-5 h-5" />
                <span className="text-xs font-medium">Ask Me</span>
              </button>
            </div>
          </div>

          {/* Chat History */}
          <div className="flex-1 overflow-y-auto p-4">
            <div className="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-3">
              RECENT CHATS
            </div>
            <div className="space-y-2">
              {conversations.map((conv) => (
                <div
                  key={conv.id}
                  onClick={() => setCurrentConversationId(conv.id)}
                  className={`
                    group relative p-3 rounded-lg cursor-pointer transition-all
                    ${currentConversationId === conv.id 
                      ? 'bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/30 dark:to-purple-900/30 border border-blue-200 dark:border-blue-700' 
                      : 'hover:bg-gray-100 dark:hover:bg-gray-800'
                    }
                  `}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                        {conv.title}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        {conv.messages.length} messages
                      </p>
                    </div>
                    {conversations.length > 1 && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          deleteConversation(conv.id);
                        }}
                        className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-red-100 dark:hover:bg-red-900/30 text-red-600 dark:text-red-400 rounded transition-opacity"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Footer Info */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <div className="text-xs text-center text-gray-500 dark:text-gray-400">
              Made with care ❤️
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg p-4">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowSidebar(!showSidebar)}
                className="md:hidden p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
              >
                <Menu className="w-5 h-5" />
              </button>
              <div className="flex items-center gap-3">
                <Sparkles className="w-6 h-6 text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600" />
                <div>
                  <h2 className="text-lg font-bold text-gray-900 dark:text-white">
                    {currentConversation?.title || 'New Chat'}
                  </h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Let's talk!
                  </p>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center p-4">
              <div className="text-center max-w-2xl">
                <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-3xl flex items-center justify-center shadow-2xl">
                  <Brain className="w-10 h-10 text-white" />
                </div>
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                  Hey there! 👋
                </h2>
                <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
                  I'm here to help you with whatever you need
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
                  <div className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
                    <Code className="w-6 h-6 text-blue-600 dark:text-blue-400 mb-2" />
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1">Fix Your Code</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Stuck on a bug? Let's solve it together</p>
                  </div>
                  <div className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
                    <BookOpen className="w-6 h-6 text-purple-600 dark:text-purple-400 mb-2" />
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1">Learn Stuff</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">I'll break down complex things into simple words</p>
                  </div>
                  <div className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
                    <Lightbulb className="w-6 h-6 text-pink-600 dark:text-pink-400 mb-2" />
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1">Get Creative</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Need ideas? Let's brainstorm something cool</p>
                  </div>
                  <div className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
                    <MessageCircle className="w-6 h-6 text-green-600 dark:text-green-400 mb-2" />
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1">Just Chat</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Ask me anything, seriously anything</p>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="max-w-4xl mx-auto">
              {messages.map((message) => (
                <ChatMessage
                  key={message.id}
                  role={message.role}
                  content={message.content}
                />
              ))}
              {isLoading && <TypingIndicator />}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input */}
        <ChatInput onSend={handleSend} disabled={isLoading} />
      </div>
    </div>
  );
}

export default App;
