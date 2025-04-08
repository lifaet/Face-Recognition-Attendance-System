import cv2
import numpy
import face_recognition
import os
import datetime
import logging
import json
from pathlib import Path
import sys
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('attendance_system.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class UIOverlay:
    def __init__(self, config):
        self.config = config
        self.message = ""
        self.show_checkmark = False
        self.display_until = 0
        
    def set_analyzing(self):
        self.message = self.config['ui']['analyzing_text']
        self.show_checkmark = False
        
    def set_welcome(self, name):
        self.message = f"{self.config['ui']['welcome_text']} {name}!"
        self.show_checkmark = True
        self.display_until = time.time() + self.config['ui']['display_time']
        
    def set_unknown(self):
        self.message = self.config['ui']['unknown_text']
        self.show_checkmark = False
        self.display_until = time.time() + 2
        
    def should_clear(self):
        return self.display_until and time.time() > self.display_until
        
    def clear(self):
        self.message = ""
        self.show_checkmark = False
        self.display_until = 0

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default configuration
        config = {
            "path": "attendees",
            "frame_skip": 2,
            "face_recognition_threshold": 0.50,
            "attendance_file": "attendance.csv",
            "ui": {
                "analyzing_text": "Analyzing...",
                "welcome_text": "Welcome,",
                "unknown_text": "Unknown Person",
                "display_time": 2
            }
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        return config

class FaceRecognitionSystem:
    def __init__(self, config):
        self.config = config
        self.images = []
        self.classNames = []
        self.encodeListKnown = []
        self.frame_count = 0
        self.ui_overlay = UIOverlay(config)
        self.setup_files()
        
    def setup_files(self):
        Path(self.config['path']).mkdir(exist_ok=True)
        if not Path(self.config['attendance_file']).exists():
            with open(self.config['attendance_file'], 'w') as f:
                f.write("Name,Date,Time\n")

    def load_images(self):
        try:
            path = self.config['path']
            myList = os.listdir(path)
            logging.info(f"Found {len(myList)} images in {path}")
            
            for cl in myList:
                img_path = os.path.join(path, cl)
                curImg = cv2.imread(img_path)
                if curImg is None:
                    logging.error(f"Failed to load image: {img_path}")
                    continue
                self.images.append(curImg)
                self.classNames.append(os.path.splitext(cl)[0])
            
            return True
        except Exception as e:
            logging.error(f"Error loading images: {str(e)}")
            return False

    def findEncodings(self):
        try:
            encodeList = []
            for img in self.images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            self.encodeListKnown = encodeList
            logging.info("Encoding completed successfully")
            return True
        except Exception as e:
            logging.error(f"Error during encoding: {str(e)}")
            return False

    def markAttendance(self, name):
        try:
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            
            with open(self.config['attendance_file'], 'r+') as f:
                myDataList = f.readlines()
                nameList = [line.split(',')[0] for line in myDataList]
                
                today_attendance = [
                    line for line in myDataList 
                    if name in line and current_date in line
                ]
                
                if not today_attendance:
                    f.writelines(f'\n{name},{current_date},{current_time}')
                    logging.info(f"Marked attendance for {name}")
                    return True
                return False
        except Exception as e:
            logging.error(f"Error marking attendance: {str(e)}")
            return False

    def draw_ui(self, img):
        if not self.ui_overlay.message:
            return img
            
        height, width = img.shape[:2]
        overlay = img.copy()
        
        # Draw semi-transparent overlay
        cv2.rectangle(overlay, (0, height-100), (width, height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, img, 0.5, 0, img)
        
        # Draw message
        cv2.putText(img, self.ui_overlay.message,
                    (20, height-40), cv2.FONT_HERSHEY_DUPLEX,
                    1.0, (255, 255, 255), 2)
                    
        # Draw checkmark if needed
        if self.ui_overlay.show_checkmark:
            check_center = (width-50, height-50)
            cv2.circle(img, check_center, 25, (0, 255, 0), -1)
            # Draw checkmark
            pts = numpy.array([
                [check_center[0]-15, check_center[1]],
                [check_center[0]-5, check_center[1]+10],
                [check_center[0]+15, check_center[1]-10]
            ], numpy.int32)
            cv2.polylines(img, [pts], False, (255, 255, 255), 3)
        
        return img

    def run(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                logging.error("Failed to open webcam")
                return False

            # Force high performance settings
            cap.set(cv2.CAP_PROP_FPS, 30)  # Reduced to stable 30FPS
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            last_recognition_time = time.time()
            recognition_cooldown = 2  # 2 second cooldown

            while True:
                success, img = cap.read()
                if not success:
                    break

                # Simple copy for display
                display_img = img.copy()
                
                # Quick face detection
                small_frame = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_small_frame)

                if face_locations:
                    # Get first face only
                    y1, x2, y2, x1 = face_locations[0]
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    
                    # Draw green box
                    cv2.rectangle(display_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Do recognition every 2 seconds
                    if time.time() - last_recognition_time > recognition_cooldown:
                        face_encoding = face_recognition.face_encodings(rgb_small_frame, [face_locations[0]])[0]
                        matches = face_recognition.compare_faces(self.encodeListKnown, face_encoding, tolerance=0.5)

                        if True in matches:
                            match_index = matches.index(True)
                            name = self.classNames[match_index].upper()
                            
                            # Draw name and mark attendance
                            cv2.putText(display_img, name, (x1, y1-10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            
                            if self.markAttendance(name):
                                self.ui_overlay.set_welcome(name)
                                self.ui_overlay.display_until = time.time() + 3  # Show for 3 seconds
                        else:
                            cv2.putText(display_img, "UNKNOWN", (x1, y1-10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        
                        last_recognition_time = time.time()

                # Draw UI if needed
                if not self.ui_overlay.should_clear():
                    display_img = self.draw_ui(display_img)
                else:
                    self.ui_overlay.clear()

                cv2.imshow('Face Recognition', display_img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()

def main():
    try:
        config = load_config()
        face_system = FaceRecognitionSystem(config)
        
        if not face_system.load_images():
            logging.error("Failed to load images. Exiting...")
            return
            
        if not face_system.findEncodings():
            logging.error("Failed to encode faces. Exiting...")
            return
            
        face_system.run()
        
    except KeyboardInterrupt:
        logging.info("Application terminated by user")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()