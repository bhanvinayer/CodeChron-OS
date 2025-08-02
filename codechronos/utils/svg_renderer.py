"""
SVG Renderer - Handles SVG graphics and icons
"""

from typing import Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET

class SVGRenderer:
    """Renders SVG graphics and icons for the application"""
    
    def __init__(self):
        self.icons = {}
        self.graphics = {}
        self.load_default_icons()
    
    def load_default_icons(self):
        """Load default icon set"""
        self.icons.update({
            "calculator": self.create_calculator_icon(),
            "notepad": self.create_notepad_icon(),
            "macdraw": self.create_paint_icon(),
            "breakout": self.create_game_icon(),
            "folder": self.create_folder_icon(),
            "file": self.create_file_icon(),
            "block": self.create_block_icon(),
            "ai": self.create_ai_icon(),
            "settings": self.create_settings_icon(),
            "close": self.create_close_icon(),
            "minimize": self.create_minimize_icon(),
            "maximize": self.create_maximize_icon()
        })
    
    def create_calculator_icon(self) -> str:
        """Create calculator icon SVG"""
        return """
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="4" width="24" height="24" rx="2" fill="#333" stroke="#000" stroke-width="2"/>
            <rect x="6" y="6" width="20" height="6" fill="#000"/>
            <text x="16" y="10" text-anchor="middle" fill="#0f0" font-family="monospace" font-size="4">888.88</text>
            
            <!-- Buttons -->
            <rect x="6" y="14" width="4" height="3" fill="#ddd" stroke="#999"/>
            <rect x="11" y="14" width="4" height="3" fill="#ddd" stroke="#999"/>
            <rect x="16" y="14" width="4" height="3" fill="#ddd" stroke="#999"/>
            <rect x="21" y="14" width="5" height="3" fill="#f66" stroke="#999"/>
            
            <rect x="6" y="18" width="4" height="3" fill="#ddd" stroke="#999"/>
            <rect x="11" y="18" width="4" height="3" fill="#ddd" stroke="#999"/>
            <rect x="16" y="18" width="4" height="3" fill="#ddd" stroke="#999"/>
            <rect x="21" y="18" width="5" height="3" fill="#f66" stroke="#999"/>
            
            <rect x="6" y="22" width="4" height="4" fill="#ddd" stroke="#999"/>
            <rect x="11" y="22" width="4" height="3" fill="#ddd" stroke="#999"/>
            <rect x="16" y="22" width="4" height="3" fill="#ddd" stroke="#999"/>
            <rect x="21" y="22" width="5" height="4" fill="#6f6" stroke="#999"/>
        </svg>
        """
    
    def create_notepad_icon(self) -> str:
        """Create notepad icon SVG"""
        return """
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <rect x="6" y="4" width="20" height="24" fill="white" stroke="#000" stroke-width="2"/>
            <rect x="6" y="4" width="20" height="4" fill="#ddd"/>
            <line x1="8" y1="12" x2="24" y2="12" stroke="#000" stroke-width="1"/>
            <line x1="8" y1="16" x2="22" y2="16" stroke="#000" stroke-width="1"/>
            <line x1="8" y1="20" x2="20" y2="20" stroke="#000" stroke-width="1"/>
            <line x1="8" y1="24" x2="18" y2="24" stroke="#000" stroke-width="1"/>
            
            <!-- Spiral binding -->
            <circle cx="10" cy="6" r="1" fill="none" stroke="#000"/>
            <circle cx="14" cy="6" r="1" fill="none" stroke="#000"/>
            <circle cx="18" cy="6" r="1" fill="none" stroke="#000"/>
            <circle cx="22" cy="6" r="1" fill="none" stroke="#000"/>
        </svg>
        """
    
    def create_paint_icon(self) -> str:
        """Create paint/draw icon SVG"""
        return """
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="4" width="24" height="18" fill="white" stroke="#000" stroke-width="2"/>
            
            <!-- Palette -->
            <circle cx="8" cy="8" r="2" fill="#f00"/>
            <circle cx="12" cy="8" r="2" fill="#0f0"/>
            <circle cx="16" cy="8" r="2" fill="#00f"/>
            <circle cx="20" cy="8" r="2" fill="#ff0"/>
            
            <!-- Brush -->
            <line x1="24" y1="24" x2="28" y2="28" stroke="#8B4513" stroke-width="2"/>
            <circle cx="26" cy="26" r="2" fill="#000"/>
            
            <!-- Paint stroke -->
            <path d="M 6 14 Q 12 12 18 16 Q 24 20 26 18" stroke="#f00" stroke-width="2" fill="none"/>
        </svg>
        """
    
    def create_game_icon(self) -> str:
        """Create game/breakout icon SVG"""
        return """
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="4" width="24" height="20" fill="#000" stroke="#333" stroke-width="2"/>
            
            <!-- Bricks -->
            <rect x="6" y="6" width="3" height="2" fill="#f00"/>
            <rect x="10" y="6" width="3" height="2" fill="#f60"/>
            <rect x="14" y="6" width="3" height="2" fill="#ff0"/>
            <rect x="18" y="6" width="3" height="2" fill="#0f0"/>
            <rect x="22" y="6" width="4" height="2" fill="#00f"/>
            
            <rect x="6" y="9" width="3" height="2" fill="#f60"/>
            <rect x="10" y="9" width="3" height="2" fill="#ff0"/>
            <rect x="14" y="9" width="3" height="2" fill="#0f0"/>
            <rect x="18" y="9" width="3" height="2" fill="#00f"/>
            <rect x="22" y="9" width="4" height="2" fill="#f0f"/>
            
            <!-- Ball -->
            <circle cx="16" cy="16" r="1" fill="white"/>
            
            <!-- Paddle -->
            <rect x="12" y="20" width="8" height="2" fill="white"/>
        </svg>
        """
    
    def create_folder_icon(self) -> str:
        """Create folder icon SVG"""
        return """
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <path d="M 4 8 L 4 26 L 28 26 L 28 10 L 16 10 L 14 8 Z" fill="#ffd700" stroke="#000" stroke-width="1"/>
            <path d="M 4 8 L 14 8 L 16 10 L 28 10 L 28 8 L 16 8 L 14 6 L 4 6 Z" fill="#ffed4e"/>
        </svg>
        """
    
    def create_file_icon(self) -> str:
        """Create file icon SVG"""
        return """
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <path d="M 6 4 L 6 28 L 26 28 L 26 12 L 18 4 Z" fill="white" stroke="#000" stroke-width="2"/>
            <path d="M 18 4 L 18 12 L 26 12" fill="#ddd" stroke="#000" stroke-width="1"/>
            <line x1="8" y1="16" x2="24" y2="16" stroke="#000"/>
            <line x1="8" y1="20" x2="22" y2="20" stroke="#000"/>
            <line x1="8" y1="24" x2="20" y2="24" stroke="#000"/>
        </svg>
        """
    
    def create_block_icon(self) -> str:
        """Create block/puzzle piece icon SVG"""
        return """
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <path d="M 4 8 L 12 8 L 12 4 L 16 4 L 16 8 L 24 8 L 24 16 L 28 16 L 28 20 L 24 20 L 24 28 L 16 28 L 16 24 L 12 24 L 12 28 L 4 28 Z" 
                  fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
            <circle cx="10" cy="14" r="2" fill="white"/>
            <circle cx="18" cy="14" r="2" fill="white"/>
        </svg>
        """
    
    def create_ai_icon(self) -> str:
        """Create AI/brain icon SVG"""
        return """
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="12" fill="#8b5cf6" stroke="#7c3aed" stroke-width="2"/>
            
            <!-- Neural network pattern -->
            <circle cx="12" cy="12" r="1.5" fill="white"/>
            <circle cx="20" cy="12" r="1.5" fill="white"/>
            <circle cx="16" cy="16" r="1.5" fill="white"/>
            <circle cx="12" cy="20" r="1.5" fill="white"/>
            <circle cx="20" cy="20" r="1.5" fill="white"/>
            
            <line x1="12" y1="12" x2="16" y2="16" stroke="white" stroke-width="1"/>
            <line x1="20" y1="12" x2="16" y2="16" stroke="white" stroke-width="1"/>
            <line x1="16" y1="16" x2="12" y2="20" stroke="white" stroke-width="1"/>
            <line x1="16" y1="16" x2="20" y2="20" stroke="white" stroke-width="1"/>
            <line x1="12" y1="12" x2="20" y2="12" stroke="white" stroke-width="0.5"/>
            <line x1="12" y1="20" x2="20" y2="20" stroke="white" stroke-width="0.5"/>
        </svg>
        """
    
    def create_settings_icon(self) -> str:
        """Create settings/gear icon SVG"""
        return """
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <path d="M 16 4 L 18 4 L 18.5 8 L 20.5 8.5 L 23 6.5 L 25.5 9 L 23.5 11.5 L 24 13.5 L 28 14 L 28 16 L 24 16.5 L 23.5 18.5 L 25.5 21 L 23 23.5 L 20.5 21.5 L 18.5 22 L 18 26 L 16 26 L 15.5 22 L 13.5 21.5 L 11 23.5 L 8.5 21 L 10.5 18.5 L 10 16.5 L 6 16 L 6 14 L 10 13.5 L 10.5 11.5 L 8.5 9 L 11 6.5 L 13.5 8.5 L 15.5 8 Z" 
                  fill="#666" stroke="#000" stroke-width="1"/>
            <circle cx="17" cy="15" r="4" fill="white" stroke="#000"/>
            <circle cx="17" cy="15" r="2" fill="#666"/>
        </svg>
        """
    
    def create_close_icon(self) -> str:
        """Create close (X) icon SVG"""
        return """
        <svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
            <circle cx="8" cy="8" r="7" fill="#ff5f57" stroke="#cc4d47"/>
            <line x1="5" y1="5" x2="11" y2="11" stroke="white" stroke-width="2"/>
            <line x1="11" y1="5" x2="5" y2="11" stroke="white" stroke-width="2"/>
        </svg>
        """
    
    def create_minimize_icon(self) -> str:
        """Create minimize (-) icon SVG"""
        return """
        <svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
            <circle cx="8" cy="8" r="7" fill="#ffbd2e" stroke="#cc961f"/>
            <line x1="5" y1="8" x2="11" y2="8" stroke="white" stroke-width="2"/>
        </svg>
        """
    
    def create_maximize_icon(self) -> str:
        """Create maximize (□) icon SVG"""
        return """
        <svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
            <circle cx="8" cy="8" r="7" fill="#28ca42" stroke="#209934"/>
            <rect x="5" y="5" width="6" height="6" fill="none" stroke="white" stroke-width="1.5"/>
        </svg>
        """
    
    def get_icon(self, name: str) -> Optional[str]:
        """Get SVG icon by name"""
        return self.icons.get(name)
    
    def create_mac_cursor(self) -> str:
        """Create Mac-style cursor SVG"""
        return """
        <svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
            <polygon points="0,0 0,12 4,8 7,11 9,9 6,6 10,2" fill="black"/>
            <polygon points="1,1 1,10 3,8 6,10 7,9 4,6 8,3" fill="white"/>
        </svg>
        """
    
    def create_loading_spinner(self, color: str = "#3b82f6") -> str:
        """Create animated loading spinner SVG"""
        return f"""
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="12" fill="none" stroke="#e5e7eb" stroke-width="3"/>
            <circle cx="16" cy="16" r="12" fill="none" stroke="{color}" stroke-width="3" 
                    stroke-linecap="round" stroke-dasharray="75.36" stroke-dashoffset="75.36">
                <animateTransform attributeName="transform" type="rotate" 
                                values="0 16 16;360 16 16" dur="1s" repeatCount="indefinite"/>
            </circle>
        </svg>
        """
    
    def create_progress_bar(self, progress: float, width: int = 200, height: int = 20) -> str:
        """Create progress bar SVG"""
        filled_width = int(width * progress)
        
        return f"""
        <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
            <rect x="0" y="0" width="{width}" height="{height}" fill="#e5e7eb" stroke="#d1d5db" rx="10"/>
            <rect x="2" y="2" width="{filled_width-4}" height="{height-4}" fill="#3b82f6" rx="8"/>
        </svg>
        """
    
    def create_window_controls(self, style: str = "mac") -> str:
        """Create window control buttons SVG"""
        if style == "mac":
            return """
            <svg width="60" height="16" viewBox="0 0 60 16" xmlns="http://www.w3.org/2000/svg">
                <circle cx="8" cy="8" r="6" fill="#ff5f57" stroke="#cc4d47"/>
                <circle cx="24" cy="8" r="6" fill="#ffbd2e" stroke="#cc961f"/>
                <circle cx="40" cy="8" r="6" fill="#28ca42" stroke="#209934"/>
            </svg>
            """
        else:
            return """
            <svg width="60" height="16" viewBox="0 0 60 16" xmlns="http://www.w3.org/2000/svg">
                <rect x="2" y="2" width="12" height="12" fill="#ddd" stroke="#999"/>
                <rect x="22" y="2" width="12" height="12" fill="#ddd" stroke="#999"/>
                <rect x="42" y="2" width="12" height="12" fill="#ddd" stroke="#999"/>
                <text x="8" y="10" text-anchor="middle" font-size="8">−</text>
                <text x="28" y="10" text-anchor="middle" font-size="8">□</text>
                <text x="48" y="10" text-anchor="middle" font-size="8">×</text>
            </svg>
            """
    
    def create_era_badge(self, era: str) -> str:
        """Create era identification badge SVG"""
        colors = {
            "mac1984": {"bg": "#666", "text": "white"},
            "block2015": {"bg": "#3b82f6", "text": "white"},
            "vibe2025": {"bg": "#8b5cf6", "text": "white"}
        }
        
        color = colors.get(era, {"bg": "#666", "text": "white"})
        
        return f"""
        <svg width="80" height="24" viewBox="0 0 80 24" xmlns="http://www.w3.org/2000/svg">
            <rect x="0" y="0" width="80" height="24" fill="{color['bg']}" rx="12"/>
            <text x="40" y="16" text-anchor="middle" fill="{color['text']}" font-size="10" font-weight="bold">
                {era.upper()}
            </text>
        </svg>
        """
    
    def optimize_svg(self, svg_content: str) -> str:
        """Optimize SVG content by removing unnecessary attributes"""
        # Basic optimization - remove extra whitespace
        lines = [line.strip() for line in svg_content.split('\n') if line.strip()]
        return ' '.join(lines)
    
    def svg_to_data_url(self, svg_content: str) -> str:
        """Convert SVG to data URL for embedding"""
        import base64
        encoded = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
        return f"data:image/svg+xml;base64,{encoded}"

# Global instance
svg_renderer = SVGRenderer()
