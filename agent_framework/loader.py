# -*- coding: utf-8 -*-
import os
import re
from typing import Dict, Any

class MarkdownLoader:
    @staticmethod
    def load_file(file_path: str) -> str:
        """Read file content"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def parse_persona(file_path: str) -> Dict[str, str]:
        """
        Parse persona markdown file
        Expects: role, goal, backstory
        """
        content = MarkdownLoader.load_file(file_path)
        
        # Simple parsing logic
        # Assume first line is Role Name
        lines = content.split('\n')
        role_name = lines[0].replace('#', '').strip()
        
        # Extract parts
        # Simple heuristic rules
        goal = "Complete assigned tasks and ensure high quality delivery."
        backstory = content # Use entire content as backstory
        
        return {
            "role": role_name,
            "goal": goal,
            "backstory": backstory
        }

    @staticmethod
    def parse_task(file_path: str) -> Dict[str, str]:
        """
        Parse task markdown file
        Expects: description, expected_output
        """
        content = MarkdownLoader.load_file(file_path)
        
        # Use entire content as description
        description = content
        
        # Try to extract output description
        expected_output = "Final output document defined in the task."
        # Match "## ??" (Output)
        output_marker = "## \u8f93\u51fa"
        if output_marker in content:
            parts = content.split(output_marker)
            if len(parts) > 1:
                # Take content before next section
                output_section = parts[1].split("##")[0].strip()
                expected_output = output_section
                
        return {
            "description": description,
            "expected_output": expected_output
        }
