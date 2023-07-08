from ultralytics import YOLO
import cv2
import cvzone
import math

import active_area


def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 720)
    cap.set(4, 480)

    # cap = cv2.VideoCapture("../Videos/motorcycle.mp4")  # For Video
    model = YOLO("../Yolo-Weights/yolov8l.pt")
    model.to('cuda')
    names = model.names
    print(names)
    print(model.device)
    while True:
        success, img = cap.read()
        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h))

                # Confidence
                conf = math.ceil(box.conf[0] * 100) / 100
                # Class Name
                cls = int(box.cls[0])

                cvzone.putTextRect(img, f'{names[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    main()

cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 480)

model = YOLO("../Yolo-Weights/yolov8l.pt")
model.to('cuda')
names = model.names
print(model.device)


def get_new_frame():
    # cap = cv2.VideoCapture("../Videos/motorcycle.mp4")  # For Video

    success, img = cap.read()
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        active_area.objectBoxCenterList.clear()
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))

            centralX = (x1 + x2) / 2
            centralY = (y1 + y2) / 2
            centralPoint = (centralX, centralY)
            active_area.objectBoxCenterList.append(centralPoint)
            cv2.circle(img, (int(centralX), int(centralY)), 2, (0, 255, 0), 5)

            # Confidence
            conf = math.ceil(box.conf[0] * 100) / 100
            # Class Name
            cls = int(box.cls[0])

            cvzone.putTextRect(img, f'{names[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

    img = active_area.draw_selectedArea_box(img)
    return success, img
