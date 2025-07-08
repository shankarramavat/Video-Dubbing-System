import { useState } from "react";
import playButton from "../assests/playLogo.png";
import "./Opton.css";
import axios from "axios";
import PropTypes from "prop-types";
import "./global.css";

const OptionCard = (props) => {
  // Function to download a file
  const downloadFile = async (url, fileName, fileType) => {
    try {
      console.log("Downloading from URL:", url);

      const response = await axios.get(url, { responseType: "blob" });

      if (response.status === 200) {
        const blob = new Blob([response.data], { type: fileType });
        const fileUrl = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = fileUrl;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(fileUrl);
        console.log("Download successful:", fileName);
      } else {
        alert(`Failed to download ${fileName}.`);
      }
    } catch (error) {
      console.error(`Error downloading ${fileName}:`, error);
    }
  };

  // Handle download based on the selected option
  const handleDownload = () => {
    console.log(`Downloading ${props.title}`);

    switch (props.title) {
      case "Video to Audio":
        console.log("Downloading audio...");
        downloadFile(
          `http://localhost:5000/audio`,
          "audio.mp3",
          "audio/mpeg"
        );
        break;
      case "Video Subtitles":
        console.log("Downloading English subtitles...");
        downloadFile(
          `http://localhost:5000/subtitle`,
          "English Subtitles.txt",
          "text/plain"
        );
        break;
      case "Translated Subtitles":
        console.log("Downloading translated subtitles...");
        downloadFile(
          `http://localhost:5000/trans_sub`,
          "Translated Subtitles.txt",
          "text/plain"
        );
        break;
      case "Dub a Video":
        console.log("Downloading dubbed video...");
        downloadFile(
          `http://localhost:5000/dub`,
          "dubbed_video.mp4",
          "video/mp4"
        );
        break;
      default:
        alert("Invalid option.");
    }
  };

  return (
    <div className="flex justify-center">
      <div className="boxStyle w-[767px] h-[261px] justify-center relative">
        <img
          className="w-[73px] h-[57px] rounded-[5px] m-5"
          src={playButton}
          alt="Play Button"
        />
        <h1 className="myFont text-xl font-bold cardText p-10">{props.title}</h1>

        <button onClick={handleDownload} className="buttonStyle mt-5">
          Download
        </button>
      </div>
    </div>
  );
};

OptionCard.propTypes = {
  title: PropTypes.string.isRequired,
};

export default OptionCard;
