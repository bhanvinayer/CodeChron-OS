"""
Block Parser - Converts visual blocks to Python code
"""

import json
from typing import List, Dict, Any
import re

class BlockParser:
    """Converts block-based visual code to Python"""
    
    def __init__(self):
        self.indent_level = 0
        self.generated_code = []
        self.imports = set()
        self.state_variables = {}
    
    def parse_blocks(self, blocks: List[Dict]) -> Dict[str, Any]:
        """
        Parse blocks and generate Python code
        
        Args:
            blocks: List of block dictionaries
            
        Returns:
            Dict with generated code and metadata
        """
        
        self.reset()
        
        try:
            # Sort blocks by position (top to bottom)
            sorted_blocks = sorted(blocks, key=lambda b: b.get('y', 0))
            
            # First pass - collect state variables and imports
            self._analyze_blocks(sorted_blocks)
            
            # Second pass - generate code
            self._generate_code(sorted_blocks)
            
            return {
                "success": True,
                "code": self._build_final_code(),
                "imports": list(self.imports),
                "state_vars": self.state_variables,
                "framework": "reflex"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "code": ""
            }
    
    def reset(self):
        """Reset parser state"""
        self.indent_level = 0
        self.generated_code = []
        self.imports = set()
        self.state_variables = {}
    
    def _analyze_blocks(self, blocks: List[Dict]):
        """First pass - analyze blocks for imports and state"""
        
        for block in blocks:
            block_type = block.get('type', '')
            
            # Add necessary imports
            if block_type in ['button', 'input', 'text', 'slider']:
                self.imports.add('import reflex as rx')
            
            # Collect state variables
            if block_type == 'variable':
                var_name = block.get('parameters', {}).get('name', 'var')
                var_value = block.get('parameters', {}).get('value', '""')
                self.state_variables[var_name] = var_value
    
    def _generate_code(self, blocks: List[Dict]):
        """Second pass - generate actual code"""
        
        for block in blocks:
            self._process_block(block)
    
    def _process_block(self, block: Dict):
        """Process individual block"""
        
        block_type = block.get('type', '')
        params = block.get('parameters', {})
        
        if block_type == 'print':
            self._add_line(f"print('{params.get('text', '')}')")
            
        elif block_type == 'variable':
            name = params.get('name', 'var')
            value = params.get('value', '""')
            self._add_line(f"{name} = {value}")
            
        elif block_type == 'if':
            condition = params.get('condition', 'True')
            self._add_line(f"if {condition}:")
            self._increase_indent()
            self._add_line("pass  # Add your code here")
            self._decrease_indent()
            
        elif block_type == 'for':
            var = params.get('variable', 'i')
            start = params.get('start', '0')
            end = params.get('end', '10')
            self._add_line(f"for {var} in range({start}, {end}):")
            self._increase_indent()
            self._add_line("pass  # Add your code here")
            self._decrease_indent()
            
        elif block_type == 'function':
            name = params.get('name', 'my_function')
            parameters = params.get('params', '')
            self._add_line(f"def {name}({parameters}):")
            self._increase_indent()
            self._add_line("pass  # Add your code here")
            self._decrease_indent()
            self._add_line("")
            
        elif block_type == 'button':
            text = params.get('text', 'Click me')
            action = params.get('action', 'print("Clicked!")')
            self._add_ui_component(f"rx.button('{text}', on_click=lambda: {action})")
            
        elif block_type == 'input':
            label = params.get('label', 'Enter text:')
            var = params.get('variable', 'user_input')
            self._add_ui_component(f"rx.input(placeholder='{label}', value={var})")
            
        elif block_type == 'slider':
            var = params.get('variable', 'slider_value')
            min_val = params.get('min', '0')
            max_val = params.get('max', '100')
            self._add_ui_component(f"rx.slider(min={min_val}, max={max_val}, value={var})")
    
    def _add_line(self, line: str):
        """Add line with proper indentation"""
        indent = "    " * self.indent_level
        self.generated_code.append(indent + line)
    
    def _add_ui_component(self, component: str):
        """Add UI component to layout"""
        # For now, just add as a line - in real implementation,
        # this would be collected and organized into proper UI structure
        self._add_line(f"# UI Component: {component}")
    
    def _increase_indent(self):
        """Increase indentation level"""
        self.indent_level += 1
    
    def _decrease_indent(self):
        """Decrease indentation level"""
        self.indent_level = max(0, self.indent_level - 1)
    
    def _build_final_code(self) -> str:
        """Build final code with proper structure"""
        
        code_parts = []
        
        # Add imports
        if self.imports:
            code_parts.extend(list(self.imports))
            code_parts.append("")
        
        # Add state class if needed
        if self.state_variables:
            code_parts.append("class AppState(rx.State):")
            for var_name, var_value in self.state_variables.items():
                code_parts.append(f"    {var_name}: str = {var_value}")
            code_parts.append("")
        
        # Add main code
        code_parts.extend(self.generated_code)
        
        # Add basic app structure if UI components exist
        has_ui = any("UI Component:" in line for line in self.generated_code)
        if has_ui:
            code_parts.append("")
            code_parts.append("def app():")
            code_parts.append("    return rx.vstack(")
            
            # Add UI components
            for line in self.generated_code:
                if "UI Component:" in line:
                    component = line.split("UI Component: ")[1]
                    code_parts.append(f"        {component},")
            
            code_parts.append("    )")
        
        return "\n".join(code_parts)
    
    def validate_blocks(self, blocks: List[Dict]) -> List[str]:
        """Validate blocks and return list of issues"""
        
        issues = []
        
        for i, block in enumerate(blocks):
            if not block.get('type'):
                issues.append(f"Block {i}: Missing type")
            
            if not block.get('parameters'):
                issues.append(f"Block {i}: Missing parameters")
            
            # Type-specific validation
            block_type = block.get('type', '')
            params = block.get('parameters', {})
            
            if block_type == 'variable':
                if not params.get('name'):
                    issues.append(f"Block {i}: Variable missing name")
            
            elif block_type == 'function':
                if not params.get('name'):
                    issues.append(f"Block {i}: Function missing name")
            
            elif block_type == 'for':
                start = params.get('start', '0')
                end = params.get('end', '10')
                try:
                    if int(start) >= int(end):
                        issues.append(f"Block {i}: For loop start >= end")
                except ValueError:
                    issues.append(f"Block {i}: For loop invalid range values")
        
        return issues
    
    def get_block_suggestions(self, current_blocks: List[Dict]) -> List[Dict]:
        """Get suggestions for next blocks based on current context"""
        
        suggestions = []
        
        # Analyze current blocks to suggest relevant next blocks
        has_variable = any(b.get('type') == 'variable' for b in current_blocks)
        has_function = any(b.get('type') == 'function' for b in current_blocks)
        has_ui = any(b.get('type') in ['button', 'input', 'slider'] for b in current_blocks)
        
        if not has_variable:
            suggestions.append({
                "type": "variable",
                "reason": "Consider adding variables to store data"
            })
        
        if has_variable and not has_function:
            suggestions.append({
                "type": "function", 
                "reason": "Create functions to process your variables"
            })
        
        if not has_ui:
            suggestions.append({
                "type": "button",
                "reason": "Add buttons for user interaction"
            })
        
        return suggestions

# Global instance
block_parser = BlockParser()
