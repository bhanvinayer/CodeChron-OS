"""
Execution Sandbox - Safe runtime for generated code
"""

import subprocess
import sys
import os
import tempfile
import json
import time
from typing import Dict, Any, Optional, List
import threading
import queue

class ExecutionSandbox:
    """Safe execution environment for generated code"""
    
    def __init__(self):
        self.timeout = 30  # seconds
        self.max_memory = 128 * 1024 * 1024  # 128MB
        self.allowed_imports = {
            'reflex', 'rx', 'streamlit', 'st', 'pandas', 'numpy',
            'matplotlib', 'PIL', 'json', 'os', 'sys', 'datetime',
            'random', 'math', 'collections', 're'
        }
        self.restricted_functions = {
            'exec', 'eval', 'compile', '__import__', 'open',
            'file', 'input', 'raw_input'
        }
    
    def execute_code(
        self,
        code: str,
        input_data: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Execute code in a sandboxed environment
        
        Args:
            code: Code to execute
            input_data: Optional input data
            env_vars: Optional environment variables
            
        Returns:
            Execution result with output, errors, and metadata
        """
        
        try:
            # Validate code safety
            validation_result = self.validate_code(code)
            if not validation_result["safe"]:
                return {
                    "success": False,
                    "error": f"Code validation failed: {validation_result['issues']}",
                    "output": "",
                    "execution_time": 0
                }
            
            # Execute in temporary environment
            return self._execute_in_sandbox(code, input_data, env_vars)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "execution_time": 0
            }
    
    def validate_code(self, code: str) -> Dict[str, Any]:
        """Validate code for security and safety"""
        
        issues = []
        
        # Check for restricted functions
        for func in self.restricted_functions:
            if func in code:
                issues.append(f"Restricted function: {func}")
        
        # Check for suspicious patterns
        suspicious_patterns = [
            'subprocess', 'os.system', 'os.popen', '__builtins__',
            'globals()', 'locals()', 'vars()', 'dir()',
            'import subprocess', 'from subprocess'
        ]
        
        for pattern in suspicious_patterns:
            if pattern in code:
                issues.append(f"Suspicious pattern: {pattern}")
        
        # Check imports
        import ast
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name not in self.allowed_imports:
                            issues.append(f"Unauthorized import: {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module not in self.allowed_imports:
                        issues.append(f"Unauthorized import: {node.module}")
        except SyntaxError as e:
            issues.append(f"Syntax error: {str(e)}")
        
        return {
            "safe": len(issues) == 0,
            "issues": issues
        }
    
    def _execute_in_sandbox(
        self,
        code: str,
        input_data: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Execute code in isolated process"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create code file
            code_file = os.path.join(temp_dir, "sandbox_code.py")
            with open(code_file, 'w') as f:
                f.write(code)
            
            # Create input file if needed
            input_file = None
            if input_data:
                input_file = os.path.join(temp_dir, "input.txt")
                with open(input_file, 'w') as f:
                    f.write(input_data)
            
            # Prepare environment
            env = os.environ.copy()
            if env_vars:
                env.update(env_vars)
            
            # Execute with timeout
            start_time = time.time()
            
            try:
                if input_file:
                    with open(input_file, 'r') as stdin:
                        result = subprocess.run(
                            [sys.executable, code_file],
                            stdin=stdin,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            timeout=self.timeout,
                            text=True,
                            env=env,
                            cwd=temp_dir
                        )
                else:
                    result = subprocess.run(
                        [sys.executable, code_file],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=self.timeout,
                        text=True,
                        env=env,
                        cwd=temp_dir
                    )
                
                execution_time = time.time() - start_time
                
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr,
                    "return_code": result.returncode,
                    "execution_time": execution_time
                }
                
            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "output": "",
                    "error": f"Execution timed out after {self.timeout} seconds",
                    "return_code": -1,
                    "execution_time": self.timeout
                }
    
    def test_code_syntax(self, code: str) -> Dict[str, Any]:
        """Test code syntax without executing"""
        
        try:
            compile(code, '<string>', 'exec')
            return {
                "valid": True,
                "error": None
            }
        except SyntaxError as e:
            return {
                "valid": False,
                "error": str(e),
                "line": e.lineno,
                "offset": e.offset
            }
    
    def analyze_code_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity and characteristics"""
        
        import ast
        
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {"error": "Invalid syntax"}
        
        stats = {
            "lines": len(code.split('\n')),
            "functions": 0,
            "classes": 0,
            "imports": 0,
            "loops": 0,
            "conditionals": 0,
            "complexity_score": 0
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                stats["functions"] += 1
            elif isinstance(node, ast.ClassDef):
                stats["classes"] += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                stats["imports"] += 1
            elif isinstance(node, (ast.For, ast.While)):
                stats["loops"] += 1
            elif isinstance(node, (ast.If, ast.IfExp)):
                stats["conditionals"] += 1
        
        # Simple complexity score
        stats["complexity_score"] = (
            stats["functions"] * 2 +
            stats["classes"] * 3 +
            stats["loops"] * 2 +
            stats["conditionals"] * 1
        )
        
        return stats
    
    def create_preview_server(self, code: str, port: int = 8000) -> Dict[str, Any]:
        """Create a preview server for web applications"""
        
        # Check if code is a web app
        if not ("reflex" in code or "streamlit" in code):
            return {
                "success": False,
                "error": "Code is not a web application"
            }
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create app file
                app_file = os.path.join(temp_dir, "preview_app.py")
                
                # Modify code to run on specific port
                if "reflex" in code:
                    preview_code = code + f"\n\nif __name__ == '__main__':\n    app.run(port={port})"
                elif "streamlit" in code:
                    preview_code = code
                
                with open(app_file, 'w') as f:
                    f.write(preview_code)
                
                # Start server in background
                if "streamlit" in code:
                    cmd = [sys.executable, "-m", "streamlit", "run", app_file, "--server.port", str(port)]
                else:
                    cmd = [sys.executable, app_file]
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=temp_dir
                )
                
                # Give server time to start
                time.sleep(2)
                
                if process.poll() is None:  # Process is running
                    return {
                        "success": True,
                        "url": f"http://localhost:{port}",
                        "pid": process.pid,
                        "process": process
                    }
                else:
                    stdout, stderr = process.communicate()
                    return {
                        "success": False,
                        "error": f"Server failed to start: {stderr.decode()}"
                    }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def format_code(self, code: str) -> str:
        """Format code using basic formatting rules"""
        
        try:
            import ast
            import astor
            
            # Parse and format
            tree = ast.parse(code)
            formatted = astor.to_source(tree)
            return formatted
            
        except:
            # Fallback: basic formatting
            lines = code.split('\n')
            formatted_lines = []
            indent_level = 0
            
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    formatted_lines.append('')
                    continue
                
                # Adjust indent level
                if stripped.endswith(':'):
                    formatted_lines.append('    ' * indent_level + stripped)
                    indent_level += 1
                elif stripped in ['else:', 'elif', 'except:', 'finally:']:
                    indent_level = max(0, indent_level - 1)
                    formatted_lines.append('    ' * indent_level + stripped)
                    indent_level += 1
                else:
                    formatted_lines.append('    ' * indent_level + stripped)
            
            return '\n'.join(formatted_lines)

# Global instance
sandbox = ExecutionSandbox()
