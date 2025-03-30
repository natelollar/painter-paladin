"""Initialize the Painter Toolset plugin.
=========================================

Restart plugin via Substance Painter if UI window is missing.
UI window will reappear.  Toggle "Python < PainterToolset".
"""

import substance_painter as sp

from .painter_toolset import toolset_ui

# List to keep track of ui elements
plugin_widgets = []


def start_plugin():
    """Start plugin."""
    # Painter Toolset UI
    custom_ui_widget = toolset_ui.PainterToolsetUI()
    dock_widget = sp.ui.add_dock_widget(custom_ui_widget)
    dock_widget.setWindowTitle("Painter Toolset Plugin")

    # Append widgets to list for later cleanup
    plugin_widgets.append(custom_ui_widget)
    plugin_widgets.append(dock_widget)

    # Show UI
    dock_widget.show()


def close_plugin():
    """Close plugin."""
    # Delete widgets
    for widget in plugin_widgets:
        sp.ui.delete_ui_element(widget)
    plugin_widgets.clear()
