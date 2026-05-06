import React, { useState } from "react";
import axios from "axios";

function Research() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleResearch = async () => {
    if (!query) return;
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await axios.get(
        `http://34.229.44.212:8000/research?query=${query}`
      );
      setResult(res.data);
    } catch (err) {
      setError("Research failed. Please check backend.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card">
      <div className="card-header">
        <h2>Autonomous Researcher</h2>
        <p>Agentic web research for logistics trends</p>
      </div>

      <div className="chat-container">
        <div className="input-group">
          <input
            className="chat-input"
            placeholder="Search latest logistics trends..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            onClick={handleResearch}
            className="btn btn-ask"
            disabled={loading}
          >
            {loading ? "Searching..." : "Research"}
          </button>
        </div>

        <div className="response-box">
          {loading && (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <p>Researcher Agent is navigating the web...</p>
            </div>
          )}

          {error && <p className="error-text">{error}</p>}

          {result && (
            <div className="response-content">
              <span className="ai-badge">Research Summary</span>
              <p className="research-result">{result.result}</p>
              <div className="file-info">
                <span>📍 Saved to: </span>
                <code>{result.file_path}</code>
              </div>
            </div>
          )}

          {!loading && !result && !error && (
            <div className="response-placeholder">
              Agent findings will appear here...
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Research;
