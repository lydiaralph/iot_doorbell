#!/usr/bin/env python3

import datetime
import logging
from pathlib import Path
from time import sleep

from picamera import PiCamera


class Camera(PiCamera):

    # Default location: current directory
    snapshots_dir = ""
    videos_dir = ""

    def __init__(self, captured_dir='../resources/captured',
                 log='../logging/smart_doorbell.full.log'):
        captured_samples_dir = Path(captured_dir).resolve()
        if not captured_samples_dir.exists():
            raise RuntimeError("Could not find captured samples directory at ",
                               self.sounds_dir)

        self.snapshots_dir = captured_samples_dir / 'images'
        self.video_dir = captured_samples_dir / 'videos'

        logging.basicConfig(filename=log, level=logging.DEBUG)

        # self.annotate_text = None
        # self.annotate_text_size = 50
        # self.annotate_background = Color('black')
        # self.annotate_foreground = Color('white')

    def capture_still(self):
        current_time = datetime.datetime.now()
        logging.info("Current time: ", current_time)
        image_filepath = str((self.snapshots_dir / str(current_time)).with_suffix('.jpg'))
        try:
            self.generic_camera_preparation()
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
            self.generic_camera_preparation()
            video_filepath = str((self.video_dir / str(current_time)).with_suffix('.h264'))
            logging.debug("Capturing video to " + video_filepath)
            self.start_recording(video_filepath)
            sleep(record_time_seconds)
            self.stop_recording()
        finally:
            self.stop_preview()
            self.close()

    def generic_camera_preparation(self):
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
