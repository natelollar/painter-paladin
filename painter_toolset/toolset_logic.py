"""Painter Toolset Logic
===============================

This module contains logic for toolset buttons and actions in Substance Painter.
"""

#import traceback  # noqa: F401

import substance_painter as sp


class ToolsetLogic:
    """Logic for the plugin."""

    def paintable_fill_layer(self) -> None:
        """Creates a Fill Layer, inserts a Paint Effect inside it, adds a Fill Effect below it,
        and ensures all channels are enabled for the Fill Effect and Layer.
        Sets blend mode for Paint Effect to Passthrough for all channels.
        Paint Effect channel activation not supported.
        Paint channels work in unison and are not separate like Fill channels.
        """
        try:
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)

            # Insert Fill Layer at the top
            insert_position = sp.layerstack.InsertPosition.above_node(selected_nodes[0])
            fill_layer = sp.layerstack.insert_fill(insert_position)
            fill_layer.set_name("fill_layer")
            sp.logging.info("Created Fill Layer")

            # Get available channels on the Fill Layer
            available_channels = set(stack.all_channels())

            # Enable available channels on Fill Layer
            fill_layer.active_channels = available_channels

            # Insert a Paint Effect inside the Fill Layer's content stack
            insert_position = sp.layerstack.InsertPosition.inside_node(
                fill_layer,
                sp.layerstack.NodeStack.Content,
            )
            paint_effect = sp.layerstack.insert_paint(insert_position)
            paint_effect.set_name("paint_effect_passthrough")
            sp.logging.info("Inserted Paint Effect inside Fill Layer")
            # Paint Effect channels fail to activate. Activation not supported.
            # paint_effect.active_channels = available_channels

            # Set blend mode to Passthrough for the Paint Effect
            passthrough_blend_mode = sp.layerstack.BlendingMode.Passthrough
            for channel in available_channels:
                paint_effect.set_blending_mode(passthrough_blend_mode, channel)

            # Insert a Fill Effect directly below the Paint Effect
            insert_position = sp.layerstack.InsertPosition.below_node(paint_effect)
            fill_effect = sp.layerstack.insert_fill(insert_position)
            fill_effect.set_name("fill_effect")
            fill_effect.active_channels = available_channels  # Enable channels on Fill Effect
            sp.logging.info("Inserted Fill Effect below Paint Effect.")

        except sp.exception.ProjectError:
            sp.logging.warning("No project loaded. Please open or start a new project.")

        except Exception as e:
            sp.logging.warning(f"{e}")

    def paintable_fill_layer_group(self) -> None:
        """Similar to "paintable_fill_layer()".
        Creats a group, a paint layer with passthrough blend mode, and a fill layer.
        Uses a group instead of effect nodes in a fill layer.
        """
        try:
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)
            available_channels = set(stack.all_channels())

            # Insert Group Layer above selection
            insert_position = sp.layerstack.InsertPosition.above_node(selected_nodes[0])
            group_layer = sp.layerstack.insert_group(insert_position)
            group_layer.set_name("group_layer")
            sp.logging.info(f"Created: {group_layer.get_name()}")

            # Insert Fill Layer inside group layer
            insert_position = sp.layerstack.InsertPosition.inside_node(
                group_layer,
                sp.layerstack.NodeStack.Substack,
            )
            fill_layer = sp.layerstack.insert_fill(insert_position)
            fill_layer.set_name("fill_layer")
            fill_layer.active_channels = available_channels  # turn on channels
            sp.logging.info(f"Created: {fill_layer.get_name()}")

            # Insert Paint Layer inside group layer
            insert_position = sp.layerstack.InsertPosition.above_node(fill_layer)
            paint_layer = sp.layerstack.insert_paint(insert_position)
            paint_layer.set_name("passthrough_paint_layer")
            sp.logging.info(f"Created: {paint_layer.get_name()}")

            # Set blend mode to Passthrough for the Paint Layer
            passthrough_blend_mode = sp.layerstack.BlendingMode.Passthrough
            for channel in available_channels:
                paint_layer.set_blending_mode(passthrough_blend_mode, channel)
            # Check blending mode
            blend_mode = paint_layer.get_blending_mode(list(available_channels)[0])
            sp.logging.info(f"{paint_layer.get_name()} - {blend_mode.name}")

        except sp.exception.ProjectError:
            sp.logging.warning("No project loaded. Please open or start a new project.")

        except Exception as e:
            # sp.logging.warning(f"Error: {e}\nTraceback: {traceback.format_exc()}")
            sp.logging.warning(f"{e}")

    def setup_mask(self, background: str) -> None:
        """Add mask to selected layers, white or black.
        Change color if mask already exists.
        """
        try:
            # Get selected
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)

            # Mask types
            white_mask = sp.layerstack.MaskBackground.White
            black_mask = sp.layerstack.MaskBackground.Black

            if background.lower() == "black":
                for node in selected_nodes:
                    mask_check = sp.layerstack.LayerNode.has_mask(node)
                    if mask_check is False:  # Apply new mask
                        sp.layerstack.LayerNode.add_mask(node, black_mask)
                    else:
                        sp.layerstack.LayerNode.set_mask_background(node, black_mask)
                    current_mask = sp.layerstack.LayerNode.get_mask_background(node)
                    sp.logging.info(f"Mask applied to {node.get_name()}: {current_mask.name}")
            elif background.lower() == "white":
                for node in selected_nodes:
                    mask_check = sp.layerstack.LayerNode.has_mask(node)
                    if mask_check is False:  # Apply new mask
                        sp.layerstack.LayerNode.add_mask(node, white_mask)
                    else:
                        sp.layerstack.LayerNode.set_mask_background(node, white_mask)
                    current_mask = sp.layerstack.LayerNode.get_mask_background(node)
                    sp.logging.info(f"Mask applied to {node.get_name()}: {current_mask.name}")
            else:
                sp.logging.warning(f"Unsupported background: {background}")

        except Exception as e:
            sp.logging.warning(f"{e}")

    def remove_layer_mask(self) -> None:
        """Remove mask from selected layers."""
        try:
            # Get selected
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)

            # Remove masks for selected
            for node in selected_nodes:
                sp.layerstack.LayerNode.remove_mask(node)

        except Exception as e:
            sp.logging.warning(f"{e}")

    def add_mask_fill(self) -> None:
        """Add fill to layer's mask.
        A decent way to control transparency.
        Will create mask first if missing.
        """
        try:
            # Get selected
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)

            # Mask types
            white_mask = sp.layerstack.MaskBackground.White

            for node in selected_nodes:
                mask_check = sp.layerstack.LayerNode.has_mask(node)
                if mask_check is False:  # Create mask first if doesn't exist
                    sp.layerstack.LayerNode.add_mask(node, white_mask)
                else:
                    pass
                insert_position = sp.layerstack.InsertPosition.inside_node(
                    node,
                    sp.layerstack.NodeStack.Mask,
                )
                fill_effect = sp.layerstack.insert_fill(insert_position)
                fill_effect.set_name("fill_effect")
                # Set and unset a fill resource to trigger the greyscale adjustment slider
                noise_resource = sp.resource.search("n:White Noise")[0]
                fill_effect.set_source(None, noise_resource.identifier())
                fill_effect.reset_source()

                sp.logging.info(f"{node.get_name()} - {fill_effect.get_name()}")

        except Exception as e:
            # sp.logging.warning(f"Error: {e}\nTraceback: {traceback.format_exc()}")
            sp.logging.warning(f"{e}")

    def enable_channels_for_selected_fill(self) -> None:
        """Enables all available channels for the currently selected Fill Layer/ Effect."""
        try:
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)

            if not selected_nodes:
                sp.logging.warning("No layer or effect selected.")
                return

            for node in selected_nodes:
                available_channels = set(stack.all_channels())
                sp.logging.info(f"Enabling channels for: {node.get_name()}")

                node.active_channels = available_channels
                sp.logging.info(f"Applied Channels: {[ch.name for ch in node.active_channels]}")

        except Exception as e:
            sp.logging.warning(f"Error enabling channels: {e}")

    def disable_all_except_base_color(self) -> None:
        """Disables all channels except Base Color for the selected Fill Layer/ Effect."""
        try:
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)

            if not selected_nodes:
                sp.logging.warning("No layer or effect selected.")
                return

            for node in selected_nodes:
                base_color_channel = {sp.textureset.ChannelType.BaseColor}
                sp.logging.info(f"Disabling all but Base Color for: {node.get_name()}")

                node.active_channels = base_color_channel
                sp.logging.info(f"Applied Channels: {[ch.name for ch in node.active_channels]}")

        except Exception as e:
            sp.logging.warning(f"Error disabling channels: {e}")

    def set_channel_value(self, channel_val: float, channel_type: str) -> None:
        """Set 0-1 channel values.

        Args:
            channel_val (float): 0-1 channel value.
            channel_type (str): BaseColor, Roughness, Metallic, etc.

        """
        try:
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)
            available_channels = set(stack.all_channels())

            if not selected_nodes:
                sp.logging.warning("No layer or effect selected.")
                return

            channel_type = getattr(sp.layerstack.ChannelType, channel_type)
            if isinstance(channel_val, (float, int)):
                color = sp.colormanagement.Color(channel_val, channel_val, channel_val)
            elif isinstance(channel_val, (tuple, list)):
                color = sp.colormanagement.Color(channel_val[0], channel_val[1], channel_val[2])

            for node in selected_nodes:
                if channel_type in available_channels:
                    node.set_source(channel_type, color)  # Set Value

                    node_attr_result = node.get_source(channel_type)  # Get Value
                    r, g, b = node_attr_result.get_color().value_raw
                    sp.logging.info(
                        f"Value applied: {node.get_name()} "
                        f"{channel_type.name}: "
                        f"{r:.2f}, {g:.2f}, {b:.2f}",
                    )

        except Exception as e:
            sp.logging.warning(f"Channel values not applied: {e}")

    def set_opacity(self, opacity_val: float) -> None:
        """Set overall channel opacity for layer.
        Not to be confused with fill/ paint layer channel value.

        Args:
            opacity_val (float): Overall channel opacity. Next to Blend Mode in the UI.

        """
        try:
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)
            available_channels = set(stack.all_channels())

            if not selected_nodes:
                sp.logging.warning("No layer or effect selected.")
                return

            for node in selected_nodes:
                sp.logging.info("# ---------------------------------------- #")
                for channel in available_channels:
                    node.set_opacity(opacity_val, channel)
                    channel_opacity = node.get_opacity(channel)
                    sp.logging.info(
                        f"{node.get_name()} - {channel.name} - {channel_opacity}",
                    )

        except Exception as e:
            sp.logging.warning(f"{e}")

    def set_passthrough_mode(self) -> None:
        """Set all channels to Passthrough blend mode for selected."""
        try:
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)
            available_channels = set(stack.all_channels())

            for node in selected_nodes:
                sp.logging.info(f"Selected: {node.get_name()}")
                # Set blend mode to Passthrough for the Layer
                passthrough_blend_mode = sp.layerstack.BlendingMode.Passthrough
                for channel in available_channels:
                    node.set_blending_mode(passthrough_blend_mode, channel)
                    blend_mode = node.get_blending_mode(channel)
                    sp.logging.info(
                        f"{channel.name} - {blend_mode.name}",
                    )

        except Exception as e:
            sp.logging.warning(f"{e}")

    def add_passthrough_paint_layer(self) -> None:
        """Add paint layer with passthrough above selected."""
        try:
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)
            available_channels = set(stack.all_channels())

            # Insert paint layer above selection
            insert_position = sp.layerstack.InsertPosition.above_node(selected_nodes[0])
            paint_layer = sp.layerstack.insert_paint(insert_position)
            paint_layer.set_name("passthrough_paint_layer")
            sp.logging.info(f"Created: {paint_layer.get_name()}")

            # Set blend mode to Passthrough for the Paint Layer
            passthrough_blend_mode = sp.layerstack.BlendingMode.Passthrough
            for channel in available_channels:
                paint_layer.set_blending_mode(passthrough_blend_mode, channel)
                blend_mode = paint_layer.get_blending_mode(channel)
                sp.logging.info(f"{channel.name} - {blend_mode.name}")

        except Exception as e:
            sp.logging.warning(f"{e}")

    def add_noise_mask(self) -> None:
        """Add mask with noise resource to selected.
        Add to existing mask if already exists.
        """
        try:
            # Get selected
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)

            # Mask
            white_mask = sp.layerstack.MaskBackground.White

            for node in selected_nodes:
                mask_check = sp.layerstack.LayerNode.has_mask(node)
                if mask_check is False:  # Create mask first if doesn't exist
                    sp.layerstack.LayerNode.add_mask(node, white_mask)
                else:
                    pass
                insert_position = sp.layerstack.InsertPosition.inside_node(
                    node,
                    sp.layerstack.NodeStack.Mask,
                )
                noise_fill_effect = sp.layerstack.insert_fill(insert_position)
                noise_fill_effect.set_name("noise_fill_effect")
                # noise_resource = sp.resource.search(
                #     "s:starterassets u:procedural n:Clouds 1"
                # )[0]
                noise_resource = sp.resource.search("Clouds 1")[0]
                noise_fill_effect.set_source(None, noise_resource.identifier())  # None (channel)

                # Set triplanar mode
                noise_fill_effect.set_projection_mode(sp.layerstack.ProjectionMode.Triplanar)
                # Adjust fill effect settings
                projection_params = noise_fill_effect.get_projection_parameters()
                projection_params.uv_transformation.scale = [2.5, 2.5]  # UV tiling
                projection_params.hardness = 0.5  # Triplanar blend hardness
                noise_fill_effect.set_projection_parameters(projection_params)

                sp.logging.info(f"Created: {node.get_name()} - {noise_fill_effect.get_name()}")

        except Exception as e:  ##
            # sp.logging.warning(f"Error: {e}\nTraceback: {traceback.format_exc()}")
            sp.logging.warning(f"{e}")

    def add_generator_mask(self, generator_name: str) -> None:
        """Add mask with fill effect. Then add generator resource to mask.
        Example: Curvature, Position, Light, etc.
        """
        try:
            # Get selected
            stack = sp.textureset.get_active_stack()
            selected_nodes = sp.layerstack.get_selected_nodes(stack)

            # Mask
            white_mask = sp.layerstack.MaskBackground.White

            for node in selected_nodes:
                mask_check = sp.layerstack.LayerNode.has_mask(node)
                if mask_check is False:  # Create mask first if doesn't exist
                    sp.layerstack.LayerNode.add_mask(node, white_mask)
                else:
                    pass
                insert_position = sp.layerstack.InsertPosition.inside_node(
                    node,
                    sp.layerstack.NodeStack.Mask,
                )
                fill_effect = sp.layerstack.insert_fill(insert_position)
                fill_effect.set_name("generator_fill_effect")
                fill_effect_resource = sp.resource.search(
                    f"s:starterassets u:generator n:{generator_name}",
                )[0]
                fill_effect.set_source(None, fill_effect_resource.identifier())
                # Set default uv mode
                fill_effect.set_projection_mode(sp.layerstack.ProjectionMode.Fill)

                sp.logging.info(f"Created: {node.get_name()} - {fill_effect.get_name()}")

        except Exception as e:
            # sp.logging.warning(f"Error: {e}\nTraceback: {traceback.format_exc()}")
            sp.logging.warning(f"{e}")
