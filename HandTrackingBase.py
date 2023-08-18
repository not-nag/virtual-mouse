import cv2
import mediapipe as mp
import pyautogui

class HandTracker:
    
    def __init__(self, maxHands):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands = maxHands)
        self.mp_drawing = mp.solutions.drawing_utils
        self.detected = False
        pyautogui.FAILSAFE = False


    def track_hands(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(frame_rgb)

        landmarks_list = []

        if results.multi_hand_landmarks:
            detected = True
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = [{"id": idx, "x": landmark.x, "y": landmark.y} for idx, landmark in enumerate(hand_landmarks.landmark)]
                landmarks_list.append(landmarks)
                #Bounding box
                # x_min = int(min(landmark['x'] for landmark in landmarks))
                # y_min = int(min(landmark['y'] for landmark in landmarks))
                # x_max = int(max(landmark['x'] for landmark in landmarks))
                # y_max = int(max(landmark['y'] for landmark in landmarks))
                # cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        else:
            detected = False
        return frame, landmarks_list, detected

    def check_fingers_up(self, landmarks_list):
        fingers_up = [False] * 5  # Initialize all fingers as not up
        if landmarks_list:
            hand_landmarks = landmarks_list[0]  # Assuming we're tracking one hand
            finger_tip_ids = [4, 8, 12, 16, 20]  # IDs of the fingertips in the landmarks list

            for finger_id in range(5):
                tip_id = finger_tip_ids[finger_id]
                if hand_landmarks[tip_id]['y'] < hand_landmarks[tip_id - 2]['y']:
                    fingers_up[finger_id] = True

        return fingers_up

    def close(self):
        self.hands.close()