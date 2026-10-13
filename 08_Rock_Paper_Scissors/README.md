# Rock Paper Scissors Using Hand Gestures

**Author:** Dharmesh Kumar  
**Language:** Python  
**Computer vision:** OpenCV + MediaPipe Hands

Play Rock Paper Scissors using your real hand gestures in front of your webcam. The computer recognizes your hand pose and chooses a random move.

## Gestures

| Gesture | Move |
|---|---|
| Closed fist | Rock |
| Open palm with fingers extended | Paper |
| Index and middle fingers extended | Scissors |

## Features

- Live webcam video
- Hand landmark detection using MediaPipe
- Gesture classification
- Random computer opponent
- Round result and score display
- Press `Q` to quit

## Requirements

- Python 3.10 or 3.11 recommended
- Webcam
- Windows, macOS, or Linux
- Packages in `requirements.txt`

## Setup in VS Code

1. Extract the ZIP and open this folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment (recommended):

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install the packages:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Run the game:
   ```bash
   python rock_paper_scissors_gestures.py
   ```

6. Allow camera access if your operating system asks for permission.

## How to Play

- Position your hand clearly in front of the camera, with your palm facing the camera.
- Hold a closed fist for Rock.
- Show an open palm for Paper.
- Raise only your index and middle fingers for Scissors.
- The game processes a round every couple of seconds while a valid gesture is detected.
- Press `Q` to close the game.

## Troubleshooting

- **Camera does not open:** Close apps using the webcam. In the Python file, change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` if needed.
- **Camera permission denied:** Enable camera access for VS Code or your terminal in your operating system's privacy settings.
- **Gesture detected incorrectly:** Use good lighting, keep the whole hand visible, and face your palm toward the camera. This project uses a simple landmark heuristic, so unusual hand angles may be misclassified.
- **MediaPipe installation error:** Use Python 3.10 or 3.11 in a fresh virtual environment and install from `requirements.txt`.

## Project Structure

```text
Rock_Paper_Scissors_Hand_Gestures/
├── rock_paper_scissors_gestures.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
└── screenshots/
    └── README.md
```

## Concepts Practiced

Python functions, loops, conditionals, random choice, computer vision, webcam frames, image color conversion, hand landmarks, and basic gesture recognition.

## Future Improvements

- Add a countdown before each round
- Improve gesture recognition for different hand angles
- Add a start screen and graphical score panel
- Save match history

## License

MIT License. See `LICENSE`.
