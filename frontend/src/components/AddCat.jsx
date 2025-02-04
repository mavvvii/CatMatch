import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/profile.css';

function AddCat() {
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [breed, setBreed] = useState('');
  const [gender, setGender] = useState('');
  const [color, setColor] = useState('');
  const [notes, setNotes] = useState('');
  const [shelters, setShelters] = useState([]);
  const [selectedShelter, setSelectedShelter] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchShelters = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/catmatch/shelters/');
        setShelters(response.data);
      } catch (error) {
        console.error('Error fetching shelters:', error);
        setError('Failed to load shelters');
      }
    };

    fetchShelters();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedShelter) {
      setError('Please select a shelter');
      return;
    }

    try {
      await axios.post('http://localhost:8000/api/catmatch/cats/', {
        name,
        age: age ? parseInt(age, 10) : null,
        breed,
        gender,
        color,
        notes,
        shelter: selectedShelter,
      });

      navigate('/main_page');
    } catch (err) {
      console.error(err);
      setError('Error adding cat');
    }
  };

  return (
    <div className="profile-container">
      <h2 className="edit-profile-title">Add a New Cat</h2>

      <div className="profile-tiles">
        <form onSubmit={handleSubmit} className="profile-tile">
          <h3>Cat Details</h3>

          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
          <input value={age} onChange={(e) => setAge(e.target.value)} type="number" placeholder="Age" />
          <input value={breed} onChange={(e) => setBreed(e.target.value)} placeholder="Breed" />

          <select value={gender} onChange={(e) => setGender(e.target.value)} required>
            <option value="">Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>

          <input value={color} onChange={(e) => setColor(e.target.value)} placeholder="Color" />
          <textarea value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Notes"></textarea>

          <select className="dropdown-menu" value={selectedShelter} onChange={(e) => setSelectedShelter(e.target.value)} required>
            <option value="">Select Shelter</option>
            {shelters.map((shelter) => (
              <option key={shelter.id} value={shelter.id}>
                {shelter.name}
              </option>
            ))}
          </select>

          <button type="submit">Add Cat</button>
        </form>

        {error && <p className="error-message">{error}</p>}
      </div>

      <button onClick={() => navigate('/main_page')} className="back-button">
        Back to Main Page
      </button>
    </div>
  );
}

export default AddCat;
