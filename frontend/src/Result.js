// File: /frontend/src/pages/Result.js
import React, { useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";

function Result() {
  const canvasRef = useRef(null);
  const location = useLocation();
  const navigate = useNavigate();
  const { text, name } = location.state || {};

  useEffect(() => {
    if (!text) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const width = 600;
    const height = 800;
    canvas.width = width;
    canvas.height = height;

    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, width, height);
    ctx.font = "14px serif";
    ctx.fillStyle = "white";

    const lines = text.split("\n");
    let y = 20;
    lines.forEach((line) => {
      ctx.fillText(line, 10, y);
      y += 18;
    });
  }, [text]);

  const downloadImage = () => {
    const canvas = canvasRef.current;
    const link = document.createElement("a");
    link.download = `${name}-portrait.png`;
    link.href = canvas.toDataURL();
    link.click();
  };

  return (
    <div className="flex flex-col items-center p-4">
      <h2 className="text-2xl mb-4">Portrait of {name}</h2>
      <canvas ref={canvasRef} className="border mb-4" />
      <div className="flex gap-4">
        <button onClick={downloadImage} className="bg-green-500 text-white px-4 py-2 rounded">
          Download Image
        </button>
        <button onClick={() => navigate("/")} className="bg-gray-500 text-white px-4 py-2 rounded">
          Go Back
        </button>
      </div>
    </div>
  );
}

export default Result;
