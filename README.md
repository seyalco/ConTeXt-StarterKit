# ConTeXt LMTX Starter Template (starter-template)

ConTeXt-StarterKit is a ready-to-use template for producing professional documents using **ConTeXt LMTX**. It provides a robust framework to streamline document creation, making it easy to organize content, settings, and resources while ensuring portability and ease of use.

## ✨ Key Features

-   **Modular Structure:** A clean and organized directory layout separates content, configurations, and resources.
-   **Automated Resource Discovery:** Recursively finds and registers files in `Sections` and `Sources`, making them instantly available throughout your document.
-   **Portable Font Management:** Use custom fonts by simply dropping them into the `Fonts` directory—no system-wide installation required.
-   **Streamlined Symbol Definition:** A Python-based workflow automates the creation and parameterization of custom symbols.
-   **Centralized Bibliography:** Manage all your bibliographic references and settings in one place.
-   **Ready to Compile:** Get started immediately with a pre-configured main file.

## 🚀 Getting Started

The main file that orchestrates the entire document is `starter-template.ctx`.

To compile your document, navigate to the project's root directory and run the following command in your terminal:

```bash
context starter-template.ctx
```

This command will process all the linked files and generate your final PDF document based on the content and configurations provided in the project structure.

## 📂 Project Structure

The project is organized into four main directories, each with a specific purpose.


.
├── starter-template.ctx   # The main file to compile
├── Backups/               # A safe place for file storage, ignored by the project
├── Sections/              # Your document's content (chapters, intro, etc.)
├── Setups/                # Global configurations and path settings
└── Sources/               # Document resources (fonts, images, symbols, etc.)

### `starter-template.ctx`

This is the master file. It loads all necessary configurations from `Setups` and includes the content from `Sections` to build the final document. You should not need to edit this file often; instead, work within the other directories.

### `Backups/`

This directory is intentionally isolated from the main project compilation. It serves as a safe location to store drafts, old versions of files, or any other assets without interfering with the build process. The contents of this folder are not tracked or used by ConTeXt.

### `Sections/`

This is where the actual content of your document resides. Each part of your document, such as the introduction, chapters, or appendices, should be a separate file within this directory. The template is configured to automatically find and make these files available for inclusion in `starter-template.ctx`.

Example:
- `Sections/preface.ctx`
- `Sections/section1.ctx`
- `Sections/conclusion.ctx`

### `Setups/`

This directory holds all the global configuration files for your document.

-   The template is pre-configured to **recursively search** for files within the `Sections` and `Sources` directories. This means any text or graphic file you add there will be automatically discoverable.
-   **Adding New Search Paths:** If you create a new top-level directory (e.g., `Appendices/`) and want its contents to be automatically discovered, you must register it. To do this, edit the `Setups/SearchPaths.ctx` file and add your new directory's name to the search path list, following the instructions within that file.

### `Sources/`

This directory is the central hub for all external resources used in your document. It is further divided into subfolders for better organization.

#### `Sources/Symbols/`

Define and manage custom symbols here. This template includes a powerful workflow using Python scripts to automatically define and parameterize symbols. Follow the guidance inside this directory to create reusable symbols that can be easily invoked throughout your document.

#### `Sources/Fonts/`

This folder enables **portable font management**. To use a custom font, simply place its file (e.g., `.otf`, `.ttf`) inside this directory. The setup automatically registers these fonts for use in your document without requiring you to install them system-wide.

#### `Sources/Bibliography/`

Manage your bibliographic data here. Place your `.bib` files in this directory and configure your citation style settings. This keeps all reference-related information neatly organized.

#### `Sources/Images/`

Place all images and graphics that you intend to use in your document here. The template is configured to recursively search this directory and all its subdirectories. This means you can organize your images into folders (e.g., `Images/chapter-1/`, `Images/plots/`) and still reference them directly by filename without specifying the full path.

## 🔧 Customization

This template is designed to be a starting point. You are encouraged to modify and extend it to fit your needs:

-   **Add New Sections:** Create new `.tex` files in the `Sections` directory and include them in `starter-template.ctx`.
-   **Define Custom Commands:** Use the files in the `Setups` directory to define your own macros, environments, and styling rules.
-   **Expand Resources:** Add your own fonts, images, and bibliography files to the corresponding `Sources` subdirectories.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

