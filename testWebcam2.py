import cv2
import requests
import json

video_capture = cv2.VideoCapture(0)
process_this_frame = True

imageResult = {}
imageResult['faceList'] = []

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    frameSmall = small_frame[:, :, ::-1]


    # Only process every other frame of video to save time
    if process_this_frame:
        #save image

        filePath = 'C:\\DataSets\\SCUTFBP5500\\image\\temp.jpg'
        cv2.imwrite(filePath, frameSmall)
        url = 'http://127.0.0.1:5000/facerate/1.0/imageresultforimagefile'
        files = {'imageFile': open(filePath, 'rb')}
        response = requests.post(url, files=files)

        # Find all the faces and face encodings in the current frame of video
        imageResult = json.loads(response.content)

    process_this_frame = not process_this_frame


    # Display the results
    for faceResult in imageResult['faceList']:
        (top, right, bottom, left) = faceResult['location']
        name = 'rating : ' + str(int(faceResult['rating'] * 20) / 2)
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
