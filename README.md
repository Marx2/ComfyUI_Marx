# ComfyUI_Marx

Custom nodes for ComfyUI.

## Nodes

### Marx Load Image

A custom implementation of the LoadImage node that replicates the core ComfyUI LoadImage functionality.

**Features:**
- Loads images from the ComfyUI input directory
- Supports multiple image formats (PNG, JPG, GIF, etc.)
- Handles animated images (GIFs) by loading all frames
- Automatically extracts alpha channel as mask
- Returns both IMAGE and MASK outputs
- Supports EXIF orientation correction

**Outputs:**
- `IMAGE`: The loaded image as a tensor (batch, height, width, channels)
- `MASK`: Alpha channel mask (or empty mask if no alpha channel)

## Installation

1. Clone or copy this directory to your ComfyUI custom_nodes folder:
   ```
   ComfyUI/custom_nodes/ComfyUI_Marx/
   ```

2. Restart ComfyUI

3. The node will appear under the "Marx/image" category

## Usage

The node works exactly like the core LoadImage node:
1. Add "Marx Load Image" node to your workflow
2. Select an image from the dropdown (images from your ComfyUI/input directory)
3. Connect the IMAGE and/or MASK outputs to other nodes

## Requirements

- ComfyUI
- PIL (Pillow)
- PyTorch
- NumPy

These dependencies are already included with ComfyUI.

