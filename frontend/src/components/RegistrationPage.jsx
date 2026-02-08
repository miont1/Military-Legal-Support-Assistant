import React, { useState } from 'react';
import { registerUser } from '../services/api';
import { useNavigate } from 'react-router-dom';

const RegistrationPage = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        email: '',
        military_status: 'Мобілізований',
        service_type: 'ЗСУ'
    });
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await registerUser(formData);
            navigate('/chat'); // Redirect to chat after successful registration
        } catch (err) {
            setError('Registration failed. Please try again.');
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <h2>Registration</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    style={{ padding: '8px' }}
                />
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
                    style={{ padding: '8px' }}
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    style={{ padding: '8px' }}
                />

                <label>Status:</label>
                <select name="military_status" value={formData.military_status} onChange={handleChange} style={{ padding: '8px' }}>
                    <option value="Мобілізований">Мобілізований</option>
                    <option value="Контрактник">Контрактник</option>
                    <option value="Строковик">Строковик</option>
                    <option value="Офіцер">Офіцер</option>
                    <option value="Звільнений">Звільнений</option>
                    <option value="Ветеран">Ветеран</option>
                    <option value="Член родини">Член родини</option>
                    <option value="Курсант">Курсант</option>
                </select>

                <label>Service Type:</label>
                <select name="service_type" value={formData.service_type} onChange={handleChange} style={{ padding: '8px' }}>
                    <option value="ЗСУ">ЗСУ</option>
                    <option value="НГУ">НГУ</option>
                    <option value="ТрО">ТрО</option>
                    <option value="ДПСУ">ДПСУ</option>
                    <option value="ССО">ССО</option>
                    <option value="Поліція">Поліція</option>
                    <option value="Нацгвардія">Нацгвардія</option>
                </select>

                <button type="submit" style={{ padding: '10px', backgroundColor: '#0056b3', color: 'white', border: 'none', cursor: 'pointer' }}>Register</button>
            </form>
        </div>
    );
};

export default RegistrationPage;
