"""
Home Page - Boot animation and landing page
"""

import reflex as rx
import asyncio

class HomeState(rx.State):
    """State for boot sequence"""
    boot_stage: int = 0
    boot_text: str = "CodeChronOS Loading..."
    show_logo: bool = False
    progress: int = 0
    boot_complete: bool = False
    
    async def start_boot_sequence(self):
        """Simulate Mac-style boot sequence"""
        stages = [
            "Initializing CodeChronOS...",
            "Loading Macintosh 1984 kernel...",
            "Mounting retro file system...",
            "Starting window manager...",
            "Loading applications...",
            "Welcome to CodeChronOS!"
        ]
        
        for i, stage in enumerate(stages):
            self.boot_stage = i
            self.boot_text = stage
            self.progress = int((i + 1) / len(stages) * 100)
            await asyncio.sleep(1)
        
        await asyncio.sleep(1)
        self.show_logo = True
        await asyncio.sleep(2)
        
        # Complete boot and switch to main interface
        self.boot_complete = True

def boot_screen() -> rx.Component:
    """Mac-style boot screen"""
    return rx.center(
        rx.vstack(
            # Apple-style logo placeholder
            rx.box(
                "🖥️",
                font_size="120px",
                margin_bottom="2rem"
            ),
            
            rx.text(
                "CodeChronOS",
                font_size="48px",
                font_weight="bold",
                font_family="'Press Start 2P', monospace",
                color="#333",
                margin_bottom="1rem"
            ),
            
            rx.text(
                "A journey through software development",
                font_size="18px",
                color="#666",
                margin_bottom="3rem"
            ),
            
            # Progress bar
            rx.progress(
                value=HomeState.progress,
                width="300px",
                height="8px",
                color_scheme="gray"
            ),
            
            rx.text(
                HomeState.boot_text,
                font_size="14px",
                color="#888",
                font_family="'VT323', monospace",
                margin_top="1rem"
            ),
            
            # Boot stages indicator
            rx.hstack(
                *[
                    rx.box(
                        width="12px",
                        height="12px",
                        border_radius="50%",
                        bg=rx.cond(
                            HomeState.boot_stage >= i,
                            "#4ade80",
                            "#e5e7eb"
                        ),
                        margin="0 4px"
                    )
                    for i in range(6)
                ],
                margin_top="2rem"
            ),
            
            spacing="4",
            align="center"
        ),
        width="100vw",
        height="100vh",
        bg="linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%)"
    )

def era_selection() -> rx.Component:
    """Era selection interface after boot"""
    return rx.center(
        rx.vstack(
            rx.text(
                "Choose Your Development Era",
                font_size="36px",
                font_weight="bold",
                margin_bottom="3rem",
                text_align="center",
                color="#1a1a1a"  # Explicit dark color to prevent gray inheritance
            ),
            
            rx.hstack(
                # 1984 Mac Era
                rx.box(
                    rx.vstack(
                        rx.text("🖥️", font_size="80px"),
                        rx.text(
                            "Mac 1984",
                            font_size="24px",
                            font_weight="bold",
                            color="#1a1a1a"  # Darker for better contrast
                        ),
                        rx.text(
                            "Classic Macintosh interface with pixel-perfect retro charm",
                            font_size="14px",
                            color="#666",
                            text_align="center",
                            max_width="200px"
                        ),
                        rx.button(
                            "Enter 1984",
                            on_click=lambda: rx.redirect("/maccode"),
                            color_scheme="gray",
                            size="3",
                            margin_top="1rem"
                        ),
                        spacing="3",
                        align="center"
                    ),
                    padding="2rem",
                    border="2px solid #e5e7eb",
                    border_radius="12px",
                    bg="white",
                    cursor="pointer",
                    _hover={
                        "transform": "translateY(-5px)",
                        "box_shadow": "0 10px 25px rgba(0,0,0,0.1)",
                        "border_color": "#cbd5e1"
                    },
                    transition="all 0.3s ease"
                ),
                
                # 2015 Block Era  
                rx.box(
                    rx.vstack(
                        rx.text("🧱", font_size="80px"),
                        rx.text(
                            "Block 2015",
                            font_size="24px", 
                            font_weight="bold",
                            color="#3b82f6"
                        ),
                        rx.text(
                            "Visual block-based coding with drag-and-drop simplicity",
                            font_size="14px",
                            color="#666",
                            text_align="center",
                            max_width="200px"
                        ),
                        rx.button(
                            "Enter 2015",
                            on_click=lambda: rx.redirect("/blockcode"),
                            color_scheme="blue",
                            size="3",
                            margin_top="1rem"
                        ),
                        spacing="3",
                        align="center"
                    ),
                    padding="2rem",
                    border="2px solid #bfdbfe",
                    border_radius="12px",
                    bg="white",
                    cursor="pointer",
                    _hover={
                        "transform": "translateY(-5px)",
                        "box_shadow": "0 10px 25px rgba(59, 130, 246, 0.1)",
                        "border_color": "#93c5fd"
                    },
                    transition="all 0.3s ease"
                ),
                
                # 2025 AI Era
                rx.box(
                    rx.vstack(
                        rx.text("🧞", font_size="80px"),
                        rx.text(
                            "Vibe 2025",
                            font_size="24px",
                            font_weight="bold",
                            color="#8b5cf6"
                        ),
                        rx.text(
                            "AI-powered natural language development environment",
                            font_size="14px",
                            color="#666",
                            text_align="center",
                            max_width="200px"
                        ),
                        rx.button(
                            "Enter 2025",
                            on_click=lambda: rx.redirect("/vibecode"),
                            color_scheme="purple",
                            size="3",
                            margin_top="1rem"
                        ),
                        spacing="3",
                        align="center"
                    ),
                    padding="2rem",
                    border="2px solid #ddd6fe",
                    border_radius="12px",
                    bg="white",
                    cursor="pointer",
                    _hover={
                        "transform": "translateY(-5px)",
                        "box_shadow": "0 10px 25px rgba(139, 92, 246, 0.1)",
                        "border_color": "#c4b5fd"
                    },
                    transition="all 0.3s ease"
                ),
                
                # Python 202X Era
                rx.box(
                    rx.vstack(
                        rx.text("🐍", font_size="80px"),
                        rx.text(
                            "Python 202X",
                            font_size="24px",
                            font_weight="bold",
                            color="#16a34a"
                        ),
                        rx.text(
                            "Classic Python playground with games and tools",
                            font_size="14px",
                            color="#666",
                            text_align="center",
                            max_width="200px"
                        ),
                        rx.button(
                            "Enter Playground",
                            on_click=lambda: rx.redirect("/playground"),
                            color_scheme="green", 
                            size="3",
                            margin_top="1rem"
                        ),
                        spacing="3",
                        align="center"
                    ),
                    padding="2rem",
                    border="2px solid #bbf7d0",
                    border_radius="12px",
                    bg="white",
                    cursor="pointer",
                    _hover={
                        "transform": "translateY(-5px)",
                        "box_shadow": "0 10px 25px rgba(22, 163, 74, 0.1)",
                        "border_color": "#86efac"
                    },
                    transition="all 0.3s ease"
                ),
                
                spacing="4",
                justify="center"
            ),
            
            rx.text(
                "Click on any era to begin your journey through software development history",
                font_size="16px",
                color="#6b7280",  # Better gray color
                text_align="center",
                margin_top="3rem"
            ),
            
            spacing="4",
            align="center"
        ),
        width="100vw",
        height="100vh",
        bg="linear-gradient(135deg, #fafafa 0%, #f0f0f0 100%)"
    )

def home_page() -> rx.Component:
    """Main home page component"""
    return rx.cond(
        HomeState.show_logo,
        era_selection(),
        rx.box(
            boot_screen(),
            on_mount=HomeState.start_boot_sequence
        )
    )
