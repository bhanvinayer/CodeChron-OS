"""
Base Window Component - Draggable retro-style window
"""

import reflex as rx

class WindowState(rx.State):
    """State for draggable windows"""
    windows: dict = {}
    
    def create_window(self, window_id: str, title: str, x: int = 100, y: int = 100):
        """Create a new window"""
        self.windows[window_id] = {
            "title": title,
            "x": x,
            "y": y,
            "width": 400,
            "height": 300,
            "minimized": False,
            "active": True
        }
    
    def move_window(self, window_id: str, x: int, y: int):
        """Move a window to new position"""
        if window_id in self.windows:
            self.windows[window_id]["x"] = x
            self.windows[window_id]["y"] = y
    
    def close_window(self, window_id: str):
        """Close a window"""
        if window_id in self.windows:
            del self.windows[window_id]
    
    def minimize_window(self, window_id: str):
        """Minimize/restore a window"""
        if window_id in self.windows:
            self.windows[window_id]["minimized"] = not self.windows[window_id]["minimized"]

def window_title_bar(title: str, window_id: str) -> rx.Component:
    """Create a Mac-style title bar"""
    return rx.hstack(
        # Window controls
        rx.hstack(
            rx.button(
                "×",
                on_click=WindowState.close_window(window_id),
                size="1",
                variant="ghost",
                color_scheme="red",
                style={
                    "width": "16px",
                    "height": "16px",
                    "border_radius": "50%",
                    "background": "#ff5f57",
                    "color": "white",
                    "font_size": "10px",
                    "padding": "0"
                }
            ),
            rx.button(
                "−",
                on_click=WindowState.minimize_window(window_id),
                size="1", 
                variant="ghost",
                color_scheme="yellow",
                style={
                    "width": "16px",
                    "height": "16px", 
                    "border_radius": "50%",
                    "background": "#ffbd2e",
                    "color": "white",
                    "font_size": "10px",
                    "padding": "0"
                }
            ),
            rx.button(
                "□",
                size="1",
                variant="ghost", 
                color_scheme="green",
                style={
                    "width": "16px",
                    "height": "16px",
                    "border_radius": "50%", 
                    "background": "#28ca42",
                    "color": "white",
                    "font_size": "8px",
                    "padding": "0"
                }
            ),
            spacing="1"
        ),
        rx.spacer(),
        rx.text(
            title,
            size="2",
            weight="bold",
            color=rx.color("gray", 12)
        ),
        rx.spacer(),
        align="center",
        width="100%",
        padding="0.5rem",
        bg=rx.color("gray", 3),
        border_bottom=f"1px solid {rx.color('gray', 6)}"
    )

def base_window(
    window_id: str,
    title: str, 
    children: rx.Component,
    width: str = "400px",
    height: str = "300px"
) -> rx.Component:
    """Create a draggable retro window"""
    
    return rx.box(
        rx.vstack(
            window_title_bar(title, window_id),
            rx.box(
                children,
                padding="1rem",
                flex="1",
                overflow="auto"
            ),
            spacing="0"
        ),
        position="absolute",
        left=f"{WindowState.windows.get(window_id, {}).get('x', 100)}px",
        top=f"{WindowState.windows.get(window_id, {}).get('y', 100)}px", 
        width=width,
        height=height,
        bg=rx.color("gray", 1),
        border=f"2px solid {rx.color('gray', 6)}",
        border_radius="8px",
        box_shadow="0 4px 12px rgba(0,0,0,0.3)",
        z_index="1000",
        class_name="draggable-window",
        style={
            "cursor": "move",
            "font_family": "'Press Start 2P', monospace"
        }
    )
