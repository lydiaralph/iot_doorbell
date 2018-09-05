from picamera import PiCamera
from time import sleep

CAMERA_DIR = "/home/pi/iot_labs/camera_captures/"

camera = PiCamera()

# camera.rotation = 180
# camera.start_preview(alpha=200) # transparency: 0 to 255
# camera.resolution = (2592, 1944) # max resolution for still photos
# (1920, 1080) max resolution for videos
# camera.framerate = 15 # necessary for enabling max resolution
# min resolution = (64, 64)
# camera.brightness = 70 # 0 to 100
# camera.contrast = 38

# Still
try:
  camera.start_preview()
  sleep(4)
  # Still
  camera.annotate_text = "Hi"
  camera.annotate_text_size = 50 # 6 to 160, default 32
  camera.annotate_background = Color('blue')
  camera.annotate_foreground = Color('yellow')
  camera.capture(CAMERA_DIR + 'image.jpg')
  # Video
  camera.start_recording(CAMERA_DIR + 'video.h264')
  sleep(4)
  camera.stop_recording()
finally:
  camera.stop_preview()
  camera.close()


# omxplayer video.h264
