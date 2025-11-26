# Test Images

This folder is for storing test images used in end-to-end testing.

## Adding Test Images

Place your test images in this folder. Supported formats:
- **JPEG** (.jpg, .jpeg)
- **PNG** (.png)
- **WEBP** (.webp)
- **BMP** (.bmp)

## Recommended Test Images

For comprehensive testing, include images with these characteristics:

### 1. **Various Sizes**
- Small images (< 1000px) - tests upscaling
- Medium images (1000-2000px) - tests moderate processing
- Large images (> 2000px) - tests downscaling/cropping

### 2. **Different Aspect Ratios**
- Wide images (21:9, 16:9) - already widescreen
- Square images (1:1) - requires significant cropping
- Portrait images (9:16, 3:4) - challenging for Frame TV format

### 3. **Content Types**
- Landscapes - common use case for Frame TV
- Artwork/paintings - typical Frame TV content
- Photographs with people - tests detail preservation
- High-detail images - tests upscaling quality
- Low-resolution images - tests extreme upscaling

### 4. **Example Test Set**
Good test images to include:
- `landscape_4k.jpg` - A 4K landscape photo
- `portrait_narrow.jpg` - A portrait orientation image
- `small_artwork.jpg` - A small (<1000px) art piece
- `wide_panorama.jpg` - A very wide panoramic image
- `square_photo.jpg` - A 1:1 aspect ratio image

## How Tests Use These Images

When you run `pytest tests/test_e2e.py::TestRealImageProcessing`, the tests will:

1. **Discover** all supported images in this folder
2. **Upload** each image via the API
3. **Calculate** optimal 16:9 crop coordinates
4. **Process** to both 4K and Full HD resolutions
5. **Verify** output dimensions and quality

## Running Real Image Tests

```bash
# Run only tests that use real images
pytest tests/test_e2e.py::TestRealImageProcessing -v

# Skip these tests if no images are present
# (Tests will automatically skip if folder is empty)
```

## File Size Considerations

- Keep test images under 16MB (app upload limit)
- Diverse file sizes help test various scenarios
- Very large files (>10MB) test edge cases

## Privacy Note

Don't commit personal or sensitive images to version control. Add specific test images to `.gitignore` if needed.
