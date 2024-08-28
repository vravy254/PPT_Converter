import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const uploadFile = () => {
    if (!file) {
      alert('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    axios.post('https://port5000-workspaces-ws-mz8z4.us10.trial.applicationstudio.cloud.sap/upload', formData, {
      withCredentials: true,
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    })
    .then(response => {
      if (response.status === 200) {
        const fileUrl = `https://port5000-workspaces-ws-mz8z4.us10.trial.applicationstudio.cloud.sap${response.data.file_url}`;
        setMessage(`File uploaded and converted successfully. <a href="${fileUrl}" download>Download the processed file</a>`);
      } else {
        setMessage('Unexpected response from the server.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      if (error.response) {
        setMessage(`Error: ${error.response.data.message}`);
      } else if (error.request) {
        setMessage('No response received from the server.');
      } else {
        setMessage('Error uploading and converting the file.');
      }
    });
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={uploadFile}>Upload and Convert</button>
      <p dangerouslySetInnerHTML={{ __html: message }}></p>
    </div>
  );
}

export default App;
