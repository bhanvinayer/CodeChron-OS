"""
Python Playground 202X - Collection of Classic Python Apps
"""

import reflex as rx
from typing import List, Dict, Any
from ..components.snake_game import snake_game
from ..components.todo_app import todo_app
from ..components.translator_app import translator_app
from ..components.memory_game import memory_game
from ..components.calculator2 import calculator_component as calculator2_component
from ..components.qr_generator_app import qr_generator_app
from ..components.password_generator_app import password_generator_app

class PlaygroundState(rx.State):
    """State for Python Playground era"""
    current_app: str = "home"
    apps_launched: List[str] = []
    high_scores: Dict[str, int] = {"snake": 0, "pong": 0}
    
    def launch_app(self, app_name: str):
        """Launch a playground app"""
        self.current_app = app_name
        if app_name not in self.apps_launched:
            self.apps_launched.append(app_name)
    
    def go_home(self):
        """Return to playground home"""
        self.current_app = "home"
    
    def update_high_score(self, game: str, score: int):
        """Update high score for games"""
        if score > self.high_scores.get(game, 0):
            self.high_scores[game] = score

def app_tile(name: str, icon: str, description: str, app_id: str, color: str = "#4A90E2") -> rx.Component:
    """Create an app tile for the playground"""
    return rx.box(
        rx.vstack(
            rx.text(
                icon,
                font_size="3rem",
                margin_bottom="0.5rem"
            ),
            rx.text(
                name,
                font_size="1.1rem",
                font_weight="bold",
                color="white",
                margin_bottom="0.3rem"
            ),
            rx.text(
                description,
                font_size="0.85rem",
                color="rgba(255,255,255,0.8)",
                text_align="center",
                line_height="1.3"
            ),
            align="center",
            spacing="1"
        ),
        bg=f"linear-gradient(135deg, {color}, {color}dd)",
        border_radius="12px",
        padding="1.5rem",
        width="180px",
        height="180px",
        cursor="pointer",
        box_shadow="0 4px 15px rgba(0,0,0,0.2)",
        _hover={
            "transform": "translateY(-5px) scale(1.02)",
            "box_shadow": "0 8px 30px rgba(0,0,0,0.3)",
        },
        transition="all 0.3s ease",
        on_click=lambda: PlaygroundState.launch_app(app_id)
    )

def playground_home() -> rx.Component:
    """Python Playground home screen with app grid"""
    return rx.vstack(
        # Header
        rx.box(
            rx.vstack(
                rx.text(
                    "🐍",
                    font_size="4rem",
                    margin_bottom="0.5rem"
                ),
                rx.text(
                    "Python Playground 202X",
                    font_size="2.5rem",
                    font_weight="bold",
                    color="#2E7D32",
                    margin_bottom="0.3rem"
                ),
                rx.text(
                    "Classic Games & Utilities Collection",
                    font_size="1.2rem",
                    color="#666",
                    margin_bottom="1rem"
                ),
                rx.text(
                    f"Apps Launched: {PlaygroundState.apps_launched.length()}",
                    font_size="0.9rem",
                    color="#888",
                    bg="#f0f0f0",
                    padding="0.3rem 0.8rem",
                    border_radius="20px"
                ),
                align="center"
            ),
            padding="2rem",
            width="100%"
        ),
        # Apps Grid (2 rows, 4 columns)
        rx.box(
            rx.grid(
                app_tile("Snake Game", "🐍", "Classic snake game with scoring", "snake", "#4CAF50"),
                app_tile("Todo List", "📝", "Task management app", "todo", "#607D8B"),
                app_tile("Memory Game", "🧠", "Test your memory skills", "memory", "#9C27B0"),
                app_tile("Translator", "🌐", "Multi-language translator", "translator", "#2196F3"),
                app_tile("Calculator", "🧮", "Advanced calculator", "calculator", "#795548"),
                app_tile("QR Generator", "📱", "Generate QR codes", "qr", "#3F51B5"),
                app_tile("Password Gen", "🔐", "Secure password generator", "password", "#FF5722"),
                app_tile("Text Editor", "📄", "Simple text editor", "editor", "#009688"),
                columns="4",
                gap="2rem",
                width="100%"
            ),
            max_width="1200px",
            margin="0 auto",
            padding="0 2rem"
        ),
        width="100%",
        min_height="100vh",
        bg="linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%)",
        spacing="0"
    )

def playground_page() -> rx.Component:
    """Main playground page component"""
    return rx.cond(
        PlaygroundState.current_app == "home",
        playground_home(),
        rx.vstack(
            # Back button
            rx.hstack(
                rx.button(
                    "← Back to Playground",
                    on_click=PlaygroundState.go_home,
                    variant="outline",
                    color_scheme="blue",
                    margin="1rem"
                ),
                rx.spacer(),
                justify="start",
                width="100%"
            ),
            
            # App content will be rendered here based on current_app
            rx.cond(
                PlaygroundState.current_app == "snake",
                snake_game(),
                rx.cond(
                    PlaygroundState.current_app == "memory",
                    memory_game(),
                    rx.cond(
                        PlaygroundState.current_app == "todo",
                        todo_app(),
                        rx.cond(
                            PlaygroundState.current_app == "translator",
                            translator_app(),
                            rx.cond(
                                PlaygroundState.current_app == "calculator",
                                calculator2_component(),
                                rx.cond(
                                    PlaygroundState.current_app == "editor",
                                    __import__("codechronos.components.text_editor", fromlist=["text_editor_component"]).text_editor_component(),
                                    rx.cond(
                                        PlaygroundState.current_app == "qr",
                                        qr_generator_app(),
                                        rx.cond(
                                            PlaygroundState.current_app == "password",
                                            password_generator_app(),
                                            rx.cond(
                                                PlaygroundState.current_app == "paint",
                                                rx.center(
                                                    rx.text("🎨 Digital Paint App Coming Soon!", font_size="2rem"),
                                                    height="70vh"
                                                ),
                                                rx.center(
                                                    rx.text(f"🚀 {PlaygroundState.current_app.title()} App Loading...", font_size="2rem"),
                                                    height="70vh"
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            width="100%",
            min_height="100vh",
            bg="linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%)"
        )
    )
