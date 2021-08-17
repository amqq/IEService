#! python
"""

 Date :		    Today is 2021-08-16
 Creator :		This script Created by amqq.ir
 Info :		    This script will be resize and edit images
 Requirement :	This script can be run on all os

 be happy :)
"""

# Project imports
import atexit
import io
import os
import socket
import traceback

from PIL import Image

from AmLogger import *
import urllib.parse as urlparse
from urllib.parse import parse_qs
from _thread import start_new_thread

# init default global mutable variables

PORT = 5001
OPTIMIZE_IMAGE = True
DEFAULT_RETURN_IMAGE_TO_INVALID_REQ_PATH = "blankpic.jpg"
DEFAULT_RESPONSE_IMAGE_QUALITY = 90
DEFAULT_RESPONSE_IMAGE_FORMAT = "webp"
DEFAULT_RESPONSE_IMAGE_HEIGHT = 200
DEFAULT_RESPONSE_IMAGE_WEIGHT = 300
ALL_IMAGE_PATH = ""
LOG_FILE = "ies.log"
SCRIPT_VERSION_NAME = "v1014"
SOCKET_LISTEN_NUMBER = 5
SOCKET_RECEIVED_BUFFER_SIZE = 2048

# init immutable variables
DEBUG_MODE = True
ACTION = "action"
WEIGHT = "weight"
HEIGHT = "height"
QUALITY = "quality"
FORMAT = "format"
IMAGE_PATH = "path"
ACCEPTED_RESPONSE_FORMAT = ['webp', 'jpeg', 'png']


def programExitHandler():
    log.Info("Program Exit")


def imageResizer(image_path, image_height, image_weight, image_format, image_quality):
    imgByteArr = io.BytesIO()
    quality = int(image_quality)
    image_org = Image.open(image_path)
    if image_format == "jpeg":
        image_org = image_org.convert('RGB')
    newsier = (int(image_weight), int(image_height))
    image_org = image_org.resize(newsier)
    image_org.save(imgByteArr, image_format, optimize=OPTIMIZE_IMAGE, quality=quality)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def getImageHeightByWeight(image_path, image_weight):
    with Image.open(image_path) as image:
        return int((float(image.size[1]) * float((image_weight / float(image.size[0])))))


def requestParser(request):
    row_get_request = request.decode().split("?")[1]
    row_get_request = row_get_request.split(" HTTP")[0]
    row_get_request = "?" + row_get_request
    request_parsed = urlparse.urlparse(row_get_request)
    request_params = {}

    try:
        request_params[ACTION] = parse_qs(request_parsed.query)['a'][0]
    except KeyError:
        try:
            request_params[ACTION] = parse_qs(request_parsed.query)["action"][0]
        except KeyError:
            return False

    try:
        request_params[QUALITY] = int(parse_qs(request_parsed.query)['q'][0])
    except KeyError:
        try:
            request_params[QUALITY] = int(parse_qs(request_parsed.query)["quality"][0])
        except KeyError:
            request_params[QUALITY] = DEFAULT_RESPONSE_IMAGE_QUALITY

    try:
        request_params[FORMAT] = parse_qs(request_parsed.query)['f'][0]
    except KeyError:
        try:
            request_params[FORMAT] = parse_qs(request_parsed.query)["format"][0]
        except KeyError:
            request_params[FORMAT] = DEFAULT_RESPONSE_IMAGE_FORMAT

    if request_params[FORMAT] not in ACCEPTED_RESPONSE_FORMAT:
        return False

    try:
        request_params[IMAGE_PATH] = ALL_IMAGE_PATH + parse_qs(request_parsed.query)['p'][0]
    except KeyError:
        try:
            request_params[IMAGE_PATH] = ALL_IMAGE_PATH + parse_qs(request_parsed.query)["path"][0]
        except KeyError:
            return False
    if not os.path.isfile(ALL_IMAGE_PATH + request_params[IMAGE_PATH]):
        return False

    if request_params[ACTION] == "resize" or request_params[ACTION] == "R" or request_params[ACTION] == "r":
        try:
            request_params[WEIGHT] = int(parse_qs(request_parsed.query)['w'][0])
        except KeyError:
            try:
                request_params[WEIGHT] = int(parse_qs(request_parsed.query)["weight"][0])
            except KeyError:
                return False

        try:
            request_params[HEIGHT] = int(parse_qs(request_parsed.query)['h'][0])
        except KeyError:
            try:
                request_params[HEIGHT] = int(parse_qs(request_parsed.query)["height"][0])
            except KeyError:
                try:
                    request_params[HEIGHT] = getImageHeightByWeight(request_params[IMAGE_PATH], request_params[WEIGHT])
                except:
                    return False
    else:
        return False

    return request_params


def isValidRequest(request):
    if "HTTP" in request.decode():
        if "?" in request.decode():
            if "&" in request.decode():
                if "=" in request.decode():
                    return True
    return False


def requestHandler(request):
    if isValidRequest(request):
        request_params = requestParser(request)
        if DEBUG_MODE:
            log.Info(f"Request Params => {request_params}")
        if not request_params:
            return imageResizer(DEFAULT_RETURN_IMAGE_TO_INVALID_REQ_PATH, DEFAULT_RESPONSE_IMAGE_HEIGHT,
                                DEFAULT_RESPONSE_IMAGE_WEIGHT, DEFAULT_RESPONSE_IMAGE_FORMAT,
                                DEFAULT_RESPONSE_IMAGE_QUALITY), DEFAULT_RESPONSE_IMAGE_FORMAT

        if request_params[ACTION] == "resize" or request_params[ACTION] == "R" or request_params[ACTION] == "r":
            return imageResizer(request_params[IMAGE_PATH], request_params[HEIGHT], request_params[WEIGHT],
                                request_params[FORMAT], request_params[QUALITY]), request_params[FORMAT]
    return imageResizer(DEFAULT_RETURN_IMAGE_TO_INVALID_REQ_PATH, DEFAULT_RESPONSE_IMAGE_HEIGHT,
                        DEFAULT_RESPONSE_IMAGE_WEIGHT, DEFAULT_RESPONSE_IMAGE_FORMAT,
                        DEFAULT_RESPONSE_IMAGE_QUALITY), DEFAULT_RESPONSE_IMAGE_FORMAT


def responseSender(data, response_format, connection=socket.socket()):
    content_type = "Content-Type: image/" + response_format
    HTTP_RESPONSE = b'\r\n'.join([
        b"HTTP/1.1 200 OK",
        b"Connection: close",
        content_type.encode(),
        bytes("Content-Length: %s" % len(data), 'utf-8'),
        b'', data
    ])
    connection.send(HTTP_RESPONSE)
    connection.close()


def connectionHandler(connection, _):
    ClientRequest = connection.recv(SOCKET_RECEIVED_BUFFER_SIZE)
    request_response, response_format = requestHandler(ClientRequest)
    responseSender(request_response, response_format, connection)


def mainSocketRequestHandler():
    global MainCDNSocket
    while True:
        client_connection, _ = MainCDNSocket.accept()
        if DEBUG_MODE:
            log.Info(f"new connection from => {_[0]}:{_[1]}")
        start_new_thread(connectionHandler, (client_connection, _))


def readDefaultVariablesFromUser():
    global PORT, DEFAULT_RETURN_IMAGE_TO_INVALID_REQ_PATH, DEFAULT_RESPONSE_IMAGE_QUALITY
    global DEFAULT_RESPONSE_IMAGE_WEIGHT, DEFAULT_RESPONSE_IMAGE_HEIGHT, DEFAULT_RESPONSE_IMAGE_FORMAT
    global OPTIMIZE_IMAGE, ALL_IMAGE_PATH
    if not DEBUG_MODE:
        try:
            log.ScriptSays("there are some small question for run this script")
            log.ScriptSays("please answer all of that carefully")
            log.ScriptSays("=====================================")
            log.ScriptSays("type tcp port number to use for image editing service (this port should be open in your "
                           "firewall)")
            PORT = int(input("Port Number : "))
            log.ScriptSays("type default returned image path (This image will respond to requests that have problems)")
            DEFAULT_RETURN_IMAGE_TO_INVALID_REQ_PATH = input("Default image Path With image name: ")
            log.ScriptSays('type all of image path (this path is default place to choose image) like: C:\pics\ ')
            ALL_IMAGE_PATH = input("All image Path : ")
            log.ScriptSays("type default quality of response image (pick from 1 to 99)")
            DEFAULT_RESPONSE_IMAGE_QUALITY = int(input("Quality Number : "))
            if DEFAULT_RESPONSE_IMAGE_QUALITY > 90:
                DEFAULT_RESPONSE_IMAGE_QUALITY = 90
            if DEFAULT_RESPONSE_IMAGE_QUALITY < 20:
                DEFAULT_RESPONSE_IMAGE_QUALITY = 15
            log.ScriptSays("type default weight of response image (most be integer)")
            DEFAULT_RESPONSE_IMAGE_WEIGHT = int(input("Image Weight : "))
            log.ScriptSays("type default height of response image (most be integer)")
            DEFAULT_RESPONSE_IMAGE_HEIGHT = int(input("Image Height : "))
            log.ScriptSays(f"type default format of response image (pick one of {ACCEPTED_RESPONSE_FORMAT})")
            DEFAULT_RESPONSE_IMAGE_FORMAT = input("Image Format : ")
            if DEFAULT_RESPONSE_IMAGE_FORMAT not in ACCEPTED_RESPONSE_FORMAT:
                log.Error("Ops image format not supported , Starting again!")
                readDefaultVariablesFromUser()
            log.ScriptSays("if you want to optimize image resizer type 'y' else type 'n' ")
            if input("turn on optimizer? :") == "y":
                OPTIMIZE_IMAGE = True
            else:
                OPTIMIZE_IMAGE = False

            log.ScriptSays("Image editing service will be run with this config :")
            log.Info(f"PORT : {PORT}")
            log.Info(f"DEFAULT_RETURN_IMAGE_TO_INVALID_REQ_PATH : {DEFAULT_RETURN_IMAGE_TO_INVALID_REQ_PATH}")
            log.Info(f"DEFAULT_RESPONSE_IMAGE_QUALITY : {DEFAULT_RESPONSE_IMAGE_QUALITY}")
            log.Info(f"DEFAULT_RESPONSE_IMAGE_WEIGHT : {DEFAULT_RESPONSE_IMAGE_WEIGHT}")
            log.Info(f"DEFAULT_RESPONSE_IMAGE_HEIGHT : {DEFAULT_RESPONSE_IMAGE_HEIGHT}")
            log.Info(f"DEFAULT_RESPONSE_IMAGE_FORMAT : {DEFAULT_RESPONSE_IMAGE_FORMAT}")
            log.Info(f"ALL_IMAGE_PATH : {ALL_IMAGE_PATH}")
            log.Info(f"OPTIMIZE_IMAGE : {OPTIMIZE_IMAGE}")
            log.ScriptSays("if you want to start image editing service whit above config type 'y' else type 'n'")
            if input("Start image editing service ? : ") == "y":
                log.Info("Ok, Loading requirements...")
            else:
                log.Error("Ops , Starting again!")
                readDefaultVariablesFromUser()
        except traceback:
            log.Error(traceback.format_exc())
            log.Error("Ops , Starting again!")
            readDefaultVariablesFromUser()


if __name__ == '__main__':
    # initializing logger and exit handler
    log = AmLogger(colored_logs=True, save_logs=True, log_file=LOG_FILE)
    atexit.register(programExitHandler)
    # saying hello :)
    log.ScriptSays("Hello,")
    log.ScriptSays("Image editing service has started successfully!")
    if DEBUG_MODE:
        log.Info("Debug mode is activated")
    # Getting user desired value ; this is make more user friendly :)
    readDefaultVariablesFromUser()
    # initialize Socket
    MainCDNSocket = socket.socket()
    MainCDNSocket.bind(("0.0.0.0", PORT))
    MainCDNSocket.listen(SOCKET_LISTEN_NUMBER)
    log.Info(f"image editing service Socket is listening at port : {PORT}")
    mainSocketRequestHandler()
