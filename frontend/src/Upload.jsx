import axios from "axios";
import React, { useState } from "react";

function Upload() {
  const [file, setFile] = useState(null);

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file);

    await axios.post("http://34.229.44.212:8000/upload", formData);
    alert("Uploaded");
  };

  return (
    <div className="glass-card">
      <div className="card-header">
        <h2>Document Upload</h2>
        <p>Upload your logistics PDF to get started</p>
      </div>
      <div className="upload-container">
        <div className="file-input-wrapper">
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <div className="custom-file-label">
            {file ? (
              <span className="file-name">📄 {file.name}</span>
            ) : (
              <span>Drag & drop or click to select a PDF</span>
            )}
          </div>
        </div>
        <button onClick={uploadFile} className="btn btn-upload">
          Upload PDF
        </button>
      </div>
    </div>
  );
}

export default Upload;