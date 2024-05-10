import argparse
import requests
import json

DEFAULT_PORT = 18000
DEFAULT_HOST = "localhost"

def command_enable_blink(args):
    url = aquire_url(args)
    response = requests.post(f"{url}/enable_blink", data=json.dumps({"enable": args.disable}),
                             headers={"Content-Type": "application/json"})
    print(response)


def command_blink(args):
    url = aquire_url(args)
    response = requests.post(f"{url}/blink", data=json.dumps({}),
                             headers={"Content-Type": "application/json"})
    print(response)


def command_change_eye_type(args):
    url = aquire_url(args)
    response = requests.post(f"{url}/change_eye_type", data=json.dumps({"id": args.id}),
                             headers={"Content-Type": "application/json"})
    print(response)


def command_eye_direction(args):
    url = aquire_url(args)
    data = {"left": {"x": args.left_x, "y": args.left_y},
            "right": {"x": args.right_x, "y": args.right_y}}
    response = requests.post(f"{url}/eye_direction", data=json.dumps(data),
                             headers={"Content-Type": "application/json"})
    print(response)


def command_adjustment(args):
    url = aquire_url(args)
    data = {"left": {"change_x": args.left_x,
                     "change_y": args.left_y,
                     "change_scale_width": args.left_scale_width,
                     "change_scale_height": args.left_scale_height,
                     "change_angle": args.left_angle},
            "right": {"change_x": args.right_x,
                      "change_y": args.right_y,
                      "change_scale_width": args.right_scale_width,
                      "change_scale_height": args.right_scale_height,
                      "change_angle": args.right_angle}}
    response = requests.post(f"{url}/adjustment", data=json.dumps(data),
                             headers={"Content-Type": "application/json"})
    print(response)


def aquire_url(args):
    return f"http://{args.host}:{args.port}"


def add_default_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-H", '--host', default=DEFAULT_HOST, type=str)
    parser.add_argument("-P", '--port', default=DEFAULT_PORT, type=int)


parser = argparse.ArgumentParser(description='LCD Eyes CLI')
subparsers = parser.add_subparsers()

parser_enable_blink = subparsers.add_parser('enable_blink')
parser_enable_blink.add_argument("-d", '--disable', action='store_false')
parser_enable_blink.set_defaults(handler=command_enable_blink)
add_default_parser(parser_enable_blink)

parser_blink = subparsers.add_parser('blink')
parser_blink.set_defaults(handler=command_blink)
add_default_parser(parser_blink)

parser_enable_blink = subparsers.add_parser('change_eye_type')
parser_enable_blink.add_argument("-i", '--id', type=str)
parser_enable_blink.set_defaults(handler=command_change_eye_type)
add_default_parser(parser_enable_blink)

parser_eye_direction = subparsers.add_parser('eye_direction')
parser_eye_direction.add_argument("-lx", '--left_x', default=0.0, type=float)
parser_eye_direction.add_argument("-ly", '--left_y', default=0.0, type=float)
parser_eye_direction.add_argument("-rx", '--right_x', default=0.0, type=float)
parser_eye_direction.add_argument("-ry", '--right_y', default=0.0, type=float)
parser_eye_direction.set_defaults(handler=command_eye_direction)
add_default_parser(parser_eye_direction)

parser_adjustment = subparsers.add_parser('adjustment')
parser_adjustment.add_argument("-lx", '--left_x', default=0.0, type=float)
parser_adjustment.add_argument("-ly", '--left_y', default=0.0, type=float)
parser_adjustment.add_argument(
    "-lsw", '--left_scale_width', default=0.0, type=float)
parser_adjustment.add_argument(
    "-lsh", '--left_scale_height', default=0.0, type=float)
parser_adjustment.add_argument("-la", '--left_angle', default=0.0, type=float)
parser_adjustment.add_argument("-rx", '--right_x', default=0.0, type=float)
parser_adjustment.add_argument("-ry", '--right_y', default=0.0, type=float)
parser_adjustment.add_argument(
    "-rsw", '--right_scale_width', default=0.0, type=float)
parser_adjustment.add_argument(
    "-rsh", '--right_scale_height', default=0.0, type=float)
parser_adjustment.add_argument("-ra", '--right_angle', default=0.0, type=float)
parser_adjustment.set_defaults(handler=command_eye_direction)
add_default_parser(parser_adjustment)


args = parser.parse_args()
if hasattr(args, 'handler'):
    args.handler(args)
else:
    parser.print_help()
