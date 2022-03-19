import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret:
        continue

    cv2.imshow('img', img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

