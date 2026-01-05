#!/usr/bin/env python3
"""
Script to rename Webflow CSS classes in both CSS and HTML files.
"""
import os
import re
from pathlib import Path

def rename_classes_in_file(file_path, class_mappings):
    """Rename CSS classes in a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for old_class, new_class in class_mappings.items():
        # Replace in class attributes
        content = re.sub(rf'class=["\']([^"\']*)\b{re.escape(old_class)}\b([^"\']*)["\']', 
                        rf'class="\1{new_class}\2"', content)
        # Replace in CSS selectors
        content = re.sub(rf'\.{re.escape(old_class)}\b', f'.{new_class}', content)
        # Replace in any other references
        content = content.replace(old_class, new_class)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Rename Webflow classes in all files."""
    base_dir = Path('.')
    
    # Class mappings: (old_name, new_name)
    class_mappings = {
        'more-webflow-templates-sub': 'more-templates-sub',
        'webflow-image-wrapper': 'image-wrapper',
        'webflow-card-wrapper': 'card-wrapper',
        'w-webflow-badge': 'w-badge',
    }
    
    # Process CSS files
    css_files = list(base_dir.rglob('*.css'))
    css_updated = 0
    for css_file in css_files:
        if rename_classes_in_file(css_file, class_mappings):
            css_updated += 1
            print(f"Updated CSS: {css_file}")
    
    # Process HTML files
    html_files = list(base_dir.rglob('*.html'))
    html_updated = 0
    for html_file in html_files:
        if rename_classes_in_file(html_file, class_mappings):
            html_updated += 1
            print(f"Updated HTML: {html_file}")
    
    print(f"\nUpdated {css_updated} CSS files and {html_updated} HTML files.")

if __name__ == '__main__':
    main()

