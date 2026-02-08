import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUserProfile, updateUserProfile, changePassword } from '../services/api';
import { ArrowLeft, Save, Lock, User, Shield } from 'lucide-react';

const ProfilePage = () => {
    const navigate = useNavigate();
    const [profile, setProfile] = useState({
        username: '',
        email: '',
        military_status: '',
        service_type: ''
    });
    const [passwords, setPasswords] = useState({
        old_password: '',
        new_password: '',
        confirm_password: ''
    });
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState({ type: '', text: '' });

    useEffect(() => {
        const loadProfile = async () => {
            try {
                const data = await getUserProfile();
                setProfile(data);
            } catch (error) {
                setMessage({ type: 'error', text: 'Не вдалося завантажити профіль' });
            } finally {
                setLoading(false);
            }
        };
        loadProfile();
    }, []);

    const handleProfileUpdate = async (e) => {
        e.preventDefault();
        setMessage({ type: '', text: '' });
        try {
            await updateUserProfile(profile);
            setMessage({ type: 'success', text: 'Профіль оновлено успішно' });
        } catch (error) {
            setMessage({ type: 'error', text: 'Помилка оновлення профілю' });
        }
    };

    const handlePasswordChange = async (e) => {
        e.preventDefault();
        setMessage({ type: '', text: '' });

        if (passwords.new_password !== passwords.confirm_password) {
            setMessage({ type: 'error', text: 'Нові паролі не співпадають' });
            return;
        }

        try {
            await changePassword({
                old_password: passwords.old_password,
                new_password: passwords.new_password
            });
            setMessage({ type: 'success', text: 'Пароль змінено успішно' });
            setPasswords({ old_password: '', new_password: '', confirm_password: '' });
        } catch (error) {
            setMessage({ type: 'error', text: 'Помилка зміни паролю. Перевірте старий пароль.' });
        }
    };

    if (loading) return <div className="min-h-screen bg-slate-900 flex items-center justify-center text-white">Завантаження...</div>;

    return (
        <div className="min-h-screen bg-slate-900 text-slate-200 font-sans p-4 md:p-8">
            <div className="max-w-4xl mx-auto">
                <button
                    onClick={() => navigate('/chat')}
                    className="flex items-center space-x-2 text-slate-400 hover:text-white mb-6 transition-colors"
                >
                    <ArrowLeft size={20} />
                    <span>Назад до чату</span>
                </button>

                <h1 className="text-3xl font-bold text-white mb-8 flex items-center gap-3">
                    <User size={32} className="text-blue-500" />
                    Налаштування профілю
                </h1>

                {message.text && (
                    <div className={`p-4 rounded-lg mb-6 ${message.type === 'error' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-green-500/10 text-green-400 border border-green-500/20'}`}>
                        {message.text}
                    </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

                    <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 shadow-xl">
                        <div className="flex items-center gap-2 mb-6 text-blue-400">
                            <Shield size={24} />
                            <h2 className="text-xl font-bold">Особиста інформація</h2>
                        </div>

                        <form onSubmit={handleProfileUpdate} className="space-y-4">
                            <div>
                                <label className="block text-xs font-medium text-slate-400 mb-1 uppercase">Ім'я користувача</label>
                                <input
                                    type="text"
                                    value={profile.username}
                                    onChange={e => setProfile({ ...profile, username: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 outline-none"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-slate-400 mb-1 uppercase">Email</label>
                                <input
                                    type="email"
                                    value={profile.email}
                                    onChange={e => setProfile({ ...profile, email: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 outline-none"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-slate-400 mb-1 uppercase">Військовий статус</label>
                                <select
                                    value={profile.military_status}
                                    onChange={e => setProfile({ ...profile, military_status: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 outline-none"
                                >
                                    {['Мобілізований', 'Контрактник', 'Строковик', 'Офіцер', 'Ветеран', 'Член родини', 'Курсант'].map(opt => (
                                        <option key={opt} value={opt}>{opt}</option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-slate-400 mb-1 uppercase">Рід військ</label>
                                <select
                                    value={profile.service_type}
                                    onChange={e => setProfile({ ...profile, service_type: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 outline-none"
                                >
                                    {['ЗСУ', 'НГУ', 'ТрО', 'ДПСУ', 'ССО', 'Поліція', 'Нацгвардія'].map(opt => (
                                        <option key={opt} value={opt}>{opt}</option>
                                    ))}
                                </select>
                            </div>
                            <button type="submit" className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center gap-2 mt-4">
                                <Save size={18} />
                                Зберегти зміни
                            </button>
                        </form>
                    </div>


                    <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 shadow-xl h-fit">
                        <div className="flex items-center gap-2 mb-6 text-blue-400">
                            <Lock size={24} />
                            <h2 className="text-xl font-bold">Безпека</h2>
                        </div>

                        <form onSubmit={handlePasswordChange} className="space-y-4">
                            <div>
                                <label className="block text-xs font-medium text-slate-400 mb-1 uppercase">Старий пароль</label>
                                <input
                                    type="password"
                                    value={passwords.old_password}
                                    onChange={e => setPasswords({ ...passwords, old_password: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 outline-none"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-slate-400 mb-1 uppercase">Новий пароль</label>
                                <input
                                    type="password"
                                    value={passwords.new_password}
                                    onChange={e => setPasswords({ ...passwords, new_password: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 outline-none"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-slate-400 mb-1 uppercase">Підтвердження паролю</label>
                                <input
                                    type="password"
                                    value={passwords.confirm_password}
                                    onChange={e => setPasswords({ ...passwords, confirm_password: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 outline-none"
                                />
                            </div>
                            <button type="submit" className="w-full bg-slate-700 hover:bg-slate-600 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center gap-2 mt-4">
                                <Lock size={18} />
                                Змінити пароль
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;
