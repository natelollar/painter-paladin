## Remote Utilities Folder
Tools for sending Python scripts from a code editor directly to Substance Painter for quick testing and development.

- Remote Utilities based on documentation found here:
    - https://adobedocs.github.io/painter-python-api/guides/remote-control/

- Typically, restarting the plugin via the Substance Painter menu was simpler for testing. `Python < Plugin Name`
    - Though, leaving the `remote_utils` folder here if needed.

---

- Make sure to launch Substance Painter in remote mode first via the `remote_launch.bat.`
    - Update Substance Painter `.exe` file path as needed.

- Add custom test functions to `example_script.py`. 
    - This is an example script that can be sent remotely to Substance Painter from a code editor.

- Setup task in a code editor to remotely send `example_script.py` to Substance Painter via `send_to_painter.py`.
    - Example task in VS Code. `.vscode/tasks.json` 
    ```
    {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Substance Send",
                "type": "shell",
                "command": "python",
                "args": [
                    "C:/Users/${env:USERNAME}/Documents/Adobe/Adobe Substance 3D Painter/python/plugins/painter-paladin/remote_utils/send_to_painter.py",
                    "${file}"
                ],
                "presentation": {
                    "reveal": "always",
                    "panel": "shared",
                    "clear": true
                },
                "problemMatcher": []
            }
        ]
    }
    ```
    - Trigger task via hotkey.
        - Example `keybindings.json` in VS Code.
    ```
    [
        {
            "key": "ctrl+alt+m",
            "command": "workbench.action.tasks.runTask",
            "args": "Substance Send",
            "when": "editorFocus"
        }
    ]
    ```

- The `send_to_painter.py` script uses a sys argument (sys.argv) to call the current file.
    - The `tasks.json` refers to this file as `${file}`.