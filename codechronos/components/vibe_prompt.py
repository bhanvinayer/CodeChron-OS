"""
Vibe Prompt - AI-powered natural language coding interface (2025 era)
"""

import reflex as rx
from typing import List, Dict, Any
import asyncio
import json
import os

class VibePromptState(rx.State):
    """State for AI prompt interface"""
    prompt: str = ""
    generated_code: str = ""
    creativity_level: float = 0.7
    is_generating: bool = False
    chat_history: List[Dict[str, Any]] = []
    error_message: str = ""
    dark_mode: bool = False
    
    # OpenAI configuration
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", "")
    
    def toggle_dark_mode(self):
        """Toggle dark mode"""
        self.dark_mode = not self.dark_mode
    
    def update_prompt(self, new_prompt: str):
        """Update the current prompt"""
        self.prompt = new_prompt
    
    def set_creativity(self, level: float):
        """Set creativity level (affects GPT temperature)"""
        self.creativity_level = level
    
    async def generate_code(self):
        """Generate code from natural language prompt using OpenAI"""
        if not self.prompt.strip():
            return
        
        self.is_generating = True
        self.error_message = ""
        
        # Add to chat history
        self.chat_history.append({
            "type": "user",
            "content": self.prompt,
            "timestamp": "now"
        })
        
        # Generate code with OpenAI
        try:
            await self.openai_generate_code()
        except Exception as e:
            self.error_message = f"OpenAI Error: {str(e)}"
            # Fallback to simulation if API fails
            await self.simulate_ai_response()
        
        self.is_generating = False
        self.prompt = ""
    
    async def openai_generate_code(self):
        """Generate code using OpenAI API with HTTP requests"""
        import aiohttp
        
        try:
            system_prompt = f"""You are an expert Reflex (Python web framework) developer. Generate clean, working Reflex code based on the user's request.

Guidelines:
- Use Reflex components (rx.text, rx.button, rx.vstack, etc.)
- Include proper state management with rx.State
- Make the code functional and runnable
- Add appropriate styling with Reflex's CSS-in-Python approach
- Creativity level: {self.creativity_level} (0.1 = conservative, 1.0 = very creative)
- Generate complete, working Reflex code that can be run immediately
- Always include proper imports and state classes
- Use modern Reflex syntax and best practices

Return only the Python code, no explanations."""
            
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": self.prompt}
                ],
                "temperature": self.creativity_level,
                "max_tokens": 2000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        generated_code = result["choices"][0]["message"]["content"].strip()
                        
                        # Clean up the code (remove markdown formatting if present)
                        if generated_code.startswith("```python"):
                            generated_code = generated_code[9:]
                        if generated_code.startswith("```"):
                            generated_code = generated_code[3:]
                        if generated_code.endswith("```"):
                            generated_code = generated_code[:-3]
                        
                        self.generated_code = generated_code.strip()
                        
                        # Add AI response to chat
                        self.chat_history.append({
                            "type": "assistant", 
                            "content": "✅ Generated custom Reflex app using OpenAI GPT-4!",
                            "code": self.generated_code,
                            "timestamp": "now"
                        })
                    else:
                        error_text = await response.text()
                        raise Exception(f"API Error {response.status}: {error_text}")
                        
        except Exception as e:
            self.error_message = f"OpenAI API Error: {str(e)}"
            raise e
    
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
            "content": f"⚠️ Using fallback simulation - {prompt_lower.split()[0] if prompt_lower.split() else 'custom'} app generated!",
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
    
    def copy_code(self):
        """Copy generated code to clipboard"""
        return rx.set_clipboard(self.generated_code)
    
    def save_app(self):
        """Save the generated app to file"""
        if not self.generated_code:
            return
        
        # Generate a filename based on the prompt or timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_app_{timestamp}.py"
        
        # Save to data/saved_apps directory
        import os
        save_dir = "data/saved_apps"
        os.makedirs(save_dir, exist_ok=True)
        
        file_path = os.path.join(save_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.generated_code)
        
        # Add confirmation to chat
        self.chat_history.append({
            "type": "assistant",
            "content": f"✅ App saved successfully as '{filename}' in {save_dir}/",
            "timestamp": "now"
        })
    
    def preview_app(self):
        """Preview the generated app (simulate running it)"""
        if not self.generated_code:
            return
        
        # Add preview notification to chat
        self.chat_history.append({
            "type": "assistant", 
            "content": "🚀 Preview functionality - In a full implementation, this would open the app in a new window or tab. For now, you can copy the code and run it locally with 'reflex run'.",
            "timestamp": "now"
        })

def creativity_slider() -> rx.Component:
    """Slider to control AI creativity level with clean design"""
    return rx.vstack(
        rx.text(
            f"Creativity Level: {VibePromptState.creativity_level:.1f}", 
            size="4",
            color=rx.cond(VibePromptState.dark_mode, "#E5E7EB", "#374151"),
            weight="medium"
        ),
        rx.slider(
            default_value=0.7,
            min=0.1,
            max=1.0,
            step=0.1,
            on_change=lambda value: VibePromptState.set_creativity(value),
            width="200px",
            color_scheme="blue"
        ),
        rx.text(
            "Higher = More experimental", 
            size="3",
            color=rx.cond(VibePromptState.dark_mode, "#9CA3AF", "#6B7280")
        ),
        spacing="3",
        align="center"
    )

def prompt_input() -> rx.Component:
    """Main prompt input area with clean, modern styling"""
    return rx.vstack(
        # Error message display with subtle styling
        rx.cond(
            VibePromptState.error_message != "",
            rx.box(
                rx.hstack(
                    rx.icon("alert-circle", size=18, color="#DC2626"),
                    rx.text(
                        VibePromptState.error_message,
                        color="#DC2626",
                        size="4",
                        weight="medium"
                    ),
                    spacing="3",
                    align="center"
                ),
                bg=rx.cond(VibePromptState.dark_mode, "#1F1F1F", "#FEF2F2"),
                border=rx.cond(VibePromptState.dark_mode, "1px solid #DC2626", "1px solid #FCA5A5"),
                border_radius="8px",
                padding="16px 20px",
                width="100%"
            ),
            rx.box()
        ),
        
        # Clean text input area
        rx.text_area(
            placeholder="Describe the app you want to create...\n\nExamples:\n• Create a calculator with history\n• Build a todo list with categories\n• Make a weather dashboard",
            value=VibePromptState.prompt,
            on_change=VibePromptState.update_prompt,
            width="100%",
            height="140px",
            font_size="18px",
            bg=rx.cond(VibePromptState.dark_mode, "#1F2937", "white"),
            border=rx.cond(VibePromptState.dark_mode, "1px solid #374151", "1px solid #D1D5DB"),
            border_radius="8px",
            padding="20px",
            color=rx.cond(VibePromptState.dark_mode, "#F9FAFB", "#111827"),
            resize="none",
            _focus={
                "border_color": "#3B82F6",
                "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.15)",
                "outline": "none"
            },
            _placeholder={"color": rx.cond(VibePromptState.dark_mode, "#0D0D0E", "#6A6F78")}
        ),
        
        # Action bar with modern button styling
        rx.hstack(
            rx.button(
                rx.hstack(
                    rx.icon("shuffle", size=18),
                    rx.text("Surprise Me", size="4"),
                    spacing="3",
                    align="center"
                ),
                variant="outline",
                size="3",
                bg=rx.cond(VibePromptState.dark_mode, "#1F2937", "white"),
                color=rx.cond(VibePromptState.dark_mode, "#D1D5DB", "#6B7280"),
                border=rx.cond(VibePromptState.dark_mode, "1px solid #374151", "1px solid #D1D5DB"),
                border_radius="8px",
                _hover={
                    "bg": rx.cond(VibePromptState.dark_mode, "#374151", "#F9FAFB"),
                    "border_color": rx.cond(VibePromptState.dark_mode, "#4B5563", "#9CA3AF"),
                    "color": rx.cond(VibePromptState.dark_mode, "#F3F4F6", "#374151")
                },
                on_click=VibePromptState.surprise_me
            ),
            rx.spacer(),
            creativity_slider(),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon("sparkles", size=18),
                    rx.text("Generate Code", size="4", weight="medium"),
                    spacing="3",
                    align="center"
                ),
                loading=VibePromptState.is_generating,
                size="4",
                bg="#3B82F6",
                color="white",
                border="none",
                border_radius="8px",
                box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
                _hover={
                    "bg": "#2563EB",
                    "transform": "translateY(-1px)",
                    "box_shadow": "0 4px 8px rgba(0, 0, 0, 0.15)"
                },
                on_click=VibePromptState.generate_code
            ),
            align="center",
            width="100%"
        ),
        spacing="5",
        width="100%",
        bg=rx.cond(VibePromptState.dark_mode, "#111827", "white"),
        border=rx.cond(VibePromptState.dark_mode, "1px solid #374151", "1px solid #E5E7EB"),
        border_radius="12px",
        padding="24px",
        box_shadow="0 2px 4px rgba(0, 0, 0, 0.08)"
    )

def chat_history() -> rx.Component:
    """Display chat history with clean, modern design"""
    return rx.vstack(
        # Clean header with subtle clear button
        rx.hstack(
            rx.text(
                "Conversation", 
                size="6",
                weight="bold",
                color=rx.cond(VibePromptState.dark_mode, "#F9FAFB", "#111827")
            ),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon("trash-2", size=16),
                    rx.text("Clear", size="3"),
                    spacing="2",
                    align="center"
                ),
                on_click=VibePromptState.clear_chat,
                variant="ghost",
                size="2",
                color=rx.cond(VibePromptState.dark_mode, "#9CA3AF", "#6B7280"),
                _hover={
                    "bg": rx.cond(VibePromptState.dark_mode, "#374151", "#F3F4F6"),
                    "color": rx.cond(VibePromptState.dark_mode, "#D1D5DB", "#374151")
                }
            ),
            justify="between",
            align="center",
            width="100%",
            margin_bottom="4"
        ),
        
        # Chat messages container
        rx.box(
            rx.foreach(
                VibePromptState.chat_history.to(List[Dict[str, Any]]),
                lambda msg: rx.box(
                    rx.hstack(
                        rx.box(
                            rx.icon(
                                rx.cond(msg["type"] == "user", "user", "bot"),
                                size=18,
                                color=rx.cond(msg["type"] == "user", "#3B82F6", "#8B5CF6")
                            ),
                            bg=rx.cond(msg["type"] == "user", "#EBF8FF", "#F3E8FF"),
                            border_radius="8px",
                            padding="8px",
                            flex_shrink="0"
                        ),
                        rx.vstack(
                            rx.text(
                                msg["content"],
                                size="4",
                                color=rx.cond(VibePromptState.dark_mode, "#F9FAFB", "#111827"),
                                line_height="1.6"
                            ),
                            rx.cond(
                                msg.get("code", ""),
                                rx.code_block(
                                    msg.get("code", ""),
                                    language="python",
                                    width="100%",
                                    bg="#1F2937",
                                    color="#F9FAFB",
                                    border_radius="8px",
                                    font_size="14px",
                                    margin_top="3"
                                ),
                                rx.box()
                            ),
                            align="start",
                            width="100%",
                            spacing="0"
                        ),
                        align="start",
                        spacing="4",
                        width="100%"
                    ),
                    padding="16px",
                    margin_bottom="3",
                    bg=rx.cond(VibePromptState.dark_mode, "#1F2937", "white"),
                    border=rx.cond(VibePromptState.dark_mode, "1px solid #374151", "1px solid #F3F4F6"),
                    border_radius="8px",
                    border_left=rx.cond(
                        msg["type"] == "user", 
                        "4px solid #3B82F6", 
                        "4px solid #8B5CF6"
                    ),
                    _hover={"bg": rx.cond(VibePromptState.dark_mode, "#374151", "#FAFBFC")}
                )
            ),
            height="400px",
            overflow_y="auto",
            width="100%",
            padding="16px",
            bg=rx.cond(VibePromptState.dark_mode, "#111827", "#FAFBFC"),
            border_radius="8px"
        ),
        spacing="0",
        width="100%",
        padding="24px"
    )

def code_output() -> rx.Component:
    """Display generated code with clean, modern design"""
    return rx.vstack(
        # Clean header with action buttons
        rx.hstack(
            rx.text(
                "Generated Code", 
                size="6",
                weight="bold",
                color=rx.cond(VibePromptState.dark_mode, "#F9FAFB", "#111827")
            ),
            rx.spacer(),
            rx.cond(
                VibePromptState.generated_code != "",
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon("copy", size=16),
                            rx.text("Copy", size="3"),
                            spacing="2",
                            align="center"
                        ),
                        on_click=VibePromptState.copy_code,
                        variant="outline",
                        size="2",
                        bg=rx.cond(VibePromptState.dark_mode, "#1F2937", "white"),
                        color=rx.cond(VibePromptState.dark_mode, "#9CA3AF", "#6B7280"),
                        border=rx.cond(VibePromptState.dark_mode, "1px solid #374151", "1px solid #D1D5DB"),
                        border_radius="6px",
                        _hover={
                            "bg": rx.cond(VibePromptState.dark_mode, "#374151", "#F9FAFB"),
                            "color": rx.cond(VibePromptState.dark_mode, "#D1D5DB", "#374151")
                        }
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("download", size=16),
                            rx.text("Save", size="3"),
                            spacing="2",
                            align="center"
                        ),
                        on_click=VibePromptState.save_app,
                        variant="outline",
                        size="2",
                        bg=rx.cond(VibePromptState.dark_mode, "#1F2937", "white"),
                        color="#059669",
                        border="1px solid #10B981",
                        border_radius="6px",
                        _hover={
                            "bg": rx.cond(VibePromptState.dark_mode, "#064E3B", "#ECFDF5"),
                            "color": "#047857"
                        }
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("play", size=16),
                            rx.text("Preview", size="3"),
                            spacing="2",
                            align="center"
                        ),
                        on_click=VibePromptState.preview_app,
                        variant="outline",
                        size="2",
                        bg=rx.cond(VibePromptState.dark_mode, "#1F2937", "white"),
                        color="#2563EB",
                        border="1px solid #3B82F6",
                        border_radius="6px",
                        _hover={
                            "bg": rx.cond(VibePromptState.dark_mode, "#1E3A8A", "#EBF8FF"),
                            "color": "#1D4ED8"
                        }
                    ),
                    spacing="3"
                ),
                rx.box()
            ),
            justify="between",
            align="center",
            width="100%",
            margin_bottom="4"
        ),
        
        # Code display area
        rx.cond(
            VibePromptState.generated_code != "",
            rx.code_block(
                VibePromptState.generated_code,
                language="python",
                width="100%",
                height="400px",
                bg="#1F2937",
                color="#F9FAFB",
                border_radius="8px",
                font_size="14px",
                overflow_y="auto",
                padding="20px"
            ),
            rx.box(
                rx.vstack(
                    rx.icon("file-text", size=56, color=rx.cond(VibePromptState.dark_mode, "#4B5563", "#D1D5DB")),
                    rx.text(
                        "Generated code will appear here",
                        color=rx.cond(VibePromptState.dark_mode, "#9CA3AF", "#6B7280"),
                        size="4",
                        text_align="center",
                        weight="medium"
                    ),
                    rx.text(
                        "Describe your app above and click Generate Code",
                        color=rx.cond(VibePromptState.dark_mode, "#6B7280", "#9CA3AF"),
                        size="3",
                        text_align="center"
                    ),
                    spacing="4",
                    align="center"
                ),
                height="400px",
                bg=rx.cond(VibePromptState.dark_mode, "#111827", "#FAFBFC"),
                border=rx.cond(VibePromptState.dark_mode, "2px dashed #374151", "2px dashed #D1D5DB"),
                border_radius="8px",
                display="flex",
                align_items="center",
                justify_content="center",
                width="100%"
            )
        ),
        spacing="0",
        width="100%",
        padding="24px"
    )

def vibe_prompt_component() -> rx.Component:
    """Complete AI prompt interface with modern, clean design"""
    return rx.vstack(
        # Modern gradient header with glassmorphism effect
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.icon("zap", size=28, color="white"),
                        bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        border_radius="12px",
                        padding="8px",
                        box_shadow="0 4px 15px rgba(102, 126, 234, 0.3)"
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text(
                                "VibeCode",
                                size="8",
                                weight="bold",
                                color=rx.cond(VibePromptState.dark_mode, "#FFFFFF", "#1F2937"),
                                background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                background_clip="text",
                                _webkit_background_clip="text",
                                _webkit_text_fill_color="transparent"
                            ),
                            rx.box(
                                rx.text(
                                    "2025",
                                    size="3",
                                    weight="bold",
                                    color="white"
                                ),
                                bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                border_radius="6px",
                                padding="2px 8px",
                                margin_left="2"
                            ),
                            align="baseline",
                            spacing="1"
                        ),
                        rx.text(
                            "AI-Powered Natural Language Coding",
                            size="3",
                            color=rx.cond(VibePromptState.dark_mode, "#9CA3AF", "#6B7280"),
                            weight="medium"
                        ),
                        spacing="1",
                        align="start"
                    ),
                    align="center",
                    spacing="4"
                ),
                rx.spacer(),
                rx.hstack(
                    rx.button(
                        rx.icon(
                            rx.cond(VibePromptState.dark_mode, "sun", "moon"), 
                            size=20
                        ),
                        on_click=VibePromptState.toggle_dark_mode,
                        variant="ghost",
                        size="3",
                        color=rx.cond(VibePromptState.dark_mode, "#F9FAFB", "#6B7280"),
                        bg=rx.cond(VibePromptState.dark_mode, "rgba(255, 255, 255, 0.1)", "rgba(0, 0, 0, 0.05)"),
                        border_radius="10px",
                        _hover={
                            "bg": rx.cond(VibePromptState.dark_mode, "rgba(255, 255, 255, 0.2)", "rgba(0, 0, 0, 0.1)"),
                            "transform": "scale(1.05)"
                        }
                    ),
                    spacing="3"
                ),
                justify="between",
                align="center",
                width="100%"
            ),
            bg=rx.cond(
                VibePromptState.dark_mode,
                "linear-gradient(135deg, #1F2937 0%, #111827 100%)",
                "linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)"
            ),
            border_bottom=rx.cond(
                VibePromptState.dark_mode,
                "1px solid #374151",
                "1px solid #E5E7EB"
            ),
            padding="20px 32px",
            box_shadow=rx.cond(
                VibePromptState.dark_mode,
                "0 4px 6px rgba(0, 0, 0, 0.3)",
                "0 4px 6px rgba(0, 0, 0, 0.1)"
            ),
            width="100%",
            backdrop_filter="blur(10px)"
        ),
        
        # Main content area with improved spacing
        rx.box(
            rx.vstack(
                prompt_input(),
                # Two-panel layout with closer spacing and subtle visual separation
                rx.hstack(
                    rx.box(
                        chat_history(),
                        width="48%",
                        bg=rx.cond(VibePromptState.dark_mode, "#1F2937", "white"),
                        border=rx.cond(VibePromptState.dark_mode, "1px solid #374151", "1px solid #E5E7EB"),
                        border_radius="12px",
                        box_shadow=rx.cond(
                            VibePromptState.dark_mode,
                            "0 4px 6px rgba(0, 0, 0, 0.3)",
                            "0 4px 6px rgba(0, 0, 0, 0.08)"
                        )
                    ),
                    rx.box(
                        width="1px",
                        height="500px",
                        bg=rx.cond(VibePromptState.dark_mode, "#374151", "#E5E7EB"),
                        margin="0 12px"
                    ),
                    rx.box(
                        code_output(),
                        width="48%",
                        bg=rx.cond(VibePromptState.dark_mode, "#1F2937", "white"),
                        border=rx.cond(VibePromptState.dark_mode, "1px solid #374151", "1px solid #E5E7EB"),
                        border_radius="12px",
                        box_shadow=rx.cond(
                            VibePromptState.dark_mode,
                            "0 4px 6px rgba(0, 0, 0, 0.3)",
                            "0 4px 6px rgba(0, 0, 0, 0.08)"
                        )
                    ),
                    width="100%",
                    align="start",
                    justify="between"
                ),
                spacing="6",
                width="100%"
            ),
            padding="16px 32px 0px 32px",
            width="100%"
        ),
        
        spacing="0",
        width="100%",
        height="100vh",
        bg=rx.cond(
            VibePromptState.dark_mode,
            "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)",
            "linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%)"
        ),
        style={
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif"
        }
    )
