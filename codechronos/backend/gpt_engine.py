"""
GPT Engine - Handles AI code generation using OpenAI API
"""

import openai
import os
from typing import Dict, List, Optional
import json
import asyncio

class GPTEngine:
    """GPT-powered code generation engine"""
    
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.conversation_history: List[Dict] = []
    
    async def generate_code(
        self, 
        prompt: str, 
        creativity_level: float = 0.7,
        target_framework: str = "reflex"
    ) -> Dict:
        """
        Generate code from natural language prompt
        
        Args:
            prompt: User's natural language description
            creativity_level: Temperature for GPT (0.1-1.0)
            target_framework: Target framework (reflex, streamlit)
        
        Returns:
            Dict with generated code, explanation, and metadata
        """
        
        system_prompt = self._build_system_prompt(target_framework)
        
        try:
            response = await self._call_openai(
                system_prompt=system_prompt,
                user_prompt=prompt,
                temperature=creativity_level
            )
            
            return self._parse_response(response, prompt)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "code": "",
                "explanation": "Failed to generate code"
            }
    
    def _build_system_prompt(self, framework: str) -> str:
        """Build system prompt based on target framework"""
        
        base_prompt = """
        You are an expert Python developer specializing in creating interactive web applications.
        Generate clean, production-ready code based on user descriptions.
        
        Guidelines:
        - Write complete, runnable code
        - Include proper imports and setup
        - Add helpful comments
        - Follow best practices
        - Make code modular and reusable
        """
        
        if framework == "reflex":
            return base_prompt + """
            
            Use Reflex (rx) framework for web applications:
            - Create State classes for data management
            - Use rx.Component for UI elements
            - Implement event handlers properly
            - Follow Reflex patterns and conventions
            
            Example structure:
            ```python
            import reflex as rx
            
            class AppState(rx.State):
                # State variables here
                pass
            
            def app_component():
                return rx.vstack(
                    # UI components here
                )
            ```
            """
        
        elif framework == "streamlit":
            return base_prompt + """
            
            Use Streamlit (st) for web applications:
            - Use st.session_state for state management
            - Create interactive widgets with st components
            - Handle user input with callbacks
            - Structure code in main function
            
            Example structure:
            ```python
            import streamlit as st
            
            def main():
                st.title("App Title")
                # App logic here
                
            if __name__ == "__main__":
                main()
            ```
            """
        
        return base_prompt
    
    async def _call_openai(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        temperature: float
    ) -> str:
        """Make async call to OpenAI API"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history[-6:])  # Last 6 messages for context
        
        response = await asyncio.to_thread(
            self.client.chat.completions.create,
            model="gpt-4",
            messages=messages,
            temperature=temperature,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    def _parse_response(self, response: str, original_prompt: str) -> Dict:
        """Parse GPT response and extract code/metadata"""
        
        # Extract code blocks
        code_blocks = []
        lines = response.split('\n')
        in_code_block = False
        current_block = []
        
        for line in lines:
            if line.strip().startswith('```'):
                if in_code_block:
                    code_blocks.append('\n'.join(current_block))
                    current_block = []
                    in_code_block = False
                else:
                    in_code_block = True
            elif in_code_block:
                current_block.append(line)
        
        # Get main code block
        main_code = code_blocks[0] if code_blocks else response
        
        # Clean up code
        main_code = self._clean_code(main_code)
        
        return {
            "success": True,
            "code": main_code,
            "explanation": self._extract_explanation(response),
            "prompt": original_prompt,
            "framework": "reflex",
            "components": self._identify_components(main_code)
        }
    
    def _clean_code(self, code: str) -> str:
        """Clean and format generated code"""
        
        # Remove common artifacts
        code = code.replace('```python', '').replace('```', '')
        
        # Remove excessive whitespace
        lines = [line.rstrip() for line in code.split('\n')]
        code = '\n'.join(lines)
        
        # Ensure proper imports
        if 'import reflex as rx' not in code and 'rx.' in code:
            code = 'import reflex as rx\n\n' + code
        
        return code.strip()
    
    def _extract_explanation(self, response: str) -> str:
        """Extract explanation from GPT response"""
        
        # Look for explanation outside code blocks
        lines = response.split('\n')
        explanation_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            elif not in_code_block and line.strip():
                explanation_lines.append(line.strip())
        
        explanation = ' '.join(explanation_lines)
        
        # Fallback explanation
        if not explanation:
            explanation = "Generated code based on your requirements."
        
        return explanation
    
    def _identify_components(self, code: str) -> List[str]:
        """Identify UI components used in the code"""
        
        components = []
        component_patterns = [
            'rx.button', 'rx.input', 'rx.text', 'rx.vstack', 'rx.hstack',
            'rx.box', 'rx.heading', 'rx.slider', 'rx.checkbox', 'rx.select'
        ]
        
        for pattern in component_patterns:
            if pattern in code:
                components.append(pattern.replace('rx.', ''))
        
        return components
    
    def add_to_conversation(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    async def refine_code(self, code: str, feedback: str) -> Dict:
        """Refine existing code based on feedback"""
        
        prompt = f"""
        Please refine this code based on the feedback:
        
        Current code:
        ```python
        {code}
        ```
        
        Feedback: {feedback}
        
        Please provide the improved version.
        """
        
        return await self.generate_code(prompt)
    
    async def explain_code(self, code: str) -> str:
        """Generate explanation for existing code"""
        
        prompt = f"""
        Please explain what this code does in simple terms:
        
        ```python
        {code}
        ```
        """
        
        try:
            response = await self._call_openai(
                system_prompt="You are a helpful coding teacher. Explain code clearly and concisely.",
                user_prompt=prompt, 
                temperature=0.3
            )
            return response
        except Exception as e:
            return f"Error explaining code: {str(e)}"

# Global instance
gpt_engine = GPTEngine()
