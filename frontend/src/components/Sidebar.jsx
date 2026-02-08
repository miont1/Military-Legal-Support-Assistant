import React, { useState } from 'react';
import { Shield, X, PlusCircle, MessageSquare, LogOut, Trash2, Settings, AlertTriangle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Sidebar = ({
    isOpen,
    onClose,
    sessions,
    currentSessionId,
    onLoadSession,
    onNewChat,
    onDeleteSession,
    onLogout
}) => {
    const navigate = useNavigate();
    const [deleteModalOpen, setDeleteModalOpen] = useState(false);
    const [sessionToDelete, setSessionToDelete] = useState(null);

    const handleDeleteClick = (e, sessionId) => {
        e.stopPropagation();
        setSessionToDelete(sessionId);
        setDeleteModalOpen(true);
    };

    const confirmDelete = () => {
        if (sessionToDelete) {
            onDeleteSession(sessionToDelete);
            setDeleteModalOpen(false);
            setSessionToDelete(null);
        }
    };

    const cancelDelete = () => {
        setDeleteModalOpen(false);
        setSessionToDelete(null);
    };

    return (
        <>
            <div className={`fixed inset-y-0 left-0 z-30 w-64 bg-slate-800 border-r border-slate-700 transform transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0 ${isOpen ? 'translate-x-0' : '-translate-x-full'} flex flex-col`}>
                <div className="p-4 border-b border-slate-700 flex justify-between items-center">
                    <div className="flex items-center space-x-2 text-blue-400 font-bold">
                        <Shield size={24} />
                        <span>LegalSupport</span>
                    </div>
                    <button onClick={onClose} className="lg:hidden text-slate-400">
                        <X size={24} />
                    </button>
                </div>

                <div className="p-4 flex-1">
                    <button
                        onClick={onNewChat}
                        className="w-full flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-500 text-white py-2 px-4 rounded-lg transition-colors mb-6"
                    >
                        <PlusCircle size={18} />
                        <span>Новий чат</span>
                    </button>

                    <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Історія чатів</h3>
                    <div className="space-y-2 overflow-y-auto max-h-[60vh] scrollbar-thin scrollbar-thumb-slate-700">
                        {sessions.map((session) => (
                            <div
                                key={session.id}
                                onClick={() => onLoadSession(session.id)}
                                className={`group flex items-center justify-between p-2 rounded-lg cursor-pointer transition-colors ${currentSessionId === session.id ? 'bg-slate-700 text-white' : 'bg-slate-700/50 text-slate-300 hover:bg-slate-700'
                                    }`}
                            >
                                <div className="flex items-center space-x-3 overflow-hidden">
                                    <MessageSquare size={16} className="text-slate-500 flex-shrink-0" />
                                    <span className="text-sm truncate">{session.title}</span>
                                </div>
                                <button
                                    onClick={(e) => handleDeleteClick(e, session.id)}
                                    className="opacity-0 group-hover:opacity-100 text-slate-500 hover:text-red-400 transition-opacity p-1"
                                    title="Видалити чат"
                                >
                                    <Trash2 size={14} />
                                </button>
                            </div>
                        ))}
                        {sessions.length === 0 && (
                            <div className="text-xs text-slate-500 italic p-2">Історія порожня</div>
                        )}
                    </div>
                </div>

                <div className="p-4 border-t border-slate-700 space-y-2">
                    <button
                        onClick={() => navigate('/profile')}
                        className="w-full flex items-center space-x-2 text-slate-400 hover:text-white hover:bg-slate-700 py-2 px-4 rounded-lg transition-colors"
                    >
                        <Settings size={18} />
                        <span>Налаштування</span>
                    </button>
                    <button
                        onClick={onLogout}
                        className="w-full flex items-center space-x-2 text-slate-400 hover:text-white hover:bg-slate-700 py-2 px-4 rounded-lg transition-colors"
                    >
                        <LogOut size={18} />
                        <span>Вийти</span>
                    </button>
                </div>
            </div>


            {deleteModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
                    <div className="bg-slate-800 border border-slate-700 rounded-xl shadow-2xl max-w-md w-full p-6 transform transition-all scale-100">
                        <div className="flex items-center space-x-3 text-red-500 mb-4">
                            <AlertTriangle size={28} />
                            <h3 className="text-xl font-bold text-white">Видалити чат?</h3>
                        </div>
                        <p className="text-slate-300 mb-6">
                            Ви впевнені, що хочете видалити цей чат? Цю дію неможливо скасувати, і вся історія листування буде втрачена.
                        </p>
                        <div className="flex justify-end space-x-3">
                            <button
                                onClick={cancelDelete}
                                className="px-4 py-2 rounded-lg bg-slate-700 text-white hover:bg-slate-600 transition-colors"
                            >
                                Скасувати
                            </button>
                            <button
                                onClick={confirmDelete}
                                className="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-500 transition-colors flex items-center space-x-2"
                            >
                                <Trash2 size={16} />
                                <span>Видалити</span>
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

export default Sidebar;
