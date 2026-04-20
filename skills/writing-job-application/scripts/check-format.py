import re
import sys
import os

def check_format(text):
    errors = []
    
    # 1. Check for Markdown formatting
    markdown_patterns = [
        (r'\*\*.*?\*\*', "Bold text (**bold**)"),
        (r'#+\s', "Headers (# Heading)"),
        (r'\[.*?\]\(.*?\)', "Markdown links ([text](url))"),
        (r'^>\s', "Blockquotes (> quote)"),
        (r'`.*?`', "Inline code (`code`)"),
    ]
    
    for pattern, name in markdown_patterns:
        if re.search(pattern, text, re.MULTILINE):
            errors.append(f"Found Markdown: {name}")

    # 2. Check for List symbols at start of line
    list_patterns = [
        (r'^\s*[-*+]\s+', "Unordered list (- or *)"),
        (r'^\s*\d+\.\s+', "Ordered list (1.)"),
    ]
    
    for pattern, name in list_patterns:
        if re.search(pattern, text, re.MULTILINE):
            errors.append(f"Found List symbol: {name}")

    # 3. Check for Special characters
    special_chars = [
        ('—', "Em-dash (—)"),
        ('–', "En-dash (–)"),
    ]
    
    for char, name in special_chars:
        if char in text:
            errors.append(f"Found Special character: {name}")

    # 4. Paragraph spacing (Check for > 2 consecutive newlines)
    if re.search(r'\n{3,}', text):
        errors.append("Excessive whitespace (3+ consecutive newlines)")

    # 5. Word count (Language agnostic)
    # English: words separated by space
    # CJK: count characters
    en_words = len(re.findall(r'\b\w+\b', text))
    cjk_chars = len(re.findall(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]', text))
    
    total_count = en_words + cjk_chars
    
    return errors, total_count

def main():
    if len(sys.argv) < 2:
        # Read from stdin if no file provided
        text = sys.stdin.read()
    else:
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found.")
            sys.exit(1)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

    errors, count = check_format(text)
    
    print("--- Format Check Report ---")
    print(f"Total Estimated Word/Char Count: {count}")
    print("---------------------------")
    
    if not errors:
        print("✅ No formatting issues found. Ready for submission!")
    else:
        print("❌ Issues detected:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
