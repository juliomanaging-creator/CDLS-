import os
from pathlib import Path

def sanitize_encoding(kb_path):
    kb_dir = Path(kb_path)
    encodings = ['utf-16', 'utf-16le', 'utf-16be', 'utf-8-sig', 'cp1252', 'latin-1']
    for md_file in kb_dir.glob("**/*.md"):
        content = None
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            for enc in encodings:
                try:
                    with open(md_file, 'r', encoding=enc) as f:
                        content = f.read()
                        break
                except: continue
        if content is not None:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    sanitize_encoding(r"C:\Projects\AWS AGENT\knowledge_base")