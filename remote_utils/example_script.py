"""Send to Substance example script.
==================================================

Test sending raw code to Substance Painter via remote connection.
"""

import sys

import substance_painter as sp


class SendToSubstance:
    def __init__(self) -> None:
        global sp # Needed for SP to detect module.

    def test_code(self) -> None:
        """Test code for remote connection. Add your own code as needed."""
        sp.logging.info(f"(sys.executable) {sys.executable}")
        sp.logging.info(f"(sys.base_prefix) {sys.base_prefix}")

        stack = sp.textureset.get_active_stack()
        selected_nodes = sp.layerstack.get_selected_nodes(stack)
        for node in selected_nodes:
            sp.logging.info(node.get_name())


if __name__ == "__main__":
    sp.logging.info("Send To Substance...")
    SendToSubstance().test_code()
