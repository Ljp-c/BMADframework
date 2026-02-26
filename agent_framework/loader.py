# -*- coding: utf-8 -*-
"""
Markdown Loader - Parse markdown files for persona and task definitions
"""
import os
import re
from typing import Dict, Any, Optional


class MarkdownLoader:
    """Utility class for loading and parsing markdown files"""
    
    @staticmethod
    def load_file(file_path: str) -> str:
        """
        Read file content with error handling
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            File content as string
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading file {file_path}: {str(e)}")
            raise

    @staticmethod
    def parse_persona(file_path: str) -> Dict[str, str]:
        """
        Parse persona markdown file with improved error handling
        
        Expected format:
        # Role Name
        
        ## Goal
        Goal description here
        
        ## Backstory
        Backstory description here
        
        Args:
            file_path: Path to persona markdown file
            
        Returns:
            Dictionary with keys: role, goal, backstory
        """
        try:
            content = MarkdownLoader.load_file(file_path)
            lines = content.split('\n')
            
            # Extract role name from first heading
            role_name = "Unknown Role"
            for line in lines:
                if line.startswith('#') and not line.startswith('##'):
                    role_name = line.replace('#', '').strip()
                    break
            
            # Extract goal section
            goal = MarkdownLoader._extract_section(content, "goal", 
                                                    "Complete assigned tasks and ensure high quality delivery.")
            
            # Extract backstory section
            backstory = MarkdownLoader._extract_section(content, "backstory", content)
            
            return {
                "role": role_name,
                "goal": goal,
                "backstory": backstory
            }
        except Exception as e:
            print(f"Error parsing persona file {file_path}: {str(e)}")
            return {
                "role": "Unknown Agent",
                "goal": "Complete assigned tasks",
                "backstory": "An AI agent ready to assist"
            }

    @staticmethod
    def parse_task(file_path: str) -> Dict[str, str]:
        """
        Parse task markdown file with improved error handling
        
        Expected format:
        # Task Name
        
        Task description here
        
        ## Output
        Expected output description
        
        Args:
            file_path: Path to task markdown file
            
        Returns:
            Dictionary with keys: description, expected_output
        """
        try:
            content = MarkdownLoader.load_file(file_path)
            
            # Extract description (everything before first ## section)
            description = content
            sections = content.split('##')
            if len(sections) > 1:
                description = sections[0].strip()
            
            # Extract expected output section
            expected_output = MarkdownLoader._extract_section(content, "output",
                                                              "Final output document defined in the task.")
            
            return {
                "description": description,
                "expected_output": expected_output
            }
        except Exception as e:
            print(f"Error parsing task file {file_path}: {str(e)}")
            return {
                "description": "Unable to load task description",
                "expected_output": "Expected output not specified"
            }

    @staticmethod
    def _extract_section(content: str, section_name: str, default: str = "") -> str:
        """
        Extract a section from markdown content by heading
        
        Args:
            content: Markdown content
            section_name: Section heading name (case-insensitive)
            default: Default value if section not found
            
        Returns:
            Section content or default value
        """
        try:
            # Create regex pattern for section heading
            pattern = rf"##\s*{section_name}\s*\n(.*?)(?=##|$)"
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            
            if match:
                return match.group(1).strip()
            return default
        except Exception:
            return default

