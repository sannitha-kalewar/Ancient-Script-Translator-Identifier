import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (event) => {
    setImage(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!image) {
      alert('Please select an image first.');
      return;
    }
    
    const formData = new FormData();
    formData.append('image', image);
    setLoading(true);
    
    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(response.data);
    } catch (error) {
      alert('Error processing image.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto bg-white rounded-xl shadow-md space-y-4 text-center">
      <h1 className="text-xl font-bold">Inscription Translator</h1>
      <input type="file" accept="image/*" onChange={handleImageChange} className="border p-2" />
      <button onClick={handleUpload} className="bg-blue-500 text-white p-2 rounded">{loading ? 'Processing...' : 'Upload & Translate'}</button>
      {result && (
        <div className="mt-4 p-4 border rounded">
          <h2 className="font-semibold">Extracted Text:</h2>
          <p>{result.extracted_text}</p>
          <h2 className="font-semibold">Translated Text:</h2>
          <p>{result.translated_text}</p>
        </div>
      )}
    </div>
  );
};

export default App;
