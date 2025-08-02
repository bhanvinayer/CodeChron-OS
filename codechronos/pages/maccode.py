"""
MacCode Page - 1984 Macintosh development environment
"""

import reflex as rx
from typing import List, Dict, Any
from ..components.base_window import base_window, WindowState
from ..components.calculator import calculator_component
from ..components.notepad import notepad_component
from ..components.mac_draw import mac_draw
from ..components.breakout import breakout_component

class MacCodeState(rx.State):
    """State for Mac 1984 interface"""
    current_time: str = "12:00 PM"
    
    # Window states
    calculator_active: bool = False
    notepad_active: bool = False
    draw_active: bool = False
    breakout_active: bool = False
    
    def open_calculator(self):
        """Open Calculator"""
        self.calculator_active = True
    
    def open_notepad(self):
        """Open Notepad"""
        self.notepad_active = True
    
    def open_macdraw(self):
        """Open MacDraw"""
        self.draw_active = True
    
    def open_breakout(self):
        """Open Breakout"""
        self.breakout_active = True

def mac_menu_bar() -> rx.Component:
    """Classic Mac menu bar"""
    return rx.hstack(
        rx.hstack(
            rx.text("🍎", font_size="16px"),
            rx.text("File", font_size="12px", font_family="'Press Start 2P', monospace"),
            rx.text("Edit", font_size="12px", font_family="'Press Start 2P', monospace"),
            rx.text("View", font_size="12px", font_family="'Press Start 2P', monospace"),
            rx.text("Tools", font_size="12px", font_family="'Press Start 2P', monospace"),
            spacing="4"
        ),
        rx.spacer(),
        rx.text(
            MacCodeState.current_time,
            font_size="12px",
            font_family="'Press Start 2P', monospace"
        ),
        width="100%",
        padding="8px 16px",
        bg="white",
        border_bottom="2px solid black",
        align="center"
    )

def application_windows() -> rx.Component:
    """Render all open application windows"""
    return rx.box(
        # Calculator window
        rx.cond(
            MacCodeState.calculator_active,
            base_window(
                "calculator",
                "Calculator",
                calculator_component(),
                width="300px",
                height="400px"
            ),
            rx.box()
        ),
        
        # Notepad window
        rx.cond(
            MacCodeState.notepad_active,
            base_window(
                "notepad",
                "Notepad",
                notepad_component(),
                width="500px",
                height="400px"
            ),
            rx.box()
        ),
        
        # MacDraw window
        rx.cond(
            MacCodeState.draw_active,
            base_window(
                "macdraw",
                "MacDraw",
                mac_draw(),
                width="600px",
                height="450px"
            ),
            rx.box()
        ),
        
        # Breakout window
        rx.cond(
            MacCodeState.breakout_active,
            base_window(
                "breakout",
                "Breakout",
                breakout_component(),
                width="450px",
                height="500px"
            ),
            rx.box()
        ),
        
        position="relative",
        width="100%",
        height="100%"
    )

def mac_desktop() -> rx.Component:
    """Mac desktop with icons and windows"""
    return rx.box(
        # Desktop icons - static placement
        # Calculator icon
        rx.box(
            rx.vstack(
                rx.text(
                    "🔢", 
                    font_size="32px", 
                    margin_bottom="4px",
                    cursor="pointer",
                    on_click=MacCodeState.open_calculator,
                    on_double_click=MacCodeState.open_calculator
                ),
                rx.text(
                    "Calculator",
                    font_size="10px",
                    font_family="'Press Start 2P', monospace",
                    color="black",
                    text_align="center",
                    max_width="60px",
                    cursor="pointer",
                    on_click=MacCodeState.open_calculator,
                    on_double_click=MacCodeState.open_calculator
                ),
                spacing="1",
                align="center"
            ),
            position="absolute",
            left="50px",
            top="100px",
            padding="8px",
            cursor="pointer",
            border_radius="4px",
            style={"&:hover": {"background": "rgba(0,0,0,0.1)"}},
            on_click=MacCodeState.open_calculator,
            on_double_click=MacCodeState.open_calculator
        ),
        
        # Notepad icon
        rx.box(
            rx.vstack(
                rx.text(
                    "📝", 
                    font_size="32px", 
                    margin_bottom="4px",
                    cursor="pointer",
                    on_click=MacCodeState.open_notepad,
                    on_double_click=MacCodeState.open_notepad
                ),
                rx.text(
                    "Notepad",
                    font_size="10px",
                    font_family="'Press Start 2P', monospace",
                    color="black",
                    text_align="center",
                    max_width="60px",
                    cursor="pointer",
                    on_click=MacCodeState.open_notepad,
                    on_double_click=MacCodeState.open_notepad
                ),
                spacing="1",
                align="center"
            ),
            position="absolute",
            left="50px",
            top="180px",
            padding="8px",
            cursor="pointer",
            border_radius="4px",
            style={"&:hover": {"background": "rgba(0,0,0,0.1)"}},
            on_click=MacCodeState.open_notepad,
            on_double_click=MacCodeState.open_notepad
        ),
        
        # MacDraw icon
        rx.box(
            rx.vstack(
                rx.text(
                    "🎨", 
                    font_size="32px", 
                    margin_bottom="4px",
                    cursor="pointer",
                    on_click=MacCodeState.open_macdraw,
                    on_double_click=MacCodeState.open_macdraw
                ),
                rx.text(
                    "MacDraw",
                    font_size="10px",
                    font_family="'Press Start 2P', monospace",
                    color="black",
                    text_align="center",
                    max_width="60px",
                    cursor="pointer",
                    on_click=MacCodeState.open_macdraw,
                    on_double_click=MacCodeState.open_macdraw
                ),
                spacing="1",
                align="center"
            ),
            position="absolute",
            left="50px",
            top="260px",
            padding="8px",
            cursor="pointer",
            border_radius="4px",
            style={"&:hover": {"background": "rgba(0,0,0,0.1)"}},
            on_click=MacCodeState.open_macdraw,
            on_double_click=MacCodeState.open_macdraw
        ),
        
        # Breakout icon
        rx.box(
            rx.vstack(
                rx.text(
                    "🎮", 
                    font_size="32px", 
                    margin_bottom="4px",
                    cursor="pointer",
                    on_click=MacCodeState.open_breakout,
                    on_double_click=MacCodeState.open_breakout
                ),
                rx.text(
                    "Breakout",
                    font_size="10px",
                    font_family="'Press Start 2P', monospace",
                    color="black",
                    text_align="center",
                    max_width="60px",
                    cursor="pointer",
                    on_click=MacCodeState.open_breakout,
                    on_double_click=MacCodeState.open_breakout
                ),
                spacing="1",
                align="center"
            ),
            position="absolute",
            left="50px",
            top="340px",
            padding="8px",
            cursor="pointer",
            border_radius="4px",
            style={"&:hover": {"background": "rgba(0,0,0,0.1)"}},
            on_click=MacCodeState.open_breakout,
            on_double_click=MacCodeState.open_breakout
        ),
        
        # Application windows
        application_windows(),
        
        position="relative",
        width="100%",
        height="calc(100vh - 40px)",
        bg="url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\"><rect width=\"20\" height=\"20\" fill=\"%23f0f0f0\"/><rect width=\"1\" height=\"1\" x=\"10\" y=\"10\" fill=\"%23e0e0e0\"/></svg>')",
        overflow="hidden"
    )

def maccode_page() -> rx.Component:
    """Complete Mac 1984 interface"""
    return rx.box(
        mac_menu_bar(),
        mac_desktop(),
        width="100vw",
        height="100vh",
        bg="#f0f0f0",
        font_family="'Press Start 2P', monospace",
        style={
            "image_rendering": "pixelated",
            "cursor": "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" viewBox=\"0 0 16 16\"><polygon points=\"0,0 0,10 3,7 6,11 8,10 5,6 8,6\" fill=\"black\"/><polygon points=\"1,1 1,8 3,6 5,9 6,8.5 4,5.5 6.5,5.5\" fill=\"white\"/></svg>'), auto"
        }
    )
