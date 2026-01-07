import hashlib
import os

import folder_paths
import numpy as np
import torch
from PIL import Image, ImageOps, ImageSequence


class MarxLoadImage:
    """
    LoadImage node that replicates the core ComfyUI LoadImage functionality.
    Loads an image from the input directory and converts it to a tensor.
    """

    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()

        # Get all subfolders in input directory
        folders = ["input"]  # Root input folder
        for item in os.listdir(input_dir):
            item_path = os.path.join(input_dir, item)
            if os.path.isdir(item_path):
                folders.append(item)

        return {
            "required": {
                "folder": (sorted(folders),),
                "image": ("STRING", {"default": ""}),
            },
        }

    @classmethod
    def get_images_in_folder(cls, folder):
        """Helper method to get list of images in the selected folder"""
        input_dir = folder_paths.get_input_directory()

        if folder == "input":
            target_dir = input_dir
        else:
            target_dir = os.path.join(input_dir, folder)

        if not os.path.exists(target_dir):
            return []

        # Get all image files
        valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
        files = []
        for f in os.listdir(target_dir):
            file_path = os.path.join(target_dir, f)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(f)
                if ext.lower() in valid_extensions:
                    files.append(f)

        return sorted(files)

    RETURN_TYPES = ("IMAGE", "MASK")
    OUTPUT_NODE = False
    FUNCTION = "load_image"
    CATEGORY = "Marx/image"

    def load_image(self, folder, image):
        input_dir = folder_paths.get_input_directory()

        # Construct the full image path
        if folder == "input":
            image_path = os.path.join(input_dir, image)
        else:
            image_path = os.path.join(input_dir, folder, image)

        # Validate path exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

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
                mask_tensor = torch.zeros((image_tensor.shape[1], image_tensor.shape[2]), dtype=torch.float32)

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
    def IS_CHANGED(cls, folder, image):
        input_dir = folder_paths.get_input_directory()

        # Construct the full image path
        if folder == "input":
            image_path = os.path.join(input_dir, image)
        else:
            image_path = os.path.join(input_dir, folder, image)

        if not os.path.exists(image_path):
            return ""

        # Generate hash based on file content
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(cls, folder, image):
        input_dir = folder_paths.get_input_directory()

        # Construct the full image path
        if folder == "input":
            image_path = os.path.join(input_dir, image)
        else:
            image_path = os.path.join(input_dir, folder, image)

        if not os.path.exists(image_path):
            return f"Invalid image file: {image} in folder: {folder}"
        return True


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "MarxLoadImage": MarxLoadImage
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "MarxLoadImage": "Marx Load Image"
}

