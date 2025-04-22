import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

const socket = new WebSocket("ws://127.0.0.1:8000/ws/chat");

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    socket.onmessage = (event) => {
      setMessages(prev => [...prev, event.data]);
    };
  }, []);

  const sendMessage = () => {
    if (msg) {
      socket.send(msg);
      setMsg("");
    }
  };

  return (
    <div className="chat-box">
      <div className="chat-messages">
        {messages.map((m, i) => <div key={i}>{m}</div>)}
      </div>
      <input
        value={msg}
        onChange={e => setMsg(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default ChatBox;
