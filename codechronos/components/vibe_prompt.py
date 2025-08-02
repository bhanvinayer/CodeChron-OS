"""
Vibe Prompt - AI-powered natural language coding interface (2025 era)
"""

import reflex as rx
from typing import List, Dict, Any

class VibePromptState(rx.State):
    """State for AI prompt interface"""
    prompt: str = ""
    generated_code: str = ""
    creativity_level: float = 0.7
    is_generating: bool = False
    chat_history: List[Dict[str, Any]] = []
    
    def update_prompt(self, new_prompt: str):
        """Update the current prompt"""
        self.prompt = new_prompt
    
    def set_creativity(self, level: float):
        """Set creativity level (affects GPT temperature)"""
        self.creativity_level = level
    
    async def generate_code(self):
        """Generate code from natural language prompt"""
        if not self.prompt.strip():
            return
        
        self.is_generating = True
        
        # Add to chat history
        self.chat_history.append({
            "type": "user",
            "content": self.prompt,
            "timestamp": "now"
        })
        
        # Simulate AI generation (replace with actual OpenAI API call)
        await self.simulate_ai_response()
        
        self.is_generating = False
        self.prompt = ""
    
    async def simulate_ai_response(self):
        """Simulate AI code generation"""
        import asyncio
        await asyncio.sleep(2)  # Simulate processing time
        
        # Simple pattern matching for demo
        prompt_lower = self.prompt.lower()
        
        if "calculator" in prompt_lower:
            code = """
import reflex as rx

class CalculatorState(rx.State):
    display: str = "0"
    
    def add_digit(self, digit: str):
        self.display = self.display + digit if self.display != "0" else digit

def calculator_app():
    return rx.vstack(
        rx.text(CalculatorState.display, font_size="2em"),
        rx.hstack(
            rx.button("1", on_click=lambda: CalculatorState.add_digit("1")),
            rx.button("2", on_click=lambda: CalculatorState.add_digit("2")),
            rx.button("3", on_click=lambda: CalculatorState.add_digit("3")),
        ),
        # Add more buttons...
    )
"""
        elif "todo" in prompt_lower or "task" in prompt_lower:
            code = """
import reflex as rx

class TodoState(rx.State):
    tasks: List[Dict[str, Any]] = []
    new_task: str = ""
    
    def add_task(self):
        if self.new_task:
            self.tasks.append({"text": self.new_task, "done": False})
            self.new_task = ""
    
    def toggle_task(self, index: int):
        self.tasks[index]["done"] = not self.tasks[index]["done"]

def todo_app():
    return rx.vstack(
        rx.heading("Todo List"),
        rx.hstack(
            rx.input(
                placeholder="Add new task...",
                value=TodoState.new_task,
                on_change=TodoState.set_new_task
            ),
            rx.button("Add", on_click=TodoState.add_task)
        ),
        rx.foreach(
            TodoState.tasks.to(List[Dict[str, Any]]),
            lambda task, i: rx.hstack(
                rx.checkbox(
                    checked=task["done"],
                    on_change=lambda _: TodoState.toggle_task(i)
                ),
                rx.text(task["text"])
            )
        )
    )
"""
        elif "weather" in prompt_lower:
            code = """
import reflex as rx
import requests

class WeatherState(rx.State):
    city: str = ""
    weather_data: dict = {}
    
    def get_weather(self):
        # Replace with actual weather API
        self.weather_data = {
            "city": self.city,
            "temperature": "22°C",
            "condition": "Sunny",
            "humidity": "60%"
        }

def weather_app():
    return rx.vstack(
        rx.heading("Weather App"),
        rx.hstack(
            rx.input(
                placeholder="Enter city...",
                value=WeatherState.city,
                on_change=WeatherState.set_city
            ),
            rx.button("Get Weather", on_click=WeatherState.get_weather)
        ),
        rx.cond(
            WeatherState.weather_data,
            rx.vstack(
                rx.text(f"City: {WeatherState.weather_data.get('city', '')}"),
                rx.text(f"Temperature: {WeatherState.weather_data.get('temperature', '')}"),
                rx.text(f"Condition: {WeatherState.weather_data.get('condition', '')}"),
                rx.text(f"Humidity: {WeatherState.weather_data.get('humidity', '')}")
            )
        )
    )
"""
        else:
            code = f"""
# Generated from prompt: "{self.prompt}"
import reflex as rx

class AppState(rx.State):
    message: str = "Hello from AI!"

def custom_app():
    return rx.vstack(
        rx.heading("AI Generated App"),
        rx.text(AppState.message),
        rx.button("Click me!", on_click=lambda: AppState.set_message("Button clicked!"))
    )

# To run this app:
# app = rx.App()
# app.add_page(custom_app)
# app.run()
"""
        
        self.generated_code = code.strip()
        
        # Add AI response to chat
        self.chat_history.append({
            "type": "assistant", 
            "content": f"I've generated a {prompt_lower.split()[0] if prompt_lower.split() else 'custom'} app for you!",
            "code": code.strip(),
            "timestamp": "now"
        })
    
    def surprise_me(self):
        """Generate a random app idea"""
        ideas = [
            "Create a colorful drawing app with different brush sizes",
            "Build a music player with playlist functionality", 
            "Make a habit tracker with progress visualization",
            "Design a password generator with security options",
            "Create a timer app with custom alerts"
        ]
        import random
        self.prompt = random.choice(ideas)
    
    def clear_chat(self):
        """Clear chat history"""
        self.chat_history = []
        self.generated_code = ""

def creativity_slider() -> rx.Component:
    """Slider to control AI creativity level"""
    return rx.vstack(
        rx.text(f"Creativity Level: {VibePromptState.creativity_level:.1f}", size="2"),
        rx.slider(
            default_value=0.7,
            min=0.1,
            max=1.0,
            step=0.1,
            on_change=lambda value: VibePromptState.set_creativity(value),
            width="200px",
            color_scheme="purple"
        ),
        rx.text("More creative = More experimental code", size="1", color="gray"),
        spacing="1",
        align="center"
    )

def prompt_input() -> rx.Component:
    """Main prompt input area"""
    return rx.vstack(
        rx.text_area(
            placeholder="Describe the app you want to create...\n\nExamples:\n• Create a calculator with history\n• Build a todo list with categories\n• Make a weather dashboard",
            value=VibePromptState.prompt,
            on_change=VibePromptState.update_prompt,
            width="100%",
            height="120px",
            font_size="16px"
        ),
        rx.hstack(
            rx.button(
                "🎲 Surprise Me",
                on_click=VibePromptState.surprise_me,
                variant="outline",
                color_scheme="purple"
            ),
            rx.spacer(),
            creativity_slider(),
            rx.spacer(),
            rx.button(
                "✨ Generate Code",
                on_click=VibePromptState.generate_code,
                loading=VibePromptState.is_generating,
                color_scheme="purple",
                size="3",
                style={
                    "background": "linear-gradient(45deg, #8b5cf6, #7c3aed)",
                    "box_shadow": "0 4px 15px rgba(139, 92, 246, 0.3)"
                }
            ),
            align="center",
            width="100%"
        ),
        spacing="3",
        width="100%"
    )

def chat_history() -> rx.Component:
    """Display chat history with user prompts and AI responses"""
    return rx.vstack(
        rx.hstack(
            rx.text("Conversation", size="4", weight="bold"),
            rx.button(
                "Clear",
                on_click=VibePromptState.clear_chat,
                size="1",
                variant="outline"
            ),
            justify="between",
            width="100%"
        ),
        rx.box(
            rx.foreach(
                VibePromptState.chat_history.to(List[Dict[str, Any]]),
                lambda msg: rx.box(
                    rx.hstack(
                        rx.avatar(
                            rx.cond(msg["type"] == "user", "👤", "🤖"),
                            size="2"
                        ),
                        rx.vstack(
                            rx.text(
                                msg["content"],
                                size="2",
                                style={"margin_bottom": "0.5rem"}
                            ),
                            rx.cond(
                                msg.get("code", ""),
                                rx.code_block(
                                    msg.get("code", ""),
                                    language="python",
                                    width="100%"
                                ),
                                rx.box()
                            ),
                            align="start",
                            width="100%"
                        ),
                        align="start",
                        spacing="3",
                        width="100%"
                    ),
                    padding="1rem",
                    margin="0.5rem 0",
                    bg=rx.cond(
                        msg["type"] == "user",
                        rx.color("blue", 2),
                        rx.color("purple", 2)
                    ),
                    border_radius="12px",
                    border_left=rx.cond(
                        msg["type"] == "user", 
                        "4px solid #3b82f6", 
                        "4px solid #8b5cf6"
                    )
                )
            ),
            max_height="400px",
            overflow_y="auto",
            width="100%"
        ),
        spacing="3",
        width="100%"
    )

def code_output() -> rx.Component:
    """Display generated code with copy functionality"""
    return rx.vstack(
        rx.text("Generated Code", size="4", weight="bold"),
        rx.cond(
            VibePromptState.generated_code != "",
            rx.vstack(
                rx.code_block(
                    VibePromptState.generated_code,
                    language="python",
                    width="100%",
                    max_height="300px"
                ),
                rx.hstack(
                    rx.button(
                        "📋 Copy Code",
                        on_click=lambda: rx.set_clipboard(VibePromptState.generated_code),
                        size="2"
                    ),
                    rx.button(
                        "💾 Save App",
                        size="2",
                        color_scheme="green"
                    ),
                    rx.button(
                        "▶️ Preview",
                        size="2",
                        color_scheme="blue"
                    ),
                    spacing="2"
                ),
                spacing="2",
                width="100%"
            ),
            rx.box(
                rx.text(
                    "Your generated code will appear here...",
                    color="gray",
                    text_align="center"
                ),
                padding="2rem",
                border="2px dashed #ccc",
                border_radius="8px",
                width="100%"
            )
        ),
        spacing="3",
        width="100%"
    )

def vibe_prompt_component() -> rx.Component:
    """Complete AI prompt interface"""
    return rx.vstack(
        rx.box(
            rx.text(
                "VibeCode 2025",
                size="8",
                weight="bold",
                background="linear-gradient(45deg, #8b5cf6, #ec4899)",
                background_clip="text",
                color="transparent"
            ),
            text_align="center",
            margin_bottom="2rem"
        ),
        
        prompt_input(),
        
        rx.hstack(
            rx.box(
                chat_history(),
                width="50%"
            ),
            rx.box(
                code_output(),
                width="50%"
            ),
            spacing="4",
            width="100%",
            align="start"
        ),
        
        spacing="4",
        width="100%",
        height="100%",
        padding="2rem",
        style={
            "background": "linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(236, 72, 153, 0.1))"
        }
    )
