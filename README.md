# Hand Gesture Recognition

## Project Overview

This project implements a hand gesture recognition system that controls the system's volume and screen brightness by detecting hand gestures via a webcam. The project is built using Flask to create a web-based interface.

## Features

- **Hand Gesture Detection**: Utilizes OpenCV and MediaPipe to detect hand gestures.
- **Volume Control**: Adjust system volume using the right hand.
- **Brightness Control**: Adjust screen brightness using the left hand.
- **Web-Based Interface**: Implemented using Flask for easy access via a web browser.

## Technologies Used

- Python
- OpenCV
- MediaPipe
- pycaw (Python Core Audio Windows Library)
- Flask

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/sushantkrsky/hand-gesture-recognition.git
    cd hand-gesture-recognition
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the Flask server:
    ```bash
    python app.py
    ```

2. Open your web browser and go to:
    ```
    http://localhost:5000
    ```

## Usage

- **Adjust Volume**: Use your right hand to control the system volume. Move your hand up to increase the volume and down to decrease it.
- **Adjust Brightness**: Use your left hand to control the screen brightness. Move your hand up to increase the brightness and down to decrease it.

## Project Structure
hand-gesture-recognition/
│
├── app.py # Flask application and Main logic for gesture detection
├── templates/
│ └── index.html # HTML file for the homepage
  └── index.html # HTML file for the webcam interface
├── requirements.txt # List of dependencies
└── README.md # Project documentation

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

---

### Acknowledgements

- **OpenCV**: [https://opencv.org/](https://opencv.org/)
- **MediaPipe**: [https://mediapipe.dev/](https://mediapipe.dev/)
- **pycaw**: [https://github.com/AndreMiras/pycaw](https://github.com/AndreMiras/pycaw)

