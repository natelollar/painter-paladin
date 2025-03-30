# Painter Toolset

- Tested in Substance Painter 2024 10.1.2 (Steam Edition), Windows 11.

- Place root "Painter Toolset" plugin folder into Substance Painter Python plugin folder.
    - Find Python plugin folder by going to `Python < Plugin Folder` in the top menubar.
    - Ex. `C:/Users/%username%/Documents/Adobe/Adobe Substance 3D Painter/python/plugins`

- Option 1: Download "Painter Toolset" from `github.com/natelollar/PainterToolset`, 
    - Unzip and drop entire `PainterToolset-main` folder into Substance Painter Python plugin folder.
- Option 2. Open up Windows command terminal in Substance Painter plugin folder location.
    - Enter: `git clone https://github.com/natelollar/PainterToolset`

- Open Painter Toolset with `Edit < Open Painter Toolset`.
    - This will open the plugins UI window.

- Toggle entire plugin on and off with `Plugin < PainterToolset` 
    - Plugin name will appear as whatever the root folder is named (Ex. PainterToolset, PainterToolset-main).  

- `PainterToolset.codeworkspace` is VS Code specific.
    - If needed, update the file paths for better import statement recognition.

- `ruff.toml` is used with the Ruff linter and formatter.
