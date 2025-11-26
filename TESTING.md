# Testing Documentation

Comprehensive test suite for the Frame TV Image Processor application.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Pytest fixtures and configuration
├── test_unit.py          # Unit tests for core functions
├── test_api.py           # Integration tests for API endpoints
└── test_e2e.py           # End-to-end workflow tests
```

## Installation

Install test dependencies:

```bash
pip install -r requirements.txt
```

This installs:
- `pytest` - Test framework
- `pytest-flask` - Flask testing utilities
- `pytest-cov` - Code coverage reporting

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
# Unit tests only
pytest tests/test_unit.py

# API integration tests only
pytest tests/test_api.py

# End-to-end tests only
pytest tests/test_e2e.py
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/test_unit.py::TestCropAndUpscale

# Run a specific test function
pytest tests/test_api.py::TestUploadEndpoint::test_upload_success
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Coverage Report

```bash
# Terminal coverage report
pytest --cov=app --cov-report=term-missing

# HTML coverage report
pytest --cov=app --cov-report=html
# Then open htmlcov/index.html in browser
```

## Test Categories

### Unit Tests (`test_unit.py`)

Tests individual functions in isolation:

- **File Validation** - `TestAllowedFile`
  - Valid file extensions (png, jpg, jpeg, webp, bmp)
  - Invalid file extensions
  - Case sensitivity
  - Edge cases

- **Image Processing** - `TestCropAndUpscale`
  - Cropping accuracy
  - Upscaling to 4K
  - Upscaling to Full HD
  - Quality preservation
  - Aspect ratio handling

- **Preset Configuration** - `TestPresets`
  - Preset definitions
  - Resolution values
  - Aspect ratio consistency

**Run unit tests:**
```bash
pytest tests/test_unit.py -v
```

### API Integration Tests (`test_api.py`)

Tests API endpoints and request/response handling:

- **Index Route** - `TestIndexRoute`
  - Page loads successfully
  - Contains expected content

- **Upload Endpoint** - `TestUploadEndpoint`
  - Successful uploads
  - Error handling (no file, invalid type, empty filename)
  - Different file formats
  - Image dimension detection

- **Process Endpoint** - `TestProcessEndpoint`
  - Successful processing to 4K and Full HD
  - Crop coordinate handling
  - Error cases (invalid preset, missing file)
  - Upscaling requirements

- **Download Endpoint** - `TestDownloadEndpoint`
  - Successful downloads
  - File not found handling

**Run API tests:**
```bash
pytest tests/test_api.py -v
```

### End-to-End Tests (`test_e2e.py`)

Tests complete workflows from start to finish:

- **Complete Workflows** - `TestEndToEndWorkflow`
  - Full 4K workflow (upload → process → download)
  - Full HD workflow
  - Multiple image processing
  - Sequential operations

- **Real Image Processing** - `TestRealImageProcessing`
  - Uses actual images from `test_images/` folder
  - Tests various image sizes and aspect ratios
  - Center crop calculations
  - Edge cases

- **Image Quality** - `TestImageQuality`
  - Output format verification
  - File size reasonableness
  - Quality settings

**Run e2e tests:**
```bash
pytest tests/test_e2e.py -v
```

## Testing with Real Images

### Setup

1. Add test images to the `test_images/` folder
2. Include various sizes, aspect ratios, and content types
3. See `test_images/README.md` for recommendations

### Run Real Image Tests

```bash
# All real image tests
pytest tests/test_e2e.py::TestRealImageProcessing -v

# Specific real image test
pytest tests/test_e2e.py::TestRealImageProcessing::test_process_real_images_4k -v
```

**Note:** These tests automatically skip if no images are found in `test_images/`

## Test Fixtures

Located in `conftest.py`:

- `app` - Configured Flask test application
- `client` - Flask test client for API requests
- `runner` - CLI test runner
- `sample_image` - Generated 800×600 test image
- `sample_image_large` - Generated 2000×1500 test image
- `sample_image_small` - Generated 400×300 test image

## Coverage Goals

Aim for high coverage in critical areas:

- **Image processing functions**: 100%
- **API endpoints**: >90%
- **Error handling**: >80%

Check current coverage:
```bash
pytest --cov=app --cov-report=term-missing
```

## Continuous Integration

To integrate with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=app --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Common Test Commands

```bash
# Quick test run (no output capture)
pytest -s

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Run tests matching a pattern
pytest -k "upload"

# Show test durations
pytest --durations=10

# Verbose with full output
pytest -vv -s
```

## Writing New Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test

```python
def test_my_feature(client, sample_image):
    """Test description"""
    # Arrange
    data = {'file': (sample_image, 'test.jpg', 'image/jpeg')}

    # Act
    response = client.post('/upload', data=data, content_type='multipart/form-data')

    # Assert
    assert response.status_code == 200
    assert response.get_json()['success'] == True
```

## Troubleshooting

### Tests Fail Due to Missing Directories

Fixtures automatically create test directories. If issues persist:
```bash
mkdir -p tests/test_uploads tests/test_processed
```

### PIL/Pillow Import Errors

Ensure Pillow is installed:
```bash
pip install Pillow==10.1.0
```

### Flask App Import Errors

Ensure you're running tests from the project root directory:
```bash
cd /path/to/image_crop_upscale
pytest
```

### Real Image Tests Always Skip

Add images to `test_images/` folder. Tests skip automatically if folder is empty.

## Best Practices

1. **Keep tests isolated** - Each test should be independent
2. **Use fixtures** - Leverage pytest fixtures for common setup
3. **Test edge cases** - Include boundary conditions and error cases
4. **Clear assertions** - One logical assertion per test when possible
5. **Descriptive names** - Test names should describe what they test
6. **Clean up** - Fixtures handle cleanup automatically

## Performance

Current test suite performance (approximate):
- Unit tests: ~2-3 seconds
- API tests: ~5-8 seconds
- E2E tests: ~10-15 seconds (varies with number of real images)

Total: ~20-30 seconds for full suite

## Future Enhancements

Potential additions to test suite:
- Performance/load testing
- Security testing (file upload vulnerabilities)
- Browser automation tests (Selenium)
- Stress testing with very large images
- Memory leak detection
- Concurrent request handling
