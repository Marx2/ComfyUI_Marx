"""
ComfyUI_Marx - Custom nodes for ComfyUI
"""

import os

import folder_paths
from aiohttp import web
from server import PromptServer

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Web directory for JavaScript files
WEB_DIRECTORY = "./js"


# Register API endpoint
@PromptServer.instance.routes.post("/marx/images")
async def get_images_by_folder(request):
  try:
    data = await request.json()
    folder = data.get("folder", "input")

    input_dir = folder_paths.get_input_directory()

    # Construct target directory
    if folder == "input":
      target_dir = input_dir
    else:
      target_dir = os.path.join(input_dir, folder)

    if not os.path.exists(target_dir):
      return web.json_response({"images": []})

    # Get all image files
    valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp',
                        '.tiff', '.tif'}
    files = []
    for f in os.listdir(target_dir):
      file_path = os.path.join(target_dir, f)
      if os.path.isfile(file_path):
        _, ext = os.path.splitext(f)
        if ext.lower() in valid_extensions:
          files.append(f)

    return web.json_response({"images": sorted(files)})
  except Exception as e:
    return web.json_response({"error": str(e)}, status=500)


NODE_CLASS_MAPPINGS = NODE_CLASS_MAPPINGS
NODE_DISPLAY_NAME_MAPPINGS = NODE_DISPLAY_NAME_MAPPINGS
