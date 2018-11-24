#!/usr/bin/env python3

from picamera import PiCamera
from configparser import ConfigParser, ExtendedInterpolation

from time import sleep
from colour import Color

import datetime


class Camera(PiCamera):

    # Default location: current directory
    snapshots_dir = ""
    videos_dir = ""

    def __init__(self):
        #project_path = "/Users/ralphl01/Dropbox/LYDIA/TECH/BBC-MSc/2018-07_IoT/iot_labs/smart_doorbell/src/main"
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read("../resources/doorbell.properties")

        # Default location: current directory
        self.snapshots_dir = config.get('CAMERA', 'snapshots_dir', fallback='')
        self.video_dir = config.get('CAMERA', 'videos_dir', fallback='')

        #self.annotate_text = None
        #self.annotate_text_size = 50
        #self.annotate_background = Color('black')
        #self.annotate_foreground = Color('white')

    def capture_still(self):
        try:
            current_time = datetime.datetime.now()
            print("Current time: ", current_time)
            self.generic_camera_preparation(current_time)
            image_filepath = self.snapshots_dir + current_time + '.jpg'
            print("Filepath for captured image: ", image_filepath)
            self.capture(image_filepath)
            return image_filepath
        finally:
            print("Stopping camera preview")
            self.stop_preview()
            self.close()

    def capture_video(self, record_time_seconds):
        try:
            current_time = datetime.datetime.now()
            self.generic_camera_preparation(current_time)
            self.start_recording(self.video_dir + current_time + '.h264')
            sleep(record_time_seconds)
            self.stop_recording()
        finally:
            self.stop_preview()
            self.close()

    def generic_camera_preparation(self, current_time):
        #self.annotate_text = current_time
        print("Starting preview of camera")
        self.start_preview()
        # To give the camera time to adjust to light levels, etc.
        sleep(2)


def main():
    c = PiCamera()
    print("PC start")
    
    try:
        c.start_preview()
        sleep(10)
        c.stop_preview()


if __name__ == "__main__":
    main()
