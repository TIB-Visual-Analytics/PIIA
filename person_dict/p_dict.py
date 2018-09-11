import operator
import logging
import h5py
import numpy as np
from sklearn.metrics import pairwise


class PersonDictionary:

    def __init__(self, threshold=0.833, group=['actors', 'politicians']):
        self.db_file = h5py.File("./person_dict/FaceDatabase.hdf5", "r")
        self.threshold = threshold
        self.known_person_names = []
        self.known_person_vectors = []
        for category in group:
            if category in self.db_file.keys():
                for person in self.db_file[category].keys():
                    self.known_person_names.append(person)
                    self.known_person_vectors.append(self.db_file[category][person].value)
            else:
                logging.error('Key "' + str(category) + '" not found!')

        if not self.known_person_names:
            raise ValueError('No people to compare to!')

    def classify_person(self, feature_vector):
        """
        Compares every given feature vectore to known
        :param feature_vectors:
        :return:
        """

        similarities = np.squeeze(pairwise.cosine_similarity(self.known_person_vectors, [feature_vector]))
        similarities_dict = dict(zip(self.known_person_names, similarities))
        likeliest_person = max(similarities_dict.items(), key=operator.itemgetter(1))[0]

        logging.info('\tMost likely person: {}'.format(likeliest_person))

        if similarities_dict[likeliest_person] > self.threshold:
            predicted_person = likeliest_person
            logging.info('\tSimilarity: {}'.format(similarities_dict[likeliest_person]))
        else:
            predicted_person = 'Unknown'
            logging.info('\tSimilarity: {} (below threshold --> Label Unknown assigned)'.format(
                similarities_dict[likeliest_person]))

        return predicted_person
