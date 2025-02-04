import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/profile.css';

function AddPhotoCat() {
  const [cats, setCats] = useState([]); // Lista kotów
  const [selectedCat, setSelectedCat] = useState('');
  const [photo, setPhoto] = useState(null); // Wybrane zdjęcie
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  // Pobieranie listy kotów
  useEffect(() => {
    const fetchCats = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/catmatch/cats/');
        setCats(response.data); // Przechowywanie danych o kotach
      } catch (err) {
        setError('Failed to fetch cats');
      }
    };
    fetchCats();
  }, []);

  const handleFileChange = (e) => {
    setPhoto(e.target.files[0]); // Ustawiamy wybrane zdjęcie
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedCat || !photo) {
      setError('Please select a cat and upload a photo');
      return;
    }

    const formData = new FormData();
    formData.append('cat', selectedCat); // Id kota
    formData.append('photo', photo); // Wybrane zdjęcie

    try {
      await axios.post('http://localhost:8000/api/catmatch/cats-photos/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setSuccess('Photo added successfully!');
      navigate('/main_page'); // Przekierowanie po sukcesie
    } catch (err) {
      setError('Error uploading photo');
    }
  };

  return (
      <div className="profile-container">
        <h2 className="edit-profile-title">Add Cat Photo</h2>
        <div className="profile-tiles">
          <div className="profile-tile">
            <form onSubmit={handleSubmit}>
              <select
                  value={selectedCat}
                  onChange={(e) => setSelectedCat(e.target.value)}
                  required
              >
                <option value="">Select a cat</option>
                {cats.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name}
                    </option>
                ))}
              </select>
              <input type="file" onChange={handleFileChange} accept="image/*" required/>
              <button type="submit">Upload Photo</button>
            </form>
            {error && <p style={{color: 'red'}}>{error}</p>}
            {success && <p style={{color: 'green'}}>{success}</p>}
          </div>
        </div>
        <button onClick={() => navigate('/main_page')} className="back-button">
          Back to Main Page
        </button>
      </div>
  );
}

export default AddPhotoCat;
