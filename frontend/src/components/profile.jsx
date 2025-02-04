import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/profile.css';

function ProfilePage() {
  const navigate = useNavigate();

  // State for user details and error/success messages
  const [userDetails, setUserDetails] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
  });

  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

useEffect(() => {
    const userId = localStorage.getItem('user_id');
    const token = localStorage.getItem('token');

    if (userId && token) {
      axios
        .get(`http://localhost:8000/api/users/update/${userId}/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          const { first_name, last_name, email } = response.data;
          setUserDetails({ first_name, last_name, email, password: '' });
        })
        .catch((error) => {
          console.error("Error fetching user details:", error);
        }); // <-- Make sure this semicolon is here
    }
}, []); // <-- The useEffect now properly closes before the dependency array


  // Handle form submission for updating user details
  const handleFormSubmit = async (e) => {
    e.preventDefault();
    const userId = localStorage.getItem('user_id');
    const token = localStorage.getItem('token');

    if (!userId || !token) {
      setError('User ID or token is missing');
      return;
    }

    try {
      const updatedData = {
        first_name: userDetails.first_name,
        last_name: userDetails.last_name,
        email: userDetails.email,
        password: userDetails.password || undefined,  // Only send password if it's not empty
      };

      // Ensure to send the correct PATCH request with the user_id
      const response = await axios.patch(
        `http://localhost:8000/api/users/update/${userId}/`,
        updatedData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setSuccessMessage('Profile updated successfully!');
      setError('');
    } catch (err) {
      console.error('Error updating user profile:', err);
      if (err.response && err.response.status === 401) {
        setError('Unauthorized: Please log in again.');
      } else if (err.response && err.response.status === 403) {
        setError('Forbidden: You do not have permission to update this user.');
      } else {
        setError('Error updating profile. Please try again.');
      }
    }
  };

  // Handle input changes for the form
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserDetails({
      ...userDetails,
      [name]: value,
    });
  };

  // Handle navigation back to main page
  const handleBack = () => {
    navigate('/main_page');
  };

  return (
    <div className="profile-container">
      <h1 className="edit-profile-title">Edit Profile</h1>

      {/* Success or error messages */}
      {successMessage && <div className="notification">{successMessage}</div>}
      {error && <div className="notification">{error}</div>}

      {/* Form for updating user details */}
      <form onSubmit={handleFormSubmit} className="profile-tiles">
        <div className="profile-tile">
          <label htmlFor="first_name">First Name</label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={userDetails.first_name}
            onChange={handleInputChange}
          />
        </div>
        <div className="profile-tile">
          <label htmlFor="last_name">Last Name</label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={userDetails.last_name}
            onChange={handleInputChange}
          />
        </div>
        <div className="profile-tile">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={userDetails.email}
            onChange={handleInputChange}
          />
        </div>
        <div className="profile-tile">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={userDetails.password}
            onChange={handleInputChange}
          />
        </div>
        <div className="profile-tile">
          <button type="submit">Save Changes</button>
        </div>
      </form>

      {/* Back to main page button */}
      <button className="back-button" onClick={handleBack}>
        Back to Main Page
      </button>
    </div>
  );
}

export default ProfilePage;
