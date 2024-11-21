# CNC Utility Application

## Overview
The CNC Utility is a Python-based graphical user interface (GUI) application designed to assist CNC machine users with various calculations, visualizations, and G-code generation. The application allows users to input geometric parameters, calculate important machining values, and visualize the location of specific points, centroids, and offsets for different geometric shapes, including rectangles, circles, and polygons.

The application provides the following features:
- **Dynamic Visualization**: Visualize geometric shapes and calculated points directly on the GUI.
- **Shape Selection and Calculations**: Supports rectangle, circle, and polygon calculations with configurable dimensions.
- **Unit Conversion**: Convert between metric and imperial units.
- **Offset Calculations**: Determine custom locations based on user-defined offsets.
- **Save and View History**: Store and view previously calculated values, which can also be saved to a text file.

## Features
- **Shape Input Options**: Select and input values for different shapes such as rectangles, circles, and polygons. The input fields dynamically update based on the selected shape.
- **Visualization**: The application provides a canvas that dynamically resizes based on the window size, allowing users to visualize the geometry and important points.
- **History Tracking**: Calculated results are stored in the history section for reference. Users can save this history to a text file or clear it when needed.
- **Z-Axis Integration**: Optionally enable Z-axis input for 3D calculations.

## Installation
To run the CNC Utility, you need Python 3.x installed on your machine along with the required dependencies. You can set up the environment by following the instructions below:

1. **Clone the repository** (if hosted on a version control platform):
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```sh
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install the dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Requirements
The required Python packages are listed in the `requirements.txt` file:
- `tkinter`: Provides the GUI components.
- `math`: Standard Python library for mathematical calculations.

To install the dependencies, use the command:
```sh
pip install -r requirements.txt
```

## Usage
1. **Run the script**:
   ```sh
   python cnc_utility.py
   ```
2. **Interact with the GUI**:
   - Select the shape type from the dropdown menu.
   - Input the required geometric parameters.
   - Use the checkboxes to enable Z-axis input or specific location offsets.
   - Click the "Calculate" button to see results and visualizations.
   - View or save the calculation history as needed.

## Files in the Repository
- **cnc_utility.py**: The main application script containing all the logic for calculations, GUI, and visualizations.
- **requirements.txt**: Lists all the Python packages required to run the application.
- **README.md**: This documentation file to help users understand the project and how to get started.

## Contributing
Contributions are welcome! Feel free to fork this repository, create a new branch, and submit a pull request with your improvements. Make sure to add proper documentation for any new features.

## License
This project is open source and available under the [MIT License](LICENSE).

## Contact
For any questions, issues, or suggestions, please open an issue on the repository or reach out to the maintainer.

