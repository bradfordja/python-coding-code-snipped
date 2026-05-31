Converting a large image to an icon involves resizing and potentially simplifying the image to ensure it looks good at a smaller size. Here are the steps you can follow using Python and the Pillow library to convert a large image to an icon:

### 1. Install Pillow
First, ensure you have Pillow installed. If not, you can install it using pip:

```bash
pip install pillow
```

### 2. Write the Python Script
Here is a Python script that resizes a large image to a smaller size suitable for an icon (e.g., 32x32 pixels) and saves it as an icon file:

```python
from PIL import Image

def convert_image_to_icon(input_image_path, output_icon_path, size=(32, 32)):
    # Open the input image
    with Image.open(input_image_path) as img:
        # Resize the image
        img = img.resize(size, Image.ANTIALIAS)
        # Save the image as an icon
        img.save(output_icon_path, format='ICO', sizes=[size])

# Example usage
input_image_path = 'large_image.png'  # Path to your large image
output_icon_path = 'icon.ico'         # Path where the icon will be saved
convert_image_to_icon(input_image_path, output_icon_path)
```

### Explanation
1. **Import the Pillow Library**: The `Image` class from the Pillow library is used to open, resize, and save the image.
2. **Define the Function**: The `convert_image_to_icon` function takes three arguments: the input image path, the output icon path, and the desired size of the icon (default is 32x32 pixels).
3. **Open the Image**: The `Image.open()` function opens the input image.
4. **Resize the Image**: The `resize()` function resizes the image to the desired size. `Image.ANTIALIAS` is used to ensure the resized image has good quality.
5. **Save as Icon**: The `save()` function saves the resized image as an icon (`.ico`) file.

### Example Usage
To use the script, replace `'large_image.png'` with the path to your large image and `'icon.ico'` with the desired output path for the icon. Run the script, and it will create an icon file from your large image.

### Additional Notes
- **Image Format**: Ensure your input image is in a format that Pillow can read (e.g., PNG, JPEG).
- **Quality**: When resizing, the quality of the icon might be impacted. Simplifying the image before resizing might help maintain clarity.
- **Multiple Sizes**: Icons can have multiple sizes embedded within a single `.ico` file. You can provide multiple sizes to the `sizes` argument if needed.

By following these steps, you can easily convert a large image to an icon using Python.