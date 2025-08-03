// canvas.js - MacDraw canvas bindings
export function setupCanvasBindings() {
  const canvas = document.getElementById("drawingCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  let drawing = false;

  function updateToolState() {
    // Always get latest tool/color/size from dataset
    return {
      tool: canvas.dataset.tool || "pencil",
      color: canvas.dataset.color || "#000000",
      size: parseInt(canvas.dataset.size) || 2
    };
  }

  canvas.onmousedown = (e) => {
    drawing = true;
    const { tool, color, size } = updateToolState();
    ctx.beginPath();
    ctx.moveTo(e.offsetX, e.offsetY);
    ctx.strokeStyle = color;
    ctx.lineWidth = size;
  };

  canvas.onmousemove = (e) => {
    if (!drawing) return;
    const { tool, color, size } = updateToolState();
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.strokeStyle = color;
    ctx.lineWidth = size;
    ctx.stroke();
  };

  canvas.onmouseup = () => drawing = false;
  canvas.onmouseleave = () => drawing = false;
}

// Auto-run if loaded as a script (for non-module environments)
if (typeof window !== 'undefined') {
  window.setupCanvasBindings = setupCanvasBindings;
  // If the canvas is already in the DOM, call immediately
  if (document.getElementById("drawingCanvas")) {
    setupCanvasBindings();
  } else {
    // Otherwise, wait for DOMContentLoaded
    window.addEventListener('DOMContentLoaded', setupCanvasBindings);
  }
}
