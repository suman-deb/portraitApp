// File: /frontend/src/pages/Search.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Search() {
  const [name, setName] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch("http://localhost:5000/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    const data = await res.json();
    navigate("/result", { state: { text: data.text, name } });
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-3xl font-bold mb-6">Text Portrait Generator</h1>
      <form onSubmit={handleSubmit} className="flex flex-col items-center">
        <input
          className="border px-4 py-2 mb-4 w-64"
          placeholder="Enter a famous person's name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button className="bg-blue-500 text-white px-4 py-2 rounded">Generate</button>
      </form>
    </div>
  );
}

export default Search;

