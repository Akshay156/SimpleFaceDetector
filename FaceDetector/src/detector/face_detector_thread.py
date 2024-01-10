import cv2
import numpy as np
from threading import Thread

from src.detector.face_detector import FaceDetect
from src.tracker.sort import Sort
from src.tools import limit_dict

class ConfigureFaceDetector():
    
    def __init__(self, config, common_class):

        self.common_class = common_class
        self.config = config
        
        self.load_detectors()

    
    def load_detectors(self):

        self.face_detector_threads = {}

        self.camera_class = self.common_class.camera_class
        camera_config = self.camera_class

        for cam_id in camera_config:

            self.common_class.face_detection_class[cam_id] = None
            self.common_class.tracker_class[cam_id] = None
            self.face_detector_threads[cam_id] = FaceDetectionThread(cam_id, self.config, self.common_class)



class FaceDetectionThread(Thread):

    def __init__(self, cam_id, config, common_class):
        
        Thread.__init__(self)

        self.face_recognition_config = common_class.FrDetectorConfig
        self.tracker_config = common_class.TrackerConfig

        self.cap = common_class.camera_class[cam_id]

        self.skip_frame = common_class.FrConfig.skip_frames

        # self.skip_frame = config.camera_config[cam_id].process.skip_frames

        self.thread_running = True

        self.face_detect = FaceDetect(
            model_path =  self.face_recognition_config.model,
            gpu_memory_fraction =  self.face_recognition_config.gpu_memory_fraction,
            visible_device_list =  self.face_recognition_config.visible_device_list
        )

        self.tracker = Sort( max_age=self.tracker_config.max_age, min_hits= self.tracker_config.min_hits)
        
        common_class.tracker_class[cam_id] = self.tracker
        common_class.face_detection_class[cam_id] = self

        common_class.FrData.recognized_faces[cam_id] = {}
        common_class.FrData.cropped_faces[cam_id] = {}

        common_class.visualize[cam_id] = False
        self.config = config

        self.cam_id = cam_id
        self.common_class = common_class

        self.common_class.FrData.unrecognized_faces[cam_id] = []
        common_class.FrData.processed_tracks[cam_id] = []

        self.start()

    def detect_face(self, img):
        bboxes, confs = self.face_detect.detectFaces(img, score_threshold=self.common_class.FrDetectorConfig.threshold)
        return bboxes, confs
    
    def run(self):

        self.thread_running = True
        
        frame_count = 0
        padding = self.common_class.FrConfig.face_padding

        self.common_class.FrData.cropped_faces[self.cam_id] = {}

        while True:
            try:
                ret, frame = self.common_class.camera_class[self.cam_id].read()
                
                if ret:

                    frame_count += 1
                    if (frame_count == self.skip_frame+1):
                        frame_bkp = frame.copy() 
                        frame_count = 0
                        
                        bboxes, confs = self.detect_face(frame)
                        bboxes = np.array(bboxes)

                        for face, conf in zip(bboxes, confs):
                            x1, y1, w, h = face
                            face[2] = x1+w
                            face[3] = y1+h
                            np.append(face, conf)

                        trackers = self.tracker.update(np.array(bboxes), frame)

                        for track in trackers:
                            x1,y1,x2,y2,id = track

                            x1 = 0 if int(x1 - padding) < 0 else int(x1 - padding)
                            y1 = 0 if int(y1 - padding) < 0 else int(y1 - padding)

                            x2 = frame.shape[1] if int(x2+padding) > frame.shape[1] else int(x2+padding)
                            y2 = frame.shape[0] if int(y2+padding) > frame.shape[0] else int(y2+padding)

                            # if self.common_class.visualize[self.cam_id]:
                            if True:
                                cv2.rectangle(frame, (x1,y1), (x2,y2), (255, 255, 0), 2)
                                
                                if id in self.common_class.FrData.recognized_faces[self.cam_id]:
                                    id = self.common_class.FrData.recognized_faces[self.cam_id][id]
                                elif id in self.common_class.FrData.unrecognized_faces[self.cam_id]:
                                    id = "unrecognized"
                                else:
                                    id = id
                                
                                id = self.common_class.FrData.recognized_faces[self.cam_id][id] if id in self.common_class.FrData.recognized_faces[self.cam_id] else id

                                
                                cv2.putText( frame, str(id), (x1+5,y1+20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 0), 2)
                            

                            if id not in self.common_class.FrData.processed_tracks[self.cam_id]:
                                if id not in self.common_class.FrData.recognized_faces[self.cam_id]: 
                                    if id not in self.common_class.FrData.unrecognized_faces[self.cam_id]:
                                        if id in self.tracker.track_age:

                                            if self.tracker.track_age[id] % self.common_class.Logic.process_for_every_track_age == 0:
                                                face = np.array(frame_bkp[y1:y2, x1:x2])
                                                limit_dict( self.common_class.FrData.cropped_faces[self.cam_id], id, face, self.common_class.Logic.max_face_store)
                    
                        cv2.imshow("Frame", frame)
                        cv2.waitKey(1)
                            
                        if self.common_class.visualize: self.common_class.FrameData.frame[self.cam_id] = frame
            
            except Exception as e:
                print(e)


