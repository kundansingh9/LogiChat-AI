import React, { useState } from "react";
import axios from "axios";

function Chat() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const ask = async () => {
    const res = await axios.get(
      `http://localhost:8000/chat?query=${query}`
    );

    setResponse(res.data.response);
  };

  return (
    <div className="glass-card">
      <div className="card-header">
        <h2>Ask AI</h2>
        <p>Query your uploaded logistics documents</p>
      </div>
      
      <div className="chat-container">
        <div className="input-group">
          <input
            className="chat-input"
            placeholder="Ask about logistics docs..."
            onChange={(e) => setQuery(e.target.value)}
          />
          <button onClick={ask} className="btn btn-ask">
            Ask AI
          </button>
        </div>

        <div className="response-box">
          {response ? (
            <div className="response-content">
              <span className="ai-badge">AI Response</span>
              <p>{response}</p>
            </div>
          ) : (
            <div className="response-placeholder">
              Your answer will appear here...
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Chat;