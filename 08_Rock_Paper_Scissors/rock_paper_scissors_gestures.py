"""
Rock Paper Scissors using Real Hand Gestures
Author: Dharmesh Kumar

Uses your webcam and MediaPipe to recognize:
  Fist             -> Rock
  Open palm        -> Paper
  Two fingers up   -> Scissors

Press Q to quit.
"""

import random
import time

import cv2
import mediapipe as mp

CHOICES = ("Rock", "Paper", "Scissors")
WINNING_PAIRS = {
    ("Rock", "Scissors"),
    ("Paper", "Rock"),
    ("Scissors", "Paper"),
}

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def finger_is_up(landmarks, tip_id, pip_id):
    """For fingers other than the thumb, compare tip and middle-joint height."""
    return landmarks[tip_id].y < landmarks[pip_id].y


def classify_gesture(hand_landmarks):
    """
    Classify a hand as Rock, Paper, Scissors, or Unknown.
    This simple heuristic works best with the palm facing the camera.
    """
    lm = hand_landmarks.landmark

    index_up = finger_is_up(lm, 8, 6)
    middle_up = finger_is_up(lm, 12, 10)
    ring_up = finger_is_up(lm, 16, 14)
    pinky_up = finger_is_up(lm, 20, 18)

    # Thumb extension is approximated using horizontal distance from its base.
    # The threshold is deliberately modest; keep the thumb visible to the camera.
    thumb_extended = abs(lm[4].x - lm[2].x) > 0.07

    extended_count = sum((index_up, middle_up, ring_up, pinky_up))

    if extended_count == 0 and not thumb_extended:
        return "Rock"
    if index_up and middle_up and ring_up and pinky_up:
        return "Paper"
    if index_up and middle_up and not ring_up and not pinky_up:
        return "Scissors"

    # A closed fist may have the thumb extended sideways, depending on angle.
    if extended_count == 0:
        return "Rock"

    return "Unknown"


def computer_choice():
    return random.choice(CHOICES)


def decide_winner(player, computer):
    if player == computer:
        return "Tie!"
    if (player, computer) in WINNING_PAIRS:
        return "You win!"
    return "Computer wins!"


def main():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open webcam. Check camera permissions or try camera index 1.")
        return

    player_score = 0
    computer_score = 0
    ties = 0
    player_gesture = "Show your hand"
    computer_gesture = "-"
    result_text = "Make Rock, Paper, or Scissors"
    last_round_time = 0.0
    round_cooldown = 2.0

    print("Rock Paper Scissors - Hand Gesture Edition")
    print("Show a fist for Rock, open palm for Paper, or two fingers for Scissors.")
    print("Press Q to quit.")

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    ) as hands:
        while True:
            ok, frame = camera.read()
            if not ok:
                print("Error: Could not read from webcam.")
                break

            # Mirror the view so it feels like looking in a mirror.
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame.flags.writeable = False
            output = hands.process(rgb_frame)
            rgb_frame.flags.writeable = True

            detected_gesture = "Unknown"
            if output.multi_hand_landmarks:
                hand = output.multi_hand_landmarks[0]
                mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
                detected_gesture = classify_gesture(hand)

            if detected_gesture in CHOICES:
                player_gesture = detected_gesture
                current_time = time.time()
                if current_time - last_round_time >= round_cooldown:
                    computer_gesture = computer_choice()
                    result_text = decide_winner(player_gesture, computer_gesture)
                    if result_text == "You win!":
                        player_score += 1
                    elif result_text == "Computer wins!":
                        computer_score += 1
                    else:
                        ties += 1
                    last_round_time = current_time
            else:
                player_gesture = "Show hand clearly"

            # On-screen UI
            cv2.rectangle(frame, (0, 0), (frame.shape[1], 155), (25, 25, 25), -1)
            cv2.putText(frame, "ROCK PAPER SCISSORS - HAND GESTURES",
                        (15, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (255, 255, 255), 2)
            cv2.putText(frame, f"Your gesture: {player_gesture}",
                        (15, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (80, 230, 120), 2)
            cv2.putText(frame, f"Computer: {computer_gesture}",
                        (15, 101), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (100, 200, 255), 2)
            cv2.putText(frame, f"Result: {result_text}",
                        (15, 134), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255, 220, 100), 2)

            score_text = f"You: {player_score}   Computer: {computer_score}   Ties: {ties}"
            cv2.putText(frame, score_text, (15, frame.shape[0] - 48),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255, 255, 255), 2)
            cv2.putText(frame, "Fist=Rock | Open palm=Paper | Two fingers=Scissors | Q=Quit",
                        (15, frame.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                        0.48, (230, 230, 230), 1)

            cv2.imshow("Rock Paper Scissors - Hand Gesture Game", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()
    print("\nFinal Score")
    print(f"You: {player_score} | Computer: {computer_score} | Ties: {ties}")


if __name__ == "__main__":
    main()
