from flask import Flask, request, jsonify, render_template
import threading
import time
import random
import os

app = Flask(__name__)
video_folder = "static"
video_files = [os.path.join(video_folder, filename) for filename in os.listdir(video_folder) if filename.endswith(".mp4")]

MAX_CONCURRENT_REQUESTS = 5

current_requests = 0
mutex = threading.Lock()

@app.route('/healthcheck')
def health():
    return {"msg": "healthy"}


@app.route('/web')
def st():
    random_video_filename = random.choice(video_files)
    print(random_video_filename)
    random_video_filename = random_video_filename.replace("static\\", "")
    return render_template('video.html', video_url=random_video_filename)

@app.route('/process')
def index():
    global current_requests

    with mutex:
        current_requests += 1

    if current_requests <= MAX_CONCURRENT_REQUESTS:
        processing_time = random.randint(5, 15)
        time.sleep(processing_time)
        
        with mutex:
            current_requests -= 1
        return jsonify({'message': 'Request processed in {} seconds'.format(processing_time)})

    else:
        with mutex:
            current_requests -= 1
        return jsonify({'message': 'errrrrrr'}), 503

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
