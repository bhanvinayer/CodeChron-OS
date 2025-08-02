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
    
    def set_brush_size(self, size: int):
        """Set brush size"""
        self.brush_size = size
    
    def set_color(self, color: str):
        """Set drawing color"""
        self.current_color = color
    
    def clear_canvas(self):
        """Clear the drawing canvas"""
        self.canvas_data = ""

def tool_palette() -> rx.Component:
    """Tool palette for Mac Draw"""
    return rx.vstack(
        rx.text("Tools", size="2", weight="bold"),
        rx.hstack(
            rx.button(
                "✏️",
                on_click=MacDrawState.set_tool("pencil"),
                variant="soft" if MacDrawState.current_tool == "pencil" else "outline",
                size="2"
            ),
            rx.button(
                "🖌️", 
                on_click=MacDrawState.set_tool("brush"),
                variant="soft" if MacDrawState.current_tool == "brush" else "outline",
                size="2"
            ),
            rx.button(
                "🧽",
                on_click=MacDrawState.set_tool("eraser"),
                variant="soft" if MacDrawState.current_tool == "eraser" else "outline", 
                size="2"
            ),
            spacing="1"
        ),
        rx.hstack(
            rx.button(
                "📏",
                on_click=MacDrawState.set_tool("line"),
                variant="soft" if MacDrawState.current_tool == "line" else "outline",
                size="2"
            ),
            rx.button(
                "▢",
                on_click=MacDrawState.set_tool("rectangle"), 
                variant="soft" if MacDrawState.current_tool == "rectangle" else "outline",
                size="2"
            ),
            rx.button(
                "○",
                on_click=MacDrawState.set_tool("circle"),
                variant="soft" if MacDrawState.current_tool == "circle" else "outline",
                size="2"
            ),
            spacing="1"
        ),
        rx.slider(
            default_value=2,
            min=1,
            max=10,
            step=1,
            on_change=MacDrawState.set_brush_size,
            width="100px"
        ),
        rx.text(f"Size: {MacDrawState.brush_size}", size="1"),
        rx.button(
            "Clear",
            on_click=MacDrawState.clear_canvas,
            color_scheme="red",
            variant="soft"
        ),
        spacing="2",
        align="start"
    )

def drawing_canvas() -> rx.Component:
    """Main drawing canvas"""
    return rx.box(
        # Canvas will be implemented with JavaScript integration
        rx.html(
            """
            <canvas 
                id="mac-draw-canvas" 
                width="300" 
                height="200"
                style="border: 1px solid #ccc; background: white; cursor: crosshair;"
            ></canvas>
            <script>
                const canvas = document.getElementById('mac-draw-canvas');
                const ctx = canvas.getContext('2d');
                let isDrawing = false;
                
                canvas.addEventListener('mousedown', startDrawing);
                canvas.addEventListener('mousemove', draw);
                canvas.addEventListener('mouseup', stopDrawing);
                
                function startDrawing(e) {
                    isDrawing = true;
                    ctx.beginPath();
                    ctx.moveTo(e.offsetX, e.offsetY);
                }
                
                function draw(e) {
                    if (!isDrawing) return;
                    ctx.lineWidth = 2;
                    ctx.lineCap = 'round';
                    ctx.strokeStyle = '#000';
                    ctx.lineTo(e.offsetX, e.offsetY);
                    ctx.stroke();
                }
                
                function stopDrawing() {
                    isDrawing = false;
                }
            </script>
            """
        ),
        padding="1rem",
        bg="white",
        border_radius="4px"
    )

def mac_draw_component() -> rx.Component:
    """Complete Mac Draw application"""
    return rx.hstack(
        tool_palette(),
        drawing_canvas(),
        spacing="4",
        align="start",
        width="100%"
    )
