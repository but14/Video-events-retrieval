import { Link } from "react-router-dom";
import "./chatList.css";


const ChatList = () => {

  return (
    <div className="chatList">
      <span className="title">VIDEO EVENT RETRIEVAL</span>
      <Link to="/dashboard">Create a new</Link>
    </div>
  );
};

export default ChatList;
