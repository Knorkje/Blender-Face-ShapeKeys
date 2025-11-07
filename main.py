import cv2
import mediapipe as mp
import time
import os

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
# File setup
output_filename = "face_mesh_coordinates.txt"

# Parameters for logging
fps = 24  # Frames per second
duration = 20  # Duration in seconds
frames_to_record = fps * duration
recording = False  # Start recording flag

# Start video capture
cap = cv2.VideoCapture(1)

frame_count = 0
start_time = None

while cap.isOpened():
    ret, frame = cap.read()
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    org = (30, 30)

    # fontScale
    fontScale = 1

    # Blue color in BGR
    color = (255, 255, 255)

    # Line thickness of 2 px
    thickness = 2
    frame = cv2.putText(frame, 'Press s to start recording frames. Press q to quit', org, font,
                        fontScale, color, thickness, cv2.LINE_AA)
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and get the face landmarks
    results = face_mesh.process(rgb_frame)
    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            for id, lm in enumerate(landmarks.landmark):
                # Convert normalized coordinates to pixel coordinates
                h, w, _ = frame.shape
                x, y = int(lm.x * w), int(lm.y * h)

                # Draw a small circle at each vertex
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

                # Display the vertex ID and its coordinates
                cv2.putText(frame, f'{id}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
    # Display the camera feed
    cv2.imshow('Face Mesh Logging', frame)

    # Start logging when 's' is pressed
    key = cv2.waitKey(1)
    if key & 0xFF == ord('s') and not recording:
        recording = True
        frame_count = 0
        start_time = time.time()

        # Ensure the file is created new
        if os.path.exists(output_filename):
            os.remove(output_filename)

        print(f"Recording started: Writing to {output_filename}")

    if recording and results.multi_face_landmarks:
        # Write coordinates to the file
        with open(output_filename, "a") as file:
            landmarks = results.multi_face_landmarks[0]  # Assume only 1 face is detected
            file.write(f"Frame: {frame_count + 1}\n")
            for id, lm in enumerate(landmarks.landmark):
                file.write(f"Vertex: {id}, x: {lm.x:.6f}, y: {lm.y:.6f}, z: {lm.z:.6f}\n")
        time.sleep(1/fps)
        frame_count += 1

        # Stop recording after the set duration
        if frame_count >= frames_to_record:
            recording = False
            print(f"Recording finished. Data written to {output_filename}")

    # Stop recording if time exceeds
    if recording and (time.time() - start_time) > duration:
        print(f"Recording interrupted after {frame_count} frames.")
        recording = False

    # Exit the program on pressing 'q'
    if key & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()