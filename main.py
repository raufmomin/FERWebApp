from flask import Flask, render_template, Response
from camera import Camera

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    response = Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src https://static.ads-twitter.com https://www.google-analytics.com 'sha256-q2sY7jlDS4SrxBg6oq/NBYk9XVSwDsterXWpH99SAn0='; img-src 'self' https://s3.amazonaws.com https://twitter.com https://pbs.twimg.com; font-src 'self' https://fonts.gstatic.com; style-src 'self' https://fonts.googleapis.com; frame-ancestors 'none';"
    response.headers["Referrer-Policy"] = "no-referrer, strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    return response


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
