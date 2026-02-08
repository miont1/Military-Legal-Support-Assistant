import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { sendMessage, getSessions, getSessionMessages, deleteSession } from '../services/api';
import ReactMarkdown from 'react-markdown';
import { Send, Shield, FileText, AlertCircle, Menu } from 'lucide-react';
import Sidebar from './Sidebar';

const ChatPage = () => {
    const navigate = useNavigate();
    const [sessions, setSessions] = useState([]);
    const [currentSessionId, setCurrentSessionId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(false);


    const [context, setContext] = useState({
        issueCategory: 'Виплати',
        documentStatus: 'Документи відсутні',
        situationStage: 'Ситуація тільки виникла'
    });

    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);


    useEffect(() => {
        loadSessions();
    }, []);

    const loadSessions = async () => {
        const data = await getSessions();
        setSessions(data);
    };

    const loadSession = async (sessionId) => {
        setLoading(true);
        try {
            const msgs = await getSessionMessages(sessionId);
            const formattedMessages = msgs.flatMap(item => [
                { sender: 'user', text: item.query_text },
                { sender: 'ai', text: item.response_text, sources: item.sources || [] }
            ]);
            setMessages(formattedMessages);
            setCurrentSessionId(sessionId);
            setSidebarOpen(false);
        } catch (error) {
            console.error("Failed to load session", error);
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteSession = async (sessionId) => {
        const success = await deleteSession(sessionId);
        if (success) {
            setSessions(sessions.filter(s => s.id !== sessionId));
            if (currentSessionId === sessionId) {
                handleNewChat();
            }
        }
    };

    const handleNewChat = () => {
        setCurrentSessionId(null);
        setMessages([{
            sender: 'ai',
            text: 'Вітаю! Я ваш військовий правовий асистент. \n\nЯ можу допомогти з питаннями щодо:\n- Виплат та грошового забезпечення\n- ВЛК та лікування\n- Звільнення зі служби\n- Відпусток\n\nОпишіть вашу ситуацію, і я знайду відповідні норми законодавства.'
        }]);
        setContext({
            issueCategory: 'Виплати',
            documentStatus: 'Документи відсутні',
            situationStage: 'Ситуація тільки виникла'
        });
        setSidebarOpen(false);
    };

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { sender: 'user', text: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const metadata = {
                issue_category: context.issueCategory,
                document_status: context.documentStatus,
                situation_stage: context.situationStage
            };

            const response = await sendMessage(input, metadata, currentSessionId);

            const aiMessage = {
                sender: 'ai',
                text: response.answer,
                sources: response.sources
            };
            setMessages(prev => [...prev, aiMessage]);


            if (!currentSessionId && response.session_id) {
                setCurrentSessionId(response.session_id);

                await loadSessions();
            }

        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, { sender: 'ai', text: 'Вибачте, сталася помилка при обробці запиту. Спробуйте пізніше.' }]);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        navigate('/');
    };

    const textareaRef = useRef(null);

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
        }
    }, [input]);

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex h-screen bg-slate-900 text-slate-200 font-sans overflow-hidden">


            {sidebarOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-20 lg:hidden"
                    onClick={() => setSidebarOpen(false)}
                />
            )}


            <Sidebar
                isOpen={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
                sessions={sessions}
                currentSessionId={currentSessionId}
                onLoadSession={loadSession}
                onNewChat={handleNewChat}
                onDeleteSession={handleDeleteSession}
                onLogout={handleLogout}
            />


            <div className="flex-1 flex flex-col min-w-0">


                <header className="bg-slate-800 border-b border-slate-700 p-4 flex items-center justify-between shadow-sm">
                    <div className="flex items-center space-x-3">
                        <button onClick={() => setSidebarOpen(true)} className="lg:hidden text-slate-400 hover:text-white">
                            <Menu size={24} />
                        </button>
                        <div>
                            <h1 className="text-lg font-bold text-white">Військовий Правовий Асистент</h1>
                            <p className="text-xs text-slate-400 hidden sm:block">Штучний інтелект на базі законодавства України</p>
                        </div>
                    </div>
                    <div className="flex items-center space-x-2">
                        <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></div>
                        <span className="text-xs text-slate-400">Онлайн</span>
                    </div>
                </header>


                <div className="flex-1 overflow-y-auto p-4 space-y-6 bg-slate-900 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
                    {messages.length === 0 && !currentSessionId && (
                        <div className="flex justify-center items-center h-full text-slate-500">
                            <p>Розпочніть новий чат...</p>
                        </div>
                    )}
                    {messages.map((msg, index) => (
                        <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-[85%] lg:max-w-[75%] rounded-2xl p-4 shadow-md ${msg.sender === 'user'
                                ? 'bg-blue-600 text-white rounded-br-none'
                                : 'bg-slate-800 text-slate-200 rounded-bl-none border border-slate-700'
                                }`}>
                                {msg.sender === 'ai' && (
                                    <div className="flex items-center space-x-2 mb-2 text-blue-400">
                                        <Shield size={16} />
                                        <span className="text-xs font-bold uppercase">Асистент</span>
                                    </div>
                                )}

                                <div className="prose prose-invert prose-sm max-w-none">
                                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                                </div>

                                {msg.sources && msg.sources.length > 0 && (
                                    <div className="mt-4 pt-3 border-t border-slate-700/50">
                                        <div className="flex items-center space-x-2 text-slate-400 mb-2">
                                            <FileText size={14} />
                                            <span className="text-xs font-semibold uppercase">Джерела:</span>
                                        </div>
                                        <ul className="space-y-1">
                                            {msg.sources.map((source, idx) => (
                                                <li key={idx} className="text-xs">
                                                    <a
                                                        href={source.url}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="text-blue-400 hover:text-blue-300 hover:underline flex items-center space-x-1"
                                                    >
                                                        <span>• {source.title}</span>
                                                    </a>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className="flex justify-start">
                            <div className="bg-slate-800 rounded-2xl rounded-bl-none p-4 border border-slate-700 flex items-center space-x-2">
                                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>


                <div className="bg-slate-800 border-t border-slate-700 p-4">
                    <div className="max-w-4xl mx-auto space-y-3">


                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                            <select
                                value={context.issueCategory}
                                onChange={(e) => setContext({ ...context, issueCategory: e.target.value })}
                                className="bg-slate-900 border border-slate-600 text-slate-300 text-xs rounded-lg px-3 py-2 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 outline-none"
                            >
                                {['Виплати', 'ВЛК', 'Звільнення', 'Відпустки', 'СЗЧ/Відповідальність', 'Інше'].map(opt => (
                                    <option key={opt} value={opt}>{opt}</option>
                                ))}
                            </select>

                            <select
                                value={context.documentStatus}
                                onChange={(e) => setContext({ ...context, documentStatus: e.target.value })}
                                className="bg-slate-900 border border-slate-600 text-slate-300 text-xs rounded-lg px-3 py-2 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 outline-none"
                            >
                                {['Є всі документи', 'Документи відсутні', 'Є лише рапорт', 'Є висновок ВЛК'].map(opt => (
                                    <option key={opt} value={opt}>{opt}</option>
                                ))}
                            </select>

                            <select
                                value={context.situationStage}
                                onChange={(e) => setContext({ ...context, situationStage: e.target.value })}
                                className="bg-slate-900 border border-slate-600 text-slate-300 text-xs rounded-lg px-3 py-2 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 outline-none"
                            >
                                {['Ситуація тільки виникла', 'Рапорт подано', 'Отримано відмову', 'Судовий розгляд'].map(opt => (
                                    <option key={opt} value={opt}>{opt}</option>
                                ))}
                            </select>
                        </div>


                        <div className="relative">
                            <textarea
                                ref={textareaRef}
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Опишіть вашу ситуацію детально..."
                                className="w-full bg-slate-900 border border-slate-600 rounded-xl pl-4 pr-12 py-3 text-slate-200 placeholder-slate-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none min-h-[80px] max-h-[300px] overflow-y-auto"
                                rows="1"
                            />
                            <button
                                onClick={handleSend}
                                disabled={!input.trim() || loading}
                                className="absolute right-2 bottom-2 p-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <Send size={18} />
                            </button>
                        </div>
                        <p className="text-[10px] text-slate-500 text-center">
                            <AlertCircle size={10} className="inline mr-1" />
                            Інформація носить довідковий характер і не замінює консультацію адвоката.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatPage;
