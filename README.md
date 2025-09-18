# ConTeXt LMTX Starter Template (starter-template)

**ConTeXt-StarterKit** is a ready-to-use template for creating professional documents with **ConTeXt LMTX**.  
It provides a robust framework to help you organize content, configurations, and resources easily, while ensuring portability and ease of use.

---

## ✨ Key Features

- **Modular Structure:** Cleanly separates content, configurations, and resources.
- **Automated Resource Discovery:** Recursively scans `Sections` and `Sources` so files are instantly available across your document.
- **Portable Font Management:** Add custom fonts simply by placing them inside the `Fonts` directory — no system installation required.
- **Streamlined Symbol Definition:** Automate the creation and parameterization of symbols with a Python workflow.
- **Centralized Bibliography:** Keep all bibliographic references and settings in one place.
- **Ready to Compile:** Preconfigured main file to get started instantly.

---

## 🚀 Getting Started

The main entry point of your project is **`starter-template.ctx`**.

To build your document, navigate to your project’s root folder and run:
```bash
context starter-template.ctx

This command will process all linked files and generate the final PDF based on your configured structure.

---

## 📂 Project Structure


.
├── starter-template.ctx   # Main file to compile
├── Backups/               # Safe storage folder (ignored by the project)
├── Sections/              # All main content (chapters, intro, etc.)
├── Setups/                # Global configurations and path settings
└── Sources/               # Resources (fonts, images, symbols, etc.)

---

### **`starter-template.ctx`**
The master file. Loads all necessary configurations from `Setups` and imports content from `Sections` to build the document.  
You’ll rarely need to modify this file directly.

---

### **`Backups/`**
An isolated directory for drafts, old versions, or unused files.  
Contents here are ignored during the build process.

---

### **`Sections/`**
Contains the main written content of your document. Each section should be a separate `.ctx` file.  

Example:
- `Sections/preface.ctx`
- `Sections/section1.ctx`
- `Sections/conclusion.ctx`

---

### **`Setups/`**
Holds all **global configuration** files.

- Configured to **recursively search** `Sections` and `Sources` directories.
- **Add New Paths:** If you create a new top-level directory (e.g., `Appendices/`), register it in `Setups/SearchPaths.ctx`.

---

### **`Sources/`**
Central resource hub. Contains:

#### `Sources/Symbols/`
Custom symbol definitions and parameters (automated via Python).

#### `Sources/Fonts/`
Portable fonts — just drop `.otf` or `.ttf` files here.

#### `Sources/Bibliography/`
All `.bib` files and bibliography style settings.

#### `Sources/Images/`
Organize all images here (supports nested folders).

---

## 🔧 Customization

- **Add New Sections:** Create new `.ctx` files in `Sections/`.
- **Define Custom Commands:** Modify configuration files in `Setups/`.
- **Expand Resources:** Add fonts, images, or bibliography entries to the respective `Sources` folders.

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for full details.


---

If you want, I can also create a **dual-language README** (English + Persian) so GitHub renders it beautifully for both audiences.  
Do you want me to prepare that next?
