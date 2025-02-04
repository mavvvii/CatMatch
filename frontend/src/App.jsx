import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/login.jsx';
import Register from './components/register.jsx';
import MainPage from './components/main_page.jsx';
import ProfilePage from './components/profile.jsx';
import AddShelter from './components/AddShelter.jsx';
import AddCat from './components/AddCat.jsx';
import AddPhotoCat from './components/AddPhotoCat.jsx'; // Importowanie nowej strony

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    if (savedToken !== token) {
      setToken(savedToken);
    }
  }, []);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={token ? <Navigate to="/main_page" /> : <Login setToken={setToken} />} />
          <Route path="/register" element={token ? <Navigate to="/main_page" /> : <Register />} />
          <Route path="/main_page" element={token ? <MainPage setToken={setToken} /> : <Navigate to="/login" />} />
          <Route path="/profile" element={token ? <ProfilePage setToken={setToken} /> : <Navigate to="/login" />} />
          <Route path="/add_shelter" element={token ? <AddShelter /> : <Navigate to="/login" />} />
          <Route path="/add_cat" element={token ? <AddCat /> : <Navigate to="/login" />} />
          <Route path="/add_photo_cat" element={token ? <AddPhotoCat /> : <Navigate to="/login" />} /> {/* Nowa trasa */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
