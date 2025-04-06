import cv2
import face_recognition
import os
import logging
import json
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("config.json not found")
        return None

def capture_training_data():
    config = load_config()
    if not config:
        return

    # Ensure attendees directory exists
    Path(config['path']).mkdir(exist_ok=True)

    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logging.error("Failed to open webcam")
            return

        person_name = input("Enter person's name (or 'q' to quit): ").strip()
        if person_name.lower() == 'q':
            return

        person_name = person_name.replace(" ", "_").upper()
        save_path = os.path.join(config['path'], f"{person_name}.jpg")

        print("\nInstructions:")
        print("1. Position face in the green box")
        print("2. Press 'c' to capture")
        print("3. Press 'q' to quit\n")

        while True:
            success, img = cap.read()
            if not success:
                logging.error("Failed to read frame")
                break

            # Display guide box
            height, width = img.shape[:2]
            center_x, center_y = width // 2, height // 2
            box_size = 300
            
            # Draw guide box
            cv2.rectangle(img, 
                         (center_x - box_size//2, center_y - box_size//2),
                         (center_x + box_size//2, center_y + box_size//2),
                         (0, 255, 0), 2)

            # Add instructions
            cv2.putText(img, "Position face in box and press 'c' to capture",
                       (20, height-40), cv2.FONT_HERSHEY_DUPLEX,
                       0.7, (255, 255, 255), 2)

            cv2.imshow('Capture Training Image', img)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                # Detect faces in frame
                face_locations = face_recognition.face_locations(img)
                
                if len(face_locations) == 0:
                    print("No face detected. Please try again.")
                    continue
                elif len(face_locations) > 1:
                    print("Multiple faces detected. Please ensure only one face is visible.")
                    continue
                
                # Save image
                cv2.imwrite(save_path, img)
                print(f"\nImage saved successfully: {save_path}")
                break

    except Exception as e:
        logging.error(f"Error capturing training data: {str(e)}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

def main():
    try:
        while True:
            print("\nFace Recognition Training System")
            print("1. Capture New Face")
            print("2. Exit")
            
            choice = input("\nSelect option: ")
            
            if choice == "1":
                capture_training_data()
            elif choice == "2":
                break
            else:
                print("Invalid option. Please try again.")

    except KeyboardInterrupt:
        print("\nTraining system terminated by user")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()