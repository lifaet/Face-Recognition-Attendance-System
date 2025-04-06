# Face Recognition Attendance System

## 📝 Overview
An automated attendance tracking system using facial recognition technology. The system provides real-time face detection, recognition, and attendance marking with a user-friendly interface.

## ✨ Key Features
- Real-time face detection and recognition
- Automated attendance logging with timestamps
- Live video feed with visual feedback
- User-friendly interface with status messages
- CSV-based attendance records
- Configurable system parameters
- Comprehensive error logging

## 🚀 Quick Start

### Prerequisites
- Python 3.6+
- Visual Studio Build Tools with C++ compiler
- CMake
- Webcam
- 4GB+ RAM

### Installation

1. **Install Build Tools**
   - Download Visual Studio Community Edition
   - Select "Desktop Development with C++"
   - Complete installation
   - Download CMake and Install and restart

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
├── Attendance.py          # Main application
├── attendees/            # Reference face images
├── attendance.csv        # Attendance records
├── config.json          # System configuration
├── attendance_system.log # System logs
└── README.md            # Documentation
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

## 📱 Usage

### Setting Up Reference Images
1. Create clear face photos of individuals
2. Name format: `firstname_lastname.jpg`
3. Place images in the `attendees/` folder

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

## 🤝 Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License
MIT License - See [LICENSE](LICENSE) file

<!-- ## 💡 Support
- Open an issue for bugs
- Submit feature requests via issues
- Email: support@example.com

---
Made with ❤️ by [Your Name] -->