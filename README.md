# DroneDesign

DroneDesign is a Python-based application designed to assist aerospace engineers, drone developers, and enthusiasts in the conceptual design of small Unmanned Aerial Vehicles (UAVs). The tool streamlines the preliminary design phase by providing computational support for key aerodynamic and structural parameters, thereby facilitating efficient and accurate design iterations.

## Features

- **Aerodynamic Calculations:** Compute essential parameters such as lift, drag, and thrust requirements based on user-defined inputs.
- **Propeller Analysis:** Evaluate propeller performance characteristics to optimize thrust and efficiency.
- **Graphical User Interface (GUI):** Intuitive interface built with PyQt5 and Qt Designer UI files for seamless user interaction.
- **Data Visualization:** Integrated plotting capabilities using Matplotlib for real-time visualization of performance metrics.
- **Modular Architecture:** Organized codebase with modular components for ease of maintenance and scalability.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/eng-james-o/DroneDesign.git
    cd DroneDesign
    ```

2. **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    > Ensure that you have Python 3.7 or higher installed.

## Project Structure

```text
DroneDesign/
├── assets/                  # Images, icons, and other static assets
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point of the application
│   ├── constants.py         # Global constants used across modules
│   ├── mplwidget.py         # Matplotlib integration for PyQt5
│   ├── plotwidget.py        # Custom plotting widgets
│   ├── propeller.py         # Propeller computation logic
│   ├── propellerwidget.py   # GUI widget for propeller analysis
│   ├── save.py              # Functionality to save/load project data
│   ├── functions/           # Core computational functions
│   ├── propeller/           # Modules related to propeller analysis
│   ├── BreezeStyleSheets/   # Custom Qt stylesheets for GUI theming
│   ├── PERFILES_WEB/        # Web-based profiles or resources
│   └── ui/                  # Qt Designer .ui files
│       └── Newmainwindow.ui
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Running the Application

To launch the application, run:

```bash
python src/main.py
```

The GUI will allow you to input design parameters, perform calculations, and visualize results pertinent to UAV design.

## Dependencies

- Python 3.7+
- PyQt5: For GUI development using Qt Designer UI files.
- Matplotlib: For plotting and data visualization.
- NumPy: For numerical computations.

Additional dependencies can be found in the `requirements.txt` file.

## Acknowledgements

Styling is based on [BreezeStyleSheets](https://github.com/eng-james-o/BreezeStyleSheets), a fork of [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet) with custom edits.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
