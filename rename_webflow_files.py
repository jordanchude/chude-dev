#!/usr/bin/env python3
"""
Script to rename Webflow CSS/JS files and update all references.
"""
import os
import re
from pathlib import Path
import shutil

def rename_files_and_update_references():
    """Rename Webflow files and update all references."""
    base_dir = Path('.')
    
    # File mappings: (old_name, new_name)
    file_mappings = [
        ('css/webflow.css', 'css/styles.css'),
        ('css/chude-dev-bb9e21.webflow.css', 'css/chude-dev-bb9e21.css'),
        ('js/webflow.js', 'js/main.js'),
    ]
    
    # Rename files
    for old_path, new_path in file_mappings:
        old_file = base_dir / old_path
        new_file = base_dir / new_path
        if old_file.exists():
            shutil.move(str(old_file), str(new_file))
            print(f"Renamed: {old_path} -> {new_path}")
        else:
            print(f"Warning: {old_path} not found")
    
    # Update references in all HTML files
    html_files = list(base_dir.rglob('*.html'))
    updated_count = 0
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update CSS references
        content = content.replace('css/webflow.css', 'css/styles.css')
        content = content.replace('css/chude-dev-bb9e21.webflow.css', 'css/chude-dev-bb9e21.css')
        
        # Update JS references
        content = content.replace('js/webflow.js', 'js/main.js')
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
            print(f"Updated references in: {html_file}")
    
    print(f"\nUpdated references in {updated_count} HTML files.")

if __name__ == '__main__':
    rename_files_and_update_references()

