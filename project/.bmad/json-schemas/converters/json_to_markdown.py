#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path

class JSONToMarkdownConverter:
    def __init__(self, schema_dir='schemas'):
        self.schema_dir = schema_dir
    
    def convert_json_to_markdown(self, json_file, output_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            title = data.get('document_info', {}).get('document_title', 'Document')
            markdown = f'# {title}\n\n'
            
            for key, value in data.items():
                markdown += f'## {key}\n'
                if isinstance(value, dict):
                    for k, v in value.items():
                        markdown += f'- **{k}**: {v}\n'
                elif isinstance(value, list):
                    for item in value:
                        markdown += f'- {item}\n'
                else:
                    markdown += f'{value}\n'
                markdown += '\n'
            
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            
            return True
        except Exception as e:
            print(f'Error: {e}')
            return False
