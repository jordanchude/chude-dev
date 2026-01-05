#!/usr/bin/env python3
"""
Script to remove all Webflow references from HTML files for SEO purposes.
"""
import os
import re
from pathlib import Path

def remove_webflow_references(file_path):
    """Remove all Webflow references from an HTML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Remove Webflow HTML comment from DOCTYPE line
    content = re.sub(r'<!--\s*This site was created in Webflow\.\s*https://webflow\.com\s*-->', '', content)
    
    # 2. Remove generator meta tag
    content = re.sub(r'<meta\s+content=["\']Webflow["\']\s+name=["\']generator["\']\s*>\s*\n?', '', content, flags=re.IGNORECASE)
    
    # 3. Remove "Powered by Webflow" links and text
    content = re.sub(r'\s*-\s*Powered by\s+<a[^>]*>Webflow</a>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*Powered by\s+<a[^>]*>Webflow</a>', '', content, flags=re.IGNORECASE)
    
    # 4. Remove Webflow badge CSS (keep the style tag but remove Webflow reference)
    content = re.sub(r'\.w-webflow-badge\s*\{[^}]*\}', '', content)
    
    # 5. Remove links to webflow.com (but keep the link structure if needed)
    content = re.sub(r'<a[^>]*href=["\']https?://[^"\']*webflow\.com[^"\']*["\'][^>]*>.*?</a>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # 6. Remove "Webflow Templates" text from links and content
    content = re.sub(r'Webflow\s+Templates?', 'Templates', content, flags=re.IGNORECASE)
    
    # 7. Remove "Webflow Template" from titles and descriptions (but keep the rest)
    content = re.sub(r'\s*-\s*Webflow\s+Ecommerce\s+website\s+template', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*-\s*Webflow\s+Template', '', content, flags=re.IGNORECASE)
    content = re.sub(r'Webflow\s+Template', 'Template', content, flags=re.IGNORECASE)
    content = re.sub(r'Webflow\s+Ecommerce\s+website\s+template', 'Ecommerce website template', content, flags=re.IGNORECASE)
    
    # 8. Remove "Webflow" from alt text
    content = re.sub(r'alt=["\']([^"\']*)\s*Webflow\s+Template([^"\']*)["\']', r'alt="\1Template\2"', content, flags=re.IGNORECASE)
    content = re.sub(r'alt=["\']([^"\']*)\s*Webflow([^"\']*)["\']', r'alt="\1\2"', content, flags=re.IGNORECASE)
    
    # 9. Remove "Webflow" from meta descriptions
    content = re.sub(r'our\s+ultimate\s+development\s+agency\s+Webflow\s+Template', 'our ultimate development agency Template', content, flags=re.IGNORECASE)
    content = re.sub(r'Devtech\s+X\s+Webflow', 'Devtech X', content, flags=re.IGNORECASE)
    
    # 10. Remove "Webflow" from headings and paragraphs
    content = re.sub(r'\bWebflow\s+Template\b', 'Template', content, flags=re.IGNORECASE)
    content = re.sub(r'\bWebflow\s+Templates?\b', 'Templates', content, flags=re.IGNORECASE)
    content = re.sub(r'\bWebflow\s+team\b', 'team', content, flags=re.IGNORECASE)
    content = re.sub(r'\bWebflow\s+Template\s+Figma\s+file\b', 'Template Figma file', content, flags=re.IGNORECASE)
    content = re.sub(r'\bWebflow\s+template\b', 'template', content, flags=re.IGNORECASE)
    
    # 11. Remove references to webflow.com in URLs (data-src, etc.)
    content = re.sub(r'https?://[^"\'\s]*webflow\.com[^"\'\s]*', '', content, flags=re.IGNORECASE)
    
    # 12. Remove "Buy now on Webflow" and similar text
    content = re.sub(r'Buy\s+now\s+on\s+Webflow', 'Buy now', content, flags=re.IGNORECASE)
    content = re.sub(r'on\s+Webflow', '', content, flags=re.IGNORECASE)
    
    # 13. Remove "More Webflow Templates" links
    content = re.sub(r'<a[^>]*class=["\'][^"\']*more-template[^"\']*["\'][^>]*>.*?More\s+Webflow\s+Templates?.*?</a>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # 14. Remove "Hire our Webflow team" text
    content = re.sub(r'Hire\s+our\s+Webflow\s+team', 'Hire our team', content, flags=re.IGNORECASE)
    
    # 15. Remove "Premium Webflow Templates" text
    content = re.sub(r'Premium\s+Webflow\s+Templates?', 'Premium Templates', content, flags=re.IGNORECASE)
    
    # 16. Remove "Looking for more amazing Webflow Templates?" text
    content = re.sub(r'Looking\s+for\s+more\s+amazing\s+Webflow\s+Templates\?', 'Looking for more amazing Templates?', content, flags=re.IGNORECASE)
    
    # 17. Remove "100\+ Webflow Templates" text
    content = re.sub(r'\d+\+\s+Webflow\s+Templates?', lambda m: m.group(0).replace('Webflow ', ''), content, flags=re.IGNORECASE)
    
    # 18. Clean up "The Devtech X Webflow Template" -> "The Devtech X Template"
    content = re.sub(r'The\s+Devtech\s+X\s+Webflow\s+Template', 'The Devtech X Template', content, flags=re.IGNORECASE)
    content = re.sub(r'Devtech\s+X\s+Webflow\s+Template', 'Devtech X Template', content, flags=re.IGNORECASE)
    
    # 19. Remove "Webflow" from image filenames in alt text (but keep the image src as is)
    # This is handled above in alt text replacement
    
    # 20. Remove "customize-your-webflow-template" references in image alt text
    content = re.sub(r'customize-your-webflow-template', 'customize-your-template', content, flags=re.IGNORECASE)
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Process all HTML files in the current directory and subdirectories."""
    base_dir = Path('.')
    html_files = list(base_dir.rglob('*.html'))
    
    processed = 0
    for html_file in html_files:
        if remove_webflow_references(html_file):
            processed += 1
            print(f"Processed: {html_file}")
    
    print(f"\nProcessed {processed} out of {len(html_files)} HTML files.")

if __name__ == '__main__':
    main()

