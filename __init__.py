"""Initialize the Painter Paladin plugin.
=========================================

Restart plugin via Substance Painter if UI window is missing.
UI window will reappear.  Toggle "Python < PainterToolset".
"""

# import importlib

import substance_painter as sp

from .painter_paladin import paladin_ui

# importlib.reload(paladin_ui)

# List to keep track of ui elements
plugin_widgets = []


def start_plugin() -> None:
    """Start plugin."""
    # Painter Paladin UI
    custom_ui_widget = paladin_ui.PainterPaladinUI()
    dock_widget = sp.ui.add_dock_widget(custom_ui_widget)
    dock_widget.setWindowTitle("Painter Paladin")

    # Append widgets to list for later cleanup
    plugin_widgets.append(custom_ui_widget)
    plugin_widgets.append(dock_widget)

    # Show UI
    dock_widget.show()


def close_plugin() -> None:
    """Close plugin."""
    # Delete widgets
    for widget in plugin_widgets:
        sp.ui.delete_ui_element(widget)
    plugin_widgets.clear()
