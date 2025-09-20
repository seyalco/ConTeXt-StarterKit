#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate-set_symbol_vars.py

Generates set_symbol_vars.ctx from symbol files (.svg, .png, .pdf)
by scanning folders, applying color rules, and merging with existing content.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional

# Settings
OUTPUT_FILE = "set_symbol_vars.ctx"
VALID_EXTENSIONS = {".svg", ".png", ".pdf"}
COLOR_RULES = {
    "colored_symbols": None,
    "uncolored_svg": "currentcolor"
}
DEFAULT_PARAMS = {
    "width": "1.6ex",
    "kern": "0.2em",
    "lower": "0.15ex"
}


def scan_directories(root_path: Path) -> Dict[str, List[str]]:
    found = defaultdict(list)
    for dirpath, _, filenames in os.walk(root_path):
        files = [f for f in filenames if Path(f).suffix.lower() in VALID_EXTENSIONS]
        if files:
            found[str(Path(dirpath).relative_to(root_path))] = sorted(files)
    return dict(found)


def parse_existing_ctx(file_path: Path) -> Dict[str, Dict[str, str]]:
    if not file_path.exists():
        return {}
    content = file_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"%\s*Symbols found in (.+?) folder:\s*?\n"
        r"\\setvariables\s*\[([^\]]+)\]\s*\[\s*\n?(.*?)\n?\]",
        re.DOTALL
    )
    return {
        m.group(2).strip(): {
            "header_path": m.group(1).strip(),
            "content": m.group(3).rstrip()
        }
        for m in pattern.finditer(content)
    }


def determine_color(folder_path: str) -> Optional[str]:
    for folder, value in COLOR_RULES.items():
        if folder in Path(folder_path).parts:
            return value
    return None


def build_block_name(folder_name: str, filename: str) -> str:
    return f"{folder_name}:{Path(filename).stem}"
    

def generate_block(folder: str, filename: str, existing_blocks: Dict[str, Dict[str, str]]) -> str:
    block_name = build_block_name(Path(folder).name, filename)
    if block_name in existing_blocks:
        params_content = existing_blocks[block_name]["content"]
    else:
        params = {}
        color = determine_color(folder)
        if color is not None:
            params["color"] = color
        params.update(DEFAULT_PARAMS)
        params["filename"] = filename
        params_content = ", \n    ".join(f"{k}={v}" for k, v in params.items()) + ","


    return (
        f"\\setvariables\n"
        f"  [{block_name}]\n"
        f"  [\n    {params_content} \n  ]\n"
    )


def build_ctx_content(found_files: Dict[str, List[str]], existing_blocks: Dict[str, Dict[str, str]]) -> str:
    lines = []
    for rel_dir in sorted(found_files.keys(), key=str.lower):
        lines.append(f"% Symbols found in {rel_dir} folder:\n")
        for filename in sorted(found_files[rel_dir], key=str.lower):
            lines.append(generate_block(rel_dir, filename, existing_blocks) + "\n")
    return "".join(lines)


def save_to_file(content: str, file_path: Path):
    file_path.write_text(content, encoding="utf-8")
    print(f"✅ {file_path} generated.")


def main():
    root = Path(__file__).parent

    # Step 1: Recursively find valid symbol files in all subdirectories
    found_files = scan_directories(root)

    # Step 2: Load existing .ctx blocks (to keep user edits and avoid overwriting them)
    existing_blocks = parse_existing_ctx(root / OUTPUT_FILE)

    # Step 3: Build final merged .ctx content (new + existing)
    final_content = build_ctx_content(found_files, existing_blocks)

    # Step 4: Save generated content to file
    save_to_file(final_content, root / OUTPUT_FILE)


if __name__ == "__main__":
    main()
