"""
Settings configuration for ComfyUI_Marx nodes
"""

# Default folder configuration
DEFAULT_FOLDERS = {
  "folder1": "e",
  "folder2": "f",
  "folder3": "g",
  "folder4": "h",
  "folder5": "i"
}


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
