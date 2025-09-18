import os
import sys

# ===============================
# Code Generator Registration
# ===============================

CODE_GENERATORS = {}

def register_code_generator(key, func):
    """
    Register a new code generator.
    - key can be a string extension ".svg" or a tuple like (".svg", "uncolored_svg")
    """
    CODE_GENERATORS[key] = func

def generate_code_for_file(file_path):
    """
    Generate code for the given file based on its extension and optional special folder rules.
    """
    file_path = file_path.replace("\\", "/")
    ext = os.path.splitext(file_path)[1].lower()  # e.g. ".svg"

    # Extract last folder and filename without extension
    parts = file_path.split("/")
    last_folder = parts[-2] if len(parts) > 1 else "."
    file_without_ext = os.path.splitext(parts[-1])[0]

    # Create symbol name like <folder>_<basename>
    symbol_name = f"{last_folder}_{file_without_ext}"

    # Step 1: Special folder handling (priority)
    for key, func in CODE_GENERATORS.items():
        if isinstance(key, tuple) and key[0] == ext and key[1] in file_path:
            return func(file_path, symbol_name)

    # Step 2: Extension only
    if ext in CODE_GENERATORS:
        return CODE_GENERATORS[ext](file_path, symbol_name)

    # Step 3: Unsupported extension
    return None


# ===============================
# Code Generator Functions
# ===============================

def svg_code_generator(file_path, symbol_name):
    """
    Generate ConTeXt code for colored SVG files (inside 'colored-svg' folder).
    Creates a reusable Metapost graphic without color modification.
    """
    return f"""\\startreusableMPgraphic{{{symbol_name}}}
  draw lmt_svg [
    filename = "\\getvariable{{{symbol_name}}}{{filename}}"
  ];
\\stopreusableMPgraphic

\\definesymbol [{symbol_name}]
  [{{%
     \\scale
       [width=\\getvariable{{{symbol_name}}}{{width}}]
       {{%
         \\lower\\getvariable{{{symbol_name}}}{{lower}}
           \\hbox{{\\reuseMPgraphic{{{symbol_name}}}}}%
       }}%
   }}]
"""

def svg_uncolored_code_generator(file_path, symbol_name):
    """
    Generate ConTeXt code for uncolored SVG files (inside 'uncolored-symbols' folder).
    Creates a reusable Metapost graphic with a predefined color applied.
    """
    return f"""\\startreusableMPgraphic{{{symbol_name}}}
  draw lmt_svg [
    filename = "\\getvariable{{{symbol_name}}}{{filename}}"
  ] withcolor \\MPcolor{{\\getvariable{{{symbol_name}}}{{color}}}};
\\stopreusableMPgraphic

\\definesymbol [{symbol_name}]
  [{{%
     \\scale
       [width=\\getvariable{{{symbol_name}}}{{width}}]
       {{%
         \\lower\\getvariable{{{symbol_name}}}{{lower}}
           \\hbox{{\\reuseMPgraphic{{{symbol_name}}}}}%
       }}%
   }}]
"""



def pdf_code_generator(file_path, symbol_name):
    return f"""\\definesymbol [{symbol_name}]
  [{{%
     \\scale
       [width=\\getvariable{{{symbol_name}}}{{width}}]
       {{%
         \\lower\\getvariable{{{symbol_name}}}{{lower}}
           \\hbox{{%
             \\externalfigure
               [\\getvariable{{{symbol_name}}}{{filename}}]
               [page=1]
           }}%
       }}%
   }}]
   """

def png_code_generator(file_path, symbol_name):
    return f"""\\definesymbol [{symbol_name}]
  [{{%
     \\scale
       [width=\\getvariable{{{symbol_name}}}{{width}}]
       {{%
         \\lower\\getvariable{{{symbol_name}}}{{lower}}
           \\hbox{{%
             \\externalfigure
               [\\getvariable{{{symbol_name}}}{{filename}}]
           }}%
       }}%
   }}]
"""

def jpg_code_generator(file_path, symbol_name):
    return f"""\\definesymbol [{symbol_name}]
  [{{%
     \\scale
       [width=\\getvariable{{{symbol_name}}}{{width}}]
       {{%
         \\lower\\getvariable{{{symbol_name}}}{{lower}}
           \\hbox{{%
             \\externalfigure
               [\\getvariable{{{symbol_name}}}{{filename}}]
           }}%
       }}%
   }}]
"""


# ===============================
# Register Generators
# ===============================

register_code_generator('.svg', svg_code_generator)
register_code_generator(('.svg', 'uncolored_svg'), svg_uncolored_code_generator)
register_code_generator('.pdf', pdf_code_generator)
register_code_generator('.png', png_code_generator)
register_code_generator('.jpg', jpg_code_generator)
register_code_generator('.jpeg', jpg_code_generator)


# ===============================
# Directory Scanning + Helpers
# ===============================

def scan_directories(base_path):
    """
    Scan all directories and subdirectories from base_path
    Returns a dictionary {directory: [list of relative file paths]}
    """
    structure = {}
    for root, dirs, files in os.walk(base_path):
        rel_dir = os.path.relpath(root, base_path)
        if rel_dir == ".":
            rel_dir = "."
        rel_files = [os.path.join(rel_dir, f) for f in files]
        structure[rel_dir] = rel_files
    return structure

def add_directory_comment(directory_path):
    """
    Generates a directory comment for output .ctx file
    """
    return f"% Files found in path {directory_path}"

def add_file_comment(file_name):
    """
    Return a comment line with the exact file name if its extension is one of:
    svg, pdf, png, jpg, jpeg
    """
    # Get file extension (without dot) in lowercase
    ext = os.path.splitext(file_name)[1][1:].lower()

    # Supported extensions
    supported_exts = {"svg", "pdf", "png", "jpg", "jpeg"}

    if ext in supported_exts:
        return f"% File: {file_name}"
    else:
        return None

def sort_code_blocks(code_blocks):
    """
    Sort the list alphabetically (case-insensitive)
    """
    return sorted(code_blocks, key=lambda x: x.lower())

def save_to_ctx_file(content, output_path):
    """
    Save text content into a .ctx file
    """
    with open(output_path, "w", encoding="utf-8") as ctx:
        ctx.write(content)
    print(f"[OK] Context file saved: {output_path}")


# ===============================
# Main Script
# ===============================

def main():
    base_path = os.getcwd()
    final_output_blocks = []

    # Step 1: Scan directories
    directory_structure = scan_directories(base_path)

    # Step 2: Iterate over sorted directories
    for directory in sorted(directory_structure.keys(), key=lambda x: x.lower()):
        files = directory_structure[directory]

        # Add directory comment
        final_output_blocks.append(add_directory_comment(directory))

        # Sort files alphabetically
        sorted_files = sorted(files, key=lambda f: f.lower())

        for file_rel_path in sorted_files:
            full_filename = os.path.basename(file_rel_path)

            # Add file comment if extension is supported
            file_comment = add_file_comment(full_filename)
            if file_comment:
                final_output_blocks.append(file_comment)

            # Generate file code only for supported files
            file_code = generate_code_for_file(file_rel_path)
            if file_code:
                final_output_blocks.append(file_code)

    # Step 3: Save to file
    output_file = os.path.join(base_path, "set_symbol_map.ctx")
    save_to_ctx_file("\n".join(final_output_blocks), output_file)
    
    
if __name__ == "__main__":
    main()

