# Vision-For-Robot-Path-Planning
Vision-based path planning for Mobile Robots

### Hardware Requirements
The system used to run both the segmentation models and the path planning code had the following specifications:

• **CPU:** AMD Ryzen 7 6800H with Radeon Graphics (3.20 GHz)
• **GPU:** NVIDIA GeForce RTX 3050Ti
• **RAM:** 16 GB (15.3 GB usable)


### Software Requirements
Software specifications include:

• **Segmentation:** Torch and Scikit-learn
• **Path planning:** Matlab and RVCTools
• **Flask Application:** Flask, SciPy, Scikit, Plotly, and Pandas

### Application
The Flask application is designed to run on a local machine and requires MATLAB R2022b installed.

#### Installation

1. Install MATLAB R2022b on your local machine.
2. Navigate to the `app` folder.
3. Create a virtual environment using your preferred method. For example, using python, run the following command in your terminal:
    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment by running the following command:
    ```bash
    source venv/bin/activate
    ```

5. Install the required dependencies by running the following command:
    ```bash
    pip install -r requirements.txt
    ```

#### Usage
Once the virtual environment has been activated and the dependencies have been installed, run the following command in your terminal:
```
python app.py
```

This will start the Flask app, which can be accessed by navigating to http://localhost:5000 in your web browser.


### Path-Planning
The MATLAB scripts are designed to perform path planning using Q-Learning with a 6-DOF robotic arm in an environment with obstacles.

#### Installation

1. Install MATLAB R2022b on your local machine.
2. Install the Robotics Toolbox for MATLAB (RVCTools) by following the instructions provided on the official website.
3. Add the RVCTools folder to the MATLAB search path. To do this, run the following command in the MATLAB command window:

    ```bash
    addpath(genpath('/path/to/rvctools'));
    ```
    Replace "/path/to/rvctools" with the actual path to the RVCTools folder on your local machine.


4. Run the RVCTools startup script by running the following command in the MATLAB command window:
    ```bash
    startup_rvc
    ```
    This will set up the RVCTools environment and add it to the MATLAB search path.

#### Usage
Once the dependencies have been installed, you can run the path planning script in MATLAB by running the following command:
```bash
Pose_Schedule_with_Reschedule([x , y, z])
```
Replace `x`, `y` and `z` with the coordinates of the target.