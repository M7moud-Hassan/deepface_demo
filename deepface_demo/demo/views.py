from django.shortcuts import render
from django.http import StreamingHttpResponse
# Create your views here.
import cv2
from django.http import HttpResponse
from django.views.decorators import gzip
from django.views.decorators.http import require_GET
from deepface import DeepFace



@gzip.gzip_page
@require_GET
def video_feed(request):
    # Open the camera
    camera = cv2.VideoCapture(0)

    # Define the video codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    def generate():
        while True:
            # Read a frame from the camera
            ret, frame = camera.read()

            if not ret:
                break

            # Write the frame to the video file
            out.write(frame)


            # result = DeepFace.analyze(frame, actions=['emotion', 'age','detection'], enforce_detection=False)

            ret, jpeg = cv2.imencode('.jpg', frame)

            # Convert the JPEG data to bytes
            data = jpeg.tobytes()

            # Yield the frame as an HTTP response
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n')

    # Return the streaming response
    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')


def webcam_view(request):
    return HttpResponse(
        """<html>
        <head>
            <title>Webcam Stream</title>
        </head>
        <body>
            <h1>Webcam Stream</h1>
            <img src="/video_feed/" />
        </body>
        </html>"""
    )