import React, { useState } from "react";
import Upload from "./Upload";
import Chat from "./Chat";
import Research from "./Research";

function App() {
  const [activeTab, setActiveTab] = useState("chat");

  return (
    <div className="app-container">
      <header className="header">
        <div className="logo-wrapper">
          <span className="logo-icon">📦</span>
        </div>
        <h1>LogiChat AI</h1>
        <p>Intelligent Logistics Document Assistant</p>
      </header>

      <div className="tabs-container">
        <button 
          className={`tab-btn ${activeTab === "chat" ? "active" : ""}`}
          onClick={() => setActiveTab("chat")}
        >
          <span className="tab-icon">📄</span> Document Assistant
        </button>
        <button 
          className={`tab-btn ${activeTab === "research" ? "active" : ""}`}
          onClick={() => setActiveTab("research")}
        >
          <span className="tab-icon">🌐</span> Autonomous Researcher
        </button>
      </div>

      <main className="main-content">
        {activeTab === "chat" ? (
          <>
            <Upload />
            <Chat />
          </>
        ) : (
          <Research />
        )}
      </main>
    </div>
  );
}

export default App;