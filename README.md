# AI-Powered Traffic Congestion Control System 🚦

This project is an intelligent traffic control system designed to dynamically manage signal timing based on real-time vehicle density. It leverages the YOLO object detection algorithm to identify vehicles and adjusts signal phases to optimize traffic flow, all visualized through an interactive Pygame simulation.

!(https://i.imgur.com/4x0y7yB.png)

---

## ✨ Key Features

* **Dynamic Signal Timing:** Automatically adjusts traffic light green times based on live vehicle counts, reducing unnecessary waiting and congestion.
* **Real-time Vehicle Detection:** Utilizes the YOLO (You Only Look Once) algorithm via the Darkflow library to detect and classify vehicles from video frames.
* **Vehicle Classification:** Identifies different vehicle types (cars, bikes, buses, trucks) to calculate traffic density more accurately.
* **Interactive Simulation:** A custom-built Pygame application provides a visual representation of the intersection, traffic flow, and dynamic signal changes.

---

## 🛠️ Tech Stack

* **Core Logic:** Python
* **AI / Machine Learning:** YOLO (Darknet), TensorFlow 1.x (via Darkflow), OpenCV
* **Simulation & UI:** Pygame

---

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

* **Python 3.6 / 3.7** (This is critical for TensorFlow 1.x compatibility)
* Pip (Python package installer)
* YOLOv2 model files (`yolov2.weights` and `yolo.cfg`)

### Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/AI-Traffic-Control.git](https://github.com/your-username/AI-Traffic-Control.git)
    cd AI-Traffic-Control
    ```

2.  **Create and Activate a Virtual Environment**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    # Make sure to use your Python 3.7 executable
    python3.7 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Required Packages**
    Install all the necessary Python libraries using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Darkflow Manually**
    The `darkflow` library requires a manual compilation step. Navigate into its directory and run the build command.
    ```bash
    # This command must be run from the root of the project
    cd darkflow
    python setup.py build_ext --inplace
    cd ..
    ```

5.  **Place YOLO Model Files**
    You need to download the pre-trained YOLOv2 model files and place them in the correct directory.
    * Place your `yolov2.weights` file in `assets/model_files/bin/`.
    * Place your `yolo.cfg` file in `assets/model_files/cfg/`.

---

## 🏃 How to Run the Simulation

Once the installation is complete, you can start the simulation.

1.  **Navigate to the Root Directory**
    Make sure you are in the main `AI-Traffic-Control` folder.

2.  **Run the Main Script**
    Execute the `simulation.py` file. A Pygame window will launch, displaying the live traffic simulation.
    ```bash
    python simulation.py
    ```
