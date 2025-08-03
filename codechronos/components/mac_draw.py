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
        self.current_tool = tool

    def set_color(self, color: str):
        self.current_color = color

    def set_brush_size(self, size: int):
        self.brush_size = size

    def get_js_state(self):
        # Returns a dict of current tool, color, and brush size for JS
        return {
            "tool": self.current_tool,
            "color": self.current_color,
            "size": self.brush_size
        }
    
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
        rx.box(
            # The canvas element with embedded JavaScript
            rx.html(f'''
                <canvas id="drawingCanvas" width="600" height="400" 
                        style="border: 2px solid #000; background: white; cursor: crosshair; display: block;"
                        data-tool="{MacDrawState.current_tool}" 
                        data-color="{MacDrawState.current_color}" 
                        data-size="{MacDrawState.brush_size}">
                </canvas>
                <script>
                (function() {{
                    const canvas = document.getElementById("drawingCanvas");
                    if (!canvas) return;
                    const ctx = canvas.getContext("2d");
                    let drawing = false;
                    
                    function updateToolState() {{
                        return {{
                            tool: canvas.dataset.tool || "pencil",
                            color: canvas.dataset.color || "#000000",
                            size: parseInt(canvas.dataset.size) || 2
                        }};
                    }}
                    
                    canvas.onmousedown = (e) => {{
                        drawing = true;
                        const {{ tool, color, size }} = updateToolState();
                        ctx.beginPath();
                        ctx.moveTo(e.offsetX, e.offsetY);
                        ctx.strokeStyle = color;
                        ctx.lineWidth = size;
                        ctx.lineCap = "round";
                    }};
                    
                    canvas.onmousemove = (e) => {{
                        if (!drawing) return;
                        const {{ tool, color, size }} = updateToolState();
                        ctx.lineTo(e.offsetX, e.offsetY);
                        ctx.strokeStyle = color;
                        ctx.lineWidth = size;
                        ctx.stroke();
                    }};
                    
                    canvas.onmouseup = () => drawing = false;
                    canvas.onmouseleave = () => drawing = false;
                    
                    // Clear canvas function
                    window.clearDrawingCanvas = function() {{
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                    }};
                }})();
                </script>
            '''),
            padding="4"
        ),
        padding="0"
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
