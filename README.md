# ComfyUI_Marx

Custom nodes for ComfyUI.

## Nodes

### Marx Load Image

A custom implementation of the LoadImage node that replicates the core ComfyUI LoadImage
functionality with enhanced folder navigation.

**Features:**

- **Folder Selection**: Choose between the root input directory or any subfolder
- Loads images from the ComfyUI input directory and its subfolders
- Supports multiple image formats (PNG, JPG, GIF, WebP, BMP, TIFF, etc.)
- Handles animated images (GIFs) by loading all frames
- Automatically extracts alpha channel as mask
- Returns both IMAGE and MASK outputs
- Supports EXIF orientation correction
- Dynamic image list based on selected folder

**Outputs:**

- `IMAGE`: The loaded image as a tensor (normalized 0-1, RGB format)
- `MASK`: Alpha channel mask (inverted, so transparent areas become opaque in mask)

**Inputs:**

- `folder`: Dropdown to select "input" (root) or any subfolder in the input directory
- `image`: Text field to enter the image filename (the UI will show available images based on folder
  selection)

## Installation

1. Clone or copy this directory to your ComfyUI custom_nodes folder:
   ```
   ComfyUI/custom_nodes/ComfyUI_Marx/
   ```

2. Restart ComfyUI

3. The node will appear under the "Marx/image" category

## Usage

The node provides folder navigation for images:
1. Add "Marx Load Image" node to your workflow
2. Select a folder from the "folder" dropdown:
    - "input" - loads from the root ComfyUI/input directory
    - Any subfolder name - loads from that subfolder
3. Enter or select an image filename in the "image" field
4. Connect the IMAGE and/or MASK outputs to other nodes

The JavaScript extension automatically updates the available images when you change folders.

## Requirements

- ComfyUI
- PIL (Pillow)
- PyTorch
- NumPy

These dependencies are already included with ComfyUI.
