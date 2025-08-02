"""
VibeCode Page - 2025 AI-powered development environment
"""

import reflex as rx
from typing import List
from ..components.vibe_prompt import vibe_prompt_component

class VibeCodeState(rx.State):
    """State for VibeCode 2025 interface"""
    ai_mode: str = "creative"  # creative, precise, experimental
    show_welcome: bool = True
    session_apps: List[str] = []
    
    def set_ai_mode(self, mode: str):
        """Set AI generation mode"""
        self.ai_mode = mode
    
    def dismiss_welcome(self):
        """Dismiss welcome screen"""
        self.show_welcome = False

def floating_nav() -> rx.Component:
    """Floating navigation with AI mode selector"""
    return rx.box(
        rx.hstack(
            rx.text("🧞 VibeCode", font_size="16px", font_weight="bold", color="white"),
            rx.spacer(),
            rx.hstack(
                rx.button(
                    "Creative",
                    on_click=lambda: VibeCodeState.set_ai_mode("creative"),
                    variant=rx.cond(VibeCodeState.ai_mode == "creative", "soft", "outline"),
                    color_scheme="purple",
                    size="2"
                ),
                rx.button(
                    "Precise", 
                    on_click=lambda: VibeCodeState.set_ai_mode("precise"),
                    variant=rx.cond(VibeCodeState.ai_mode == "precise", "soft", "outline"),
                    color_scheme="blue",
                    size="2"
                ),
                rx.button(
                    "Experimental",
                    on_click=lambda: VibeCodeState.set_ai_mode("experimental"),
                    variant=rx.cond(VibeCodeState.ai_mode == "experimental", "soft", "outline"),
                    color_scheme="pink",
                    size="2"
                ),
                spacing="2"
            ),
            align="center",
            width="100%"
        ),
        position="fixed",
        top="20px",
        left="50%",
        transform="translateX(-50%)",
        width="90%",
        max_width="1200px", 
        padding="1rem",
        bg="rgba(139, 92, 246, 0.9)",
        backdrop_filter="blur(10px)",
        border_radius="50px",
        border="1px solid rgba(255,255,255,0.2)",
        box_shadow="0 8px 32px rgba(139, 92, 246, 0.3)",
        z_index="1000"
    )

def welcome_screen() -> rx.Component:
    """Welcome screen for new users"""
    return rx.center(
        rx.box(
            rx.vstack(
                rx.text(
                    "🧞",
                    font_size="120px",
                    margin_bottom="1rem"
                ),
                rx.text(
                    "Welcome to VibeCode 2025",
                    font_size="48px",
                    font_weight="bold",
                    background="linear-gradient(45deg, #8b5cf6, #ec4899)",
                    background_clip="text",
                    color="transparent",
                    text_align="center"
                ),
                rx.text(
                    "The future of development is here",
                    font_size="20px",
                    color="#64748b",
                    text_align="center",
                    margin_bottom="2rem"
                ),
                
                rx.vstack(
                    rx.text("✨ Describe what you want to build in natural language", font_size="16px"),
                    rx.text("🎯 AI generates production-ready Python code", font_size="16px"),
                    rx.text("🚀 Instant preview and testing", font_size="16px"),
                    rx.text("🔧 Refine and iterate with conversational commands", font_size="16px"),
                    spacing="2",
                    align="start",
                    margin_bottom="3rem"
                ),
                
                rx.hstack(
                    rx.button(
                        "Start Creating",
                        on_click=VibeCodeState.dismiss_welcome,
                        size="4",
                        color_scheme="purple",
                        style={
                            "background": "linear-gradient(45deg, #8b5cf6, #7c3aed)",
                            "box_shadow": "0 4px 15px rgba(139, 92, 246, 0.3)"
                        }
                    ),
                    rx.button(
                        "Watch Demo",
                        variant="outline",
                        size="4",
                        color_scheme="purple"
                    ),
                    spacing="3"
                ),
                
                spacing="4",
                align="center",
                max_width="600px"
            ),
            padding="4rem",
            text_align="center"
        ),
        width="100vw",
        height="100vh",
        bg="linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(236, 72, 153, 0.1))"
    )

def ai_status_indicator() -> rx.Component:
    """Show current AI mode and status"""
    return rx.box(
        rx.hstack(
            rx.box(
                width="8px",
                height="8px",
                border_radius="50%",
                bg="#10b981",
                style={
                    "animation": "pulse 2s infinite"
                }
            ),
            rx.text(
                f"AI Mode: {VibeCodeState.ai_mode.title()}",
                font_size="12px",
                color="white"
            ),
            spacing="2"
        ),
        position="fixed",
        bottom="20px",
        right="20px",
        padding="0.5rem 1rem",
        bg="rgba(0,0,0,0.7)",
        border_radius="20px",
        backdrop_filter="blur(10px)"
    )

def background_effects() -> rx.Component:
    """Animated background effects"""
    return rx.box(
        # Animated gradient orbs
        rx.box(
            width="300px",
            height="300px",
            border_radius="50%",
            bg="radial-gradient(circle, rgba(139, 92, 246, 0.3), transparent)",
            position="absolute",
            top="-150px",
            right="-150px",
            style={
                "animation": "float 6s ease-in-out infinite"
            }
        ),
        rx.box(
            width="200px", 
            height="200px",
            border_radius="50%",
            bg="radial-gradient(circle, rgba(236, 72, 153, 0.2), transparent)",
            position="absolute",
            bottom="-100px",
            left="-100px",
            style={
                "animation": "float 8s ease-in-out infinite reverse"
            }
        ),
        position="fixed",
        top="0",
        left="0",
        width="100%",
        height="100%",
        pointer_events="none",
        z_index="-1"
    )

def vibecode_page() -> rx.Component:
    """Complete VibeCode 2025 interface"""
    return rx.box(
        # Custom CSS for animations
        rx.html(
            """
            <style>
                @keyframes float {
                    0%, 100% { transform: translateY(0px) rotate(0deg); }
                    33% { transform: translateY(-20px) rotate(5deg); }
                    66% { transform: translateY(10px) rotate(-3deg); }
                }
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
            </style>
            """
        ),
        
        background_effects(),
        
        rx.cond(
            VibeCodeState.show_welcome,
            welcome_screen(),
            rx.box(
                floating_nav(),
                rx.box(
                    vibe_prompt_component(),
                    padding_top="100px"
                ),
                ai_status_indicator()
            )
        ),
        
        width="100vw",
        height="100vh",
        bg="linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)",
        color="white",
        overflow_x="hidden"
    )
