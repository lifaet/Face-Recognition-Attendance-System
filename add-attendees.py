import cv2
import face_recognition
import os
from pathlib import Path
import sys

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found")
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
            print("Error: Failed to open webcam")
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
                print("Error: Failed to read frame")
                break

            # ...existing code for guide box and display...

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                face_locations = face_recognition.face_locations(img)
                
                if len(face_locations) == 0:
                    print("No face detected. Please try again.")
                    continue
                elif len(face_locations) > 1:
                    print("Multiple faces detected. Please ensure only one face is visible.")
                    continue
                
                cv2.imwrite(save_path, img)
                print(f"\nImage saved successfully: {save_path}")
                break

    except Exception as e:
        print(f"Error capturing training data: {str(e)}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

# ...rest of the code remains the same...