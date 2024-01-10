#import tensorflow as tf
import cv2
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import os

import sys


class FaceDetect:
    def __init__(self, model_path, gpu_memory_fraction, visible_device_list):

        with tf.io.gfile.GFile(model_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        graph = tf.Graph()
        with graph.as_default():
            tf.import_graph_def(graph_def, name='import')

        self.input_image = graph.get_tensor_by_name('import/image_tensor:0')
        self.output_ops = [
            graph.get_tensor_by_name('import/boxes:0'),
            graph.get_tensor_by_name('import/scores:0'),
            graph.get_tensor_by_name('import/num_boxes:0'),
        ]

        # gpu_options = tf.GPUOptions(
        #     per_process_gpu_memory_fraction=gpu_memory_fraction,
        #     visible_device_list=visible_device_list
        # )
        config_proto = tf.ConfigProto(log_device_placement=False)
        self.sess = tf.Session(graph=graph, config=config_proto)
        self.padding = 0.35
        
    def detectFaces(self, image, score_threshold=0.5):

        image1 = image
        h, w, _ = image.shape
        image = np.expand_dims(image, 0)

        boxes, scores, num_boxes = self.sess.run(
            self.output_ops, feed_dict={self.input_image: image}
        )
        num_boxes = num_boxes[0]
        boxes = boxes[0][:num_boxes]
        scores = scores[0][:num_boxes]

        to_keep = scores > 0.2
        boxes = boxes[to_keep]
        scores = scores[to_keep]

        scaler = np.array([h, w, h, w], dtype='float32')
        boxes = boxes * scaler

        if boxes is None:
            return None

        bboxes = []
        confs = []

        for box, score in zip(boxes, scores):
            a, b, c, d = box
            ymin = int(a)
            xmin = int(b)
            ymax = int(c)
            xmax = int(d)

            h = ymax - ymin
            w = xmax - xmin

            im_w, im_h = image1.shape[:2]

            ymin = int(max(ymin - (w * self.padding), 0))
            ymax = int(min(ymax + (w * self.padding), im_w))
            xmin = int(max(xmin - (h * self.padding), 0))
            xmax = int(min(xmax + (h * self.padding), im_h))

            bboxes.append((xmin, ymin, xmax - xmin, ymax - ymin))
            confs.append(score)
           
        return bboxes, confs

    def detectAndCropLargestFace(self, image, score_threshold=0.5):
       
        try:
            face_boxes = self.detectFaces(image, score_threshold)

            if not face_boxes or len(face_boxes) == 0:
                return None

            xmin, ymin, width, height = max(face_boxes, key=lambda b: b[2]*b[3])
        
            xmin = int(xmin)
            ymin = int(ymin)
            xmax = int(xmin + width)
            ymax = int(ymin + height)

            h = ymax - ymin
            w = xmax - xmin
            im_w, im_h = image.shape[:2]

            cropped_face = image[ymin:ymax, xmin:xmax]
            # crp_img = cropped_face[:, :, ::-1]
            img = cv2.resize(cropped_face, (224, 224), interpolation=cv2.INTER_CUBIC)
            # cv2.imshow('CroppedImage', img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # return img
            return img, (xmin, ymin, w, h)
        except:
            return None    

    def detectAndCropFaces(self, image, score_threshold=0.5):

        face_boxes = self.detectFaces(image, score_threshold)

        if not face_boxes or len(face_boxes) == 0:
            return None

        retVal = []

        for bbox in face_boxes:
            xmin, ymin, width, height = bbox
            xmin = int(xmin)
            ymin = int(ymin)
            xmax = int(xmin + width)
            ymax = int(ymin + height)

            h = ymax - ymin
            w = xmax - xmin
            im_w, im_h = image.shape[:2]

            cropped_face = image[ymin:ymax, xmin:xmax]
            # cv2.imshow('CroppedImage', cropped_face)
            # cv2.waitKey(0)

            # crp_img = cropped_face[:, :, ::-1]
            crp_img = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)
            # img = cv2.resize(crp_img, (224, 224))
            # cv2.imshow('CroppedImage', crp_img)
            # cv2.waitKey(0)

            retVal.append((crp_img, (xmin, ymin, xmax, ymax)))

        return retVal
