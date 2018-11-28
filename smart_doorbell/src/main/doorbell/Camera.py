#!/usr/bin/env python3

from picamera import PiCamera
from configparser import ConfigParser, ExtendedInterpolation

from time import sleep
from colour import Color

import datetime
import logging

class Camera(PiCamera):

    # Default location: current directory
    snapshots_dir = ""
    videos_dir = ""

    def __init__(self, cfg='../resources/doorbell.properties', log='../logging/smart_doorbell.full.log'):
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(cfg)

        # Default location: current directory
        self.snapshots_dir = config.get('CAMERA', 'snapshots_dir', fallback='')
        self.video_dir = config.get('CAMERA', 'videos_dir', fallback='')

        logging.basicConfig(filename=log, level=logging.DEBUG)

        #self.annotate_text = None
        #self.annotate_text_size = 50
        #self.annotate_background = Color('black')
        #self.annotate_foreground = Color('white')

    def capture_still(self):
        current_time = datetime.datetime.now()
        logging.info("Current time: ", current_time)
        image_filepath = self.snapshots_dir + current_time + '.jpg'
        try:
            self.generic_camera_preparation(current_time)
            logging.info("Filepath for captured image: ", image_filepath)
            self.capture(image_filepath)
        except Exception as e:
            logging.error("Encountered camera error: ", str(e))
            image_filepath = None
        finally:
            logging.info("Stopping camera preview")
            self.stop_preview()
            self.close()
            return image_filepath

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
        logging.info("Starting preview of camera")
        self.start_preview()
        # To give the camera time to adjust to light levels, etc.
        sleep(2)


if __name__ == "__main__":
    c = PiCamera()
    logging.info("PC start")
    
    try:
        c.start_preview()
        sleep(10)
    finally:
        c.stop_preview()
        c.close()
    
