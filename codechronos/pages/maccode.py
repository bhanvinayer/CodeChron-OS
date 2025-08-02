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
    
    # Window states with positions
    calculator_active: bool = False
    calculator_x: int = 150
    calculator_y: int = 80
    
    notepad_active: bool = False
    notepad_x: int = 200
    notepad_y: int = 120
    
    draw_active: bool = False
    draw_x: int = 250
    draw_y: int = 160
    
    breakout_active: bool = False
    breakout_x: int = 300
    breakout_y: int = 200
    
    # Desktop state
    selected_icon: str = ""
    
    def open_calculator(self):
        """Open Calculator"""
        print("Opening calculator")  # Debug print
        self.calculator_active = True
        self.selected_icon = "calculator"
    
    def open_notepad(self):
        """Open Notepad"""
        print("Opening notepad")  # Debug print
        self.notepad_active = True
        self.selected_icon = "notepad"
    
    def open_macdraw(self):
        """Open MacDraw"""
        print("Opening macdraw")  # Debug print
        self.draw_active = True
        self.selected_icon = "macdraw"
    
    def open_breakout(self):
        """Open Breakout"""
        print("Opening breakout")  # Debug print
        self.breakout_active = True
        self.selected_icon = "breakout"
    
    def close_calculator(self):
        """Close Calculator"""
        self.calculator_active = False
    
    def close_notepad(self):
        """Close Notepad"""
        self.notepad_active = False
    
    def close_macdraw(self):
        """Close MacDraw"""
        self.draw_active = False
    
    def close_breakout(self):
        """Close Breakout"""
        self.breakout_active = False
    
    def clear_selection(self):
        """Clear icon selection"""
        self.selected_icon = ""

def mac_window_title_bar(title: str, on_close) -> rx.Component:
    """Create an authentic Mac-style title bar"""
    return rx.hstack(
        # Left side - close button
        rx.box(
            rx.box(
                width="12px",
                height="12px",
                border_radius="50%",
                bg="white",
                border="1px solid #000",
                cursor="pointer",
                on_click=on_close,
                style={
                    "&:hover": {
                        "background": "#ff0000"
                    }
                }
            ),
            padding="4px"
        ),
        
        # Center - title
        rx.center(
            rx.text(
                title,
                font_size="12px",
                font_family="'Press Start 2P', monospace",
                color="black",
                font_weight="bold"
            ),
            flex="1"
        ),
        
        # Right side - spacer for symmetry
        rx.box(width="20px"),
        
        width="100%",
        height="20px",
        bg="white",
        border_bottom="2px solid black",
        align="center",
        cursor="move"
    )

def mac_window(
    title: str,
    children: rx.Component,
    x: int,
    y: int,
    width: str = "300px",
    height: str = "250px",
    on_close=None
) -> rx.Component:
    """Create an authentic Mac-style window"""
    return rx.box(
        rx.vstack(
            mac_window_title_bar(title, on_close),
            rx.box(
                children,
                bg="white",
                padding="8px",
                flex="1",
                overflow="auto",
                border_left="2px solid black",
                border_right="2px solid black",
                border_bottom="2px solid black"
            ),
            spacing="0"
        ),
        position="absolute",
        left=f"{x}px",
        top=f"{y}px",
        width=width,
        height=height,
        bg="white",
        border="2px solid black",
        box_shadow="4px 4px 0px rgba(0,0,0,0.5)",
        z_index="100",
        font_family="'Press Start 2P', monospace"
    )

def mac_menu_bar() -> rx.Component:
    """Classic Mac menu bar"""
    return rx.hstack(
        # Apple menu and main menus
        rx.hstack(
            rx.box(
                rx.text("🍎", font_size="14px"),
                bg="black",
                color="white",
                padding="2px 6px",
                cursor="pointer"
            ),
            rx.text("File", font_size="12px", font_family="'Press Start 2P', monospace", cursor="pointer", padding="2px 8px"),
            rx.text("Edit", font_size="12px", font_family="'Press Start 2P', monospace", cursor="pointer", padding="2px 8px"),
            rx.text("View", font_size="12px", font_family="'Press Start 2P', monospace", cursor="pointer", padding="2px 8px"),
            rx.text("Tools", font_size="12px", font_family="'Press Start 2P', monospace", cursor="pointer", padding="2px 8px"),
            spacing="2"
        ),
        rx.spacer(),
        # Time display
        rx.text(
            MacCodeState.current_time,
            font_size="12px",
            font_family="'Press Start 2P', monospace"
        ),
        width="100%",
        padding="4px 8px",
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
            mac_window(
                "Calculator",
                calculator_component(),
                MacCodeState.calculator_x,
                MacCodeState.calculator_y,
                width="280px",
                height="320px",
                on_close=MacCodeState.close_calculator
            ),
            rx.box()
        ),
        
        # Notepad window
        rx.cond(
            MacCodeState.notepad_active,
            mac_window(
                "Notepad",
                notepad_component(),
                MacCodeState.notepad_x,
                MacCodeState.notepad_y,
                width="450px",
                height="350px",
                on_close=MacCodeState.close_notepad
            ),
            rx.box()
        ),
        
        # MacDraw window
        rx.cond(
            MacCodeState.draw_active,
            mac_window(
                "MacDraw",
                mac_draw(),
                MacCodeState.draw_x,
                MacCodeState.draw_y,
                width="500px",
                height="400px",
                on_close=MacCodeState.close_macdraw
            ),
            rx.box()
        ),
        
        # Breakout window
        rx.cond(
            MacCodeState.breakout_active,
            mac_window(
                "Breakout",
                breakout_component(),
                MacCodeState.breakout_x,
                MacCodeState.breakout_y,
                width="400px",
                height="450px",
                on_close=MacCodeState.close_breakout
            ),
            rx.box()
        ),
        
        position="relative",
        width="100%",
        height="100%",
        z_index="50"
    )

def mac_desktop() -> rx.Component:
    """Mac desktop with icons and windows"""
    return rx.box(
        # Desktop icons as simple buttons (like the working test button)
        # Calculator icon
        rx.button(
            "🔢\nCalculator",
            on_click=MacCodeState.open_calculator,
            position="absolute",
            left="20px",
            top="60px",
            width="80px",
            height="60px",
            bg="#e0e0e0",
            border="1px solid black",
            font_size="10px",
            font_family="'Press Start 2P', monospace",
            color="black",
            cursor="pointer",
            z_index="100",
            style={
                "white-space": "pre-line",
                "text-align": "center",
                "&:hover": {"background": "rgba(0,0,0,0.1)"}
            }
        ),
        
        # Notepad icon
        rx.button(
            "📝\nNotepad",
            on_click=MacCodeState.open_notepad,
            position="absolute",
            left="20px",
            top="140px",
            width="80px",
            height="60px",
            bg="#e0e0e0",
            border="1px solid black",
            font_size="10px",
            font_family="'Press Start 2P', monospace",
            color="black",
            cursor="pointer",
            z_index="100",
            style={
                "white-space": "pre-line",
                "text-align": "center",
                "&:hover": {"background": "rgba(0,0,0,0.1)"}
            }
        ),
        
        # MacDraw icon
        rx.button(
            "🎨\nMacDraw",
            on_click=MacCodeState.open_macdraw,
            position="absolute",
            left="20px",
            top="220px",
            width="80px",
            height="60px",
            bg="#e0e0e0",
            border="1px solid black",
            font_size="10px",
            font_family="'Press Start 2P', monospace",
            color="black",
            cursor="pointer",
            z_index="100",
            style={
                "white-space": "pre-line",
                "text-align": "center",
                "&:hover": {"background": "rgba(0,0,0,0.1)"}
            }
        ),
        
        # Breakout icon
        rx.button(
            "🎮\nBreakout",
            on_click=MacCodeState.open_breakout,
            position="absolute",
            left="20px",
            top="300px",
            width="80px",
            height="60px",
            bg="#e0e0e0",
            border="1px solid black",
            font_size="10px",
            font_family="'Press Start 2P', monospace",
            color="black",
            cursor="pointer",
            z_index="100",
            style={
                "white-space": "pre-line",
                "text-align": "center",
                "&:hover": {"background": "rgba(0,0,0,0.1)"}
            }
        ),
        
        # Application windows
        application_windows(),
        
        position="relative",
        width="100%",
        height="calc(100vh - 30px)",
        bg="white",  # White background for better visibility
        overflow="hidden"
    )

def maccode_page() -> rx.Component:
    """Complete Mac 1984 interface - like the demo site"""
    return rx.box(
        mac_menu_bar(),
        mac_desktop(),
        width="100vw",
        height="100vh",
        bg="white",  # White background
        font_family="'Press Start 2P', monospace",
        style={
            "image_rendering": "pixelated",
            "cursor": "crosshair",
            "user_select": "none"
        }
    )
