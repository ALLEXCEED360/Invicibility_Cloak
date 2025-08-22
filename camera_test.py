# Quick camera test
import cv2
cap = cv2.VideoCapture(0)  # Try 0, 1, 2 if 0 doesn't work
ret, frame = cap.read()
if ret:
    print("✅ Camera working!")
    cv2.imshow('Test', frame)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
else:
    print("❌ Camera not working, try different index")
cap.release()