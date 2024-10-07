import cv2
import dlib
import numpy as np
from imutils import face_utils

# Load the face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 3D model points
model_points = np.array([
    (0.0, 0.0, 0.0),             # Nose tip
    (0.0, -330.0, -65.0),        # Chin
    (-225.0, 170.0, -135.0),     # Left eye left corner
    (225.0, 170.0, -135.0),      # Right eye right corner
    (-150.0, -150.0, -125.0),    # Left mouth corner
    (150.0, -150.0, -125.0)      # Right mouth corner
], dtype="double")

# Camera internals
size = (640, 480)  # Example size, change to your actual video feed size
focal_length = size[1]
center = (size[1] // 2, size[0] // 2)
camera_matrix = np.array([
    [focal_length, 0, center[0]],
    [0, focal_length, center[1]],
    [0, 0, 1]
], dtype="double")

# Distortion coefficients (assuming no lens distortion)
dist_coeffs = np.zeros((4, 1))

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        image_points = np.array([
            shape[30],     # Nose tip
            shape[8],      # Chin
            shape[36],     # Left eye left corner
            shape[45],     # Right eye right corner
            shape[48],     # Left mouth corner
            shape[54]      # Right mouth corner
        ], dtype="double")

        success, rotation_vector, translation_vector = cv2.solvePnP(
            model_points, image_points, camera_matrix, dist_coeffs)

        (nose_end_point2D, jacobian) = cv2.projectPoints(
            np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

        p1 = (int(image_points[0][0]), int(image_points[0][1]))
        p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

        cv2.line(frame, p1, p2, (0, 255, 255), 2)

        # Calculate the Euler angles
        rmat, _ = cv2.Rodrigues(rotation_vector)
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

        angle_threshold = 15  # Degrees threshold to detect significant head movement
        danger_threshold = 40 # Degrees threshold to detect danger head movement
        if angles[1] < -danger_threshold:
            text = "Danger! Turned Left"
            color = (0, 0, 255)  # Red color for danger
        elif angles[1] > danger_threshold:
            text = "Danger! Turned Right"
            color = (0, 0, 255)  # Red color for danger
        elif angles[1] < -angle_threshold:
            text = "Looking Left"
            color = (0, 255, 0)  # Green color for safe
        elif angles[1] > angle_threshold:
            text = "Looking Right"
            color = (0, 255, 0)  # Green color for safe
        elif angles[0] < -angle_threshold:
            text = "Looking Down"
            color = (0, 255, 0)  # Green color for safe
        elif angles[0] > angle_threshold:
            text = "Looking Up"
            color = (0, 255, 0)  # Green color for safe
        else:
            text = "Looking Forward"
            color = (0, 255, 0)  # Green color for safe

        cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Head Pose Estimation", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
