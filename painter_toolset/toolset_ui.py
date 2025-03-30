"""Toolset UI Window
===============================

This module contains the PySide UI window and button connections.
"""

import importlib

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from . import debug_info, toolset_logic
from .debug_info import DebugInfo
from .toolset_logic import ToolsetLogic

importlib.reload(debug_info)
importlib.reload(toolset_logic)


class PainterToolsetUI(QWidget):
    """Pyside UI window with tabs for Painter Toolset."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create layout
        self.setup_ui()

    def setup_ui(self):
        """Set up all main UI elements."""
        # ----------------------------------------------- #
        # -------------------- Setup -------------------- #
        # Create main layout
        main_layout = QVBoxLayout(self)

        # Create QTabWidget to hold tabs.
        tab_main_widget = QTabWidget()

        # Create tabs with layout and scroll areas.
        tab1_scroll_area = QScrollArea()
        tab1_scroll_area.setWidgetResizable(True)
        tab1_content = QWidget()
        tab1_scroll_area.setWidget(tab1_content)
        tab1_layout = QVBoxLayout(tab1_content)
        tab2_scroll_area = QScrollArea()
        tab2_scroll_area.setWidgetResizable(True)
        tab2_content = QWidget()
        tab2_scroll_area.setWidget(tab2_content)
        tab2_layout = QVBoxLayout(tab2_content)
        tab3_scroll_area = QScrollArea()
        tab3_scroll_area.setWidgetResizable(True)
        tab3_content = QWidget()
        tab3_scroll_area.setWidget(tab3_content)
        tab3_layout = QVBoxLayout(tab3_content)

        # ----------------------------------------------- #
        # -------------------- TAB 1 -------------------- #
        # Toolset Tab

        # -------------------- #
        # Paintable fill layer creation.
        paintable_fill_layout = QHBoxLayout()
        # Button. Create Fill Layer with Paint Effect in Passthrough & then Fill Effect.
        paintable_fill_layer_btn = CustomButton(
            title="Paintable Fill Layer (Passthrough)",
        )
        paintable_fill_layer_btn.clicked.connect(
            lambda: ToolsetLogic().paintable_fill_layer(),
        )
        paintable_fill_layout.addWidget(paintable_fill_layer_btn)
        # Button. Create Group with Fill Layer and Paint Layer in Passthrough.
        paintable_fill_layer_btn = CustomButton(
            title="Paintable Fill Layer Group (Passthrough)",
        )
        paintable_fill_layer_btn.clicked.connect(
            lambda: ToolsetLogic().paintable_fill_layer_group(),
        )
        paintable_fill_layout.addWidget(paintable_fill_layer_btn)
        # Add to tab layout.
        tab1_layout.addLayout(paintable_fill_layout)

        # -------------------- #
        # Channels enable/ disable. For Fill layer.
        channels_toggle_layout = QHBoxLayout()
        # Button. Enable all channels for selected.
        apply_channels_btn = CustomButton(title="Enable All Channels (Fill Layer)")
        apply_channels_btn.clicked.connect(
            lambda: ToolsetLogic().enable_channels_for_selected_fill(),
        )
        channels_toggle_layout.addWidget(apply_channels_btn)
        # Button. Enable Base Color only.
        disable_all_except_base_btn = CustomButton(title="Color Channel Only (Fill Layer)")
        disable_all_except_base_btn.clicked.connect(
            lambda: ToolsetLogic().disable_all_except_base_color(),
        )
        channels_toggle_layout.addWidget(disable_all_except_base_btn)
        # Add to tab layout.
        tab1_layout.addLayout(channels_toggle_layout)

        # -------------------- #
        # Set skin color values.
        set_skin_color_layout = QHBoxLayout()
        # Create row title.
        skin_color_label = QLabel("Skin Color (Fill):")
        skin_color_label.setFixedWidth(88)
        set_skin_color_layout.addWidget(skin_color_label)
        # RGB values.
        skin_color_values = [
            (221, 176, 166),  # Very Light
            (251, 179, 153),  # Light
            (200, 151, 129),  # Medium
            (207, 147, 113),
            (206, 128, 95),  # Tan
            (140, 85, 61),  # Dark
        ]
        # Buttons.
        for value in skin_color_values:
            set_skin_color_btn = CustomButton(value)
            rgb_0_1 = tuple(rgb_val / 255 for rgb_val in value)
            set_skin_color_btn.clicked.connect(
                lambda v=rgb_0_1: ToolsetLogic().set_channel_value(v, "BaseColor"),
            )
            set_skin_color_layout.addWidget(set_skin_color_btn, 1)
        # Add to tab layout.
        tab1_layout.addLayout(set_skin_color_layout)

        # -------------------- #
        # Button. Set monochrome color values.
        set_mono_color_layout = QHBoxLayout()
        # Create row title.
        mono_color_label = QLabel("Mono Color (Fill):")
        mono_color_label.setFixedWidth(88)
        set_mono_color_layout.addWidget(mono_color_label)
        # Grayscale values.
        mono_color_values = [0.0, 0.25, 0.5, 0.75, 1.0]
        # Buttons.
        for value in mono_color_values:
            rgb_val = int(value * 255)
            set_mono_color_btn = CustomButton(rgb_val)
            set_mono_color_btn.clicked.connect(
                lambda v=value: ToolsetLogic().set_channel_value(v, "BaseColor"),
            )
            set_mono_color_layout.addWidget(set_mono_color_btn)
        # Add to tab layout.
        tab1_layout.addLayout(set_mono_color_layout)

        # -------------------- #
        # Set roughness values.
        set_roughness_layout = QHBoxLayout()
        # Create row title.
        roughness_label = QLabel("Roughness (Fill):")
        roughness_label.setFixedWidth(88)
        set_roughness_layout.addWidget(roughness_label)
        # Grayscale values.
        roughness_values = [0.0, 0.25, 0.5, 0.75, 1.0]
        # Buttons.
        for value in roughness_values:
            set_roughness_btn = CustomButton(title=f"{value}")
            set_roughness_btn.clicked.connect(
                lambda v=value: ToolsetLogic().set_channel_value(v, "Roughness"),
            )
            set_roughness_layout.addWidget(set_roughness_btn)
        # Add to tab layout.
        tab1_layout.addLayout(set_roughness_layout)

        # -------------------- #
        # Buttons. Set metallic values.
        set_metallic_layout = QHBoxLayout()
        metallic_label = QLabel("Metallic (Fill):")
        metallic_label.setFixedWidth(88)
        set_metallic_layout.addWidget(metallic_label)
        metallic_values = [0.0, 0.25, 0.5, 0.75, 1.0]
        for value in metallic_values:
            set_metallic_btn = CustomButton(title=f"{value}")
            set_metallic_btn.clicked.connect(
                lambda v=value: ToolsetLogic().set_channel_value(v, "Metallic"),
            )
            set_metallic_layout.addWidget(set_metallic_btn)
        tab1_layout.addLayout(set_metallic_layout)

        # -------------------- #
        # Buttons. Set opacity for all channels, for selected.
        set_opacity_layout = QHBoxLayout()
        opacity_label = QLabel("Opacity:")
        opacity_label.setFixedWidth(88)
        set_opacity_layout.addWidget(opacity_label)
        opacity_values = [0.0, 0.25, 0.5, 0.75, 1.0]
        for value in opacity_values:
            set_opacity_btn = CustomButton(title=f"{value}")
            set_opacity_btn.clicked.connect(
                lambda v=value: ToolsetLogic().set_opacity(opacity_val=v),
            )
            set_opacity_layout.addWidget(set_opacity_btn)
        tab1_layout.addLayout(set_opacity_layout)

        # -------------------- #
        # Add or set masks.
        set_mask_layout = QHBoxLayout()
        # Button.
        black_mask_btn = CustomButton(title="Set Black Mask")
        black_mask_btn.clicked.connect(
            lambda: ToolsetLogic().setup_mask(background="Black"),
        )
        set_mask_layout.addWidget(black_mask_btn)
        # Button.
        white_mask_btn = CustomButton(title="Set White Mask")
        white_mask_btn.clicked.connect(
            lambda: ToolsetLogic().setup_mask(background="White"),
        )
        set_mask_layout.addWidget(white_mask_btn)
        tab1_layout.addLayout(set_mask_layout)

        # -------------------- #
        # Remove mask and add mask with fill.
        mask_01_layout = QHBoxLayout()
        # Button. Remove Mask
        remove_layer_mask_btn = CustomButton(title="Remove Mask")
        remove_layer_mask_btn.clicked.connect(
            lambda: ToolsetLogic().remove_layer_mask(),
        )
        mask_01_layout.addWidget(remove_layer_mask_btn)
        # Button. Add fill effect to mask for transparency control.
        add_mask_fill = CustomButton(title="Add Mask Fill")
        add_mask_fill.clicked.connect(
            lambda: ToolsetLogic().add_mask_fill(),
        )
        mask_01_layout.addWidget(add_mask_fill)
        tab1_layout.addLayout(mask_01_layout)

        # -------------------- #
        # Set channels to passthrough and create passthrough paint layer.
        passthrough_btns_layout = QHBoxLayout()
        # Button. Set blending mode to passthrough.
        set_passthrough_mode_btn = CustomButton(title="Set Passthrough Mode")
        set_passthrough_mode_btn.clicked.connect(
            lambda: ToolsetLogic().set_passthrough_mode(),
        )
        passthrough_btns_layout.addWidget(set_passthrough_mode_btn)
        # Button. Passthrough paint layer.
        add_passthrough_paint_layer_btn = CustomButton(title="Add Passthrough Layer")
        add_passthrough_paint_layer_btn.clicked.connect(
            lambda: ToolsetLogic().add_passthrough_paint_layer(),
        )
        passthrough_btns_layout.addWidget(add_passthrough_paint_layer_btn)
        tab1_layout.addLayout(passthrough_btns_layout)

        # ----------------------------------------------- #
        # -------------------- TAB 2 -------------------- #
        # Debug tab.

        # -------------------- #
        # Buttons. Get helpful info.
        envrionment_info_btn = CustomButton(title="Environment Info (Log Window)")
        envrionment_info_btn.clicked.connect(DebugInfo.environment_info)
        tab2_layout.addWidget(envrionment_info_btn)

        logging_example_btn = CustomButton(title="Logging Example (Log Window)")
        logging_example_btn.clicked.connect(DebugInfo.logging_example)
        tab2_layout.addWidget(logging_example_btn)

        log_window_btn = CustomButton(title="Toggle Log Window")
        log_window_btn.clicked.connect(lambda: DebugInfo().toggle_window("Log Window"))
        tab2_layout.addWidget(log_window_btn)

        python_console_btn = CustomButton(title="Toggle Python Console")
        python_console_btn.clicked.connect(
            lambda: DebugInfo().toggle_window("pythonConsole"),
        )
        tab2_layout.addWidget(python_console_btn)

        available_qt_windows_btn = CustomButton(title="Print Available Qt Windows")
        available_qt_windows_btn.clicked.connect(DebugInfo.available_qt_windows)
        tab2_layout.addWidget(available_qt_windows_btn)

        layer_help_btn = CustomButton(title="Selected Layer help()")
        layer_help_btn.clicked.connect(DebugInfo.layer_help)
        tab2_layout.addWidget(layer_help_btn)

        # -------------------- #
        # Buttons. Python module help().
        module_help_layout = QHBoxLayout()

        ui_module_help_btn = CustomButton(title="ui help()")
        ui_module_help_btn.clicked.connect(lambda: DebugInfo.module_help("ui"))
        module_help_layout.addWidget(ui_module_help_btn)

        layerstack_module_help_btn = CustomButton(title="layerstack help()")
        layerstack_module_help_btn.clicked.connect(
            lambda: DebugInfo().module_help("layerstack"),
        )
        module_help_layout.addWidget(layerstack_module_help_btn)

        textureset_module_help_btn = CustomButton(title="textureset help()")
        textureset_module_help_btn.clicked.connect(
            lambda: DebugInfo().module_help("textureset"),
        )
        module_help_layout.addWidget(textureset_module_help_btn)

        colormanagement_module_help_btn = CustomButton(title="colormanagement help()")
        colormanagement_module_help_btn.clicked.connect(
            lambda: DebugInfo().module_help("colormanagement"),
        )
        module_help_layout.addWidget(colormanagement_module_help_btn)
        logging_module_help_btn = CustomButton(title="logging help()")
        logging_module_help_btn.clicked.connect(lambda: DebugInfo.module_help("logging"))
        module_help_layout.addWidget(logging_module_help_btn)

        resource_module_help_btn = CustomButton(title="resource help()")
        resource_module_help_btn.clicked.connect(
            lambda: DebugInfo().module_help("resource"),
        )
        module_help_layout.addWidget(resource_module_help_btn)

        # Add to tab layout.
        tab2_layout.addLayout(module_help_layout)

        # -------------------- #
        # Button. For testing.
        test_code_btn = CustomButton(title="Test Code")
        test_code_btn.clicked.connect(lambda: DebugInfo().test_code())
        tab2_layout.addWidget(test_code_btn)

        # ----------------------------------------------- #
        # -------------------- TAB 3 -------------------- #
        # Extra tab.

        # -------------------- #
        # Add noise mask.  Add curvature mask.
        # Works as new mask or pre-existing mask.
        mask_effect_01_layout = QHBoxLayout()
        # Button.
        add_noise_mask_btn = CustomButton(title="Noise Mask")
        add_noise_mask_btn.clicked.connect(
            lambda: ToolsetLogic().add_noise_mask(),
        )
        mask_effect_01_layout.addWidget(add_noise_mask_btn)
        # Button.
        add_curvature_mask_btn = CustomButton(title="Curvature Mask")
        add_curvature_mask_btn.clicked.connect(
            lambda: ToolsetLogic().add_generator_mask("Curvature"),
        )
        mask_effect_01_layout.addWidget(add_curvature_mask_btn)
        tab3_layout.addLayout(mask_effect_01_layout)

        # -------------------- #
        # Add position mask.  Add light mask.
        # Works as new or pre-existing mask.
        mask_effect_02_layout = QHBoxLayout()
        # Button.
        add_position_mask_btn = CustomButton(title="Position Mask")
        add_position_mask_btn.clicked.connect(
            lambda: ToolsetLogic().add_generator_mask("Position"),
        )
        mask_effect_02_layout.addWidget(add_position_mask_btn)
        # Button.
        add_light_mask_btn = CustomButton(title="Light Mask")
        add_light_mask_btn.clicked.connect(
            lambda: ToolsetLogic().add_generator_mask("Light"),
        )
        mask_effect_02_layout.addWidget(add_light_mask_btn)
        tab3_layout.addLayout(mask_effect_02_layout)

        # -------------------- #
        # Set metal color values.
        # As in BaseColor picked from metal images.
        set_metal_color_layout = QHBoxLayout()
        # Row title.
        metal_color_label = QLabel("Metal Color (Fill):")
        metal_color_label.setFixedWidth(88)
        set_metal_color_layout.addWidget(metal_color_label)
        # RGB values.
        metal_color_values = [
            (176, 174, 174),
            (160, 152, 147),
            (209, 127, 61),
            (114, 67, 54),
            (111, 156, 200),
            (37, 123, 174),
        ]
        # Buttons.
        for value in metal_color_values:
            set_metal_color_btn = CustomButton(value)
            rgb_0_1 = tuple(rgb_val / 255 for rgb_val in value)
            set_metal_color_btn.clicked.connect(
                lambda v=rgb_0_1: ToolsetLogic().set_channel_value(v, "BaseColor"),
            )
            set_metal_color_layout.addWidget(set_metal_color_btn)
        # Add to tab layout.
        tab3_layout.addLayout(set_metal_color_layout)

        # -------------------- #
        # Buttons. Set basic color values.
        set_basic_color_layout = QHBoxLayout()
        basic_color_label = QLabel("Basic Color (Fill):")
        basic_color_label.setFixedWidth(88)
        set_basic_color_layout.addWidget(basic_color_label)
        basic_color_values = [
            (255, 0, 0),  # Red
            (255, 255, 0),  # Yellow
            (0, 255, 0),  # Green
            (0, 255, 255),  # Cyan
            (0, 0, 255),  # Blue
            (255, 0, 255),  # Magenta
        ]
        for value in basic_color_values:
            set_basic_color_btn = CustomButton(value)
            rgb_0_1 = tuple(rgb_val / 255 for rgb_val in value)
            set_basic_color_btn.clicked.connect(
                lambda v=rgb_0_1: ToolsetLogic().set_channel_value(v, "BaseColor"),
            )
            set_basic_color_layout.addWidget(set_basic_color_btn)
        tab3_layout.addLayout(set_basic_color_layout)

        # ------------------------------------------------ #
        # -------------------- Finish -------------------- #
        tab1_layout.addStretch()
        tab2_layout.addStretch()
        tab3_layout.addStretch()

        tab_main_widget.addTab(tab1_scroll_area, "Toolset")
        tab_main_widget.addTab(tab2_scroll_area, "Debug")
        tab_main_widget.addTab(tab3_scroll_area, "Extra")

        main_layout.addWidget(tab_main_widget)


class CustomButton(QFrame):
    """Custom button with better resizing for SP API.
    Can be styled with either a background color or a text title.
    Background will be gray if title given.
    """

    # Signal emitted whenever QFrame box is clicked.
    clicked = Signal()

    def __init__(
        self,
        rgb_tuple: int | tuple[int, int, int] | None = None,
        title: str | None = None,
        parent=None,
    ) -> None:
        """Initialize a custom button with either a color or title.

        Args:
            rgb_tuple: An (R, G, B) tuple representing the button color.
                Can also be single integer value (RGB 255).
                Can be None if title is provided.
            title: Text to display on the button. If provided, rgb_tuple is ignored.
            parent: The parent widget in Qt's hierarchy. Defaults to None.

        """
        super().__init__(parent)

        # Set minimum size so QFrame button doesn't shrink too small.
        self.setMinimumSize(QSize(24, 24))

        # Allows QFrame button width to expand.
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        if title is None:  # if no title, go with color background
            if isinstance(rgb_tuple, int):  # if single int is given
                self.rgb_tuple = (rgb_tuple, rgb_tuple, rgb_tuple)
            else:  # if full rgb tuple is given
                self.rgb_tuple = rgb_tuple
            # Use stylesheet to set the background color and border styling.
            # Hover effect is also handled here. Increase border thickness on mouse hover.
            r, g, b = self.rgb_tuple
            self.setStyleSheet(f"""
                QFrame {{
                background-color: rgb({r}, {g}, {b}); 
                border-radius: 3px; 
                border: 1px solid rgba(102, 102, 102, 200);
                }}
                QFrame:hover {{
                border: 1px solid rgba(200, 200, 255, 200);
                border-radius: 3px;
                }}
            """)
        else:  # if title is given add button text. apply gray background.
            title_layout = QVBoxLayout(self)
            title_layout.setContentsMargins(0, 0, 0, 0)
            title_layout.setSpacing(0)

            # Add button text.
            # Use QLabel on top. QFrame not supporting text.
            self.label = QLabel(title)
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setStyleSheet("background-color: transparent;")
            title_layout.addWidget(self.label)
            self.setLayout(title_layout)

            # Apply background color to the frame
            # Turn off QLabel color, only use QFrame. Was doubling values.
            self.setStyleSheet("""
                QFrame {
                background-color: rgb(42, 42, 42); 
                border: 1px solid rgba(102, 102, 102, 100);
                border-radius: 3px;
                padding: 0px;          
                }
                QFrame:hover {
                background-color: rgb(36, 36, 36); 
                border: 1px solid rgba(200, 200, 255, 100);
                border-radius: 3px;
                padding: 0px; 
                }
                QLabel {
                background-color: transparent; 
                border: 0px;
                border-radius: 0px;
                padding: 0px;          
                }      
                QLabel:hover {
                background-color: transparent; 
                border: 0px;
                border-radius: 0px;
                padding: 0px;          
                }        
            """)

        # Enable mouse tracking.
        # Not required for hover effect.
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        """Handles mouse press event on this widget."""
        self.clicked.emit()
        super().mousePressEvent(event)
