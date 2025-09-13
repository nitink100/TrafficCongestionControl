AI-Powered Traffic Congestion Control System 🚦
This project is an AI-driven traffic control system designed to dynamically manage signal timing based on real-time vehicle density. It uses the YOLO (You Only Look Once) object detection algorithm to identify vehicles and adjusts signal phases to optimize traffic flow and reduce congestion. The system is visualized through an interactive Pygame simulation.

✨ Key Features
Dynamic Signal Timing: Automatically adjusts traffic light green times based on live vehicle counts, reducing unnecessary waiting.

Real-time Vehicle Detection: Utilizes the YOLO (You Only Look Once) algorithm via Darkflow to detect and classify vehicles from video frames.

Vehicle Classification: Identifies different vehicle types (cars, bikes, buses, trucks) to calculate traffic density more accurately.

Interactive Simulation: A custom-built Pygame application provides a visual representation of the intersection, traffic flow, and dynamic signal changes.

🛠️ Tech Stack
Core Logic: Python

AI / Machine Learning: YOLO (Darknet), TensorFlow (via Darkflow), OpenCV

Simulation & UI: Pygame

Skills: Flask, Machine Learning

🚀 Getting Started
Follow these instructions to get a local copy up and running.

Prerequisites
Python 3.6 / 3.7 (due to TensorFlow 1.x dependency for Darkflow)

Pip & a virtual environment tool

YOLOv2 model files (yolov2.weights and yolo.cfg)

Installation
Clone the repository:

git clone [https://github.com/your-username/AI-Traffic-Control.git](https://github.com/your-username/AI-Traffic-Control.git)
cd AI-Traffic-Control

Create and activate a virtual environment:

python3.7 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Install Darkflow:
Navigate to the darkflow directory and run the build command.

cd darkflow
python setup.py build_ext --inplace
cd ..

Place Model Files:

Place your yolov2.weights file in the assets/model_files/bin/ directory.

Place your yolo.cfg file in the assets/model_files/cfg/ directory.

🏃 How to Run
To start the simulation, run the main script from the root directory:

python simulation.py

A Pygame window will launch, displaying the live traffic simulation.
