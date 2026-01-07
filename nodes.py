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


def create_marx_load_image_class(folder_number):
  """
  Factory function to create MarxLoadImage node classes.
  Each class reads from its configured folder.

  Args:
      folder_number: Integer from 1-5 indicating which folder to read from
  """

  class MarxLoadImage:
    """
    LoadImage node that loads images from a specific configured folder.
    Loads an image from the input directory and converts it to a tensor.
    """

    @classmethod
    def INPUT_TYPES(cls):
      input_dir = folder_paths.get_input_directory()

      # Get the configured folder path from settings file
      try:
        from .settings import get_folder_path_from_settings
      except ImportError:
        from settings import get_folder_path_from_settings

      folder_name = get_folder_path_from_settings(folder_number)

      # Build the full path to the configured folder
      if folder_name and folder_name != ".":
        target_dir = os.path.join(input_dir, folder_name)
      else:
        # If folder is "." or empty, use root input directory
        target_dir = input_dir

      # List files from the target directory
      files = []
      if os.path.exists(target_dir) and os.path.isdir(target_dir):
        try:
          if folder_name and folder_name != ".":
            # Prefix files with folder name for correct path resolution
            files = [os.path.join(folder_name, f) for f in
                     os.listdir(target_dir)
                     if os.path.isfile(os.path.join(target_dir, f))]
          else:
            # Root directory files - no prefix needed
            files = [f for f in os.listdir(target_dir)
                     if os.path.isfile(os.path.join(target_dir, f))]
        except Exception:
          pass

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
      image_path = folder_paths.get_annotated_filepath(image)

      # Generate hash based on file modification time and size
      m = hashlib.sha256()
      with open(image_path, 'rb') as f:
        m.update(f.read())
      return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(cls, image):
      if not folder_paths.exists_annotated_filepath(image):
        return "Invalid image file: {}".format(image)
      return True

  # Set a unique class name for each node
  MarxLoadImage.__name__ = f"MarxLoadImage{folder_number}"
  return MarxLoadImage


# Create 5 separate node classes
MarxLoadImage1 = create_marx_load_image_class(1)
MarxLoadImage2 = create_marx_load_image_class(2)
MarxLoadImage3 = create_marx_load_image_class(3)
MarxLoadImage4 = create_marx_load_image_class(4)
MarxLoadImage5 = create_marx_load_image_class(5)

# Node class mappings
NODE_CLASS_MAPPINGS = {
  "MarxLoadImage1": MarxLoadImage1,
  "MarxLoadImage2": MarxLoadImage2,
  "MarxLoadImage3": MarxLoadImage3,
  "MarxLoadImage4": MarxLoadImage4,
  "MarxLoadImage5": MarxLoadImage5,
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
  "MarxLoadImage1": "Marx Load Image 1",
  "MarxLoadImage2": "Marx Load Image 2",
  "MarxLoadImage3": "Marx Load Image 3",
  "MarxLoadImage4": "Marx Load Image 4",
  "MarxLoadImage5": "Marx Load Image 5",
}

