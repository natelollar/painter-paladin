# Painter Paladin
A Substance Painter plugin. Has a dockable window with some helpful tools.
The main idea is to add tools that help with repetitive tasks.

---

- Tested in Substance Painter 2024 10.1.2 (Steam Edition), Windows 11.

- Place root "painter-paladin" folder into Substance Painter Python plugin folder.
    - Find Python plugin folder by going to `Python < Plugin Folder` in the top menubar.
    - Ex. `C:/Users/%username%/Documents/Adobe/Adobe Substance 3D Painter/python/plugins`

- Option 1: Download "Painter Paladin" from `github.com/natelollar/painter-paladin`, 
    - Unzip and drop entire `painter-paladin-main` folder into Substance Painter Python plugin folder.
- Option 2. Open up Windows command terminal in Substance Painter plugin folder location.
    - Enter: `git clone https://github.com/natelollar/painter-paladin`

- Open "Painter Paladin" by toggling the plugin on and off with `Python < Painter Paladin`.
    - This will open the plugins UI window if not already open.
    - Plugin name will appear as whatever the root folder is named (Ex. painter-paladin, painter-paladin-main).  

- UI window position and on/off state should be generally remembered between SP sessions.

- `ruff.toml` is used with the Ruff linter and formatter.

- Included `remote_utils` folder for testing, though not required.  
    - Helps send scripts remotley to SP via code editor.
    - Usually, though, restarting the plugin via `Python < Plugin Folder` was the simpler approach.

- Also, included `remove_pycache.bat` script, though not required.
    - Deletes (__pycache__) folders to help with testing.

## Features
- Apply settings to more than one layer, group, or layer effect at a time.
- Plan is to add more features over time.
- Feel free to send feature requests.

### Toolset Tab
- Quickly add passthrough layers for painting/ smudging fill layers.
- Enable disable fill layer channels.
- Quickly apply fill layer colors.
- Apply preset roughness or metallic settings.
- Apply opacity presets across all channels.
- Set mask and remove mask quickly.

### Debug Tab
- View environment information.
- Toggle Log Window and Python Console.
- Access Python module and layer documentation.
- Test Code button.

### Extra Tab
- Quickly add basic masks (noise, curvature, position, light).
- Apply additional preset color values to fill layers/ effects.
