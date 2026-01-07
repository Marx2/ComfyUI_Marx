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
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {
            "required": {
                "image": (sorted(files), {"image_upload": True})
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


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "MarxLoadImage": MarxLoadImage
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "MarxLoadImage": "Marx Load Image"
}

