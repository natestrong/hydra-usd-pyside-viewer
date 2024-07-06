# Hydra USD PySide Viewer

![storytwin-hydra.gif](images%2Fstorytwin-hydra.gif)

This project is a simple USD (Universal Scene Description) viewer built with PySide6 and integrated with Hydra for
rendering. It includes a timeline widget for animation playback, inspired by BigRoy’s example on [Gist](https://gist.github.com/BigRoy/5ac50208969fdc69a722d66874faf8a2).

# Features
	•	Load and display USD files
	•	Control animation playback with a timeline widget
	•	Adjust frames per second (FPS) for playback

# Setup Instructions
### Prerequisites
	•	Python 3.11 (or adjust as needed)
	•	PySide6
	•	PyOpenGL
	•	OpenUSD (built from source)

## Step-by-Step Setup
### 1.	Clone the Repository
```bash
git clone https://github.com/your-username/hydra-usd-pyside-viewer.git
cd hydra-usd-pyside-viewer
```

### 2.	Setup Python Environment
This project uses pyenv for managing the Python version. You can set up pyenv as follows, but it’s optional.
```bash
pyenv install 3.11.5
pyenv virtualenv 3.11.5 hydra-usd-pyside
pyenv activate hydra-usd-pyside
```

### 3.	Install Dependencies
```bash
pip install -r requirements.txt
```
### 4.	Build OpenUSD
Follow the instructions on the OpenUSD GitHub repository to build USD from source. Use the --build-monolithic option to ensure all necessary components are included.
```bash
git clone https://github.com/PixarAnimationStudios/OpenUSD.git
cd OpenUSD
python build_scripts/build_usd.py /opt/local/USD --python --build-monolithic
```

### 5.	Update env_setup.py
Modify the USD_INSTALL_PATH variable in env_setup.py to point to your USD build location.
```python
# Define the USD installation path
USD_INSTALL_PATH = '/opt/local/USD'
```

### 6.	Run the Application
```python
python src/main.py
```

## Usage
	•	Play Animation: Use the play button on the timeline widget to start/stop the animation.
	•	Adjust FPS: Use the FPS control to change the playback speed.
	•	Navigate Frames: Use the slider or frame input boxes to jump to specific frames.


## Project Structure
	•	env_setup.py: Sets up the necessary environment variables for USD.
	•	src/main.py: Main application script.
	•	timeline.py: Contains the timeline widget and playback control logic.
	•	requirements.txt: List of Python dependencies.

## Notes
	•	Ensure the USD build location is correctly set in env_setup.py.
	•	The project uses pyenv for environment management, but it’s optional. You can use any Python environment setup that 

### Code Borrowed from BigRoy here: https://gist.github.com/BigRoy/5ac50208969fdc69a722d66874faf8a2
