import cv2

cap = cv2.VideoCapture(0)  # 0 é a webcam padrão

if not cap.isOpened():
    raise RuntimeError("Não foi possível acessar a webcam.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Webcam Test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
