"""
Block Editor - Visual block-based coding interface (2015 era)
"""

import reflex as rx
import json

class BlockEditorState(rx.State):
    """State for block-based coding editor"""
    blocks: list = []
    selected_block_type: str = "print"
    canvas_blocks: list = []
    generated_code: str = ""
    
    def add_block(self, block_type: str):
        """Add a new block to the canvas"""
        new_block = {
            "id": len(self.canvas_blocks),
            "type": block_type,
            "x": 100,
            "y": 100 + len(self.canvas_blocks) * 60,
            "parameters": self.get_default_parameters(block_type)
        }
        self.canvas_blocks.append(new_block)
    
    def get_default_parameters(self, block_type: str) -> dict:
        """Get default parameters for block type"""
        defaults = {
            "print": {"text": "Hello World!"},
            "variable": {"name": "x", "value": "10"},
            "if": {"condition": "x > 5"},
            "for": {"variable": "i", "start": "0", "end": "10"},
            "function": {"name": "my_function", "params": ""},
            "button": {"text": "Click me", "action": "print('Clicked!')"},
            "input": {"label": "Enter text:", "variable": "user_input"},
            "slider": {"min": "0", "max": "100", "variable": "slider_value"}
        }
        return defaults.get(block_type, {})
    
    def generate_code(self):
        """Generate Python code from blocks"""
        code_lines = []
        
        for block in self.canvas_blocks:
            if block["type"] == "print":
                code_lines.append(f"print('{block['parameters']['text']}')")
            elif block["type"] == "variable":
                code_lines.append(f"{block['parameters']['name']} = {block['parameters']['value']}")
            elif block["type"] == "if":
                code_lines.append(f"if {block['parameters']['condition']}:")
                code_lines.append("    pass  # Add your code here")
            elif block["type"] == "for":
                var = block['parameters']['variable']
                start = block['parameters']['start']
                end = block['parameters']['end']
                code_lines.append(f"for {var} in range({start}, {end}):")
                code_lines.append("    pass  # Add your code here")
            elif block["type"] == "function":
                name = block['parameters']['name']
                params = block['parameters']['params']
                code_lines.append(f"def {name}({params}):")
                code_lines.append("    pass  # Add your code here")
            elif block["type"] == "button":
                text = block['parameters']['text']
                action = block['parameters']['action']
                code_lines.append(f"# Button: {text}")
                code_lines.append(f"# Action: {action}")
            elif block["type"] == "input":
                label = block['parameters']['label']
                var = block['parameters']['variable']
                code_lines.append(f"{var} = input('{label}')")
            elif block["type"] == "slider":
                var = block['parameters']['variable']
                min_val = block['parameters']['min']
                max_val = block['parameters']['max']
                code_lines.append(f"# Slider: {var} (range {min_val}-{max_val})")
        
        self.generated_code = "\n".join(code_lines)
    
    def clear_canvas(self):
        """Clear all blocks from canvas"""
        self.canvas_blocks = []
        self.generated_code = ""

def block_palette() -> rx.Component:
    """Palette of available blocks"""
    return rx.vstack(
        rx.text("Logic Blocks", size="3", weight="bold", color="blue"),
        rx.vstack(
            rx.button(
                "Print", 
                on_click=lambda: BlockEditorState.add_block("print"),
                width="120px",
                color_scheme="blue",
                style={"background": "linear-gradient(45deg, #3b82f6, #1d4ed8)"}
            ),
            rx.button(
                "Variable",
                on_click=lambda: BlockEditorState.add_block("variable"), 
                width="120px",
                color_scheme="green",
                style={"background": "linear-gradient(45deg, #10b981, #047857)"}
            ),
            rx.button(
                "If Statement",
                on_click=lambda: BlockEditorState.add_block("if"),
                width="120px", 
                color_scheme="orange",
                style={"background": "linear-gradient(45deg, #f59e0b, #d97706)"}
            ),
            rx.button(
                "For Loop",
                on_click=lambda: BlockEditorState.add_block("for"),
                width="120px",
                color_scheme="purple", 
                style={"background": "linear-gradient(45deg, #8b5cf6, #7c3aed)"}
            ),
            rx.button(
                "Function",
                on_click=lambda: BlockEditorState.add_block("function"),
                width="120px",
                color_scheme="red",
                style={"background": "linear-gradient(45deg, #ef4444, #dc2626)"}
            ),
            spacing="2"
        ),
        
        rx.text("UI Blocks", size="3", weight="bold", color="teal", margin_top="1rem"),
        rx.vstack(
            rx.button(
                "Button",
                on_click=lambda: BlockEditorState.add_block("button"),
                width="120px",
                color_scheme="teal",
                style={"background": "linear-gradient(45deg, #14b8a6, #0d9488)"}
            ),
            rx.button(
                "Text Input", 
                on_click=lambda: BlockEditorState.add_block("input"),
                width="120px",
                color_scheme="cyan",
                style={"background": "linear-gradient(45deg, #06b6d4, #0891b2)"}
            ),
            rx.button(
                "Slider",
                on_click=lambda: BlockEditorState.add_block("slider"),
                width="120px",
                color_scheme="pink",
                style={"background": "linear-gradient(45deg, #ec4899, #db2777)"}
            ),
            spacing="2"
        ),
        
        rx.button(
            "Clear All",
            on_click=BlockEditorState.clear_canvas,
            width="120px",
            color_scheme="gray",
            margin_top="1rem"
        ),
        
        spacing="2",
        padding="1rem",
        bg=rx.color("gray", 1),
        border_radius="8px",
        align="start"
    )

def block_canvas() -> rx.Component:
    """Canvas area for arranging blocks"""
    return rx.box(
        rx.vstack(
            rx.text("Block Canvas", size="4", weight="bold"),
            rx.box(
                rx.foreach(
                    BlockEditorState.canvas_blocks,
                    lambda block: rx.box(
                        rx.text(
                            f"{block['type'].upper()}",
                            size="2",
                            weight="bold",
                            color="white"
                        ),
                        padding="0.5rem",
                        margin="0.5rem",
                        bg=rx.cond(
                            block["type"] == "print", "blue",
                            rx.cond(
                                block["type"] == "variable", "green",
                                rx.cond(
                                    block["type"] == "if", "orange",
                                    rx.cond(
                                        block["type"] == "for", "purple",
                                        rx.cond(
                                            block["type"] == "function", "red",
                                            "teal"
                                        )
                                    )
                                )
                            )
                        ),
                        border_radius="8px",
                        border="2px solid white",
                        cursor="move",
                        style={
                            "box_shadow": "0 4px 8px rgba(0,0,0,0.2)",
                            "transform": "rotate(-2deg)"
                        }
                    )
                ),
                min_height="300px",
                width="100%",
                bg=rx.color("gray", 2),
                border="2px dashed #ccc",
                border_radius="8px",
                padding="1rem"
            ),
            spacing="2"
        ),
        width="100%"
    )

def code_preview() -> rx.Component:
    """Preview generated Python code"""
    return rx.vstack(
        rx.hstack(
            rx.text("Generated Code", size="4", weight="bold"),
            rx.button(
                "Generate",
                on_click=BlockEditorState.generate_code,
                color_scheme="blue",
                size="2"
            ),
            justify="space-between",
            width="100%"
        ),
        rx.code_block(
            BlockEditorState.generated_code or "# Click 'Generate' to see Python code",
            language="python",
            width="100%",
            min_height="200px"
        ),
        spacing="2",
        width="100%"
    )

def block_editor_component() -> rx.Component:
    """Complete block editor interface"""
    return rx.hstack(
        block_palette(),
        rx.vstack(
            block_canvas(),
            code_preview(),
            spacing="4",
            width="100%"
        ),
        spacing="4",
        width="100%",
        height="100%",
        align="start"
    )
