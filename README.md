# ComfyUI_Marx

Custom nodes for ComfyUI with configurable folder-based image loading.

## Nodes

### Marx Load Image 1-5

Five separate image loader nodes, each configured to read from a specific folder defined in ComfyUI
settings.

- **Marx Load Image 1** - Reads from folder configured in "Marx Folder 1" setting (default: `e`)
- **Marx Load Image 2** - Reads from folder configured in "Marx Folder 2" setting (default: `f`)
- **Marx Load Image 3** - Reads from folder configured in "Marx Folder 3" setting (default: `g`)
- **Marx Load Image 4** - Reads from folder configured in "Marx Folder 4" setting (default: `h`)
- **Marx Load Image 5** - Reads from folder configured in "Marx Folder 5" setting (default: `i`)

**Features:**

- **Folder-based Organization**: Each node reads from its own configured subfolder
- **Folder Path Display**: Each node displays its configured folder path (e.g., "📁 input/e")
- **Settings Integration**: Folder paths configured via ComfyUI's native settings panel
- Supports multiple image formats (PNG, JPG, GIF, etc.)
- Handles animated images (GIFs) by loading all frames
- Automatically extracts alpha channel as mask
- Returns both IMAGE and MASK outputs
- Supports EXIF orientation correction

**Inputs:**

- `folder_path`: (Read-only display) Shows the configured folder path for this node
- `image`: Dropdown selector showing images from the node's configured folder

**Outputs:**
- `IMAGE`: The loaded image as a tensor (batch, height, width, channels)
- `MASK`: Alpha channel mask (or empty mask if no alpha channel)

## Installation

1. Clone or copy this directory to your ComfyUI custom_nodes folder:
   ```
   ComfyUI/custom_nodes/ComfyUI_Marx/
   ```

2. Restart ComfyUI

3. Configure folder paths in Settings (see Configuration section below)

4. The nodes will appear under the "Marx/image" category

## Configuration

### Setting Up Folders

1. Open ComfyUI → Click **Settings** (gear icon)
2. Scroll to find **Marx Folder 1-5** settings
3. Enter subfolder paths relative to `ComfyUI/input/` directory
    - Example: `portraits`, `landscapes`, `textures`, etc.
    - Use `.` to reference the root input directory
4. Click **Save**
5. Refresh ComfyUI for changes to take effect

### Default Configuration

If no settings are configured, the nodes use these default folders:

- Marx Load Image 1 → `ComfyUI/input/e/`
- Marx Load Image 2 → `ComfyUI/input/f/`
- Marx Load Image 3 → `ComfyUI/input/g/`
- Marx Load Image 4 → `ComfyUI/input/h/`
- Marx Load Image 5 → `ComfyUI/input/i/`

### Folder Structure Example

```
ComfyUI/input/
  ├── e/                    # Marx Load Image 1
  │   ├── image1.png
  │   └── image2.png
  ├── f/                    # Marx Load Image 2
  │   ├── photo1.jpg
  │   └── photo2.jpg
  ├── portraits/            # Marx Load Image 3 (if configured)
  │   └── person1.jpg
  └── landscapes/           # Marx Load Image 4 (if configured)
      └── scene1.png
```

## Usage

1. Configure your folder paths in ComfyUI Settings
2. Create the corresponding folders in `ComfyUI/input/`
3. Add images to those folders
4. Add any "Marx Load Image" node to your workflow
5. Select an image from the dropdown
6. Connect the IMAGE and/or MASK outputs to other nodes

**Workflow Example:**

- Marx Load Image 1 for base images
- Marx Load Image 2 for control images
- Marx Load Image 3 for masks
- Marx Load Image 4 for references
- Marx Load Image 5 for additional inputs

## Requirements

- ComfyUI
- PIL (Pillow)
- PyTorch
- NumPy

These dependencies are already included with ComfyUI.

## Documentation

For detailed settings configuration, see [SETTINGS.md](SETTINGS.md)

