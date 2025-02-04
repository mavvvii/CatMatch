import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/register.css';

function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/users/auth/register/', {
        username,
        password,
        email,
      });
      console.log('Registration successful:', response.data);
      navigate('/login');
    } catch (err) {
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-register">
      <div className="bg-white p-8 rounded-3xl shadow-xl w-full max-w-md transform transition duration-500 hover:scale-105">
        {/* GIF przesuwający się w poziomie */}
        <div className="image-container text-center mb-6">
          <img
            src="../../public/jumping-gatito.gif" // ścieżka do GIF-a
            alt="Loading"
            className="image-bouncing"  // Klasa CSS z animacją
          />
        </div>
        <h1 className="text-4xl font-extrabold text-center mb-6">Register a New Account</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-600">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-50 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-4 focus:ring-blue-400 transition duration-300"
              placeholder="Enter your username"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-50 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-4 focus:ring-blue-400 transition duration-300"
              placeholder="Enter your email"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-50 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-4 focus:ring-blue-400 transition duration-300"
              placeholder="Enter your password"
              required
            />
          </div>
          {error && <p className="text-red-500 text-sm text-center">{error}</p>}
          <button
            type="submit"
            className="w-70 py-3 bg-gradient-to-r from-indigo-600 to-blue-500 text-white rounded-lg font-semibold hover:bg-gradient-to-l hover:from-blue-500 hover:to-indigo-600 transition duration-300"
          >
            Register
          </button>
        </form>
        <p className="text-center text-gray-600 mt-6">
          Already have an account?{' '}
          <a href="/login" className="text-blue-500 font-medium hover:underline">
            Log in
          </a>
        </p>
      </div>
    </div>
  );
}

export default Register;
