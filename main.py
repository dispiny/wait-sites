from flask import Flask, request, jsonify
import threading
import time
import random

app = Flask(__name__)

# 최대 동시 요청 수
MAX_CONCURRENT_REQUESTS = 5

# 현재 처리 중인 요청 수를 추적하기 위한 변수
current_requests = 0

# 뮤텍스를 사용하여 현재 요청 수를 동기화
mutex = threading.Lock()

@app.route('/healthcheck')
def health():
    return {"msg": "healthy"}

@app.route('/web')
def st():
    return {"ss": "ㅅㄷㄴㅅ"}

@app.route('/process')
def index():
    global current_requests

    # 요청이 들어올 때마다 현재 요청 수를 증가시킴
    with mutex:
        current_requests += 1

    if current_requests <= MAX_CONCURRENT_REQUESTS:
        # 최대 동시 요청 수를 초과하지 않으면 처리
        # 5~15초 동안 대기
        processing_time = random.randint(5, 15)
        time.sleep(processing_time)
        
        with mutex:
            current_requests -= 1
        return jsonify({'message': 'Request processed in {} seconds'.format(processing_time)})

    else:
        # 최대 동시 요청 수를 초과한 경우 503 오류 반환
        with mutex:
            current_requests -= 1
        return jsonify({'message': 'errrrrrr'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
