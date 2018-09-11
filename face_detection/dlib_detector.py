import dlib
import logging
import numpy as np


class DlibDetector:

    def __init__(self):
        self.margin_minimum = 15
        self.margin_percentage = 20
        self.detector = dlib.get_frontal_face_detector()
        self.mvr = np.vectorize(self.__map_value_range, otypes=[np.float32])

    def set_margin_minimum(self, minimum):
        self.margin_minimum = minimum

    def set_margin_percentage(self, percentage):
        self.margin_percentage = percentage

    def __map_value_range(self, original_value):
        old_max = 256
        old_min = 0
        new_max = 1
        new_min = 0
        old_range = (old_max - old_min)
        new_range = (new_max - new_min)
        new_value = (((original_value - old_min) * new_range) / old_range) + new_min
        return new_value

    def find_faces(self, picture):
        """
        Detects faces in a given picture, extracts them and maps the resulting image in range 0-1.
        :param picture: Input picture
        :return: List of resulting images
        """
        faces = []

        # The 1 in the second argument indicates that we should upsample the image
        # 1 time. This will make everything bigger and allow us to detect more
        # faces.
        detections = self.detector(picture, 1)

        for i, d in enumerate(detections):

            # determine bounds for detected face
            top = d.top()
            bottom = d.bottom()
            left = d.left()
            right = d.right()

            margin = int(
                round(
                    max(self.margin_minimum, (max(bottom - top, right - left) // 2) * (self.margin_percentage // 100))))

            if top - margin >= 0:
                top -= margin
            else:
                top = 0

            if bottom + margin < picture.shape[0]:
                bottom += margin
            else:
                bottom = picture.shape[0] - 1

            if left - margin >= 0:
                left -= margin
            else:
                left = 0

            if right + margin < picture.shape[1]:
                right += margin
            else:
                right = picture.shape[1] - 1

            faces.append(self.mvr(picture[top:bottom, left:right]))

        logging.info('{} Face(s) detected.'.format(len(faces)))
        return faces
