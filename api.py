from flask import Flask
from flask import request
from queue import Queue
from event import (Event, EventAdjustment, EventEyeDirection,
                   EventSynchronise, EventChangeEyeType, EventSave, EventBlink, EventEnableBlink)
from typing import Optional
PORT = 18000

app = Flask(__name__, static_folder='.', static_url_path='')
events: Queue[Event] = Queue()


@app.route('/')
def index():
    return "hello"


@app.route('/adjustment', methods=['POST'])
def post_adjustment():
    payload = request.json
    left = payload.get("left", {})
    right = payload.get("right", {})

    param: Optional[EventAdjustment.Param] = [None, None]

    for i, e in enumerate([left, right]):
        change_x = e.get("change_x", 0.0)
        change_y = e.get("change_y", 0.0)
        change_scale_width = e.get("change_scale_width", 0.0)
        change_scale_height = e.get("change_scale_height", 0.0)
        change_angle = e.get("change_angle", 0.0)
        param[i] = EventAdjustment.Param(change_x, change_y,
                                         change_scale_width, change_scale_height, change_angle)

    events.put(EventAdjustment(*param))
    response = "Success."
    return response, 202


@app.route('/eye_direction', methods=['POST'])
def post_eye_direction():
    payload = request.json
    left = payload.get("left", {})
    right = payload.get("right", {})
    param: Optional[EventEyeDirection.Param] = [None, None]
    for i, e in enumerate([left, right]):
        x = e.get("x", 0.0)
        y = e.get("y", 0.0)
        param[i] = EventEyeDirection.Param(x, y)
    events.put(EventEyeDirection(*param))
    response = "Success."
    return response, 202


@app.route('/change_eye_type', methods=['POST'])
def post_change_eye_type():
    payload = request.json
    id = payload.get("id", "")

    events.put(EventChangeEyeType(id))
    response = "Success."
    return response, 202


@app.route('/synchronise', methods=['POST'])
def post_synchronise():
    payload = request.json
    left = payload.get("left", {})
    right = payload.get("right", {})
    enable_save = payload.get("enable_save", False)

    param: Optional[EventSynchronise.Param] = [None, None]
    for i, e in enumerate([left, right]):
        file_path = e.get("file_path", 0.0)
        origin_x = e.get("origin_x", 0.0)
        origin_y = e.get("origin_y", 0.0)
        scale_width = e.get("scale_width", 0.0)
        scale_height = e.get("scale_height", 0.0)
        angle = e.get("angle", 0.0)
        param[i] = EventSynchronise.Param(file_path,
                                          origin_x,
                                          origin_y,
                                          scale_width,
                                          scale_height,
                                          angle)

    events.put(EventSynchronise(*param, enable_save))
    response = "Success."
    return response, 202


@app.route('/upload', methods=['POST'])
def post_upload():
    payload = request.json
    left = payload.get("left", {})
    right = payload.get("right", {})
    enable_save = payload.get("enable_save", False)

    param: Optional[EventSynchronise.Param] = [None, None]
    for i, e in enumerate([left, right]):
        file_path = e.get("file_path", 0.0)
        origin_x = e.get("origin_x", 0.0)
        origin_y = e.get("origin_y", 0.0)
        scale_width = e.get("scale_width", 0.0)
        scale_height = e.get("scale_height", 0.0)
        angle = e.get("angle", 0.0)
        param[i] = EventSynchronise.Param(file_path,
                                          origin_x,
                                          origin_y,
                                          scale_width,
                                          scale_height,
                                          angle)

    events.put(EventSynchronise(*param, enable_save))
    response = "Success."
    return response, 202


@app.route('/save', methods=['POST'])
def post_save():
    payload = request.json
    events.put(EventSave())
    response = "Success."
    return response, 202


@app.route('/blink', methods=['POST'])
def post_blink():
    payload = request.json
    events.put(EventBlink())
    response = "Success."
    return response, 202


@app.route('/enable_blink', methods=['POST'])
def post_enable_blink():
    payload = request.json
    events.put(EventEnableBlink(payload.get("enable", True)))
    response = "Success."
    return response, 202


def run():
    app.run(port=PORT, host="0.0.0.0", debug=False)


if __name__ == "__main__":
    app.run(port=PORT, debug=False)
