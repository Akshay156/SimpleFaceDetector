
import multiprocessing as mp
import time
import src.camera.video_custom as vs


import cv2
import sys
import numpy as np
from threading import Thread
import json

class mainStreamClass(Thread):
    def __init__(
            self, 
            frame_rate,
            resolution,
            uri,
            type):
        Thread.__init__(self)
        #Current Cam
        self.type = type
        self.camProcess = None
        self.cam_queue = None
        self.stopbit = None
        self.uri = uri
        self.framerate = frame_rate
        self.resolution = resolution
        self.thread_running = False
        self.latest_frame = None
        
        # self.start_main()
        # self.start()
    
    def start_main(self):

        if self.type == "rtsp":
            #set  queue size
            self.cam_queue = mp.Queue(maxsize=100)

            #get all cams
            time.sleep(3)

            self.stopbit = mp.Event()
            self.camProcess = vs.StreamCapture(self.uri,
                                self.stopbit,
                                self.cam_queue,
                                self.framerate,
                                self.resolution)
            
            self.camProcess.start()

            lastFTime = time.time()

            # self.run()   
        
        else:
            self.cap = cv2.VideoCapture(self.uri) 
    
    def stop(self):
        # self.join()
        self.stopCamStream()
        self.thread_running = False

    def read(self):
        if self.latest_frame is not None:
            return True, self.latest_frame.copy()
        else:
            return False, None
        
    def run(self):
        self.thread_running = True
        try: 
            while self.thread_running:

                if self.type == "rtsp":

                    if not self.cam_queue.empty():

                        ret, frame = self.cam_queue.get()
                        frame = cv2.resize(frame, (640, 480))
                        lastFTime = time.time()

                        if ret == vs.StreamCommands.FRAME:
                            if frame is not None:
                                self.latest_frame = frame
                            
                else:

                    ret, frame = self.cap.read()

                    # if self.type == "file":
                    #     time.sleep(1/self.framerate)

                    if ret:
                        self.latest_frame = frame

                    else: 
                        try:

                            self.start_main()
                            # self.start()
                        except Exception as e:
                            
                            self.stopCamStream()
                            # self.stop()
                            
                            self.start_main()
                            print(e)
                            # self.start()

        except KeyboardInterrupt:
            print('Keyboard interrupt')

        except:
            e = sys.exc_info()
            print('Main Exception')
            print(e)

        self.thread_running = False
        
        self.stopCamStream()
    
    def stopCamStream(self):
        print('stop camera streaming ')

        if self.type == "rtsp":
            if self.stopbit is not None:
                try:
                    self.stopbit.set()
                    while not self.cam_queue.empty():
                        try:
                            _ = self.cam_queue.get()
                        except:
                            break
                    self.cam_queue.close()
                except Exception as e:
                    print(e)
        else:
            self.latest_frame = None
            self.cap.release()

        if self.camProcess is not None: 
            self.camProcess.join()
        

class ConfigureCam():
    
    def __init__(self, config, common_class):
        self.config = config
        self.common_class = common_class

        self.camera_threads = {}
        self.load_cameras()
        self.start_gstreamer()

        
    def load_cameras(self):
        cam_id = "camera_1"
        # for cam_id in self.config:
        cam_data = self.config.camera_1

        if cam_data.type == "rtsp":
            uri= cam_data.uri
        
        elif cam_data.type == "usb":
            uri= '/dev/video0'

        else:
            uri = cam_data.ip_address

        # configuration_data = json.loads(cam_data.configuration)
        configuration_data = cam_data
        
        self.common_class.camera_class[cam_id] = mainStreamClass(
            frame_rate = configuration_data.fps,
            resolution = [ configuration_data.resolution[0], configuration_data.resolution[1]],
            uri = uri,
            type = cam_data.type
        )
            # self.common_class.camera_class[cam_id] = self

    def start_gstreamer(self):
            for cam_id in self.common_class.camera_class:

                
                self.common_class.camera_class[cam_id].start_main()
                self.common_class.camera_class[cam_id].start()
                    
                

        




    






        