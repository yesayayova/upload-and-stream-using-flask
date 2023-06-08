from flask import Flask, render_template, request, Response
from werkzeug.utils import secure_filename
import cv2
import os

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/static/uploads'
application.config['MAX_CONTENT_PATH'] = 1000000

def gen_frames():  # generate frame by frame from camera
    camera = cv2.VideoCapture(filename)

    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']

        global filename
        filename = application.config['UPLOAD_FOLDER'] + '/' + secure_filename(f.filename)

        try:
            f.save(filename)
            return render_template('form.html', filename=secure_filename(f.filename), notif='Upload Success')
        except:
            return render_template('upload_gagal.html')
    return render_template('form.html')

@application.route('/stream', methods=['GET', 'POST'])
def stream():
    if request.method == 'POST':
        return render_template('streaming.html')
    return render_template('upload_gagal.html')

@application.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    application.run(debug=True)
