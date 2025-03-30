import sys

import lib_remote


def send_script_to_painter():
    # Create connection to Substance Painter
    Remote = lib_remote.RemotePainter()

    # Check connection
    try:
        Remote.checkConnection()
        print("Connection to Substance Painter established")
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    # Get script path from command-line argument
    if len(sys.argv) < 2:
        print("Error: No script file provided. Please pass a script file path.")
        sys.exit(1)

    script_path = sys.argv[1]  # Use the file path passed by Sublime
    try:
        with open(script_path) as file:
            script_content = file.read()
    except FileNotFoundError:
        print(f"Error: Script file not found at {script_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading script file: {e}")
        sys.exit(1)

    # Execute the script in Substance Painter
    try:
        result = Remote.execScript(script_content, "python")
        print("Script executed successfully")
        if result:
            print(f"Result from Substance Painter: {result}")
    except lib_remote.ExecuteScriptError as e:
        print(f"Script execution failed: {e}")
    except Exception as e:
        print(f"Unexpected error during execution: {e}")


if __name__ == "__main__":
    send_script_to_painter()


# Docs
# https://adobedocs.github.io/painter-python-api/guides/remote-control/