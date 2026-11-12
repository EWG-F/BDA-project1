#!/usr/bin/env python3
"""
Creates clean, extractable TrendScope.zip package
"""

import os
import zipfile

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ZIP_OUTPUT = os.path.join(BASE_DIR, "TrendScope.zip")

EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "env"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db", "TrendScope.zip"}

def create_zip():
    print(f"Creating {ZIP_OUTPUT}...")
    with zipfile.ZipFile(ZIP_OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BASE_DIR):
            # Exclude unwanted directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.endswith(".egg-info")]
            
            for file in files:
                if file in EXCLUDE_FILES or file.endswith(".pyc"):
                    continue
                
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, BASE_DIR)
                
                # Prefix with TrendScope/ root directory inside ZIP
                zip_entry_path = os.path.join("TrendScope", rel_path)
                zipf.write(full_path, zip_entry_path)
                print(f"Added: {zip_entry_path}")

    print("ZIP package created successfully!")

if __name__ == "__main__":
    create_zip()
