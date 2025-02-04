import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/profile.css';

function AddShelter() {
  const [name, setName] = useState('');
  const [street, setStreet] = useState('');
  const [postalCode, setPostalCode] = useState('');
  const [city, setCity] = useState('');
  const [country, setCountry] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const shelterData = {
        name,
        street,
        postal_code: postalCode,
        city,
        country,
        phone_number: phoneNumber,
        email
      };

      await axios.post('http://localhost:8000/api/catmatch/shelters/', shelterData);
      navigate('/main_page');
    } catch (err) {
      setError('Error adding shelter');
    }
  };

  return (
      <div className="profile-container">
        <h2 className="edit-profile-title">Add Shelter</h2>
        <div className="profile-tiles">
          <div className="profile-tile">
            <form onSubmit={handleSubmit}>
              <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Name"
                  required
              />
              <input
                  value={street}
                  onChange={(e) => setStreet(e.target.value)}
                  placeholder="Street"
                  required
              />
              <input
                  value={postalCode}
                  onChange={(e) => setPostalCode(e.target.value)}
                  placeholder="Postal Code"
                  required
              />
              <input
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  placeholder="City"
                  required
              />
              <input
                  value={country}
                  onChange={(e) => setCountry(e.target.value)}
                  placeholder="Country"
                  required
              />
              <input
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  placeholder="Phone Number"
                  required
              />
              <input
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Email"
                  required
              />
              <button type="submit">Submit</button>
            </form>
            {error && <p>{error}</p>}
          </div>
        </div>
        <button onClick={() => navigate('/main_page')} className="back-button">
          Back to Main Page
        </button>
      </div>
  );
}

export default AddShelter;
