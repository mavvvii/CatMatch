import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/login.css';

function Login({ setToken }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/users/auth/login/', {
        username,
        password,
      });
      const { token, user_id } = response.data;
      localStorage.setItem('token', token);
      localStorage.setItem('user_id', user_id);
      setToken(token);
      navigate('/main_page');
    } catch (err) {
      setError('Invalid credentials. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-login">
      <div className="bg-white p-8 rounded-3xl shadow-xl w-full max-w-md transform transition duration-500 hover:scale-105">
        {/* GIF przesuwający się w poziomie */}
        <div className="image-container text-center mb-6">
          <img
            src="../../public/jumping-gatito.gif" // ścieżka do GIF-a
            alt="Loading"
            className="image-bouncing"  // Klasa CSS z animacją
          />
        </div>
        <h1 className="text-4xl font-extrabold text-center mb-6">Log in to Your Account</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="username" className="block text-gray-700 font-semibold mb-2">
              Username
            </label>
            <input
              id="username"
              className="w-80 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-4 focus:ring-blue-400 transition duration-300"
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-gray-700 font-semibold mb-2">
              Password
            </label>
            <input
              id="password"
              className="w-50 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-4 focus:ring-blue-400 transition duration-300"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="text-red-500 text-sm text-center">{error}</p>}
          <button type="submit" className="w-70 bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-gradient-to-l hover:from-indigo-600 hover:to-blue-500 transition duration-300 transform hover:scale-105 shadow-md">
            Log In
          </button>
        </form>
        <p className="text-center text-gray-600 mt-6">
          Don’t have an account?{' '}
          <a href="/register" className="text-blue-500 font-medium hover:underline">
            Sign Up
          </a>
        </p>
      </div>
    </div>
  );
}

export default Login;
