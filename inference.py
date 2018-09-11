import argparse
import logging
import json
import os
import sys

from skimage import io

from cnn.network import Descriptor
from face_detection.dlib_detector import DlibDetector
from person_dict.p_dict import PersonDictionary


def map_value_range(original_value):
    old_max = 256
    old_min = 0
    new_max = 1
    new_min = 0
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    new_value = (((original_value - old_min) * new_range) / old_range) + new_min
    return new_value


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--image', type=str, required=True, help='path to image file')
    args = parser.parse_args()
    return args


def main():
    # load arguments
    args = parse_args()

    # define logging level and format
    level = logging.DEBUG
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=level)

    # read image file
    img = io.imread(args.image)
    if len(img.shape) == 3 and img.shape[2] == 4:  # remove alpha channel if available
        img = img[:, :, :3]

    # init face detection
    face_detector = DlibDetector()

    # init CNN model to extract facial features
    cur_dir = os.path.dirname(__file__)
    descriptor = Descriptor(model_path=os.path.join(cur_dir, 'model', 'model.ckpt-500000'), input_size=224)

    # init person dictionary
    dictionary = PersonDictionary(threshold=0.833, group=['actors', 'politicians'])

    # find faces
    faces = face_detector.find_faces(img)

    face_id = 0
    for face in faces:
        face_id += 1
        logging.info('Classifying face {}'.format(face_id))
        # get deep representation
        representation = descriptor.calc_deep_representations(face)

        # get output for persons in the dictionary
        predicted_person = dictionary.classify_person(representation)

    return 0


if __name__ == '__main__':
    sys.exit(main())
