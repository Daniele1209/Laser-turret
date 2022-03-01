from face_detection import *

if __name__ == '__main__':

    # To capture video from webcam.
    camera_port = 0
    camera = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)
    # To use a video file as input
    # cap = cv2.VideoCapture('filename.mp4')

    apply_detection(camera)
    cv2.destroyAllWindows()
