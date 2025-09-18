**Symbol Manager for ConTeXt** is a tool for managing thousands of custom symbols in the **ConTeXt LMTX** typesetting environment in a structured, editable, and scalable way.

This system is written in **Python**, and instead of directly embedding Lua code, its output is generated as `.ctx` files, which the user can easily edit and customize.

---

### Advantages of Using Python over Lua
- Greater flexibility and the ability to easily change parameters.
- Editable output (`.ctx`).
- Better understanding of the structure and how symbols are defined.
- Systematic management of size, color, kerning, height, and scale for each symbol.
- The ability to reuse definitions across different ConTeXt projects.

---

### Script Structure
1.  **`tex_safe_renamer.py`** → Renames files to a ConTeXt-compatible format.
2.  **`set_symbol_vars.py`** → Defines and saves global variables (size, color, etc.) into a `.ctx` file.
3.  **`set_symbol_maps.py`** → Creates symbol definitions for PDF, SVG, PNG, and JPG outputs.
4.  **`symbolmap.ctx`** → The main ConTeXt file that imports all symbol definitions.

---

### Folders and Color System
- **`colored_symbols`** → Symbols with a fixed color (the original file's color does not change).
- **`uncolored_svg`** → Symbols without a default color that can be dynamically colored (default: `currentcolor`).

---

### Naming Conventions and Automatic Prefixing
- Prefixes are automatically generated based on the name of the last subfolder followed by an `_`.
- Full support for various alphabets and Persian names (with the ability to add zero-width non-joiners to prevent characters from sticking together).
- A renaming script (`tex_safe_renamer.py`) for automatic correction.

---

### How to Use
1.  Run `python tex_safe_renamer.py` → Sanitize filenames.
2.  Run `python set_symbol_vars.py` → Set symbol variables and modify the `.ctx` file.
3.  Run `python set_symbol_maps.py` → Generate symbol definitions for different formats.
4.  In your main ConTeXt file:
    ```tex
    \input{symbolmap.ctx}
    ```

---

### Additional Notes
- You can define different versions of the same symbol with different sizes.
- For symbols with completely different and specific settings, it is better to create a separate folder.

---

**Prerequisites:**
- Python 3.11+
- ConTeXt LMTX

**License:** Free and unrestricted.

---
