import cv2
from darkflow.net.build import TFNet
import os

# --- MODEL CONFIGURATION ---
# This dictionary tells darkflow where to find the YOLO model configuration and weights.
options = {
    'model': 'assets/model_files/cfg/yolo.cfg',
    'load': 'assets/model_files/bin/yolov2.weights',
    'threshold': 0.3,
    'gpu': 0.0  # Set to 1.0 to use GPU if configured
}

# Initialize the TensorFlow-based YOLO model
try:
    tfnet = TFNet(options)
    print("YOLO model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    print("Please ensure TensorFlow 1.x is installed and model files are in the correct directory.")
    tfnet = None

# --- VEHICLE DETECTION FUNCTION ---
def detect_vehicles(image_path):
    """
    Detects and classifies vehicles in a given image using the YOLO model.

    Args:
        image_path (str): The full path to the input image.

    Returns:
        tuple: A tuple containing the annotated image (with bounding boxes) 
               and a dictionary of vehicle counts.
    """
    if not tfnet:
        print("Detection skipped because the model is not loaded.")
        return None, {}

    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image from {image_path}")
            return None, {}

        # Use darkflow to get predictions
        predictions = tfnet.return_predict(image)
        
        vehicle_counts = {'car': 0, 'bus': 0, 'truck': 0, 'rickshaw': 0, 'bike': 0}
        
        # Draw bounding boxes and count vehicles
        for pred in predictions:
            label = pred['label']
            if label in vehicle_counts:
                top_left = (pred['topleft']['x'], pred['topleft']['y'])
                bottom_right = (pred['bottomright']['x'], pred['bottomright']['y'])
                
                # Draw rectangle and label on the image
                image = cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
                image = cv2.putText(image, label, top_left, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                
                # Increment vehicle count
                vehicle_counts[label] += 1
        
        return image, vehicle_counts

    except Exception as e:
        print(f"An error occurred during vehicle detection: {e}")
        return None, {}

# --- STANDALONE TEST SCRIPT ---
# This part allows you to test the detection script independently.
if __name__ == '__main__':
    print("Running vehicle detection in standalone test mode...")
    
    input_dir = "assets/test_images"
    output_dir = "assets/output_images"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process all images in the test directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_dir, filename)
            print(f"Processing {image_path}...")
            
            annotated_image, counts = detect_vehicles(image_path)
            
            if annotated_image is not None:
                output_path = os.path.join(output_dir, f"output_{filename}")
                cv2.imwrite(output_path, annotated_image)
                print(f"Detected: {counts}")
                print(f"Output image saved to: {output_path}\n")

    print("Detection test finished.")