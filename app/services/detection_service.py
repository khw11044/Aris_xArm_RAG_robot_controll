import cv2
import time
from ultralytics import YOLO
from utils.CupPosition import set_cup_position

model_path = './utils/CupDetectModel/best.pt'
boxes = [
    (510, 0, 630, 100),  # 첫 번째 박스
    (370, 0, 490, 100),  # 두 번째 박스
    (230, 0, 340, 100)   # 세 번째 박스
]

class CupDetection:
    def __init__(self, model_path=model_path, boxes=boxes):
        self.model = YOLO(model_path)
        self.boxes = boxes
        self.detection_times = [None, None, None]

    def detect_position(self, frame):
        # Perform inference with YOLO model
        results = self.model(frame, verbose=False)
        current_time = time.time()
        detected_in_boxes = [False, False, False]  # Track which boxes have cups in this frame

        # Draw the fixed boxes on the frame
        for i, (x1, y1, x2, y2) in enumerate(self.boxes):
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f"Box {i+1}", (x1+5, y1+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Check if any objects are detected in the boxes with confidence >= 0.80
        if results[0].boxes:
            for box in results[0].boxes:
                if box.conf[0] >= 0.80 and box.cls[0] == 0:  # Process only "cup" detections
                    box_x1, box_y1, box_x2, box_y2 = box.xyxy[0]
                    
                    # Draw bounding box for the detected cup
                    cv2.rectangle(frame, (int(box_x1), int(box_y1)), (int(box_x2), int(box_y2)), (0, 255, 0), 2)
                    cv2.putText(frame, f"{box.conf[0]:.2f}", (int(box_x1)+20, int(box_y1) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(frame, f"Cup", (int(box_x1)+25, int(box_y1) + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Check each predefined box for a detected cup
                    for i, (fixed_x1, fixed_y1, fixed_x2, fixed_y2) in enumerate(self.boxes):
                        if (fixed_x1 < box_x1 < fixed_x2 and fixed_y1 < box_y1 < fixed_y2) or \
                           (fixed_x1 < box_x2 < fixed_x2 and fixed_y1 < box_y1 < fixed_y2) or \
                           (fixed_x1 < box_x1 < fixed_x2 and fixed_y1 < box_y2 < fixed_y2) or \
                           (fixed_x1 < box_x2 < fixed_x2 and fixed_y1 < box_y2 < fixed_y2):
                            detected_in_boxes[i] = True
                            # Start the timer if it isn't already running
                            if self.detection_times[i] is None:
                                self.detection_times[i] = current_time
                            # Check if the cup has stayed in the box for at least 3 seconds
                            elif current_time - self.detection_times[i] >= 0.01:
                                self.reset_detection_state()
                                set_cup_position(i + 1)
                                return i + 1, frame  # Return the position (1, 2, or 3) and the annotated frame
                        else:
                            # Reset the timer if the cup is no longer in the box
                            self.detection_times[i] = None

        return None, frame  # No cup detected in a box for 3 seconds, return None

    def reset_detection_state(self):
        self.detection_times = [None, None, None]

    def show_frame(self, frame):
        # Display the webcam feed for debugging purposes
        cv2.imshow("Webcam Feed", frame)

    def wait_for_key(self):
        # Wait for a keypress
        return cv2.waitKey(1) & 0xFF