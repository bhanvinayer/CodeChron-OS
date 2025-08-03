#!/usr/bin/env python3
"""
Demo script to showcase the improved VibeCode UI
Run this to see the enhanced interface with:
- Larger fonts throughout
- Modern gradient header
- Better spacing between panels
- Full dark theme support
- Glassmorphism effects
"""

import reflex as rx
from codechronos.components.vibe_prompt import vibe_prompt_component, VibePromptState

def index():
    """Main page with improved VibeCode interface"""
    return vibe_prompt_component()

# Configure the app
app = rx.App(
    style={
        "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif",
    }
)

app.add_page(index, route="/")

if __name__ == "__main__":
    print("🚀 Starting improved VibeCode UI Demo...")
    print("✨ Features:")
    print("   • Dramatically increased font sizes")
    print("   • Modern gradient header with glassmorphism")
    print("   • Closer spacing between Conversation and Generated Code")
    print("   • Full dark theme support (click moon/sun icon)")
    print("   • Enhanced visual aesthetics")
    print("   • Improved button and interaction styling")
    print("\n🌙 Try the dark theme toggle in the top-right!")
    print("📱 Open http://localhost:3000 in your browser")
    
    app.run(debug=True)
