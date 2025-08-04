"""
BlockCode Page - 2015 visual block coding environment
"""

import reflex as rx
from typing import List
from ..components.block_editor import block_editor_component

class BlockCodeState(rx.State):
    """State for BlockCode 2015 interface"""
    current_project: str = "My Awesome App"
    show_tutorial: bool = True
    
    def new_project(self):
        """Create a new project"""
        self.current_project = "Untitled Project"
    
    def hide_tutorial(self):
        """Hide the tutorial overlay"""
        self.show_tutorial = False

def project_header() -> rx.Component:
    """Project header with title and controls"""
    return rx.hstack(
        rx.hstack(
            rx.text("🧱", font_size="24px"),
            rx.text(
                "BlockCode 2015",
                font_size="24px",
                font_weight="bold",
                color="#2563eb"
            ),
            spacing="2"
        ),
        rx.spacer(),
        rx.text(
            BlockCodeState.current_project,
            font_size="18px",
            font_weight="bold"
        ),
        rx.spacer(),
        rx.hstack(
            rx.button(
                "New",
                on_click=BlockCodeState.new_project,
                color_scheme="blue",
                variant="outline"
            ),
            rx.button(
                "Share",
                color_scheme="purple",
                variant="outline"
            ),
            spacing="2"
        ),
        width="100%",
        padding="1rem 2rem",
        bg="white",
        border_bottom="2px solid #e5e7eb",
        align="center"
    )

def tutorial_overlay() -> rx.Component:
    """Tutorial overlay for first-time users"""
    return rx.box(
        rx.center(
            rx.box(
                rx.vstack(
                    rx.text(
                        "Welcome to BlockCode!",
                        font_size="28px",
                        font_weight="bold",
                        color="#2563eb"
                    ),
                    rx.text(
                        "Drag blocks from the palette to create your app visually",
                        font_size="16px",
                        color="#6b7280",
                        text_align="center"
                    ),
                    rx.vstack(
                        rx.text("📋 Logic blocks: Control your app's behavior", font_size="14px"),
                        rx.text("🎨 UI blocks: Add buttons, inputs, and visual elements", font_size="14px"),
                        rx.text("🔧 Connect blocks to build complex functionality", font_size="14px"),
                        rx.text("⚡ Generate Python code instantly", font_size="14px"),
                        spacing="1",
                        align="start"
                    ),
                    rx.button(
                        "Let's Start Building!",
                        on_click=BlockCodeState.hide_tutorial,
                        size="3",
                        color_scheme="blue"
                    ),
                    spacing="4",
                    align="center"
                ),
                padding="3rem",
                bg="white",
                border_radius="16px",
                border="2px solid #e5e7eb",
                max_width="500px",
                box_shadow="0 20px 50px rgba(0,0,0,0.1)"
            )
        ),
        position="fixed",
        top="0",
        left="0",
        width="100vw",
        height="100vh",
        bg="rgba(0,0,0,0.5)",
        z_index="9999"
    )

def side_panel() -> rx.Component:
    """Side panel with tips"""
    return rx.vstack(
        rx.text("Quick Tips", font_size="16px", font_weight="bold", color="#374151"),
        rx.vstack(
            rx.text("💡 Drag blocks to the canvas", font_size="12px", color="#6b7280"),
            rx.text("🔗 Snap blocks together", font_size="12px", color="#6b7280"),
            rx.text("⚙️ Click blocks to edit properties", font_size="12px", color="#6b7280"),
            rx.text("🚀 Hit Generate to see Python code", font_size="12px", color="#6b7280"),
            align="start",
            spacing="1"
        ),
        
        width="250px",
        height="100%",
        padding="2rem",
        bg="#f9fafb",
        border_right="2px solid #e5e7eb",
        spacing="3",
        align="start"
    )

def main_editor_area() -> rx.Component:
    """Main editing area with block editor"""
    return rx.box(
        block_editor_component(),
        width="100%",
        height="100%",
        padding="2rem",
        bg="#1A202C"  # Dark background
    )

def blockcode_page() -> rx.Component:
    """Complete BlockCode 2015 interface"""
    return rx.box(
        rx.cond(
            BlockCodeState.show_tutorial,
            tutorial_overlay(),
            rx.box()
        ),
        
        rx.vstack(
            project_header(),
            rx.hstack(
                side_panel(),
                main_editor_area(),
                spacing="0",
                width="100%",
                height="calc(100vh - 80px)"
            ),
            spacing="0"
        ),
        
        width="100vw",
        height="100vh",
        bg="#ffffff",
        font_family="system-ui, -apple-system, sans-serif"
    )
