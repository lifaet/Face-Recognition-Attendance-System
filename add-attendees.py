import cv2
import face_recognition
import os
import json
from pathlib import Path

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Config file not found. Creating default configuration...")
        default_config = {
            "path": "attendees",
            "frame_skip": 2,
            "face_recognition_threshold": 0.50,
            "attendance_file": "attendance.csv",
            "ui": {
                "analyzing_text": "Analyzing...",
                "welcome_text": "Welcome,",
                "unknown_text": "Unknown Person",
                "display_time": 3
            }
        }
        try:
            with open('config.json', 'w') as f:
                json.dump(default_config, f, indent=4)
            print("Default configuration created successfully.")
            return default_config
        except Exception as e:
            print(f"Error creating config file: {str(e)}")
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

def list_attendees():
    config = load_config()
    if config and os.path.exists(config['path']):
        attendees = [f.replace('.jpg', '') for f in os.listdir(config['path']) 
                    if f.endswith('.jpg')]
        if attendees:
            print("\nRegistered Attendees:")
            for i, name in enumerate(attendees, 1):
                print(f"{i}. {name}")
        else:
            print("\nNo attendees registered yet.")
    else:
        print("\nAttendees directory not found.")

def delete_attendee():
    config = load_config()
    if not config or not os.path.exists(config['path']):
        print("\nNo attendees directory found.")
        return

    attendees = [f for f in os.listdir(config['path']) if f.endswith('.jpg')]
    if not attendees:
        print("\nNo attendees to delete.")
        return

    print("\nSelect attendee to delete:")
    for i, name in enumerate(attendees, 1):
        print(f"{i}. {name.replace('.jpg', '')}")

    try:
        choice = int(input("\nEnter number (or 0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(attendees):
            file_to_delete = os.path.join(config['path'], attendees[choice-1])
            os.remove(file_to_delete)
            print(f"\nDeleted: {attendees[choice-1].replace('.jpg', '')}")
        else:
            print("\nInvalid selection.")
    except ValueError:
        print("\nInvalid input. Please enter a number.")

def main():
    try:
        while True:
            print("\nFace Recognition Training System")
            print("================================")
            print("1. Add New Person")
            print("2. View Registered Attendees")
            print("3. Delete Attendee")
            print("4. Exit")
            
            choice = input("\nSelect option: ")
            
            if choice == "1":
                capture_training_data()
            elif choice == "2":
                list_attendees()
            elif choice == "3":
                delete_attendee()
            elif choice == "4":
                print("\nExiting training system...")
                break
            else:
                print("\nInvalid option. Please try again.")

    except KeyboardInterrupt:
        print("\nTraining system terminated by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()