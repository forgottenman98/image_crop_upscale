# Frame TV Image Processor

A web application for cropping and upscaling images to specific resolutions for Samsung Frame TVs.

## Features

- **Image Upload**: Drag-and-drop or click to upload images (PNG, JPG, JPEG, WEBP, BMP)
- **Preset Resolutions**: Quick selection for 4K (3840×2160) and Full HD (1920×1080)
- **Interactive Cropping**: Drag and resize crop box with locked aspect ratio
- **Smart Upscaling**: High-quality Lanczos resampling for crisp results
- **Instant Download**: Process and download your optimized image

## Tech Stack

- **Backend**: Flask (Python)
- **Image Processing**: Pillow
- **Frontend**: HTML/CSS/JavaScript
- **Crop Tool**: Cropper.js

## Installation

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Application

1. **Start the Flask server**:
```bash
python app.py
```

2. **Open your browser** and navigate to:
```
http://localhost:5000
```

## Usage

1. **Upload an Image**: Click or drag-and-drop your image
2. **Select Resolution**: Choose 4K or Full HD preset
3. **Crop**: Drag and resize the crop box to select your desired area
4. **Process**: Click "Process & Upscale Image"
5. **Download**: Save your optimized image

## Project Structure

```
image_crop_upscale/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML page
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── app.js        # Frontend logic
├── uploads/              # Temporary uploaded images
└── processed/            # Processed images ready for download
```

## How It Works

1. **Upload**: User uploads an image via drag-and-drop or file picker
2. **Preview**: Image is displayed with Cropper.js overlay
3. **Select**: User chooses target resolution (locks aspect ratio)
4. **Crop**: User positions and sizes the crop box
5. **Process**:
   - Crop coordinates are sent to Flask backend
   - Pillow crops the image to selected area
   - Image is upscaled to target resolution using Lanczos resampling
   - High-quality JPEG is saved (quality=95)
6. **Download**: Processed image is served for download

## Configuration

Edit `app.py` to customize:

- **Max file size**: `app.config['MAX_CONTENT_LENGTH']` (default: 16MB)
- **Allowed formats**: `app.config['ALLOWED_EXTENSIONS']`
- **Add presets**: Modify `PRESETS` dictionary
- **Output quality**: Change `quality` parameter in `crop_and_upscale()`

## Adding Custom Resolutions

In `app.py`, add to the `PRESETS` dictionary:

```python
PRESETS = {
    '4k': {'width': 3840, 'height': 2160, 'name': '4K Ultra HD'},
    'fhd': {'width': 1920, 'height': 1080, 'name': 'Full HD'},
    'custom': {'width': 2560, 'height': 1440, 'name': 'QHD'}  # Add this
}
```

## Testing

Comprehensive test suite with unit, integration, and end-to-end tests.

### Quick Start

```bash
# Install test dependencies (if not already installed)
pip install -r requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test categories
pytest tests/test_unit.py      # Unit tests only
pytest tests/test_api.py       # API integration tests
pytest tests/test_e2e.py       # End-to-end tests
```

### Testing with Your Images

1. Add your test images to the `test_images/` folder
2. Run real image tests:
```bash
pytest tests/test_e2e.py::TestRealImageProcessing -v
```

### Coverage Report

```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

For detailed testing documentation, see [TESTING.md](TESTING.md)

## Known Issues

### Image Preview Requires Double-Click on Subsequent Uploads

**Issue:** When uploading a second image after processing the first one, clicking a preset button (4K or Full HD) shows the preview of the first image. Clicking the same preset button a second time correctly displays the new image.

**Workaround:** Click your desired preset button twice when uploading subsequent images.

**Technical Details:**
This appears to be a timing issue with Cropper.js initialization when images are cached by the browser. The following fixes have been attempted:

1. **State Reset on Upload** - Destroying cropper instance and resetting UI state when new image is uploaded
2. **Race Condition Fix** - Setting `onload` handler before changing image `src`
3. **Cache Handling** - Checking `image.complete` property to handle cached images
4. **Handler Cleanup** - Removing old `onload` handlers before setting new ones

The issue persists despite these attempts. The root cause may be related to how Cropper.js interacts with the browser's image caching mechanism or the DOM update cycle.

**Impact:** Minor inconvenience - functionality works correctly after second click.

## Notes

- Uploaded and processed images are stored temporarily
- For production, consider adding cleanup jobs to remove old files
- JPEG output format provides good balance of quality and file size
- Lanczos resampling ensures high-quality upscaling

## License

Free to use and modify for personal projects.
