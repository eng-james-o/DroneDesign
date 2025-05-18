# DroneDesign

DroneDesign is a Python-based application designed to assist aerospace engineers, drone developers, and enthusiasts in the conceptual design of small Unmanned Aerial Vehicles (UAVs). The tool streamlines the preliminary design phase by providing computational support for key aerodynamic and structural parameters, thereby facilitating efficient and accurate design iterations.

## Features

1. Aerodynamic Calculations: Compute essential parameters such as lift, drag, and thrust requirements based on user-defined inputs.

2. Propeller Analysis: Evaluate propeller performance characteristics to optimize thrust and efficiency.

3. Graphical User Interface (GUI): Intuitive interface built with PySide2 and QML for seamless user interaction.

4. Data Visualization: Integrated plotting capabilities using Matplotlib for real-time visualization of performance metrics.

5. Modular Architecture: Organized codebase with modular components for ease of maintenance and scalability.


## Installation

1. Clone the Repository:

```bash
git clone https://github.com/eng-james-o/DroneDesign.git
cd DroneDesign
```


2. Create a Virtual Environment (Optional but recommended):

python```python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate```


3. Install Dependencies:

bash```pip install -r requirements.txt```

Note: Ensure that you have Python 3.7 or higher installed.



## Usage

To launch the application, execute the following command:

bash```python main.py```

Upon launching, the GUI will allow you to input design parameters, perform calculations, and visualize results pertinent to UAV design.

Project Structure

```text
DroneDesign/
├── BreezeStyleSheets/       # Custom QML stylesheets for GUI theming
├── PERFILES_WEB/            # Web-based profiles or resources
├── UI/                      # QML files defining the user interface
├── functions/               # Core computational functions
├── other_assets/            # Additional assets (e.g., images, icons)
├── propeller/               # Modules related to propeller analysis
├── __pycache__/             # Compiled Python files
├── main.py                  # Entry point of the application
├── constants.py             # Global constants used across modules
├── mplwidget.py             # Matplotlib integration for PySide2
├── plotwidget.py            # Custom plotting widgets
├── propeller.py             # Propeller computation logic
├── propellerwidget.py       # GUI widget for propeller analysis
├── save.py                  # Functionality to save/load project data
├── storage.txt              # Temporary storage file
├── todo.txt                 # Development to-do list
├── main.pyproject           # Project configuration file
├── main.pyproject.user      # User-specific project settings
├── Newmainwindow.ui         # UI design file
├── SearchButton.svg         # SVG asset for search functionality
└── README.md                # Project documentation ```

## Dependencies

1. Python 3.7+

2. PySide2: For GUI development using Qt for Python.

3. Matplotlib: For plotting and data visualization.

4. NumPy: For numerical computations.


Additional dependencies can be found in the requirements.txt file.

## Contributing

Contributions are welcome and appreciated. To contribute:

1. Fork the repository.


2. Create a new branch:

bash```git checkout -b feature/YourFeature```


3. Commit your changes:

bash```git commit -m 'Add YourFeature'```


4. Push to the branch:

bash```git push origin feature/YourFeature```


5. Open a pull request detailing your changes.



Please ensure that your code adheres to the project's coding standards and includes appropriate documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
