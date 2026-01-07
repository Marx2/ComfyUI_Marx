import hashlib
import os

import folder_paths
import numpy as np
import torch
from PIL import Image, ImageOps, ImageSequence

# Try relative import first (for ComfyUI), fallback to absolute (for testing)
try:
  from .settings import DEFAULT_FOLDERS
except ImportError:
  from settings import DEFAULT_FOLDERS


def create_marx_load_image_class(folder_type, folder_number):
  """
  Factory function to create MarxLoadImage node classes.
  Each class reads from its configured folder.

  Args:
      folder_type: "input" or "output"
      folder_number: Integer from 1-3 indicating which folder to read from
  """

  class MarxLoadImage:
    """
    LoadImage node that loads images from a specific configured folder.
    Loads an image from the input directory and converts it to a tensor.
    """

    # Store folder type and number as class attributes
    _folder_type = folder_type
    _folder_number = folder_number

    @classmethod
    def INPUT_TYPES(cls):
      # Use appropriate directory based on folder type
      if folder_type == "input":
        base_dir = folder_paths.get_input_directory()
      else:  # output
        base_dir = folder_paths.get_output_directory()

      # Get the configured folder path from settings file
      try:
        from .settings import get_folder_path_from_settings
      except ImportError:
        from settings import get_folder_path_from_settings

      folder_name = get_folder_path_from_settings(folder_type, folder_number)

      # Build the full path to the configured folder
      if folder_name and folder_name != ".":
        target_dir = os.path.join(base_dir, folder_name)
      else:
        # If folder is "." or empty, use root directory
        target_dir = base_dir

      # List files from the target directory
      files = []
      # Image file extensions to filter
      image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp',
                          '.tiff', '.tif', '.avif')

      if os.path.exists(target_dir) and os.path.isdir(target_dir):
        try:
          if folder_name and folder_name != ".":
            # Prefix files with folder name for correct path resolution
            files = [os.path.join(folder_name, f) for f in
                     os.listdir(target_dir)
                     if os.path.isfile(os.path.join(target_dir, f))
                     and not f.startswith(
                '.')  # Skip hidden files like .DS_Store
                     and f.lower().endswith(
                image_extensions)]  # Only image files
          else:
            # Root directory files - no prefix needed
            files = [f for f in os.listdir(target_dir)
                     if os.path.isfile(os.path.join(target_dir, f))
                     and not f.startswith('.')  # Skip hidden files
                     and f.lower().endswith(
                image_extensions)]  # Only image files
        except Exception:
          pass

      # For output nodes, provide explicit file list with image_folder configuration
      # This allows navigation while still using output directory
      if folder_type == "output":
        return {
          "required": {
            "image": (sorted(files) if files else [""], {
              "image_upload": True,
              "image_folder": "output"
            })
          },
        }
      else:
        return {
          "required": {
            "image": (sorted(files) if files else [""], {"image_upload": True})
          },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    OUTPUT_NODE = False
    FUNCTION = "load_image"
    CATEGORY = "Marx/image"

    def load_image(self, image):
      # Handle path resolution based on folder type
      if self._folder_type == "output":
        # For output directory, construct path manually
        output_dir = folder_paths.get_output_directory()

        # Get the configured folder path
        try:
          from .settings import get_folder_path_from_settings
        except ImportError:
          from settings import get_folder_path_from_settings

        folder_name = get_folder_path_from_settings(self._folder_type,
                                                    self._folder_number)

        if folder_name and folder_name != ".":
          # Image path already includes folder prefix from INPUT_TYPES
          image_path = os.path.join(output_dir, image)
        else:
          image_path = os.path.join(output_dir, image)
      else:
        # For input directory, use standard ComfyUI path resolution
        image_path = folder_paths.get_annotated_filepath(image)

      # Load image
      img = Image.open(image_path)

      # Handle animated images (GIFs, etc.)
      output_images = []
      output_masks = []

      for i in ImageSequence.Iterator(img):
        i = ImageOps.exif_transpose(i)

        # Convert to RGB if needed
        if i.mode == 'I':
          i = i.point(lambda i: i * (1 / 255))
        image_array = i.convert("RGB")

        # Convert to numpy array and normalize
        image_np = np.array(image_array).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)[None,]

        # Handle alpha channel for mask
        if 'A' in i.getbands():
          mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
          mask_tensor = torch.from_numpy(mask)
          mask_tensor = 1. - mask_tensor
        else:
          mask_tensor = torch.zeros(
              (image_tensor.shape[1], image_tensor.shape[2]),
              dtype=torch.float32)

        output_images.append(image_tensor)
        output_masks.append(mask_tensor.unsqueeze(0))

      if len(output_images) > 1:
        output_image = torch.cat(output_images, dim=0)
        output_mask = torch.cat(output_masks, dim=0)
      else:
        output_image = output_images[0]
        output_mask = output_masks[0]

      return (output_image, output_mask)

    @classmethod
    def IS_CHANGED(cls, image):
      # Handle path resolution based on folder type
      if cls._folder_type == "output":
        output_dir = folder_paths.get_output_directory()

        try:
          from .settings import get_folder_path_from_settings
        except ImportError:
          from settings import get_folder_path_from_settings

        folder_name = get_folder_path_from_settings(cls._folder_type,
                                                    cls._folder_number)

        if folder_name and folder_name != ".":
          image_path = os.path.join(output_dir, image)
        else:
          image_path = os.path.join(output_dir, image)
      else:
        image_path = folder_paths.get_annotated_filepath(image)

      # Check if file exists (important for output folder)
      if not os.path.exists(image_path):
        return ""

      # Generate hash based on file modification time and size
      m = hashlib.sha256()
      with open(image_path, 'rb') as f:
        m.update(f.read())
      return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(cls, image):
      # Handle path resolution based on folder type
      if cls._folder_type == "output":
        output_dir = folder_paths.get_output_directory()

        try:
          from .settings import get_folder_path_from_settings
        except ImportError:
          from settings import get_folder_path_from_settings

        folder_name = get_folder_path_from_settings(cls._folder_type,
                                                    cls._folder_number)

        if folder_name and folder_name != ".":
          image_path = os.path.join(output_dir, image)
        else:
          image_path = os.path.join(output_dir, image)

        if not os.path.exists(image_path):
          return "Invalid image file: {}".format(image)
      else:
        if not folder_paths.exists_annotated_filepath(image):
          return "Invalid image file: {}".format(image)

      return True

  # Set a unique class name for each node
  MarxLoadImage.__name__ = f"MarxLoad{folder_type.capitalize()}Image{folder_number}"
  return MarxLoadImage


# Create 6 separate node classes (3 input, 3 output)
MarxLoadInputImage1 = create_marx_load_image_class("input", 1)
MarxLoadInputImage2 = create_marx_load_image_class("input", 2)
MarxLoadInputImage3 = create_marx_load_image_class("input", 3)
MarxLoadOutputImage1 = create_marx_load_image_class("output", 1)
MarxLoadOutputImage2 = create_marx_load_image_class("output", 2)
MarxLoadOutputImage3 = create_marx_load_image_class("output", 3)

# Node class mappings
NODE_CLASS_MAPPINGS = {
  "MarxLoadInputImage1": MarxLoadInputImage1,
  "MarxLoadInputImage2": MarxLoadInputImage2,
  "MarxLoadInputImage3": MarxLoadInputImage3,
  "MarxLoadOutputImage1": MarxLoadOutputImage1,
  "MarxLoadOutputImage2": MarxLoadOutputImage2,
  "MarxLoadOutputImage3": MarxLoadOutputImage3,
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
  "MarxLoadInputImage1": "Load Input Image 1 Marx",
  "MarxLoadInputImage2": "Load Input Image 2 Marx",
  "MarxLoadInputImage3": "Load Input Image 3 Marx",
  "MarxLoadOutputImage1": "Load Output Image 1 Marx",
  "MarxLoadOutputImage2": "Load Output Image 2 Marx",
  "MarxLoadOutputImage3": "Load Output Image 3 Marx",
}

