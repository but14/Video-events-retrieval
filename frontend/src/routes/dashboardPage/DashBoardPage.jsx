import "./dashboardPage.css";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

const DashboardPage = () => {
  const [videoSrc, setVideoSrc] = useState(null);
  const [youtubeURL, setYoutubeURL] = useState("");
  const [showForm, setShowForm] = useState(false);

  const location = useLocation();

  //Lay video tu query parameter
  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const videoParam = queryParams.get("video"); //Lay video tu query parameter
    if (videoParam) {
      if (videoParam.includes("youtube.com")) {
        const videoId = videoParam.split("v=")[1]?.split("&")[0];
        if (videoId) {
          setVideoSrc(`https://www.youtube.com/embed/${videoId}`);
        }
      } else {
        setVideoSrc(videoParam); //Neu khoing phai youtube, lay video tu link
      }
    }
  }, [location]);

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const videoURL = URL.createObjectURL(file);
      setVideoSrc(videoURL);
    }
  };

  const handleYoutubeSubmit = (e) => {
    e.preventDefault();
    const videoId = youtubeURL.split("v=")[1]?.split("&")[0];
    if (videoId) {
      setVideoSrc(`https://www.youtube.com/embed/${videoId}`);
    }
  };

  return (
    <div className="dashboardPage">
      {/* <div className="texts">
        <div className="logo">
          <img src="/logo.png" alt="" />
          <h1>VIRE SYSTEM</h1>
        </div>
      </div>
  
      <div className="formContainer">
        <form>
          <input type="text" name="text" placeholder="Ask me anything..." />
          <button>
            <img src="/arrow.png" alt="" />
          </button>
        </form>
      </div>  */}
      <button
        className="uploadBtn"
        onClick={() => document.getElementById("videoUpload").click()}
      >
        Upload from your computer
      </button>
      <input
        id="videoUpload"
        type="file"
        accept="video/*"
        style={{ display: "none" }}
        onChange={handleUpload}
      />

      <button onClick={() => setShowForm(!showForm)} className="uploadBtn">
        Upload from URL
      </button>
      <div className={`youtubeFormContainer ${showForm ? "show" : ""}`}>
        <form onSubmit={handleYoutubeSubmit} className="youtubeForm">
          <input
            type="text"
            placeholder="Enter YouTube URL"
            value={youtubeURL}
            onChange={(e) => setYoutubeURL(e.target.value)}
          />
          <button type="submit" className="uploadBtn">
            Submit
          </button>
        </form>
      </div>
      <div className="content">
        <div className="videoscreen">
          {videoSrc ? (
            videoSrc.includes("youtube.com") ? (
              <iframe
                src={videoSrc}
                title="YouTube Video"
                width="100%"
                height="100%"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
            ) : (
              <video src={videoSrc} controls width="100%" height="100%" />
            )
          ) : (
            "VIDEO UPLOAD"
          )}
        </div>
        <div className="retrievalevent">TEXT</div>
      </div>

      <button className="btnSum">
        Analysis
        <img src="/send.png" alt="" />
      </button>
    </div>
  );
};

export default DashboardPage;
