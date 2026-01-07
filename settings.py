"""
Settings configuration for ComfyUI_Marx nodes
"""

import json
import os

# Default folder configuration
DEFAULT_FOLDERS = {
  "folder1": "e",
  "folder2": "f",
  "folder3": "g",
  "folder4": "h",
  "folder5": "i"
}


def get_comfy_settings_path():
  """
  Get the path to ComfyUI's settings file
  """
  # Try to find ComfyUI root directory
  current_dir = os.path.dirname(os.path.abspath(__file__))

  # Go up to find ComfyUI root (custom_nodes parent)
  comfy_root = current_dir
  for _ in range(10):  # Safety limit
    parent = os.path.dirname(comfy_root)
    if os.path.basename(comfy_root) == "custom_nodes":
      comfy_root = parent
      break
    comfy_root = parent

  # Try common settings paths
  possible_paths = [
    os.path.join(comfy_root, "user", "default", "comfy.settings.json"),
    os.path.join(comfy_root, "user", "comfy.settings.json"),
    os.path.join(comfy_root, "comfy.settings.json"),
  ]

  for path in possible_paths:
    if os.path.exists(path):
      return path

  return None


def get_folder_path_from_settings(folder_number):
  """
  Read folder path from ComfyUI's settings JSON file
  Returns the configured path or default if not found

  Args:
    folder_number: Integer from 1-5

  Returns:
    str: The folder path
  """
  default_key = f"folder{folder_number}"
  default_value = DEFAULT_FOLDERS.get(default_key, "")

  settings_path = get_comfy_settings_path()
  if not settings_path:
    return default_value

  try:
    with open(settings_path, 'r') as f:
      settings = json.load(f)
      setting_key = f"Marx.folder{folder_number}"
      value = settings.get(setting_key)
      if value and value.strip():
        return value.strip()
  except Exception as e:
    # If reading fails, use default
    pass

  return default_value


def get_setting_value(settings_manager, key, default):
  """
  Get a setting value from ComfyUI's settings manager
  """
  try:
    if hasattr(settings_manager, 'get'):
      value = settings_manager.get(key)
      if value is not None:
        return value
  except Exception:
    pass
  return default


def get_folder_paths(settings_manager=None):
  """
  Get the configured folder paths from settings or use defaults
  Returns a list of 5 folder paths
  """
  folders = []
  for i in range(1, 6):
    key = f"Marx.folder{i}"
    default = DEFAULT_FOLDERS[f"folder{i}"]

    if settings_manager:
      folder = get_setting_value(settings_manager, key, default)
    else:
      folder = default

    folders.append(folder)

  return folders


def register_settings():
  """
  Register custom settings with ComfyUI's settings system
  This should be called when the extension loads
  """
  return [
    {
      "id": "Marx.folder1",
      "name": "Marx Folder 1",
      "type": "text",
      "defaultValue": DEFAULT_FOLDERS["folder1"],
      "tooltip": "Subfolder path in ComfyUI/input directory for image selector 1"
    },
    {
      "id": "Marx.folder2",
      "name": "Marx Folder 2",
      "type": "text",
      "defaultValue": DEFAULT_FOLDERS["folder2"],
      "tooltip": "Subfolder path in ComfyUI/input directory for image selector 2"
    },
    {
      "id": "Marx.folder3",
      "name": "Marx Folder 3",
      "type": "text",
      "defaultValue": DEFAULT_FOLDERS["folder3"],
      "tooltip": "Subfolder path in ComfyUI/input directory for image selector 3"
    },
    {
      "id": "Marx.folder4",
      "name": "Marx Folder 4",
      "type": "text",
      "defaultValue": DEFAULT_FOLDERS["folder4"],
      "tooltip": "Subfolder path in ComfyUI/input directory for image selector 4"
    },
    {
      "id": "Marx.folder5",
      "name": "Marx Folder 5",
      "type": "text",
      "defaultValue": DEFAULT_FOLDERS["folder5"],
      "tooltip": "Subfolder path in ComfyUI/input directory for image selector 5"
    }
  ]
