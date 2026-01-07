# ComfyUI_Marx Implementation Summary

## Overview

Successfully created a custom ComfyUI node that replicates the LoadImage functionality with enhanced
folder navigation capabilities.

## Files Created

### Core Files

1. **`__init__.py`** (50 lines)
    - Module initialization
    - Registers node mappings
    - Defines WEB_DIRECTORY for JavaScript files
    - Registers `/marx/images` API endpoint for dynamic folder browsing

2. **`nodes.py`** (160 lines)
    - `MarxLoadImage` class implementation
    - Supports folder selection (root input or any subfolder)
    - Loads images in multiple formats (PNG, JPG, GIF, WebP, BMP, TIFF)
    - Handles animated images (GIFs)
    - Extracts alpha channel as mask
    - Returns IMAGE and MASK outputs
    - Includes proper validation and caching

3. **`js/marx_load_image.js`** (65 lines)
    - Frontend JavaScript extension
    - Provides dynamic UI updates when folder changes
    - Fetches available images from selected folder via API
    - Automatically updates image dropdown

4. **`README.md`** (77 lines)
    - Complete documentation
    - Installation instructions
    - Usage guide
    - Technical details

5. **`example_workflow.json`**
    - Example ComfyUI workflow demonstrating the node

## Key Features

### Folder Navigation

- **Dropdown Selection**: Choose between "input" (root) or any subfolder
- **Dynamic Updates**: JavaScript extension automatically fetches images when folder changes
- **API Endpoint**: `/marx/images` provides image list for selected folder

### Image Processing

- **Format Support**: PNG, JPG, JPEG, GIF, BMP, WebP, TIFF
- **Animated Images**: Full support for GIF frames
- **Alpha Channel**: Automatically extracted as mask output
- **EXIF Orientation**: Automatic correction based on EXIF data
- **Normalization**: Images normalized to 0-1 range

### Outputs

- **IMAGE**: Tensor format (batch, height, width, channels) - RGB, normalized 0-1
- **MASK**: Alpha channel mask (inverted for ComfyUI convention)

## Usage Instructions

1. **Installation**:
    - Files are already in `/Users/i318088/prv/ComfyUI/custom_nodes/ComfyUI_Marx/`
    - Restart ComfyUI to load the node

2. **Using the Node**:
    - Add "Marx Load Image" from "Marx/image" category
    - Select folder from dropdown ("input" or subfolder name)
    - Enter or select image filename
    - Connect IMAGE/MASK outputs to other nodes

3. **Adding Images**:
    - Place images in `ComfyUI/input/` or create subfolders
    - Restart ComfyUI to refresh folder list
    - JavaScript extension will dynamically load images

## Technical Architecture

### Backend (Python)

- Node registration via `NODE_CLASS_MAPPINGS`
- API endpoint for folder-based image listing
- Full image processing pipeline
- Validation and error handling

### Frontend (JavaScript)

- Extension registration with ComfyUI app
- Widget callback override for dynamic updates
- API communication for image list fetching
- Automatic UI updates

### API

- **Endpoint**: `POST /marx/images`
- **Request**: `{"folder": "subfolder_name"}`
- **Response**: `{"images": ["img1.png", "img2.jpg", ...]}`

## Differences from Core LoadImage

1. **Folder Navigation**: Added folder selection dropdown
2. **Dynamic Loading**: JavaScript extension for dynamic image lists
3. **API Integration**: Custom endpoint for folder browsing
4. **Enhanced Validation**: Proper path validation for subfolders

## Testing

All Python files have been validated:

- ✓ `__init__.py` - syntax valid
- ✓ `nodes.py` - syntax valid
- ✓ JavaScript files - standard ES6 modules

## Next Steps

1. Restart ComfyUI
2. Node will appear under "Marx/image" category
3. Test with images in input directory and subfolders
4. Check browser console for any JavaScript errors if needed

## Compatibility

- ComfyUI: Latest version
- Python: 3.8+
- Dependencies: Already included with ComfyUI (torch, numpy, PIL, aiohttp)

