import requests
import json

PORT = 18000
URL = f"http://localhost:{PORT}"
#URL = f"http://192.168.11.9:{PORT}"


if __name__ == "__main__":
    response = requests.get(URL)
    print(response)
    response = requests.post(f"{URL}/adjustment", data=json.dumps({"left": {"change_x": 10}, "right": {}}),
                             headers={"Content-Type": "application/json"})
    print(response)
    response = requests.post(f"{URL}/eye_direction", data=json.dumps({"left": {"x": 10}, "right": {}}),
                             headers={"Content-Type": "application/json"})
    print(response)

    data = {
        "right": {
            "file_path": "./resource/tsugu_left_grgr.png",
            "origin_x": 234.0,
            "origin_y": 249.0,
            "scale_width": 1.03,
            "scale_height": 1,
            "angle": 360
        },
        "left": {
            "file_path": "./resource/tsugu_right_grgr.png",
            "origin_x": 213.0,
            "origin_y": 245.0,
            "scale_width": 1.06,
            "scale_height": 1,
            "angle": 368
        }
    }
    response = requests.post(f"{URL}/synchronise", data=json.dumps(data),
                             headers={"Content-Type": "application/json"})
    print(response)

    response = requests.post(f"{URL}/change_eye_type", data=json.dumps({"id": "default"}),
                             headers={"Content-Type": "application/json"})
    print(response)

    response = requests.post(f"{URL}/blink", data=json.dumps({}),
                             headers={"Content-Type": "application/json"})
    print(response)
