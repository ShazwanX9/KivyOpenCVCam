# Kivy OpenCV Camera

This project implements a simple Kivy application that utilizes OpenCV for real-time camera processing. Users can apply various filters to the camera feed and display the processed output on the screen.

## Features

- **Real-time Camera Feed**: Access and display live camera input using Kivy's `Camera` widget.
- **Filter Support**: Apply custom image processing filters to the camera frames using OpenCV.
- **Modular Design**: Easily add or modify filters without changing the core application logic.

## Requirements

To run this application, you need the following dependencies:

- Python 3.x
- Kivy
- OpenCV
- NumPy

You can install the required packages using pip:

```bash
pip install kivy opencv-python numpy
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/kivy-opencv-camera.git
   cd kivy-opencv-camera
   ```

2. Ensure you have the necessary dependencies installed.

3. Run the application:

   ```bash
   python main.py
   ```

   Replace `main.py` with the name of your main Python file if it differs.

## Usage

- The application initializes the camera and displays the live feed.
- You can add custom filters by modifying the `img_filters` and `cam_filters` lists in the `KivyCvCameraSet` class.
- The default filter included in the example is a standard filter that flips and converts the camera frames.

### Example of Adding a Custom Filter

To add a new filter, define a new function like this:

```python
def custom_filter(frame: np.ndarray) -> np.ndarray:
    # Apply your custom processing here
    return processed_frame
```

Then, add the filter to the `cam_filters` or `img_filters` list in the `TestCamera` class:

```python
class TestCamera(App):
    def build(self):
        return KivyCvCameraSet(cam_filters=[standard_filter, custom_filter])
```

## Custom Filters

You can create custom filters by defining a function that takes a NumPy array (the image frame) as input and returns a processed NumPy array. Filters can be stacked, and the order of application is the order in which they are added to the filters list.

### Example Filter

Here’s an example of a simple grayscale filter:

```python
def grayscale_filter(frame: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## Contact

For any questions or feedback, you can reach me at [shazwanx9@gmail.com].