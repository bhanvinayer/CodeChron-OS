"""
Exporter - Handles exporting code and projects
"""

import os
import zipfile
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import tempfile

class Exporter:
    """Handles exporting projects and code"""
    
    def __init__(self, export_dir: str = "data/saved_apps"):
        self.export_dir = export_dir
        os.makedirs(export_dir, exist_ok=True)
    
    def export_project(
        self,
        project_name: str,
        code: str,
        era: str,
        metadata: Optional[Dict] = None,
        format: str = "zip"
    ) -> Dict[str, Any]:
        """
        Export a complete project
        
        Args:
            project_name: Name of the project
            code: Generated code
            era: Which era created the project
            metadata: Additional project metadata
            format: Export format (zip, folder, single_file)
            
        Returns:
            Export result with file path and details
        """
        
        try:
            if format == "zip":
                return self._export_as_zip(project_name, code, era, metadata)
            elif format == "folder":
                return self._export_as_folder(project_name, code, era, metadata)
            elif format == "single_file":
                return self._export_as_single_file(project_name, code, era, metadata)
            else:
                raise ValueError(f"Unsupported export format: {format}")
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _export_as_zip(
        self,
        project_name: str,
        code: str,
        era: str,
        metadata: Optional[Dict]
    ) -> Dict[str, Any]:
        """Export project as ZIP file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{project_name}_{era}_{timestamp}.zip"
        filepath = os.path.join(self.export_dir, filename)
        
        with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Main code file
            if era == "mac1984":
                code_filename = "app.py"
            elif era == "block2015":
                code_filename = "blocks_app.py"
            elif era == "vibe2025":
                code_filename = "ai_generated_app.py"
            else:
                code_filename = "main.py"
            
            zipf.writestr(code_filename, code)
            
            # Requirements file
            requirements = self._generate_requirements(code, era)
            zipf.writestr("requirements.txt", requirements)
            
            # README file
            readme = self._generate_readme(project_name, era, metadata)
            zipf.writestr("README.md", readme)
            
            # Project metadata
            project_info = {
                "name": project_name,
                "era": era,
                "created_at": datetime.now().isoformat(),
                "framework": self._detect_framework(code),
                "metadata": metadata or {},
                "export_version": "1.0"
            }
            zipf.writestr("project.json", json.dumps(project_info, indent=2))
            
            # Era-specific files
            if era == "mac1984":
                self._add_mac_assets(zipf)
            elif era == "block2015":
                self._add_block_assets(zipf, metadata)
            elif era == "vibe2025":
                self._add_ai_assets(zipf, metadata)
        
        return {
            "success": True,
            "filepath": filepath,
            "filename": filename,
            "size": os.path.getsize(filepath),
            "format": "zip"
        }
    
    def _export_as_folder(
        self,
        project_name: str,
        code: str,
        era: str,
        metadata: Optional[Dict]
    ) -> Dict[str, Any]:
        """Export project as folder structure"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{project_name}_{era}_{timestamp}"
        folder_path = os.path.join(self.export_dir, folder_name)
        
        os.makedirs(folder_path, exist_ok=True)
        
        # Main code file
        code_filename = "app.py"
        with open(os.path.join(folder_path, code_filename), 'w') as f:
            f.write(code)
        
        # Requirements file
        requirements = self._generate_requirements(code, era)
        with open(os.path.join(folder_path, "requirements.txt"), 'w') as f:
            f.write(requirements)
        
        # README file
        readme = self._generate_readme(project_name, era, metadata)
        with open(os.path.join(folder_path, "README.md"), 'w') as f:
            f.write(readme)
        
        # Project metadata
        project_info = {
            "name": project_name,
            "era": era,
            "created_at": datetime.now().isoformat(),
            "framework": self._detect_framework(code),
            "metadata": metadata or {},
            "export_version": "1.0"
        }
        with open(os.path.join(folder_path, "project.json"), 'w') as f:
            json.dump(project_info, f, indent=2)
        
        return {
            "success": True,
            "filepath": folder_path,
            "filename": folder_name,
            "format": "folder"
        }
    
    def _export_as_single_file(
        self,
        project_name: str,
        code: str,
        era: str,
        metadata: Optional[Dict]
    ) -> Dict[str, Any]:
        """Export project as single Python file with embedded metadata"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{project_name}_{era}_{timestamp}.py"
        filepath = os.path.join(self.export_dir, filename)
        
        # Build single file with metadata as comments
        file_content = f'''"""
Project: {project_name}
Era: {era}
Created: {datetime.now().isoformat()}
Generated by: CodeChronOS
Framework: {self._detect_framework(code)}

{json.dumps(metadata or {}, indent=2) if metadata else "No additional metadata"}
"""

{code}

if __name__ == "__main__":
    # Auto-run the app
    try:
        app.run()
    except:
        print("Run this file with: python {filename}")
'''
        
        with open(filepath, 'w') as f:
            f.write(file_content)
        
        return {
            "success": True,
            "filepath": filepath,
            "filename": filename,
            "size": os.path.getsize(filepath),
            "format": "single_file"
        }
    
    def _generate_requirements(self, code: str, era: str) -> str:
        """Generate requirements.txt based on code analysis"""
        
        requirements = []
        
        # Base requirements
        if "import reflex" in code or "rx." in code:
            requirements.append("reflex>=0.4.0")
        
        if "import streamlit" in code or "st." in code:
            requirements.append("streamlit>=1.29.0")
        
        if "import pygame" in code:
            requirements.append("pygame>=2.5.2")
        
        if "from PIL import" in code or "import PIL" in code:
            requirements.append("Pillow>=10.0.0")
        
        if "import numpy" in code or "np." in code:
            requirements.append("numpy>=1.24.0")
        
        if "import matplotlib" in code:
            requirements.append("matplotlib>=3.7.0")
        
        if "import pandas" in code or "pd." in code:
            requirements.append("pandas>=2.0.0")
        
        # Era-specific requirements
        if era == "vibe2025":
            requirements.append("openai>=1.3.0")
        
        if not requirements:
            requirements.append("# No external dependencies detected")
        
        return "\n".join(requirements)
    
    def _generate_readme(
        self,
        project_name: str,
        era: str,
        metadata: Optional[Dict]
    ) -> str:
        """Generate README.md file"""
        
        readme = f"""# {project_name}

Generated by CodeChronOS - {era.upper()}

## Description

This project was created using CodeChronOS, an educational platform that simulates the evolution of software development from 1984 to 2025.

**Era**: {era}
**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Installation

1. Make sure you have Python 3.8+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

```bash
python app.py
```

## About CodeChronOS

CodeChronOS is an immersive journey through software development history:

- **Mac 1984**: Classic Macintosh interface with pixel-perfect retro charm
- **Block 2015**: Visual block-based coding with drag-and-drop simplicity  
- **Vibe 2025**: AI-powered natural language development environment

Visit [CodeChronOS](https://codechronos.dev) to create your own projects!

## Project Details

"""
        
        if metadata:
            readme += f"""
### Metadata
```json
{json.dumps(metadata, indent=2)}
```
"""
        
        readme += """
## License

Generated code is provided as-is for educational purposes.
"""
        
        return readme
    
    def _detect_framework(self, code: str) -> str:
        """Detect which framework is being used"""
        
        if "import reflex" in code or "rx." in code:
            return "reflex"
        elif "import streamlit" in code or "st." in code:
            return "streamlit"
        elif "import pygame" in code:
            return "pygame"
        elif "import tkinter" in code:
            return "tkinter"
        else:
            return "python"
    
    def _add_mac_assets(self, zipf: zipfile.ZipFile):
        """Add Mac 1984 era specific assets"""
        
        # Add classic Mac styling
        mac_css = """
        /* Mac 1984 Classic Styling */
        .mac-window {
            border: 2px solid black;
            background: white;
            font-family: 'Monaco', monospace;
        }
        
        .mac-titlebar {
            background: #ddd;
            border-bottom: 1px solid black;
            padding: 4px;
        }
        """
        zipf.writestr("assets/mac.css", mac_css)
    
    def _add_block_assets(self, zipf: zipfile.ZipFile, metadata: Optional[Dict]):
        """Add Block 2015 era specific assets"""
        
        # Add block definitions if available
        if metadata and "blocks" in metadata:
            zipf.writestr("blocks.json", json.dumps(metadata["blocks"], indent=2))
    
    def _add_ai_assets(self, zipf: zipfile.ZipFile, metadata: Optional[Dict]):
        """Add AI 2025 era specific assets"""
        
        # Add prompt history if available
        if metadata and "prompts" in metadata:
            zipf.writestr("prompts.json", json.dumps(metadata["prompts"], indent=2))
    
    def list_exports(self) -> List[Dict[str, Any]]:
        """List all exported projects"""
        
        exports = []
        
        if not os.path.exists(self.export_dir):
            return exports
        
        for filename in os.listdir(self.export_dir):
            filepath = os.path.join(self.export_dir, filename)
            
            if os.path.isfile(filepath):
                # Parse filename to extract info
                parts = filename.split('_')
                if len(parts) >= 3:
                    project_name = parts[0]
                    era = parts[1]
                    timestamp = parts[2].split('.')[0]
                else:
                    project_name = filename.split('.')[0]
                    era = "unknown"
                    timestamp = "unknown"
                
                stat = os.stat(filepath)
                
                exports.append({
                    "filename": filename,
                    "filepath": filepath,
                    "project_name": project_name,
                    "era": era,
                    "timestamp": timestamp,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        # Sort by modification time (newest first)
        exports.sort(key=lambda x: x["modified"], reverse=True)
        
        return exports

# Global instance
exporter = Exporter()
