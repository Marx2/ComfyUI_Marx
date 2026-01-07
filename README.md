# ComfyUI_Marx

Custom nodes for ComfyUI with configurable folder-based image loading organized by Input and Output
categories. They are similar to the built-in Load Image node but allow you to set specific
subfolders for each
node via ComfyUI's settings.

## Screenshots

### Input Image Loader

![Load Input Image Marx](docs/images/marx_load_input_image.png)

Loads images from configured subfolders in the input directory. Features folder path display and
support for nested folder under input directory. You configure folder in ComfyUI settings.

### Output Image Loader

![Load Output Image Marx](docs/images/marx_load_output_image.png)

Loads images from configured subfolders in the output directory. Features inline preview,
Previous/Next navigation buttons, and support for nested folders. You configure folder in ComfyUI
settings. There are separate Previous/Next buttons, because standard ones does not work properly (
ComfyUI limitation).

## Nodes

### Input Image Loaders (3 nodes)

Reads from ComfyUI's **input** directory (`ComfyUI/input/`):

- **Load Input Image 1 Marx** - Reads from folder configured in "Marx Folder Input 1" setting (
  default: `input1`)
- **Load Input Image 2 Marx** - Reads from folder configured in "Marx Folder Input 2" setting (
  default: `input2`)
- **Load Input Image 3 Marx** - Reads from folder configured in "Marx Folder Input 3" setting (
  default: `input3`)

### Output Image Loaders (3 nodes)

Reads from ComfyUI's **output** directory (`ComfyUI/output/`):

- **Load Output Image 1 Marx** - Reads from folder configured in "Marx Folder Output 1" setting (
  default: `output1`)
- **Load Output Image 2 Marx** - Reads from folder configured in "Marx Folder Output 2" setting (
  default: `output2`)
- **Load Output Image 3 Marx** - Reads from folder configured in "Marx Folder Output 3" setting (
  default: `output3`)

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
2. Scroll to find **Marx Folder Input/Output** settings:
    - **Marx Folder Input 1-3** - Subfolders relative to `ComfyUI/input/`
    - **Marx Folder Output 1-3** - Subfolders relative to `ComfyUI/output/`
3. Enter subfolder paths
    - Example: `portraits`, `landscapes`, `textures`, etc.
   - Use `.` to reference the root directory
4. Click **Save**
5. Refresh ComfyUI for changes to take effect

### Default Configuration

If no settings are configured, the nodes use these default folders:

- Load Input Image 1 Marx → `ComfyUI/input/input1/`
- Load Input Image 2 Marx → `ComfyUI/input/input2/`
- Load Input Image 3 Marx → `ComfyUI/input/input3/`
- Load Output Image 1 Marx → `ComfyUI/output/output1/`
- Load Output Image 2 Marx → `ComfyUI/output/output2/`
- Load Output Image 3 Marx → `ComfyUI/output/output3/`

### Folder Structure Example

```
ComfyUI/
  ├── input/              # Input nodes read from here
  │   ├── input1/         # Load Input Image 1 Marx
  │   ├── input2/         # Load Input Image 2 Marx
  │   ├── input3/         # Load Input Image 3 Marx
  │   └── portraits/      # Custom folder (configure in settings)
  └── output/             # Output nodes read from here
      ├── output1/        # Load Output Image 1 Marx
      ├── output2/        # Load Output Image 2 Marx
      ├── output3/        # Load Output Image 3 Marx
      └── processed/      # Custom folder (configure in settings)
```



