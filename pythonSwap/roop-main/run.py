#!/usr/bin/env python3

import socketio
from roop import core
from io import StringIO
from PIL import Image
from datetime import datetime

sio = socketio.Client()
frameCropPath = 'E:\\work\\ADI\\frameCrop\\frameCrop.png'
now = datetime.now()
gnrFileName = now.strftime("%d%m%Y_%H%M%S") + ".png"
mergeImageFolder = 'E:\\work\\ADI\\SocketIO\\mergeImage\\'
mergeImagePath = mergeImageFolder + gnrFileName

def merge_images(image1_path, image2_path, output_path):
    # Open images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # Determine the dimensions of the merged image
    width = max(image1.width, image2.width)
    height = max(image1.height, image2.height)

    # Resize images to match the dimensions of the merged image
    image1 = image1.resize((width, height))
    image2 = image2.resize((width, height))

    # Create a new blank image with the merged dimensions
    merged_image = Image.new('RGB', (width, height))

    # Paste images onto the blank image
    merged_image.paste(image1, (0, 0))
    merged_image.paste(image2, (0, 0), mask=image2)

    # Save the merged image
    merged_image.save(output_path)


@sio.on("sendPath")
def sendPath(data):
    print("I've received ", data)
    path = data.split("$")
    print(path)
    merge_images(path[0], frameCropPath, mergeImagePath)
    output = core.run_socket(mergeImagePath, path[1])
    print(output)
    sio.emit("output", output)


if __name__ == '__main__':
    sio.connect('http://localhost:8080')
    sio.wait()
