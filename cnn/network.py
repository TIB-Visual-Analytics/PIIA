import logging
import numpy as np
import tensorflow as tf

from cnn import cnn_architectures


class Descriptor:

    def __init__(self, model_path, input_size=224):
        self.input_size = input_size

        logging.info('---------------------------')
        logging.info('Restore model from: {}'.format(model_path))
        logging.info('-#-#-#-#-#-#-#-#-#')

        self.g = tf.Graph()
        with self.g.as_default():
            self.sess = tf.Session(graph=self.g)

            self.image_placeholder = tf.placeholder(shape=[1, None, None, 3], dtype=tf.float32)

            _, self.endpoints = cnn_architectures.create_model(
                'resnet_v2_101', self.image_placeholder, num_classes=None, is_training=False)

            self.net = self.endpoints['resnet_v2_101/block4']

            saver = tf.train.Saver()
            saver.restore(self.sess, model_path)

            self.net = tf.reduce_mean(self.net, [1, 2], name='pool5', keep_dims=True)
            self.net = tf.squeeze(self.net)

    def calc_deep_representations(self, img):
        # normalize image to -1 .. 1
        img_pre = tf.subtract(self.image_placeholder, 0.5)
        img_pre = tf.multiply(img_pre, 2.0)

        img_pre = tf.image.resize_bilinear(img_pre, [self.input_size, self.input_size])

        # get image
        img_v = self.sess.run(img_pre, feed_dict={self.image_placeholder: np.expand_dims(img, axis=0)})

        # get deep representation
        deep_representation = self.sess.run(self.net, feed_dict={self.image_placeholder: img_v})

        return deep_representation
