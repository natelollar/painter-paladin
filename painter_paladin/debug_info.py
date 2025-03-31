"""Debug Info
==================================================

Get info helpful for debugging.
"""

import platform
import sys

import substance_painter as sp
from PySide6 import QtWidgets


class DebugInfo:
    """Debugging and testing functions for the plugin."""

    @staticmethod
    def environment_info() -> None:
        """Get info from the current Substance Painter environment."""
        # Substance Painter .exe location
        sp.logging.info(f"Substance Painter Location: {sys.executable}")
        # Substance Painter version
        sp.logging.info(f"Substance Painter Version: {sp.application.version_info()}")
        # Python location
        sp.logging.info(f"Python Location: {sys.base_prefix}")
        # Python version info
        sp.logging.info(f"Python Version: {sys.version}")
        # Windows version
        sp.logging.info(f"Windows version: {platform.platform()}")

        # Current project info
        if sp.project.is_open():
            sp.logging.info(f"Project name: {sp.project.name()}")
            sp.logging.info(f"Project file path: {sp.project.file_path()}")
        else:
            sp.logging.info("No project currently open.")

    @staticmethod
    def logging_example() -> None:
        """Get info from the current Substance Painter environment."""
        sp.logging.info("Here is an INFO logging example.")
        sp.logging.warning("Here is a WARNING logging example.")
        sp.logging.error("Here is an ERROR logging example.")

    @staticmethod
    def available_qt_windows() -> None:
        """Print available PySide Qt windows to log window."""
        try:
            # Get the main window
            main_window = sp.ui.get_main_window()

            # Find all dock widgets
            dock_widgets = main_window.findChildren(QtWidgets.QDockWidget)

            # Print widgets to log window.
            for widget in dock_widgets:
                sp.logging.info(f"{widget.objectName()}")

        except Exception as e:
            sp.logging.warning(f"{e}")

    @staticmethod
    def layer_help() -> None:
        """Get python help() for selected layer."""
        try:
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)

            if not selected_nodes:
                sp.logging.warning("No layer or effect selected.")
                return

            for node in selected_nodes:
                help(node)
                sp.logging.info(
                    f"Help outputed above for:\n{node.get_name()}\n"
                    f"Copy and paste to code editor as '.md' for better viewing.",
                )

        except Exception as e:
            sp.logging.warning(f"{e}")

    @staticmethod
    def module_help(module_name_str: str) -> None:
        """Get python help() for a substance_painter api module.

        Args:
            module_name_str (str): Substance Painter API module name.
            Ex. "ui", "textureset", "layerstack"

        """
        try:
            module = getattr(sp, module_name_str)
            help(module)
            sp.logging.info(
                f"Help outputed above for:\n{module}\n"
                f"Copy and paste to code editor as '.md' for better viewing.",
            )
        except Exception as e:
            sp.logging.warning(f"{e}")

    @staticmethod
    def toggle_window(window_name: str) -> None:
        """Toggle a Substance Painter Qt Window open and close.

        Args:
            window_name (str): Qt window name. Ex. "Log Window".
            Dev can get window names with "available_qt_windows()".

        """
        try:
            # Get the main window
            main_window = sp.ui.get_main_window()

            # Find all dock widgets
            dock_widgets = main_window.findChildren(QtWidgets.QDockWidget)

            # Look for the Window dock and toggle its visibility
            for dock in dock_widgets:
                if dock.objectName() == window_name:
                    # Toggle visibility
                    if dock.isVisible():
                        sp.logging.info(f"Closing {window_name}")
                        dock.setVisible(False)
                    else:
                        dock.setVisible(True)
                        dock.raise_()
                        sp.logging.info(f"Opening {window_name}")
                    break

        except Exception as e:
            sp.logging.warning(f"{e}")

    def test_code(self) -> None:
        """Send test code."""
        sp.logging.info("Test...")
