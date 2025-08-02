"""
CodeChronOS - Main Application Entry Point
A journey through software development eras: 1984 → 2015 → 2025
"""

import reflex as rx
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import pages
from .pages.home import home_page
from .pages.maccode import maccode_page
from .pages.blockcode import blockcode_page
from .pages.vibecode import vibecode_page
from .pages.mutation_log import mutation_log_page

# Import utils
from .utils.theme_switcher import ThemeSwitcher
from .utils.audio_player import AudioPlayer

class State(rx.State):
    """Global application state"""
    current_era: str = "1984"  # 1984, 2015, 2025
    theme_mode: str = "mac1984"  # mac1984, block2015, vibe2025
    boot_complete: bool = False
    audio_enabled: bool = True
    
    def set_era(self, era: str):
        """Switch between development eras"""
        self.current_era = era
        if era == "1984":
            self.theme_mode = "mac1984"
        elif era == "2015":
            self.theme_mode = "block2015"
        elif era == "2025":
            self.theme_mode = "vibe2025"
    
    def complete_boot(self):
        """Mark boot sequence as complete"""
        self.boot_complete = True
    
    def toggle_audio(self):
        """Toggle audio on/off"""
        self.audio_enabled = not self.audio_enabled
    
    def start_mac_era(self):
        """Start Mac 1984 era"""
        self.set_era("1984")
        self.complete_boot()
    
    def start_block_era(self):
        """Start Block 2015 era"""
        self.set_era("2015")
        self.complete_boot()
    
    def start_vibe_era(self):
        """Start Vibe 2025 era"""
        self.set_era("2025")
        self.complete_boot()

def navbar() -> rx.Component:
    """Navigation bar with era switching"""
    return rx.hstack(
        rx.text(
            "CodeChronOS",
            font_size="1.5rem",
            font_weight="bold",
            color="white"
        ),
        rx.spacer(),
        rx.hstack(
            rx.button(
                "Mac 1984",
                on_click=State.set_era("1984"),
                variant="ghost",
                color_scheme="gray"
            ),
            rx.button(
                "Block 2015",
                on_click=State.set_era("2015"),
                variant="ghost",
                color_scheme="blue"
            ),
            rx.button(
                "Vibe 2025",
                on_click=State.set_era("2025"),
                variant="ghost",
                color_scheme="purple"
            ),
            spacing="2"
        ),
        justify="between",
        align="center",
        width="100%",
        padding="1rem",
        bg="rgba(0,0,0,0.8)",
        backdrop_filter="blur(10px)"
    )

def welcome_screen() -> rx.Component:
    """Welcome screen with era selection"""
    return rx.center(
        rx.vstack(
            rx.text(
                "Welcome to CodeChronOS",
                font_size="3rem",
                font_weight="bold",
                text_align="center",
                background="linear-gradient(45deg, #667eea, #764ba2)",
                background_clip="text",
                color="transparent"
            ),
            rx.text(
                "Experience the evolution of software development",
                font_size="1.2rem",
                color="gray.600",
                text_align="center",
                margin_bottom="32px"
            ),
            rx.hstack(
                rx.vstack(
                    rx.text("🖥️", font_size="4rem"),
                    rx.text("Mac 1984", font_weight="bold"),
                    rx.text("Classic Mac development", color="gray.600"),
                    rx.button(
                        "Enter Mac Era",
                        on_click=State.start_mac_era,
                        color_scheme="gray",
                        size="3"
                    ),
                    align="center",
                    spacing="2",
                    padding="2rem",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="8px"
                ),
                rx.vstack(
                    rx.text("🧩", font_size="4rem"),
                    rx.text("Block 2015", font_weight="bold"),
                    rx.text("Visual programming", color="gray.600"),
                    rx.button(
                        "Enter Block Era",
                        on_click=State.start_block_era,
                        color_scheme="blue",
                        size="3"
                    ),
                    align="center",
                    spacing="2",
                    padding="2rem",
                    border="1px solid",
                    border_color="blue.200",
                    border_radius="8px"
                ),
                rx.vstack(
                    rx.text("🤖", font_size="4rem"),
                    rx.text("Vibe 2025", font_weight="bold"),
                    rx.text("AI-powered coding", color="gray.600"),
                    rx.button(
                        "Enter AI Era",
                        on_click=State.start_vibe_era,
                        color_scheme="purple",
                        size="3"
                    ),
                    align="center",
                    spacing="2",
                    padding="2rem",
                    border="1px solid",
                    border_color="purple.200",
                    border_radius="8px"
                ),
                spacing="4"
            ),
            spacing="4",
            align="center"
        ),
        height="100vh",
        width="100%"
    )

def era_content() -> rx.Component:
    """Content area that changes based on selected era"""
    return rx.cond(
        State.current_era == "1984",
        maccode_page(),
        rx.cond(
            State.current_era == "2015",
            blockcode_page(),
            vibecode_page()
        )
    )

def index() -> rx.Component:
    """Main application layout"""
    return rx.box(
        rx.cond(
            State.boot_complete,
            rx.vstack(
                navbar(),
                era_content(),
                spacing="0"
            ),
            home_page()
        ),
        width="100vw",
        height="100vh"
    )

# Create the Reflex app
app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="medium",
        scaling="100%"
    )
)

# Add the main page
app.add_page(index)
app.add_page(maccode_page, route="/maccode")
app.add_page(blockcode_page, route="/blockcode") 
app.add_page(vibecode_page, route="/vibecode")
app.add_page(mutation_log_page, route="/logs")
