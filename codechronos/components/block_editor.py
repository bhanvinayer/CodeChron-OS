"""
Block Editor - Visual block-based coding interface (2015 era)
"""

import reflex as rx
import json
from typing import List, Dict, Any

class CanvasBlock(rx.Base):
    """Model for a canvas block"""
    id: int
    type: str
    x: int
    y: int
    parameters: Dict[str, str]

class BlockEditorState(rx.State):
    """State for block-based coding editor"""
    blocks: List[Dict[str, Any]] = []
    selected_block_type: str = "print"
    canvas_blocks: List[CanvasBlock] = []
    generated_code: str = ""
    editing_block_id: int = -1
    edit_parameter: str = ""
    edit_value: str = ""
    
    def add_block(self, block_type: str):
        """Add a new block to the canvas"""
        new_block = CanvasBlock(
            id=len(self.canvas_blocks),
            type=block_type,
            x=100,
            y=100 + len(self.canvas_blocks) * 60,
            parameters=self.get_default_parameters(block_type)
        )
        self.canvas_blocks.append(new_block)
    
    def start_editing(self, block_id: int, parameter: str, current_value: str):
        """Start editing a block parameter"""
        self.editing_block_id = block_id
        self.edit_parameter = parameter
        self.edit_value = current_value
    
    def save_edit(self):
        """Save the edited parameter value"""
        if self.editing_block_id >= 0 and self.editing_block_id < len(self.canvas_blocks):
            self.canvas_blocks[self.editing_block_id].parameters[self.edit_parameter] = self.edit_value
        self.editing_block_id = -1
        self.edit_parameter = ""
        self.edit_value = ""
    
    def cancel_edit(self):
        """Cancel editing"""
        self.editing_block_id = -1
        self.edit_parameter = ""
        self.edit_value = ""
    
    def set_edit_value(self, value: str):
        """Set the edit value"""
        self.edit_value = value
    
    def get_default_parameters(self, block_type: str) -> Dict[str, str]:
        """Get default parameters for block type"""
        defaults = {
            "constant": {"name": "PI", "value": "3.14159"},
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
            if block.type == "constant":
                name = block.parameters['name']
                value = block.parameters['value']
                code_lines.append(f"{name} = {value}")
            elif block.type == "print":
                code_lines.append(f"print('{block.parameters['text']}')")
            elif block.type == "variable":
                code_lines.append(f"{block.parameters['name']} = {block.parameters['value']}")
            elif block.type == "if":
                code_lines.append(f"if {block.parameters['condition']}:")
                code_lines.append("    pass  # Add your code here")
            elif block.type == "for":
                var = block.parameters['variable']
                start = block.parameters['start']
                end = block.parameters['end']
                code_lines.append(f"for {var} in range({start}, {end}):")
                code_lines.append("    pass  # Add your code here")
            elif block.type == "function":
                name = block.parameters['name']
                params = block.parameters['params']
                code_lines.append(f"def {name}({params}):")
                code_lines.append("    pass  # Add your code here")
            elif block.type == "button":
                text = block.parameters['text']
                action = block.parameters['action']
                code_lines.append(f"# Button: {text}")
                code_lines.append(f"# Action: {action}")
            elif block.type == "input":
                label = block.parameters['label']
                var = block.parameters['variable']
                code_lines.append(f"{var} = input('{label}')")
            elif block.type == "slider":
                var = block.parameters['variable']
                min_val = block.parameters['min']
                max_val = block.parameters['max']
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
                "Constant", 
                on_click=lambda: BlockEditorState.add_block("constant"),
                width="120px",
                color_scheme="indigo",
                style={"background": "linear-gradient(45deg, #C7D2FE, #A5B4FC)"}  # Pastel indigo
            ),
            rx.button(
                "Print", 
                on_click=lambda: BlockEditorState.add_block("print"),
                width="120px",
                color_scheme="blue",
                style={"background": "linear-gradient(45deg, #93C5FD, #60A5FA)"}  # Pastel blue
            ),
            rx.button(
                "Variable",
                on_click=lambda: BlockEditorState.add_block("variable"), 
                width="120px",
                color_scheme="green",
                style={"background": "linear-gradient(45deg, #86EFAC, #4ADE80)"}  # Pastel green
            ),
            rx.button(
                "If Statement",
                on_click=lambda: BlockEditorState.add_block("if"),
                width="120px", 
                color_scheme="orange",
                style={"background": "linear-gradient(45deg, #FCD34D, #F59E0B)"}  # Pastel orange
            ),
            rx.button(
                "For Loop",
                on_click=lambda: BlockEditorState.add_block("for"),
                width="120px",
                color_scheme="purple", 
                style={"background": "linear-gradient(45deg, #C4B5FD, #A78BFA)"}  # Pastel purple
            ),
            rx.button(
                "Function",
                on_click=lambda: BlockEditorState.add_block("function"),
                width="120px",
                color_scheme="red",
                style={"background": "linear-gradient(45deg, #FCA5A5, #F87171)"}  # Pastel red
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
                style={"background": "linear-gradient(45deg, #5EEAD4, #2DD4BF)"}  # Pastel teal
            ),
            rx.button(
                "Text Input", 
                on_click=lambda: BlockEditorState.add_block("input"),
                width="120px",
                color_scheme="cyan",
                style={"background": "linear-gradient(45deg, #67E8F9, #22D3EE)"}  # Pastel cyan
            ),
            rx.button(
                "Slider",
                on_click=lambda: BlockEditorState.add_block("slider"),
                width="120px",
                color_scheme="pink",
                style={"background": "linear-gradient(45deg, #F9A8D4, #EC4899)"}  # Pastel pink
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

def render_block(block: CanvasBlock) -> rx.Component:
    """Render a single block with editable parameters"""
    
    # Get block color
    block_color = rx.cond(
        block.type == "constant", "#C7D2FE",   # Pastel indigo for constants
        rx.cond(
            block.type == "print", "#93C5FD",      # Pastel blue
            rx.cond(
                block.type == "variable", "#86EFAC",   # Pastel green
                rx.cond(
                    block.type == "if", "#FCD34D",         # Pastel orange
                    rx.cond(
                        block.type == "for", "#C4B5FD",        # Pastel purple
                        rx.cond(
                            block.type == "function", "#FCA5A5",   # Pastel red
                            rx.cond(
                                block.type == "button", "#5EEAD4",     # Pastel teal
                                rx.cond(
                                    block.type == "input", "#67E8F9",      # Pastel cyan
                                    "#F9A8D4"                              # Pastel pink (slider)
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    
    # Create parameter display based on block type using rx.cond
    parameter_display = rx.cond(
        block.type == "constant",
        rx.vstack(
            rx.text(f"name: {block.parameters['name']}", size="1", color="white"),
            rx.text(f"value: {block.parameters['value']}", size="1", color="white"),
            spacing="1"
        ),
        rx.cond(
            block.type == "print",
            rx.text(f"text: {block.parameters['text']}", size="1", color="white"),
            rx.cond(
                block.type == "variable",
                rx.vstack(
                    rx.text(f"name: {block.parameters['name']}", size="1", color="white"),
                    rx.text(f"value: {block.parameters['value']}", size="1", color="white"),
                    spacing="1"
                ),
                rx.cond(
                    block.type == "if",
                    rx.text(f"condition: {block.parameters['condition']}", size="1", color="white"),
                    rx.cond(
                        block.type == "for",
                        rx.vstack(
                            rx.text(f"variable: {block.parameters['variable']}", size="1", color="white"),
                            rx.text(f"start: {block.parameters['start']}", size="1", color="white"),
                            rx.text(f"end: {block.parameters['end']}", size="1", color="white"),
                            spacing="1"
                        ),
                        rx.cond(
                            block.type == "function",
                            rx.vstack(
                                rx.text(f"name: {block.parameters['name']}", size="1", color="white"),
                                rx.text(f"params: {block.parameters['params']}", size="1", color="white"),
                                spacing="1"
                            ),
                            rx.cond(
                                block.type == "button",
                                rx.vstack(
                                    rx.text(f"text: {block.parameters['text']}", size="1", color="white"),
                                    rx.text(f"action: {block.parameters['action']}", size="1", color="white"),
                                    spacing="1"
                                ),
                                rx.cond(
                                    block.type == "input",
                                    rx.vstack(
                                        rx.text(f"label: {block.parameters['label']}", size="1", color="white"),
                                        rx.text(f"variable: {block.parameters['variable']}", size="1", color="white"),
                                        spacing="1"
                                    ),
                                    rx.cond(
                                        block.type == "slider",
                                        rx.vstack(
                                            rx.text(f"min: {block.parameters['min']}", size="1", color="white"),
                                            rx.text(f"max: {block.parameters['max']}", size="1", color="white"),
                                            rx.text(f"variable: {block.parameters['variable']}", size="1", color="white"),
                                            spacing="1"
                                        ),
                                        rx.text("No parameters", size="1", color="white")
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    
    return rx.box(
        rx.vstack(
            rx.text(
                block.type.upper(),
                size="2",
                weight="bold",
                color="white"
            ),
            # Display parameters based on block type
            parameter_display,
            spacing="2"
        ),
        padding="0.8em 1.2em",
        margin="0.5rem",
        bg=block_color,
        border_radius="6px",
        cursor="pointer",
        width="fit-content",
        min_width="150px",
        max_width="200px",
        text_align="center",
        box_shadow="0 2px 4px rgba(0,0,0,0.15)",
        style={
            "&:hover": {
                "transform": "translateY(-1px)",
                "box_shadow": "0 3px 6px rgba(0,0,0,0.25)"
            }
        }
    )

def block_canvas() -> rx.Component:
    """Canvas area for arranging blocks"""
    return rx.box(
        rx.vstack(
            rx.text("Block Canvas", size="4", weight="bold"),
            rx.box(
                rx.foreach(
                    BlockEditorState.canvas_blocks,
                    render_block
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
            justify="between",
            width="100%"
        ),
        rx.code_block(
            rx.cond(
                BlockEditorState.generated_code != "",
                BlockEditorState.generated_code,
                "# Click 'Generate' to see Python code"
            ),
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
