"""
Theme Switcher - Handles theme switching between eras
"""

import reflex as rx
from typing import Dict, Any

class ThemeSwitcher:
    """Manages theme switching across different eras"""
    
    def __init__(self):
        self.themes = {
            "mac1984": {
                "name": "Mac 1984",
                "primary_color": "#000000",
                "secondary_color": "#ffffff", 
                "background": "#f0f0f0",
                "accent": "#666666",
                "font_family": "'Press Start 2P', monospace",
                "border_style": "solid",
                "border_width": "2px",
                "box_shadow": "2px 2px 4px rgba(0,0,0,0.3)"
            },
            "block2015": {
                "name": "Block 2015",
                "primary_color": "#3b82f6",
                "secondary_color": "#ffffff",
                "background": "linear-gradient(135deg, #dbeafe 0%, #ede9fe 100%)", 
                "accent": "#10b981",
                "font_family": "system-ui, -apple-system, sans-serif",
                "border_style": "solid",
                "border_width": "1px",
                "box_shadow": "0 4px 12px rgba(0,0,0,0.1)"
            },
            "vibe2025": {
                "name": "Vibe 2025",
                "primary_color": "#8b5cf6",
                "secondary_color": "#ec4899",
                "background": "linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)",
                "accent": "#06b6d4",
                "font_family": "system-ui, -apple-system, sans-serif",
                "border_style": "solid", 
                "border_width": "1px",
                "box_shadow": "0 8px 32px rgba(139, 92, 246, 0.3)"
            }
        }
    
    def get_theme(self, theme_name: str) -> Dict[str, Any]:
        """Get theme configuration"""
        return self.themes.get(theme_name, self.themes["mac1984"])
    
    def get_css_variables(self, theme_name: str) -> str:
        """Generate CSS variables for theme"""
        theme = self.get_theme(theme_name)
        
        css_vars = f"""
        :root {{
            --primary-color: {theme['primary_color']};
            --secondary-color: {theme['secondary_color']};
            --background: {theme['background']};
            --accent-color: {theme['accent']};
            --font-family: {theme['font_family']};
            --border-style: {theme['border_style']};
            --border-width: {theme['border_width']};
            --box-shadow: {theme['box_shadow']};
        }}
        """
        
        return css_vars
    
    def apply_theme_to_component(self, component: rx.Component, theme_name: str) -> rx.Component:
        """Apply theme styling to a component"""
        theme = self.get_theme(theme_name)
        
        # Apply theme-specific styles
        styled_component = component
        
        if theme_name == "mac1984":
            styled_component = rx.box(
                component,
                font_family=theme["font_family"],
                color=theme["primary_color"],
                style={
                    "image_rendering": "pixelated",
                    "filter": "contrast(1.1)"
                }
            )
        elif theme_name == "block2015":
            styled_component = rx.box(
                component,
                font_family=theme["font_family"],
                style={
                    "transition": "all 0.3s ease",
                    "border_radius": "8px"
                }
            )
        elif theme_name == "vibe2025":
            styled_component = rx.box(
                component,
                font_family=theme["font_family"],
                color="white",
                style={
                    "backdrop_filter": "blur(10px)",
                    "border_radius": "16px"
                }
            )
        
        return styled_component
    
    def get_button_style(self, theme_name: str) -> Dict[str, str]:
        """Get button styling for theme"""
        
        if theme_name == "mac1984":
            return {
                "background": "#ffffff",
                "border": "2px outset #cccccc",
                "font_family": "'Press Start 2P', monospace",
                "font_size": "8px",
                "padding": "8px 16px",
                "cursor": "pointer",
                "&:hover": {
                    "background": "#f0f0f0"
                },
                "&:active": {
                    "border": "2px inset #cccccc"
                }
            }
        elif theme_name == "block2015":
            return {
                "background": "linear-gradient(45deg, #3b82f6, #1d4ed8)",
                "border": "none",
                "border_radius": "8px",
                "color": "white",
                "font_weight": "600",
                "padding": "12px 24px",
                "cursor": "pointer",
                "transition": "all 0.3s ease",
                "&:hover": {
                    "transform": "translateY(-2px)",
                    "box_shadow": "0 4px 12px rgba(59, 130, 246, 0.3)"
                }
            }
        elif theme_name == "vibe2025":
            return {
                "background": "linear-gradient(45deg, #8b5cf6, #7c3aed)",
                "border": "1px solid rgba(255,255,255,0.2)",
                "border_radius": "50px",
                "color": "white",
                "font_weight": "500",
                "padding": "12px 32px",
                "cursor": "pointer",
                "backdrop_filter": "blur(10px)",
                "transition": "all 0.3s ease",
                "&:hover": {
                    "box_shadow": "0 8px 32px rgba(139, 92, 246, 0.4)",
                    "transform": "scale(1.02)"
                }
            }
        
        return {}
    
    def get_window_style(self, theme_name: str) -> Dict[str, str]:
        """Get window styling for theme"""
        
        if theme_name == "mac1984":
            return {
                "background": "white",
                "border": "2px solid black",
                "box_shadow": "4px 4px 0px rgba(0,0,0,0.5)",
                "font_family": "'Press Start 2P', monospace"
            }
        elif theme_name == "block2015":
            return {
                "background": "white",
                "border": "1px solid #e5e7eb",
                "border_radius": "12px",
                "box_shadow": "0 10px 25px rgba(0,0,0,0.1)",
                "transition": "all 0.3s ease"
            }
        elif theme_name == "vibe2025":
            return {
                "background": "rgba(255,255,255,0.1)",
                "border": "1px solid rgba(255,255,255,0.2)",
                "border_radius": "20px",
                "backdrop_filter": "blur(20px)",
                "box_shadow": "0 8px 32px rgba(0,0,0,0.3)"
            }
        
        return {}
    
    def generate_theme_css(self, theme_name: str) -> str:
        """Generate complete CSS for theme"""
        
        theme = self.get_theme(theme_name)
        
        if theme_name == "mac1984":
            return f"""
            .mac-theme {{
                font-family: 'Press Start 2P', monospace;
                image-rendering: pixelated;
                background: {theme['background']};
            }}
            
            .mac-theme .window {{
                background: white;
                border: 2px solid black;
                box-shadow: 4px 4px 0px rgba(0,0,0,0.5);
            }}
            
            .mac-theme .button {{
                background: #ffffff;
                border: 2px outset #cccccc;
                font-family: 'Press Start 2P', monospace;
                font-size: 8px;
                padding: 8px 16px;
            }}
            
            .mac-theme .button:hover {{
                background: #f0f0f0;
            }}
            
            .mac-theme .button:active {{
                border: 2px inset #cccccc;
            }}
            
            .draggable-window {{
                cursor: move;
            }}
            """
        
        elif theme_name == "block2015":
            return f"""
            .block-theme {{
                font-family: system-ui, -apple-system, sans-serif;
                background: {theme['background']};
            }}
            
            .block-theme .block {{
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
                transform: rotate(-2deg);
            }}
            
            .block-theme .block:hover {{
                transform: rotate(0deg) scale(1.05);
                box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            }}
            
            .block-theme .button {{
                background: linear-gradient(45deg, #3b82f6, #1d4ed8);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: 600;
                padding: 12px 24px;
                transition: all 0.3s ease;
            }}
            
            .block-theme .button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            }}
            """
        
        elif theme_name == "vibe2025":
            return f"""
            .vibe-theme {{
                font-family: system-ui, -apple-system, sans-serif;
                background: {theme['background']};
                color: white;
            }}
            
            .vibe-theme .glass {{
                background: rgba(255,255,255,0.1);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 20px;
                backdrop-filter: blur(20px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }}
            
            .vibe-theme .button {{
                background: linear-gradient(45deg, #8b5cf6, #7c3aed);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 50px;
                color: white;
                font-weight: 500;
                padding: 12px 32px;
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }}
            
            .vibe-theme .button:hover {{
                box-shadow: 0 8px 32px rgba(139, 92, 246, 0.4);
                transform: scale(1.02);
            }}
            
            @keyframes float {{
                0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
                33% {{ transform: translateY(-20px) rotate(5deg); }}
                66% {{ transform: translateY(10px) rotate(-3deg); }}
            }}
            
            .vibe-theme .floating {{
                animation: float 6s ease-in-out infinite;
            }}
            """
        
        return ""

# Global instance
theme_switcher = ThemeSwitcher()
