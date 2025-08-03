"""
Mac Draw - Classic drawing application component
"""

import reflex as rx

class MacDrawState(rx.State):
    """State for Mac Draw application"""
    current_tool: str = "pencil"  # pencil, brush, eraser, line, rectangle, circle
    brush_size: int = 2
    current_color: str = "#000000"
    
    def set_tool(self, tool: str):
        self.current_tool = tool
        # Trigger canvas update via JavaScript
        return rx.call_script(f"window.updateCanvasProps && window.updateCanvasProps('{tool}', '{self.current_color}', {self.brush_size})")

    def set_color(self, color: str):
        self.current_color = color
        # Trigger canvas update via JavaScript
        return rx.call_script(f"window.updateCanvasProps && window.updateCanvasProps('{self.current_tool}', '{color}', {self.brush_size})")

    def set_brush_size(self, size: int):
        self.brush_size = size
        # Trigger canvas update via JavaScript
        return rx.call_script(f"window.updateCanvasProps && window.updateCanvasProps('{self.current_tool}', '{self.current_color}', {size})")

    def clear_canvas(self):
        """Clear the canvas - this will be handled by JavaScript"""
        return rx.call_script("window.clearDrawingCanvas && window.clearDrawingCanvas()")

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
            ></canvas>
            <div id="status" style="font-size: 12px; color: #666; margin-top: 5px;">
                Initializing canvas...
            </div>
            <script>
                // Global variables
                let canvas, ctx, status;
                let isDrawing = false;
                let currentColor = '#000000';
                let currentSize = 2;
                let currentTool = 'pencil';
                
                // Wait for DOM to be ready
                function initCanvas() {
                    canvas = document.getElementById('drawingCanvas');
                    status = document.getElementById('status');
                    
                    if (!canvas) {
                        console.log('Canvas not found');
                        return;
                    }
                    
                    ctx = canvas.getContext('2d');
                    
                    // Set default drawing properties
                    ctx.strokeStyle = currentColor;
                    ctx.lineWidth = currentSize;
                    ctx.lineCap = 'round';
                    ctx.lineJoin = 'round';
                    
                    canvas.addEventListener('mousedown', function(e) {
                        isDrawing = true;
                        
                        // Update context properties before drawing
                        ctx.strokeStyle = currentColor;
                        ctx.lineWidth = currentSize;
                        
                        ctx.beginPath();
                        ctx.moveTo(e.offsetX, e.offsetY);
                        status.textContent = 'Drawing at (' + e.offsetX + ', ' + e.offsetY + ') with ' + currentColor;
                        console.log('Started drawing at', e.offsetX, e.offsetY, 'color:', currentColor, 'size:', currentSize);
                    });
                    
                    canvas.addEventListener('mousemove', function(e) {
                        if (!isDrawing) return;
                        ctx.lineTo(e.offsetX, e.offsetY);
                        ctx.stroke();
                        status.textContent = 'Drawing to (' + e.offsetX + ', ' + e.offsetY + ')';
                    });
                    
                    canvas.addEventListener('mouseup', function() {
                        isDrawing = false;
                        status.textContent = 'Ready to draw - Current: ' + currentTool + ', ' + currentColor + ', ' + currentSize + 'px';
                    });
                    
                    canvas.addEventListener('mouseleave', function() {
                        isDrawing = false;
                        status.textContent = 'Ready to draw - Current: ' + currentTool + ', ' + currentColor + ', ' + currentSize + 'px';
                    });
                    
                    status.textContent = 'Canvas ready! Click and drag to draw';
                    console.log('Canvas initialized successfully');
                }
                
                // Global functions for external control
                window.updateCanvasProps = function(tool, color, size) {
                    currentTool = tool;
                    currentColor = color;
                    currentSize = size;
                    console.log('Updated canvas props:', tool, color, size);
                    if (status) {
                        status.textContent = 'Updated: ' + tool + ', ' + color + ', ' + size + 'px';
                    }
                };
                
                window.clearDrawingCanvas = function() {
                    if (canvas && ctx) {
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        if (status) status.textContent = 'Canvas cleared - Ready to draw';
                    }
                };
                
                // Initialize canvas when DOM is ready
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', initCanvas);
                } else {
                    initCanvas();
                }
                
                // Also try with a small delay as backup
                setTimeout(initCanvas, 100);
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
            # Current tool info
            rx.hstack(
                rx.text(f"Tool: {MacDrawState.current_tool.title()}", size="2"),
                rx.box(
                    width="20px",
                    height="20px", 
                    background_color=MacDrawState.current_color,
                    border="1px solid #000",
                    border_radius="4px"
                ),
                rx.text(f"Size: {MacDrawState.brush_size}px", size="2"),
                spacing="3",
                align="center"
            ),
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
