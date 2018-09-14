from doorbell import Camera
from doorbell.Camera import Camera


class TestCamera(object):
    under_test = Camera.Camera()

    def test_initialisation(self):
        assert(self.under_test.annotate_text == '')
        assert(self.under_test.annotate_text_size == 50)

    def test_capture_still(self):
        self.under_test.generic_camera_preparation('abc')
        assert(self.under_test.annotate_text == 'abc')



