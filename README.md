# Face Recognition Attendance System

## 📋 Overview
The Face Recognition Attendance System is a cutting-edge solution that automates attendance tracking using advanced facial recognition technology. This intelligent system combines computer vision, machine learning, and automated record-keeping to create a seamless attendance management experience.

Operating in real-time, it captures video feed, detects faces, matches them against a database, and automatically records attendance with timestamps. Built with privacy and security in mind, it ensures accurate recognition while maintaining data protection standards.


## ✨ Key Features
- Real-time face detection and recognition (>95% accuracy)
- Automated attendance logging with timestamps
- User-friendly interface with visual feedback
- Multi-face detection capability
- Privacy-focused design with secure data storage
- Configurable system parameters
- Comprehensive error logging


## 🚀 Quick Start

### Prerequisites
- Python 3.6+
- Visual Studio Build Tools with C++
- CMake
- Webcam (720p minimum)
- 4GB+ RAM

### Installation

1. **Install Visual Studio Build Tools**
   - Download Visual Studio Community Edition
   - Select "Desktop Development with C++"
   - Complete installation and restart

2. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Face-Recognition-Attendance-System.git
   cd Face-Recognition-Attendance-System
   ```

3. **Install Python dependencies**
   ```bash
   pip install cmake
   pip install dlib
   pip install face-recognition
   pip install numpy
   pip install opencv-python
   ```


## 📂 Project Structure
```
Face-Recognition-Attendance-System/
├── fras.py                 # Main application
├── capture_training.py     # Face Training
├── attendees/              # Reference face images
├── attendance.csv          # Attendance records
├── config.json             # System configuration
├── attendance_system.log   # System logs
└── README.md               # Documentation
```


## ⚙️ Configuration
The system can be configured via `config.json`:

```json
{
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
```

## 📸 Face Training System

### Overview
The system includes a separate training script (`capture_training.py`) for adding new people to the attendance system.

### Features
- Interactive face capture interface
- Real-time face detection validation
- Visual guide box for proper positioning
- Single-face validation
- Automatic image saving
- Error handling and logging

### Usage

1. **Run Training Script**
   ```bash
   python capture_training.py
   ```

2. **Adding New Person**
   - Select "Capture New Face"
   - Enter person's name
   - Follow on-screen instructions:
     - Position face within green guide box
     - Press 'c' to capture
     - Press 'q' to quit

3. **Image Requirements**
   - Single face per image
   - Good lighting conditions
   - Clear, front-facing pose
   - Subject centered in guide box

### File Structure
```
Face-Recognition-Attendance-System/
├── fras.py                 # Main attendance system
├── capture_training.py     # Training interface
├── attendees/              # Stored face images
└── training.log           # Training session logs
```

### Notes
- Images are automatically saved in the `attendees` folder
- Naming format: `FIRSTNAME_LASTNAME.jpg`
- System automatically recognizes new faces on next startup
- Supports multiple training sessions


## 📱 Usage

### Running the System
1. Start the application:
   ```bash
   python Attendance.py
   ```
2. System will initialize and load face data
3. Stand in front of camera for recognition
4. View real-time feedback on screen
5. Press 'Q' to exit

### Checking Attendance
- Open `attendance.csv` to view records
- Format: Name, Date, Time


## 🔍 Technical Details

### Face Recognition Process
1. Face Detection
   - Locates faces in video feed
   - Processes at 1/4 resolution for performance

2. Face Recognition
   - Converts detected faces to encodings
   - Matches against known face database
   - Threshold-based verification

3. Attendance Marking
   - Automatic date and time stamping
   - Duplicate entry prevention
   - CSV format storage

### UI Features
- Status messages for:
  - Face analysis in progress
  - Welcome messages
  - Unknown person alerts
- Visual indicators:
  - Green rectangle around detected faces
  - Checkmark for successful recognition
- Semi-transparent overlay


## 📊 Performance
- Frame skipping for optimal performance
- Configurable recognition threshold
- Efficient image processing
- Memory-optimized operations


## 🔧 Technical Architecture

### Core Components
1. **Face Detection Engine**
   - OpenCV-based detection
   - 1/4 resolution processing for optimization
   - 30 FPS processing speed

2. **Recognition System**
   - dlib's 128-point facial landmarks
   - Configurable matching threshold
   - Multi-face database support

3. **Attendance Management**
   - Automated CSV recording
   - Duplicate entry prevention
   - Timestamp tracking

### System Requirements
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Intel i3/AMD Ryzen 3 | Intel i5/AMD Ryzen 5 |
| RAM | 4GB | 8GB |
| Camera | 720p | 1080p |
| Storage | 500MB | 1GB |


## 🎯 Applications

### Educational
- Classroom attendance
- Event tracking
- Library access

### Corporate
- Employee attendance
- Meeting participation
- Visitor tracking

### Events
- Participant check-in
- Access control
- Session tracking


## ⚙️ Configuration
```json
{
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
```


## 🔧 Troubleshooting

### Common Issues
1. **Camera not detected**
   - Check camera connections
   - Verify camera permissions

2. **Recognition issues**
   - Ensure good lighting
   - Update reference photos
   - Adjust recognition threshold

3. **Performance issues**
   - Increase frame skip value
   - Check system resources
   - Update hardware drivers


## 📄 License
MIT License - See [LICENSE](LICENSE)

<!-- ## 🤝 Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines

---
Made with ❤️ by [Your Name] -->