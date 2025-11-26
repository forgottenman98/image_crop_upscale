import pytest
import os
from PIL import Image
import tempfile
from app import allowed_file, crop_and_upscale, PRESETS

class TestAllowedFile:
    """Test file validation"""

    def test_allowed_extensions(self):
        """Test that valid file extensions are allowed"""
        assert allowed_file('test.png') == True
        assert allowed_file('test.jpg') == True
        assert allowed_file('test.jpeg') == True
        assert allowed_file('test.webp') == True
        assert allowed_file('test.bmp') == True

    def test_disallowed_extensions(self):
        """Test that invalid file extensions are rejected"""
        assert allowed_file('test.gif') == False
        assert allowed_file('test.txt') == False
        assert allowed_file('test.pdf') == False
        assert allowed_file('test.exe') == False

    def test_case_insensitive(self):
        """Test that file extension check is case insensitive"""
        assert allowed_file('test.PNG') == True
        assert allowed_file('test.JPG') == True
        assert allowed_file('test.JPEG') == True

    def test_no_extension(self):
        """Test that files without extensions are rejected"""
        assert allowed_file('test') == False

    def test_multiple_dots(self):
        """Test files with multiple dots in filename"""
        assert allowed_file('my.test.image.png') == True
        assert allowed_file('my.test.image.txt') == False


class TestCropAndUpscale:
    """Test image processing functions"""

    def test_crop_and_upscale_4k(self):
        """Test cropping and upscaling to 4K resolution"""
        # Create a test image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as input_file:
            input_path = input_file.name
            img = Image.new('RGB', (1600, 1200), color='red')
            img.save(input_path)

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as output_file:
            output_path = output_file.name

        try:
            # Crop and upscale
            crop_coords = {'x': 100, 'y': 100, 'width': 1200, 'height': 675}
            crop_and_upscale(
                input_path,
                output_path,
                crop_coords,
                PRESETS['4k']['width'],
                PRESETS['4k']['height']
            )

            # Verify output
            assert os.path.exists(output_path)
            with Image.open(output_path) as result:
                assert result.size == (3840, 2160)

        finally:
            # Cleanup
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_crop_and_upscale_fhd(self):
        """Test cropping and upscaling to Full HD resolution"""
        # Create a test image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as input_file:
            input_path = input_file.name
            img = Image.new('RGB', (1600, 1200), color='blue')
            img.save(input_path)

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as output_file:
            output_path = output_file.name

        try:
            # Crop and upscale
            crop_coords = {'x': 50, 'y': 50, 'width': 1200, 'height': 675}
            crop_and_upscale(
                input_path,
                output_path,
                crop_coords,
                PRESETS['fhd']['width'],
                PRESETS['fhd']['height']
            )

            # Verify output
            assert os.path.exists(output_path)
            with Image.open(output_path) as result:
                assert result.size == (1920, 1080)

        finally:
            # Cleanup
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_crop_coordinates(self):
        """Test that crop coordinates are applied correctly"""
        # Create a test image with distinct quadrants
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as input_file:
            input_path = input_file.name
            img = Image.new('RGB', (800, 600))
            # Fill different areas with different colors
            pixels = img.load()
            for i in range(400):
                for j in range(300):
                    pixels[i, j] = (255, 0, 0)  # Top-left red
            for i in range(400, 800):
                for j in range(300):
                    pixels[i, j] = (0, 255, 0)  # Top-right green
            for i in range(400):
                for j in range(300, 600):
                    pixels[i, j] = (0, 0, 255)  # Bottom-left blue
            for i in range(400, 800):
                for j in range(300, 600):
                    pixels[i, j] = (255, 255, 0)  # Bottom-right yellow
            img.save(input_path)

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as output_file:
            output_path = output_file.name

        try:
            # Crop top-left quadrant (should be red)
            crop_coords = {'x': 0, 'y': 0, 'width': 400, 'height': 225}
            crop_and_upscale(
                input_path,
                output_path,
                crop_coords,
                1920,
                1080
            )

            # Verify output exists and has correct dimensions
            assert os.path.exists(output_path)
            with Image.open(output_path) as result:
                assert result.size == (1920, 1080)

        finally:
            # Cleanup
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_upscaling_quality(self):
        """Test that small images are upscaled correctly"""
        # Create a small test image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as input_file:
            input_path = input_file.name
            img = Image.new('RGB', (480, 270), color='purple')
            img.save(input_path)

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as output_file:
            output_path = output_file.name

        try:
            # Upscale entire image to 4K
            crop_coords = {'x': 0, 'y': 0, 'width': 480, 'height': 270}
            crop_and_upscale(
                input_path,
                output_path,
                crop_coords,
                3840,
                2160
            )

            # Verify upscaled correctly
            assert os.path.exists(output_path)
            with Image.open(output_path) as result:
                assert result.size == (3840, 2160)
                # Verify it's still an image (not corrupted)
                assert result.mode == 'RGB'

        finally:
            # Cleanup
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)


class TestPresets:
    """Test preset configurations"""

    def test_presets_exist(self):
        """Test that required presets are defined"""
        assert '4k' in PRESETS
        assert 'fhd' in PRESETS

    def test_4k_resolution(self):
        """Test 4K preset has correct resolution"""
        assert PRESETS['4k']['width'] == 3840
        assert PRESETS['4k']['height'] == 2160

    def test_fhd_resolution(self):
        """Test Full HD preset has correct resolution"""
        assert PRESETS['fhd']['width'] == 1920
        assert PRESETS['fhd']['height'] == 1080

    def test_preset_aspect_ratios(self):
        """Test that presets maintain 16:9 aspect ratio"""
        for preset_key, preset in PRESETS.items():
            aspect_ratio = preset['width'] / preset['height']
            assert abs(aspect_ratio - 16/9) < 0.01, f"{preset_key} should be 16:9"
