import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser, loginUser } from '../services/api';

const AuthPage = () => {
    const [isLogin, setIsLogin] = useState(true);
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        email: '',
        military_status: 'Мобілізований',
        service_type: 'ЗСУ'
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (isLogin) {
                const data = await loginUser({ username: formData.username, password: formData.password });
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify({ username: formData.username }));
                navigate('/chat');
            } else {
                await registerUser({
                    username: formData.username,
                    email: formData.email,
                    password: formData.password,
                    military_status: formData.military_status,
                    service_type: formData.service_type
                });

                // Auto login after register
                const data = await loginUser({ username: formData.username, password: formData.password });
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify({ username: formData.username }));
                navigate('/chat');
            }
        } catch (err) {
            console.error(err);
            setError('Помилка: ' + (err.response?.data?.detail || 'Перевірте дані або спробуйте пізніше'));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4 font-sans">
            <div className="bg-slate-800 rounded-2xl shadow-2xl w-full max-w-md overflow-hidden border border-slate-700">
                {/* Header / Tabs */}
                <div className="flex border-b border-slate-700">
                    <button
                        onClick={() => setIsLogin(true)}
                        className={`flex-1 py-4 text-sm font-medium transition-colors ${isLogin
                            ? 'bg-slate-800 text-blue-400 border-b-2 border-blue-400'
                            : 'bg-slate-900/50 text-slate-400 hover:text-slate-200'
                            }`}
                    >
                        Вхід
                    </button>
                    <button
                        onClick={() => setIsLogin(false)}
                        className={`flex-1 py-4 text-sm font-medium transition-colors ${!isLogin
                            ? 'bg-slate-800 text-blue-400 border-b-2 border-blue-400'
                            : 'bg-slate-900/50 text-slate-400 hover:text-slate-200'
                            }`}
                    >
                        Реєстрація
                    </button>
                </div>

                {/* Form */}
                <div className="p-8">
                    <h2 className="text-2xl font-bold text-white mb-2 text-center">
                        {isLogin ? 'З поверненням!' : 'Створити акаунт'}
                    </h2>
                    <p className="text-slate-400 text-center mb-8 text-sm">
                        {isLogin
                            ? 'Військовий правовий асистент'
                            : 'Долучайтесь до системи правової підтримки'}
                    </p>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">
                                Ім'я користувача
                            </label>
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                placeholder="Ваш позивний або ім'я"
                                required
                            />
                        </div>

                        {!isLogin && (
                            <>
                                <div>
                                    <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">
                                        Email
                                    </label>
                                    <input
                                        type="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                        placeholder="email@example.com"
                                    />
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">
                                            Статус
                                        </label>
                                        <select
                                            name="military_status"
                                            value={formData.military_status}
                                            onChange={handleChange}
                                            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        >
                                            {['Мобілізований', 'Контрактник', 'Строковик', 'Офіцер', 'Ветеран', 'Член родини'].map(opt => (
                                                <option key={opt} value={opt}>{opt}</option>
                                            ))}
                                        </select>
                                    </div>
                                    <div>
                                        <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">
                                            Рід військ
                                        </label>
                                        <select
                                            name="service_type"
                                            value={formData.service_type}
                                            onChange={handleChange}
                                            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        >
                                            {['ЗСУ', 'НГУ', 'ТрО', 'ДПСУ', 'ССО', 'Поліція'].map(opt => (
                                                <option key={opt} value={opt}>{opt}</option>
                                            ))}
                                        </select>
                                    </div>
                                </div>
                            </>
                        )}

                        <div>
                            <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">
                                Пароль
                            </label>
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                placeholder="••••••••"
                                required
                            />
                        </div>

                        {error && (
                            <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-sm">
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-4 rounded-lg transition-colors shadow-lg shadow-blue-600/20 disabled:opacity-50 disabled:cursor-not-allowed mt-6"
                        >
                            {loading ? 'Обробка...' : (isLogin ? 'Увійти' : 'Зареєструватися')}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default AuthPage;
