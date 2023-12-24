import socket
import struct
import cv2
import numpy as np

cascPath = r"C:\Users\nguye\AppData\Roaming\Python\Python311\site-packages\cv2\data\haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

frame_count = 0
stream = bytearray()

# Initial values
degree_x = 90
degree_y = 140
distance_x = 0
distance_y = 0
center_y = 0
center_x = 0

print('Connecting to server...')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('192.168.137.172', 2222))

    print('Receiving data ')
    while True:
        data = sock.recv(4096)
        if not data:
            break
        stream += data

        a = stream.find(b'\xff\xd8')
        b = stream.find(b'\xff\xd9', a)

        if a != -1 and b != -1:
            jpg = stream[a:b + 2]
            stream = stream[b + 2:]
            buffer = np.frombuffer(jpg, dtype=np.uint8)
            frame = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
            
            frame = cv2.flip(frame, cv2.ROTATE_180)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=10,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Sort faces by size in descending order
            faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)

            # Draw a rectangle around all detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)

            # If at least one face is detected
            if len(faces) > 0:
                # Get the largest face
                (x, y, w, h) = faces[0]
                center_x = x + w // 2
                center_y = y + h // 2

                # Draw a point at the center and display its coordinates on the image
                cv2.circle(frame, (center_x, center_y), radius=5, color=(0, 0, 255), thickness=-1)
                cv2.putText(frame, f'({center_x}, {center_y})', (center_x - 50, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            height, width = frame.shape[:2]
            center_frame_x = width // 2
            center_frame_y = height // 2
            cv2.circle(frame, (center_frame_x, center_frame_y), radius=5, color=(0, 255, 0), thickness=-1)
            cv2.putText(frame, f'({center_frame_x}, {center_frame_y})', (center_frame_x - 50, center_frame_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Draw a line connecting the center of the frame and the center of the nearest face and display the distance between them
            if len(faces) > 0:
                distance_x = center_x - center_frame_x
                distance_y = center_y - center_frame_y
                if abs(distance_x) > 160 or abs(distance_y) > 120: 
                    # Calculate degrees
                    degree_x = degree_x + ((-distance_x) / 16)
                    degree_y = degree_y + ((-distance_y) / 16)

                    # Ensure degrees are within 0-180 range
                    degree_x = max(0, min(180, degree_x))
                    degree_y = max(0, min(180, degree_y))
                cv2.line(frame,(center_frame_x ,center_frame_y),(center_x ,center_y),(255 ,0 ,0),5)
                cv2.putText(frame,f'Distance x: {distance_x}, Distance y: {distance_y}',(width -580 ,height -20),cv2.FONT_HERSHEY_SIMPLEX ,1 ,(0 ,0 ,255) ,1)

            cv2.imshow('Video', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            if key == ord('r'):
                degree_x = 90
                degree_y = 140
            frame_count += 1
            
            # Send data to server

            print(center_x, center_y, degree_x, degree_y)
            data = struct.pack('iiff', int(center_x), int(center_y), degree_x, degree_y)
            sock.send(data)

print('\nFrames received ', frame_count)
