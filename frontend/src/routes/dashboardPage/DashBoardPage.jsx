import "./dashboardPage.css";
import { Link } from "react-router-dom";

const DashboardPage = () => {
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
      <button className="uploadBtn">Upload from your computer</button>
      <button className="uploadBtn">Upload from URL</button>
      <div className="content">
        <div className="videoscreen">VIDEO</div>
        <div className="retrievalevent">TEXT</div>
      </div>
    </div>
  );
};

export default DashboardPage;
