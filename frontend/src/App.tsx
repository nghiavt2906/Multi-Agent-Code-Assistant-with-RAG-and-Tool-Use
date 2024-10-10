import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  agentTrace?: any[];
  executionTime?: number;
}

interface AgentStep {
  agent: string;
  input: string;
  output: string;
  tools_used: string[];
  timestamp: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showAgentTrace, setShowAgentTrace] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await axios.post('/api/v1/chat', {
        message: userMessage,
        use_rag: true,
        temperature: 0.7
      });

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.response,
        agentTrace: response.data.agent_trace,
        executionTime: response.data.execution_time
      }]);
    } catch (error: any) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${error.response?.data?.detail || error.message}`
      }]);
    } finally {
      setLoading(false);
    }
  };

  const getAgentIcon = (agentType: string) => {
    const icons: Record<string, string> = {
      planner: '📋',
      coder: '💻',
      reviewer: '🔍',
      debugger: '🐛',
      optimizer: '⚡'
    };
    return icons[agentType] || '🤖';
  };

  const getAgentColor = (agentType: string) => {
    const colors: Record<string, string> = {
      planner: 'bg-blue-100 text-blue-800',
      coder: 'bg-green-100 text-green-800',
      reviewer: 'bg-yellow-100 text-yellow-800',
      debugger: 'bg-red-100 text-red-800',
      optimizer: 'bg-purple-100 text-purple-800'
    };
    return colors[agentType] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-gray-100">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 p-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">🤖 Multi-Agent Code Assistant</h1>
            <p className="text-sm text-gray-400">Powered by GPT-4 & Claude with RAG</p>
          </div>
          <button
            onClick={() => setShowAgentTrace(!showAgentTrace)}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
          >
            {showAgentTrace ? 'Hide' : 'Show'} Agent Trace
          </button>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-6xl mx-auto space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <h2 className="text-3xl font-bold mb-4">Welcome! 👋</h2>
              <p className="text-gray-400 mb-6">Ask me to help you with coding tasks:</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-3xl mx-auto">
                {[
                  'Create a REST API with FastAPI',
                  'Debug a React component that won\'t re-render',
                  'Optimize this database query',
                  'Write unit tests for my function'
                ].map((example, i) => (
                  <button
                    key={i}
                    onClick={() => setInput(example)}
                    className="p-4 bg-gray-800 hover:bg-gray-700 rounded-lg text-left transition-colors"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-3xl ${message.role === 'user' ? 'bg-blue-600' : 'bg-gray-800'} rounded-lg p-4`}>
                {message.role === 'user' ? (
                  <p>{message.content}</p>
                ) : (
                  <div>
                    <div className="message-content prose prose-invert max-w-none">
                      <ReactMarkdown
                        components={{
                          code({ node, inline, className, children, ...props }) {
                            const match = /language-(\w+)/.exec(className || '');
                            return !inline && match ? (
                              <SyntaxHighlighter
                                style={vscDarkPlus as any}
                                language={match[1]}
                                PreTag="div"
                                {...props}
                              >
                                {String(children).replace(/\n$/, '')}
                              </SyntaxHighlighter>
                            ) : (
                              <code className={className} {...props}>
                                {children}
                              </code>
                            );
                          },
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    </div>

                    {/* Agent Trace */}
                    {showAgentTrace && message.agentTrace && message.agentTrace.length > 0 && (
                      <div className="mt-4 pt-4 border-t border-gray-700">
                        <h4 className="text-sm font-semibold mb-2 text-gray-400">Agent Execution Trace:</h4>
                        <div className="space-y-2">
                          {message.agentTrace.map((step: AgentStep, i: number) => (
                            <div key={i} className={`p-2 rounded text-xs ${getAgentColor(step.agent)}`}>
                              <div className="font-semibold">
                                {getAgentIcon(step.agent)} {step.agent.toUpperCase()}
                              </div>
                              {step.tools_used.length > 0 && (
                                <div className="text-xs opacity-75">
                                  Tools: {step.tools_used.join(', ')}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                        {message.executionTime && (
                          <p className="text-xs text-gray-500 mt-2">
                            ⏱️ Execution time: {message.executionTime.toFixed(2)}s
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-800 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                  <span className="text-gray-400">Agents are working...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-gray-700 p-4 bg-gray-800">
        <div className="max-w-6xl mx-auto flex space-x-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask me to help with coding..."
            className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-lg font-semibold transition-colors"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
