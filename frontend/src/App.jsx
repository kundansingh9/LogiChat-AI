import React from "react";
import Upload from "./Upload";
import Chat from "./Chat";

function App() {
  return (
    <div className="app-container">
      <header className="header">
        <div className="logo-wrapper">
          <span className="logo-icon">📦</span>
        </div>
        <h1>LogiChat AI</h1>
        <p>Intelligent Logistics Document Assistant</p>
      </header>

      <main className="main-content">
        <Upload />
        <Chat />
      </main>
    </div>
  );
}

export default App;