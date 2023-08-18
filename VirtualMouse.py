from HandTrackingBase import HandTracker
import cv2
import time
import pyautogui
import math

def main():
    width, height = 640, 480
    screen_width, screen_height = pyautogui.size()
    tracker = HandTracker(1)
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    pTime = 0
    min_distance = 0.06

    # Define the restricting window boundaries
    restrict_top = int(height * 0.3)  # 20% from top
    restrict_bottom = int(height * 0.7)  # 80% from bottom
    restrict_left = int(width * 0.3)  # 20% from left
    restrict_right = int(width * 0.7)  # 80% from right
    
    dragging = False
    drag_start_position = None

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        if not ret:
            break

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)

        tracked_frame, landmarks_list, detected = tracker.track_hands(frame)

        fingers_up = tracker.check_fingers_up(landmarks_list)
        if fingers_up[1] and fingers_up[2] and not any(fingers_up[3:]):
            hand_landmarks = landmarks_list[0]
            index_tip_x = hand_landmarks[8]['x']
            index_tip_y = hand_landmarks[8]['y']
            middle_tip_x = hand_landmarks[12]['x']
            middle_tip_y = hand_landmarks[12]['y']

            distance = math.sqrt((index_tip_x - middle_tip_x)**2 + (index_tip_y - middle_tip_y)**2)
            if distance < min_distance:
                cursor_x = index_tip_x * width
                cursor_y = index_tip_y * height

                if restrict_left < cursor_x < restrict_right and restrict_top < cursor_y < restrict_bottom:
                    relative_x = (cursor_x - restrict_left) / (restrict_right - restrict_left)
                    relative_y = (cursor_y - restrict_top) / (restrict_bottom - restrict_top)
                    target_x = int(relative_x * screen_width)
                    target_y = int(relative_y * screen_height)
                    pyautogui.moveTo(target_x, target_y)
        elif detected and fingers_up[0] and not any(fingers_up[1:]):
                pyautogui.mouseUp()
        elif detected and fingers_up[4] and not any(fingers_up[1:4]):
                pyautogui.mouseDown()
        elif not fingers_up[1] and fingers_up[2] and not any (fingers_up[3:]):
            pyautogui.click(button='left')
        elif fingers_up[1] and not fingers_up[2] and not any (fingers_up[3:]):
            pyautogui.click(button='right')
        elif fingers_up[1] and fingers_up[2] and fingers_up[3] and not any (fingers_up[4:]):  
            pyautogui.click(clicks=2, interval=0.2)
            time.sleep(0.1)

        # Draw the restricting window on the frame
        cv2.rectangle(tracked_frame, (restrict_left, restrict_top), (restrict_right, restrict_bottom), (0, 255, 0), 2)

        cv2.imshow("Tracked Hands", tracked_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    tracker.close()

if __name__ == "__main__":
    main()
