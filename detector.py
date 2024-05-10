import cv2
import threading
from ultralytics import YOLO

import time

MODEL_PATH = "./resource/yolov8n.pt"
ENABLE_DEBUG_PRINT = True


class Detector:
    def __init__(self, device_id=0) -> None:
        self.model = YOLO(MODEL_PATH)
        self.capture = cv2.VideoCapture(device_id)
        self.t = threading.Thread(target=self.run)

        self.detect: bool = False
        self.x: int = 0
        self.y: int = 0
        self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.wait_time_seconds = 0.5

    def is_detect(self):
        return self.detect

    def primary_target(self):
        return self.x, self.y

    def start(self):
        self.t.start()

    def stop(self):
        self.t.do_run = False
        self.t.join()

    def run(self):
        while True:
            ret, frame = self.capture.read()
            results = self.model.track(frame, persist=True)

            if len(results[0].boxes.data):
                sx, sy, ex, ey, t, _ = results[0].boxes.data[0][0:6]
                self.x = int((sx + ex) / 2)
                self.y = int((sy + ey) / 2)
                self.detect = True
            else:
                self.x = 0
                self.y = 0
                self.detect = False
            if ENABLE_DEBUG_PRINT:
                self.debug_print(results)

            if not getattr(self.t, "do_run", True):
                break

            time.sleep(self.wait_time_seconds)

    def debug_print(self, results: list):
        annotated_frame = results[0].plot()
        cv2.imshow("frame", annotated_frame)
        cv2.waitKey(1)

    def __del__(self):
        self.capture.release()
        self.t.do_run = False


if __name__ == "__main__":
    model = YOLO(MODEL_PATH)
    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        results = model.track(frame, persist=True)
        annotated_frame = results[0].plot()
        # Display the annotated frame
        if len(results[0].boxes.data):
            sx, sy, ex, ey, t, _ = results[0].boxes.data[0][0:6]
            sx = int((sx + ex) / 2)
            sy = int((sy + ey) / 2)
            cv2.rectangle(
                annotated_frame,
                (sx, sy),
                (sx + 1, sy + 1),
                (255, 0, 0),
                cv2.FILLED,
                cv2.LINE_AA,
            )
        cv2.imshow("frame", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    capture.release()
    cv2.destroyAllWindows()
