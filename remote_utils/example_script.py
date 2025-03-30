"""Send to Substance example script.
===============================

Test sending raw code to Substance Painter via remote connection.
"""

import sys

import substance_painter as sp


class SendToSubstance:
    def __init__(self):
        global sp

    def test(self):
        sp.logging.info(f"(sys.executable) {sys.executable}")
        sp.logging.info(f"(sys.base_prefix) {sys.base_prefix}")

        stack = sp.textureset.get_active_stack()
        selected_nodes = sp.layerstack.get_selected_nodes(stack)
        for node in selected_nodes:
            print(node.get_name())


if __name__ == "__main__":
    print("Send To Substance Executed...")
    SendToSubstance().test_code()
