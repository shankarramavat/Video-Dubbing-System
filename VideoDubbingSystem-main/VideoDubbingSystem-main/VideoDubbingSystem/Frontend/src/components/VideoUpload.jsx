import React, { useState } from "react";
import "./upload_btn.css"; // Make sure to import your CSS file

function VideoUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState("");

  const languageOptions = [
    { value: "hin", label: "Hindi" },
    { value: "mar", label: "Marathi" },
    { value: "guj", label: "Bangala" },
    { value: "kan", label: "Kannada" },
    { value: "tel", label: "Telugu" },
  ];

  // Handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
  };

  // Handle language selection
  const handleLanguageChange = (e) => {
    console.log("Language selected:", e.target.value);
    setSelectedLanguage(e.target.value);
  };

  // Handle file upload
  const handleUpload = async () => {
    try {
      if (!selectedFile) {
        alert("Please select a video file.");
        return;
      }

      if (!selectedLanguage) {
        alert("Please select a language.");
        return;
      }

      const formData = new FormData();
      formData.append("video", selectedFile);

      const uploadUrl = `http://localhost:5000/upload/${selectedLanguage}`;
      console.log("Uploading to:", uploadUrl);

      const response = await fetch(uploadUrl, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        alert("Video uploaded successfully.");
      } else {
        alert("Failed to upload video.");
      }
    } catch (error) {
      console.error("Error uploading video:", error);
    }
  };

  return (
    <div className="upload-container">
      <select value={selectedLanguage} onChange={handleLanguageChange}>
        <option value=""> Select Language </option>
        {languageOptions.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>

      <br />

      {/* Hidden File Input */}
      <input
        type="file"
        accept="video/*"
        id="file-input"
        onChange={handleFileChange}
        style={{ display: "none" }}
      />

      {/* Button Container for Inline Layout */}
      <div className="button-container">
        <label htmlFor="file-input" className="btn">Choose File</label>
        {selectedFile && <span className="file-name">{selectedFile.name}</span>}
        <button className="btn" onClick={handleUpload}>Upload</button>
      </div>
    </div>
  );
}

export default VideoUpload;
