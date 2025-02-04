import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/main_page.css'; // Importujemy plik CSS

function MainPage({ setToken }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);

  const [cats, setCats] = useState([]);
  const [adoptedCats, setAdoptedCats] = useState(new Set());
  const [photos, setPhotos] = useState({});
  const [currentPhotoIndex, setCurrentPhotoIndex] = useState({});
  const [currentCatIndex, setCurrentCatIndex] = useState(0);
  const [notification, setNotification] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCatsAndPhotos = async () => {
      try {
        const [catsResponse, adoptedResponse] = await Promise.all([
          axios.get('http://localhost:8000/api/catmatch/cats/'),
          axios.get('http://localhost:8000/api/catmatch/cats-adopted/'),
        ]);

        const allCats = catsResponse.data;
        const adoptedCatIds = new Set(adoptedResponse.data.map(entry => entry.cat));
        const availableCats = allCats.filter(cat => !adoptedCatIds.has(cat.id));

        setCats(availableCats);
        setAdoptedCats(adoptedCatIds);

        const photosData = {};
        const photoIndexData = {};

        await Promise.all(
          availableCats.map(async (cat) => {
            try {
              const photoResponse = await axios.get(
                `http://localhost:8000/api/catmatch/cats-photos/${cat.id}/`
              );
              photosData[cat.id] = photoResponse.data;
              photoIndexData[cat.id] = 0;
            } catch (error) {
              console.error(`Error fetching photos for cat ${cat.id}:`, error);
              photosData[cat.id] = [];
            }
          })
        );

        setPhotos(photosData);
        setCurrentPhotoIndex(photoIndexData);
      } catch (error) {
        console.error("Error fetching cat data:", error);
      }
    };

    fetchCatsAndPhotos();
  }, []);

  const handleNextPhoto = (catId) => {
    if (photos[catId]?.length > 1) {
      setCurrentPhotoIndex((prev) => ({
        ...prev,
        [catId]: (prev[catId] + 1) % photos[catId].length,
      }));
    }
  };

  const handlePreviousPhoto = (catId) => {
    if (photos[catId]?.length > 1) {
      setCurrentPhotoIndex((prev) => ({
        ...prev,
        [catId]: (prev[catId] - 1 + photos[catId].length) % photos[catId].length,
      }));
    }
  };

  const handleAdopt = async (catId) => {
    try {
      const userId = localStorage.getItem('user_id');
      if (!userId || !catId) {
        alert("User or cat ID is missing.");
        return;
      }

      await axios.post("http://localhost:8000/api/catmatch/cats-adopted/", {
        adoption_date: new Date().toISOString().split("T")[0],
        cat: catId,
        user: userId,
      });

      setCats(prevCats => prevCats.filter(cat => cat.id !== catId));
      setAdoptedCats(prevAdopted => new Set([...prevAdopted, catId]));
      setNotification("Cat adopted successfully!");
      setTimeout(() => setNotification(null), 3000);
    } catch (error) {
      console.error("Error adopting cat:", error);
      alert("There was an error adopting the cat. Please try again.");
    }
  };

  const handleSkipCat = () => {
    setCurrentCatIndex((prevIndex) => (prevIndex + 1) % cats.length);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    navigate('/login');
  };

  return (
    <div className="main-container">
      {/* Główny przycisk Menu */}
      <div className="flex justify-end p-4">
        <button onClick={() => setMenuOpen(!menuOpen)} className="menu-button">
          {menuOpen ? "Close Menu" : "Menu"}
        </button>
      </div>

      {/* Dropdown Menu */}
      {menuOpen && (
        <div className="dropdown-menu">
          <button onClick={() => navigate("/add_shelter")}>Add Shelter</button>
          <button onClick={() => navigate("/add_cat")}>Add Cat</button>
          <button onClick={() => navigate("/add_photo_cat")}>Add Photo for Cat</button>
          <button onClick={() => navigate("/profile")}>Profile</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}

      {/* Content Area */}
      <div className="flex-1 p-6">
        {/* Main Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
          {cats.length > 0 && (
            <div key={cats[currentCatIndex].id} className="modal-content">
              <h2>{cats[currentCatIndex].name}</h2>

              {/* Wyświetlanie zdjęcia */}
              {photos[cats[currentCatIndex].id]?.length > 0 ? (
                <div>
                  <img
                    src={photos[cats[currentCatIndex].id][currentPhotoIndex[cats[currentCatIndex].id]]?.photo}
                    alt={`Photo of ${cats[currentCatIndex].name}`}
                    className="cat-photo"
                  />
                  <button onClick={() => handlePreviousPhoto(cats[currentCatIndex].id)}>
                    ◀
                  </button>
                  <button onClick={() => handleNextPhoto(cats[currentCatIndex].id)}>
                    ▶
                  </button>
                </div>
              ) : (
                <p>No photos available</p>
              )}

              {/* Informacje o kocie */}
              <div className="cat-info">
                <p><strong>Age:</strong> {cats[currentCatIndex].age}</p>
                <p><strong>Breed:</strong> {cats[currentCatIndex].breed}</p>
                <p><strong>Gender:</strong> {cats[currentCatIndex].gender}</p>
                <p><strong>Color:</strong> {cats[currentCatIndex].color}</p>
                <p><strong>Notes:</strong> {cats[currentCatIndex].notes}</p>
                <p><strong>Shelter:</strong> {cats[currentCatIndex].shelter}</p>
              </div>

              {/* Przycisk Adopcji */}
              <div className="flex justify-center space-x-4 mt-4">
                <button onClick={() => handleAdopt(cats[currentCatIndex].id)} className="menu-button">
                  ❤️ Adopt
                </button>
                <button onClick={handleSkipCat} className="menu-button">
                  ❌ Skip
                </button>
              </div>
            </div>
          )}
          {cats.length === 0 && <p>No cats available</p>}
          <div className="notification-container">
            {notification && <div className="notification">{notification}</div>}
          </div>
        </div>
      </div>

    </div>
  );
}

export default MainPage;
