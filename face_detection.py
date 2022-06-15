import cv2
import time
from serial import Serial

# import model
face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

def get_hit_point(rectangle):
    x, y, w, h = rectangle
    x2 = x + w
    y2 = y + h
    # get center of rectangle
    mid_point = [(x + x2) / 2, (y + y2) / 2]
    # higher it by 20% and return
    return int(mid_point[0]), int(mid_point[1] - 2 * h // 10)

def get_max_rect(faces):
    biggest_face = (0, 0, 0, 0)
    for (x, y, w, h) in faces:
        if w + h > biggest_face[2] + biggest_face[3]:
            biggest_face = (x, y, w, h)
    return biggest_face

def apply_detection(cap):

    arduino = Serial('COM3', 9600)
    time.sleep(2)
    print("Connection to arduino...")

    while True:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Get faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw the rectangle around the biggest face in the frame
        (x, y, w, h) = get_max_rect(faces)
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        if x and y:
            hit_point = get_hit_point((x, y, w, h))
            cv2.circle(img, hit_point, 1, (0, 0, 255), 3)
            try:
                data = "X{0:d}Y{1:d}Z".format((hit_point[0]+50), (hit_point[1]))
                print ("output = '" +data+ "'")
                arduino.write(str.encode(data))
            except:
                print("Err")
                arduino.close()
                break
        
        # Display
        cv2.imshow('img', img)
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    # Release the VideoCapture object
    cap.release()
    arduino.close() 