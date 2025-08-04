import reflex as rx
from typing import List, Tuple

# ------------------------ State ------------------------
class MacDrawState(rx.State):
    current_tool: str = "pencil"
    brush_size: int = 2
    color: str = "#000000"
    paths: List[List[Tuple[int, int]]] = []
    current_path: List[Tuple[int, int]] = []
    is_drawing: bool = False

    def set_tool(self, tool: str):
        self.current_tool = tool

    def set_color(self, color: str):
        self.color = color

    def set_size(self, size: int):
        self.brush_size = size
    
    def start_drawing(self, pos):
        """Start a new drawing path"""
        self.is_drawing = True
        self.current_path = [pos]
    
    def add_point(self, pos):
        """Add a point to the current path"""
        if self.is_drawing:
            self.current_path.append(pos)
    
    def stop_drawing(self):
        """Finish the current path"""
        if self.is_drawing and self.current_path:
            self.paths.append(self.current_path.copy())
            self.current_path = []
        self.is_drawing = False
    
    def clear_canvas(self):
        """Clear all drawings"""
        self.paths = []
        self.current_path = []
        self.is_drawing = False

# ------------------------ UI Components ------------------------
def tool_palette() -> rx.Component:
    return rx.vstack(
        rx.text("Tools", weight="bold", color="#000"),
        rx.hstack(
            rx.button(
                "✏️", 
                on_click=MacDrawState.set_tool("pencil"),
                color_scheme=rx.cond(MacDrawState.current_tool == "pencil", "blue", "gray")
            ),
            rx.button(
                "🖌️", 
                on_click=MacDrawState.set_tool("brush"),
                color_scheme=rx.cond(MacDrawState.current_tool == "brush", "blue", "gray")
            ),
            rx.button(
                "🧽", 
                on_click=MacDrawState.set_tool("eraser"),
                color_scheme=rx.cond(MacDrawState.current_tool == "eraser", "blue", "gray")
            ),
            spacing="2"
        ),
        rx.button(
            "🗑️ Clear",
            on_click=rx.call_script("if(window.clearCanvas) window.clearCanvas()"),
            color_scheme="red",
            size="2"
        ),
        spacing="2"
    )

def color_palette() -> rx.Component:
    colors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FFFFFF"]
    return rx.vstack(
        rx.text("Colors", weight="bold", color="#000"),
        rx.hstack(
            *[
                rx.box(
                    background_color=color,
                    width="25px",
                    height="25px",
                    border=rx.cond(
                        MacDrawState.color == color,
                        "3px solid #007acc",
                        "1px solid #ccc"
                    ),
                    on_click=MacDrawState.set_color(color),
                    cursor="pointer"
                ) for color in colors
            ],
            spacing="1"
        ),
        spacing="2"
    )

def size_controls() -> rx.Component:
    return rx.vstack(
        rx.text("Size", weight="bold", color="#000"),
        rx.hstack(
            rx.button(
                "S", 
                on_click=MacDrawState.set_size(1),
                color_scheme=rx.cond(MacDrawState.brush_size == 1, "blue", "gray")
            ),
            rx.button(
                "M", 
                on_click=MacDrawState.set_size(3),
                color_scheme=rx.cond(MacDrawState.brush_size == 3, "blue", "gray")
            ),
            rx.button(
                "L", 
                on_click=MacDrawState.set_size(5),
                color_scheme=rx.cond(MacDrawState.brush_size == 5, "blue", "gray")
            ),
            spacing="2"
        ),
        rx.text(f"Current: {MacDrawState.brush_size}px", font_size="12px", color="gray"),
        spacing="2"
    )

def working_canvas() -> rx.Component:
    """Working HTML5 canvas with inline JavaScript"""
    return rx.html(f"""
        <div>
            <canvas id="drawCanvas" width="600" height="400" 
                    style="border: 2px solid #000; background: white; cursor: crosshair; display: block; margin: 0;">
            </canvas>
            <script>
                (function() {{
                    const canvas = document.getElementById('drawCanvas');
                    if (!canvas) {{
                        setTimeout(arguments.callee, 100);
                        return;
                    }}
                    
                    const ctx = canvas.getContext('2d');
                    let isDrawing = false;
                    
                    // Set initial drawing properties
                    ctx.strokeStyle = '{MacDrawState.color}';
                    ctx.lineWidth = {MacDrawState.brush_size};
                    ctx.lineCap = 'round';
                    ctx.lineJoin = 'round';

                    function getMousePos(e) {{
                        const rect = canvas.getBoundingClientRect();
                        return {{
                            x: e.clientX - rect.left,
                            y: e.clientY - rect.top
                        }};
                    }}

                    canvas.onmousedown = function(e) {{
                        isDrawing = true;
                        const pos = getMousePos(e);
                        ctx.beginPath();
                        ctx.moveTo(pos.x, pos.y);
                    }};

                    canvas.onmousemove = function(e) {{
                        if (!isDrawing) return;
                        const pos = getMousePos(e);
                        ctx.lineTo(pos.x, pos.y);
                        ctx.stroke();
                    }};

                    canvas.onmouseup = function() {{
                        isDrawing = false;
                    }};

                    canvas.onmouseleave = function() {{
                        isDrawing = false;
                    }};
                    
                    // Clear function accessible globally
                    window.clearCanvas = function() {{
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                    }};
                }})();
            </script>
        </div>
    """)

def mac_draw() -> rx.Component:
    """MacDraw 1984 - Classic Mac drawing application"""
    return rx.vstack(
        rx.heading("🖥️ MacDraw 1984", size="6", color="#000"),
        rx.hstack(
            rx.vstack(
                tool_palette(), 
                color_palette(), 
                size_controls(), 
                spacing="4"
            ),
            working_canvas(),
            spacing="5"
        ),
        spacing="4",
        padding="4"
    )
