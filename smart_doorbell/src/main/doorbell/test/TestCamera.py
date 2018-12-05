# #!/usr/bin/env python3
#
# try:
#     import unittest2 as unittest
# except ImportError:
#     import unittest
#
# from doorbell import Camera
#
#
# class TestCamera(unittest.TestCase):
#
#     def setUp(self):
#         self.under_test = Camera.Camera()
#
#     def test_basic_camera_setup(self):
#         assert(self.under_test.annotate_text == '')
#         assert(self.under_test.annotate_text_size == 50)
#         assert self.under_test.snapshots_dir is not None
#
#     def test_capture_still(self):
#         self.under_test.generic_camera_preparation('abc')
#         assert(self.under_test.annotate_text == 'abc')
#
#
# if __name__ == 'main':
#     unittest.main()
