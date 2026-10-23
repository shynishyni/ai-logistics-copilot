import React, { useState, useRef, useEffect } from 'react';
import { Truck, Send, Bot, User, ShieldCheck, Database, Sparkles, Box, Activity } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome-1',
      role: 'assistant',
      content: "Hello! I am your **AI Logistics Copilot**. I can help you calculate rates across carriers (FedEx, UPS, DHL), track shipments, lookup customs regulations, and plan logistics operations.\n\nTry asking:\n* *\"Find the cheapest shipping option from Chennai to Bangalore for a 50kg box.\"*\n* *\"What are the customs filing requirements for exporting software hardware to Germany?\"*"
    }
  ]);
  const [input, setInput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isGenerating]);

  const handleSend = async (textToSend?: string) => {
    const query = textToSend || input;
    if (!query.trim() || isGenerating) return;

    const userMsgId = Date.now().toString();
    const newMessages: Message[] = [
      ...messages,
      { id: userMsgId, role: 'user', content: query }
    ];
    setMessages(newMessages);
    setInput('');
    setIsGenerating(true);

    const assistantMsgId = (Date.now() + 1).toString();
    setMessages(prev => [
      ...prev,
      { id: assistantMsgId, role: 'assistant', content: '' }
    ]);

    try {
      const response = await fetch('/api/v1/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          content: query
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantText = '';

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));
                if (data.event === 'delta' && data.text) {
                  assistantText += data.text;
                  setMessages(prev =>
                    prev.map(msg =>
                      msg.id === assistantMsgId ? { ...msg, content: assistantText } : msg
                    )
                  );
                } else if (data.event === 'done' && data.session_id) {
                  setSessionId(data.session_id);
                }
              } catch (e) {
                // Ignore parse errors for incomplete JSON stream lines
              }
            }
          }
        }
      }
    } catch (err) {
      console.error('Streaming error:', err);
      setMessages(prev =>
        prev.map(msg =>
          msg.id === assistantMsgId
            ? { ...msg, content: msg.content || '⚠️ Connection error. Please ensure FastAPI backend is running on http://localhost:8000.' }
            : msg
        )
      );
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-7xl mx-auto p-4 gap-4">
      {/* Header */}
      <header className="glass-panel p-4 flex items-center justify-between shadow-xl">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-blue to-brand-cyan flex items-center justify-center shadow-glow-blue">
            <Truck className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
              AI Logistics Copilot
            </h1>
            <p className="text-xs text-slate-400">Gemini 2.5 • MCP Server • pgvector RAG • HITL Guardrails</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/30 font-medium">
            v1.0 Streaming Chat
          </span>
          <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-medium flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            System Ready
          </span>
        </div>
      </header>

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 flex-1 min-h-0">
        {/* Chat Main Window */}
        <div className="lg:col-span-3 glass-panel flex flex-col overflow-hidden">
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex gap-3 max-w-[85%] animate-fade-in ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}>
                <div className={`w-9 h-9 rounded-full flex items-center justify-center shrink-0 font-semibold text-xs text-white ${
                  msg.role === 'user' 
                    ? 'bg-gradient-to-br from-purple-600 to-indigo-600' 
                    : 'bg-gradient-to-br from-blue-600 to-cyan-600'
                }`}>
                  {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>
                <div className={msg.role === 'user' ? 'bubble-user' : 'bubble-assistant'}>
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                </div>
              </div>
            ))}
            {isGenerating && messages[messages.length - 1]?.content === '' && (
              <div className="flex gap-3 max-w-[85%] animate-fade-in">
                <div className="w-9 h-9 rounded-full bg-gradient-to-br from-blue-600 to-cyan-600 flex items-center justify-center shrink-0">
                  <Bot className="w-4 h-4 text-white" />
                </div>
                <div className="bubble-assistant text-slate-400 flex items-center gap-2">
                  <Sparkles className="w-4 h-4 animate-spin text-brand-cyan" />
                  Generating logistics response...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 border-t border-white/10 bg-slate-950/60 flex gap-3 items-center">
            <input
              type="text"
              className="flex-1 bg-slate-900/90 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-400 focus:outline-none focus:border-brand-blue focus:ring-2 focus:ring-brand-blue/25 transition-all"
              placeholder="Ask about shipment rates, tracking, or customs regulations..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              disabled={isGenerating}
            />
            <button className="btn-primary" onClick={() => handleSend()} disabled={isGenerating || !input.trim()}>
              <Send className="w-4 h-4" /> Send
            </button>
          </div>
        </div>

        {/* Sidebar Status Panel */}
        <div className="glass-panel p-5 flex flex-col gap-5 hidden lg:flex">
          <div>
            <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
              <Activity className="w-4 h-4 text-brand-blue" /> Active Workflow State
            </h2>
            <div className="glass-card space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Session ID</span>
                <span className="font-mono text-slate-200">{sessionId ? sessionId.slice(0, 8) + '...' : 'New Session'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Origin</span>
                <span className="text-slate-200">Pending</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Destination</span>
                <span className="text-slate-200">Pending</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Workflow Status</span>
                <span className="text-brand-blue font-medium">Conversational</span>
              </div>
            </div>
          </div>

          <div>
            <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
              <Box className="w-4 h-4 text-brand-purple" /> Sample Logistics Queries
            </h2>
            <div className="space-y-2">
              <button
                className="btn-secondary w-full"
                onClick={() => handleSend("Compare FedEx, UPS, and DHL rates for shipping 50kg from Chennai to Bangalore.")}
              >
                🚚 Rate Comparison (Chennai &rarr; Bangalore)
              </button>
              <button
                className="btn-secondary w-full"
                onClick={() => handleSend("What are the required customs documents for shipping electrical components internationally?")}
              >
                📋 Customs Policy Lookup
              </button>
            </div>
          </div>

          <div className="mt-auto pt-4 border-t border-white/10 text-xs text-slate-400 space-y-1.5">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" /> Human-in-the-Loop Active
            </div>
            <div className="flex items-center gap-2">
              <Database className="w-4 h-4 text-blue-400" /> PostgreSQL + pgvector Enabled
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
