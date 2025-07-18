MyProject/
├── Main.ctx                    ; Main entry point for compilation
├── README.md                   ; Project info
│
├── Setups/                     ; Setup files (page, layout, fonts, etc.)
│   ├── page-setup.tex
│   ├── interaction.tex
│   └── typographic.tex
│
├── Sections/                   ; Logical content sections of the document
│   ├── introduction.tex
│   ├── chapter1.tex
│   └── conclusion.tex
│
├── Sources/                    ; External resources (images, fonts, etc.)
│   ├── Images/
│   │   └── diagram1.png
│   ├── Fonts/
│   │   └── myfont.otf
│   └── Bib/                    ; Optional: bibliography or references
│       └── refs.bib
│
├── Symbols/                    ; Custom symbols or emoji maps
│   └── emojis.tex
│
├── Environments/               ; Reusable environments (e.g., definitions, boxed setups)
│   └── colorboxes.tex
│
├── Styles/                     ; Color themes, font families, spacing presets
│   └── dark-theme.tex
│
├── Macros/                     ; Project-wide macro definitions
│   └── custom-commands.tex
│
├── Builds/                     ; Output files (PDF, logs, etc.)
│   └── output.pdf
│
└── .emacs-session/             ; Emacs session file, untracked
