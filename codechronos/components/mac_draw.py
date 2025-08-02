"""
Mac Draw - Classic drawing application component
"""

import reflex as rx

class MacDrawState(rx.State):
    """State for Mac Draw application"""
    canvas_data: str = ""
    current_tool: str = "pencil"  # pencil, brush, eraser, line, rectangle, circle
    brush_size: int = 2
    current_color: str = "#000000"
    is_drawing: bool = False
    drawing_paths: list = []
    current_path: list = []
    
    def set_tool(self, tool: str):
        """Set the current drawing tool"""
        self.current_tool = tool
    
    def set_color(self, color: str):
        """Set the current drawing color"""
        self.current_color = color
    
    def set_brush_size(self, size: int):
        """Set the current brush size"""
        self.brush_size = size
    
    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas_data = ""
        self.drawing_paths = []
        self.current_path = []
    
    def start_drawing(self, x: int, y: int):
        """Start drawing at position"""
        self.is_drawing = True
        self.current_path = [{"x": x, "y": y, "color": self.current_color, "size": self.brush_size}]
    
    def continue_drawing(self, x: int, y: int):
        """Continue drawing to position"""
        if self.is_drawing:
            self.current_path.append({"x": x, "y": y, "color": self.current_color, "size": self.brush_size})
    
    def stop_drawing(self):
        """Stop drawing"""
        if self.is_drawing and self.current_path:
            self.drawing_paths.append(self.current_path)
            self.current_path = []
        self.is_drawing = False

def tool_palette() -> rx.Component:
    """Render the tool palette"""
    return rx.vstack(
        rx.text("Tools", size="2", weight="bold"),
        rx.hstack(
            rx.button(
                "✏️",
                on_click=MacDrawState.set_tool("pencil"),
                variant=rx.cond(MacDrawState.current_tool == "pencil", "soft", "outline"),
                size="2"
            ),
            rx.button(
                "🖌️",
                on_click=MacDrawState.set_tool("brush"),
                variant=rx.cond(MacDrawState.current_tool == "brush", "soft", "outline"), 
                size="2"
            ),
            rx.button(
                "🧽",
                on_click=MacDrawState.set_tool("eraser"),
                variant=rx.cond(MacDrawState.current_tool == "eraser", "soft", "outline"), 
                size="2"
            ),
            rx.button(
                "📏",
                on_click=MacDrawState.set_tool("line"),
                variant=rx.cond(MacDrawState.current_tool == "line", "soft", "outline"),
                size="2"
            ),
            rx.button(
                "⬛",
                on_click=MacDrawState.set_tool("rectangle"),
                variant=rx.cond(MacDrawState.current_tool == "rectangle", "soft", "outline"),
                size="2"
            ),
            rx.button(
                "⭕",
                on_click=MacDrawState.set_tool("circle"),
                variant=rx.cond(MacDrawState.current_tool == "circle", "soft", "outline"),
                size="2"
            ),
            spacing="2"
        ),
        spacing="3"
    )

def color_palette() -> rx.Component:
    """Render the color palette"""
    colors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#FFFFFF"]
    
    return rx.vstack(
        rx.text("Colors", size="2", weight="bold"),
        rx.hstack(
            *[
                rx.button(
                    width="30px",
                    height="30px",
                    background_color=color,
                    border=rx.cond(MacDrawState.current_color == color, "2px solid #000", "1px solid #ccc"),
                    on_click=MacDrawState.set_color(color),
                    border_radius="4px"
                ) for color in colors
            ],
            spacing="1"
        ),
        spacing="3"
    )

def brush_size_controls() -> rx.Component:
    """Render brush size controls"""
    return rx.vstack(
        rx.text("Brush Size", size="2", weight="bold"),
        rx.hstack(
            rx.button("S", on_click=MacDrawState.set_brush_size(1), size="1"),
            rx.button("M", on_click=MacDrawState.set_brush_size(3), size="1"),
            rx.button("L", on_click=MacDrawState.set_brush_size(5), size="1"),
            spacing="2"
        ),
        spacing="3"
    )

def drawing_canvas() -> rx.Component:
    """Render the main drawing canvas using HTML5 Canvas"""
    return rx.box(
        rx.html(
            """
            <canvas 
                id="drawingCanvas" 
                width="600" 
                height="400"
                style="border: 2px solid #000; background: white; cursor: crosshair; display: block;"
                onmousedown="window.startDrawing && window.startDrawing(event)"
                onmousemove="window.draw && window.draw(event)"
                onmouseup="window.stopDrawing && window.stopDrawing()"
                onmouseout="window.stopDrawing && window.stopDrawing()"
                onmouseleave="window.stopDrawing && window.stopDrawing()"
            ></canvas>
            
            <script>
                // Create a namespace to avoid conflicts
                window.MacDrawCanvas = window.MacDrawCanvas || {};
                
                // Drawing state
                window.MacDrawCanvas.isDrawing = false;
                window.MacDrawCanvas.currentX = 0;
                window.MacDrawCanvas.currentY = 0;
                window.MacDrawCanvas.canvas = null;
                window.MacDrawCanvas.ctx = null;
                
                // Initialize canvas
                window.MacDrawCanvas.init = function() {
                    const canvas = document.getElementById('drawingCanvas');
                    if (!canvas) return false;
                    
                    window.MacDrawCanvas.canvas = canvas;
                    window.MacDrawCanvas.ctx = canvas.getContext('2d');
                    
                    // Set default drawing properties
                    window.MacDrawCanvas.ctx.strokeStyle = '#000000';
                    window.MacDrawCanvas.ctx.lineWidth = 2;
                    window.MacDrawCanvas.ctx.lineCap = 'round';
                    window.MacDrawCanvas.ctx.lineJoin = 'round';
                    
                    return true;
                };
                
                // Drawing functions
                window.MacDrawCanvas.startDrawing = function(e) {
                    if (!window.MacDrawCanvas.canvas || !window.MacDrawCanvas.ctx) {
                        if (!window.MacDrawCanvas.init()) return;
                    }
                    
                    window.MacDrawCanvas.isDrawing = true;
                    const rect = window.MacDrawCanvas.canvas.getBoundingClientRect();
                    window.MacDrawCanvas.currentX = e.clientX - rect.left;
                    window.MacDrawCanvas.currentY = e.clientY - rect.top;
                };
                
                window.MacDrawCanvas.draw = function(e) {
                    if (!window.MacDrawCanvas.isDrawing || !window.MacDrawCanvas.canvas || !window.MacDrawCanvas.ctx) return;
                    
                    const rect = window.MacDrawCanvas.canvas.getBoundingClientRect();
                    const newX = e.clientX - rect.left;
                    const newY = e.clientY - rect.top;
                    
                    window.MacDrawCanvas.ctx.beginPath();
                    window.MacDrawCanvas.ctx.moveTo(window.MacDrawCanvas.currentX, window.MacDrawCanvas.currentY);
                    window.MacDrawCanvas.ctx.lineTo(newX, newY);
                    window.MacDrawCanvas.ctx.stroke();
                    
                    window.MacDrawCanvas.currentX = newX;
                    window.MacDrawCanvas.currentY = newY;
                };
                
                window.MacDrawCanvas.stopDrawing = function() {
                    window.MacDrawCanvas.isDrawing = false;
                };
                
                window.MacDrawCanvas.clear = function() {
                    if (!window.MacDrawCanvas.canvas || !window.MacDrawCanvas.ctx) {
                        if (!window.MacDrawCanvas.init()) return;
                    }
                    window.MacDrawCanvas.ctx.clearRect(0, 0, window.MacDrawCanvas.canvas.width, window.MacDrawCanvas.canvas.height);
                };
                
                // Global aliases for HTML event handlers
                window.startDrawing = window.MacDrawCanvas.startDrawing;
                window.draw = window.MacDrawCanvas.draw;
                window.stopDrawing = window.MacDrawCanvas.stopDrawing;
                window.clearDrawingCanvas = window.MacDrawCanvas.clear;
                
                // Initialize immediately and also set up a retry mechanism
                setTimeout(function() {
                    window.MacDrawCanvas.init();
                    
                    // Set up event listeners as backup
                    const canvas = document.getElementById('drawingCanvas');
                    if (canvas) {
                        // Remove any existing listeners first
                        canvas.onmousedown = window.startDrawing;
                        canvas.onmousemove = window.draw;
                        canvas.onmouseup = window.stopDrawing;
                        canvas.onmouseout = window.stopDrawing;
                        canvas.onmouseleave = window.stopDrawing;
                    }
                }, 100);
            </script>
            """
        ),
        padding="4"
    )

def mac_draw() -> rx.Component:
    """Main Mac Draw component"""
    return rx.vstack(
        rx.hstack(
            rx.text("🎨 Mac Draw", size="6", weight="bold"),
            rx.spacer(),
            rx.html(
                """
                <button 
                    onclick="window.clearDrawingCanvas && window.clearDrawingCanvas()"
                    style="
                        background: #ff4757; 
                        color: white; 
                        border: 1px solid #ff4757; 
                        border-radius: 4px; 
                        padding: 8px 16px; 
                        cursor: pointer;
                        font-size: 14px;
                    "
                    onmouseover="this.style.background='#ff3838'"
                    onmouseout="this.style.background='#ff4757'"
                >
                    Clear
                </button>
                """
            ),
            width="100%",
            align="center"
        ),
        
        rx.hstack(
            # Left sidebar with tools
            rx.vstack(
                tool_palette(),
                color_palette(),
                brush_size_controls(),
                width="200px",
                spacing="4"
            ),
            
            # Main canvas area
            drawing_canvas(),
            
            spacing="4",
            width="100%"
        ),
        
        spacing="4",
        width="100%",
        height="100vh",
        padding="4"
    )
