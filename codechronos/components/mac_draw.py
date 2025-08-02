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
    
    def start_drawing(self):
        """Start drawing"""
        self.is_drawing = True
    
    def stop_drawing(self):
        """Stop drawing"""
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
    """Render the main drawing canvas"""
    return rx.box(
        rx.html(
            f"""
            <canvas 
                id="drawingCanvas" 
                width="600" 
                height="400"
                style="border: 2px solid #000; background: white; cursor: crosshair;"
                onmousedown="startDrawing(event)"
                onmousemove="draw(event)"
                onmouseup="stopDrawing()"
                onmouseout="stopDrawing()"
            ></canvas>
            
            <script>
                let isDrawing = false;
                let currentX = 0;
                let currentY = 0;
                const canvas = document.getElementById('drawingCanvas');
                const ctx = canvas.getContext('2d');
                
                function startDrawing(e) {{
                    isDrawing = true;
                    [currentX, currentY] = [e.offsetX, e.offsetY];
                }}
                
                function draw(e) {{
                    if (!isDrawing) return;
                    
                    ctx.beginPath();
                    ctx.moveTo(currentX, currentY);
                    ctx.lineTo(e.offsetX, e.offsetY);
                    ctx.strokeStyle = '{MacDrawState.current_color}';
                    ctx.lineWidth = {MacDrawState.brush_size};
                    ctx.lineCap = 'round';
                    ctx.stroke();
                    
                    [currentX, currentY] = [e.offsetX, e.offsetY];
                }}
                
                function stopDrawing() {{
                    isDrawing = false;
                }}
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
            rx.button(
                "Clear",
                on_click=MacDrawState.clear_canvas,
                variant="outline",
                color_scheme="red"
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
