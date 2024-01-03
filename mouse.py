import cv2
import mediapipe as mp
import pyautogui
import os
import time

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# Virtual Mouse movement function
def move_virtual_mouse(x, y):
    screen_width, screen_height = pyautogui.size()
    mapped_x = int(x * screen_width)
    mapped_y = int(y * screen_height)
    pyautogui.moveTo(mapped_x, mapped_y)

# Single click function  (Index finger)
def single_click(index_finger_tip, thumb_tip):
    distance_index_thumb = ((thumb_tip.x - index_finger_tip.x)**2 + (thumb_tip.y - index_finger_tip.y)**2)**0.5
    if distance_index_thumb < 0.03:  
        pyautogui.click()

# Double click function (Middle finger)
def double_click(middle_finger_tip, thumb_tip):
    distance_middle_thumb = ((thumb_tip.x - middle_finger_tip.x)**2 + (thumb_tip.y - middle_finger_tip.y)**2)**0.5
    if distance_middle_thumb < 0.03:  
        pyautogui.click(clicks=2)

# Screenshot function (Ring finger)
def capture_screenshot(ring_finger_tip, thumb_tip):
    distance_ring_thumb = ((thumb_tip.x - ring_finger_tip.x)**2 + (thumb_tip.y - ring_finger_tip.y)**2)**0.5
    if distance_ring_thumb < 0.03:  
        # Capture a screenshot
        folder_path = "screenshots"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        screenshot_name = f"screenshot_{int(time.time())}.png"
        screenshot_path = os.path.join(folder_path, screenshot_name)
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)

# Calculator function (Pinky finger)
def open_calculator(pinky_finger_tip, thumb_tip):
    distance_pinky_thumb = ((thumb_tip.x - pinky_finger_tip.x)**2 + (thumb_tip.y - pinky_finger_tip.y)**2)**0.5
    if distance_pinky_thumb < 0.03:  
        os.system("calc")  # Command to open the calculator 

# Function to detect hand gestures and perform corresponding actions
def detect_hand_and_actions(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get hand landmarks for different fingers
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            
            # Move the virtual mouse based on the position of the index finger
            x, y = index_finger_tip.x, index_finger_tip.y
            move_virtual_mouse(x, y)
            
            # Perform actions based on gestures
            single_click(index_finger_tip, thumb_tip)
            double_click(middle_finger_tip, thumb_tip)
            capture_screenshot(ring_finger_tip, thumb_tip)
            open_calculator(pinky_finger_tip, thumb_tip)

# Open the camera and start processing frames
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Detect hand gestures and perform actions
    detect_hand_and_actions(frame)

    # Display the frame with hand landmarks
    cv2.imshow('AI Virtual Mouse', frame)

    # Exit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
