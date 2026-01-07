"""
ComfyUI_Marx - Custom nodes for ComfyUI
"""

import os

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Register web directory for JavaScript extensions
WEB_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
