import React, { useState } from "react";

function ChatBox() {
  const [msg, setMsg] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSendMessage = () => {
    if (msg.trim()) {
      setMessages([...messages, msg]);
      setMsg(""); // Clear the input field
    }
  };

  return (
    <div className="chat-box">
      <div className="messages">
        {messages.map((m, i) => (
          <div key={i}>{m}</div>
        ))}
      </div>
      <input
        type="text"
        value={msg}
        onChange={(e) => setMsg(e.target.value)}
        placeholder="Type a message..."
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
}

export default ChatBox;
