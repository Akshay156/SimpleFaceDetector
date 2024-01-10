from threading import Thread
from requests import request

import time 
import cv2
from src.tools import limit_dict

import base64

class ServerConfigurator:
    
    def __init__(self, config, common_class):

        self.config = config
        self.common_class = common_class

        self.load()
    
    def load(self):
        
        for cam_id in self.common_class.camera_class:

            self.common_class.server_class[cam_id] = FaceServerHandler(cam_id, self.config, self.common_class)


class FaceServerHandler(Thread):

    def __init__(self, cam_id, config, common_class):

        Thread.__init__(self)
        
        self.config = config
        self.thread_running = False

        self.common_class = common_class


        self.cam_id = cam_id
        
        self.face_search_api = f"http://localhost:5100/search-face/" 
        self.face_log_api = f"http://localhost:5100/log-face/" 

        # self.attendance_log_api = f"https://{web_server_config.ip_address}:{web_server_config.port}{attendance_log[1]}"
        
        self.fr_data = self.common_class.FrData

        self.start()


    def run(self):

        self.thread_running = True

        while self.thread_running:
    
            time.sleep(1/self.common_class.camera_class[self.cam_id].framerate)

            cropped_face_dataset = self.fr_data.cropped_faces[self.cam_id]
            iter_face_data =  list(cropped_face_dataset.keys())
            for i, track_id in enumerate(iter_face_data):

                faces = []
                
                # if len(face_data) < self.config.FaceData.min_num_faces_to_check:
                    
                if track_id in cropped_face_dataset:
                    faces = cropped_face_dataset[track_id]
                
                    for j,cropped_face in enumerate(faces):
                        try:

                        #     if track_id in self.fr_data.processed_tracks[self.cam_id]:
                        #         if track_id in self.fr_data.cropped_faces[self.cam_id]:
                        #             self.fr_data.cropped_faces[self.cam_id].pop(track_id)
                        #         continue

                        #     if len(self.fr_data.cropped_faces[self.cam_id]) > self.common_class.Logic.max_face_store:
                        #         self.fr_data.cropped_faces[self.cam_id].pop(list(self.fr_data.cropped_faces[self.cam_id].keys())[0])


                        #     if track_id in self.fr_data.cropped_faces[self.cam_id]:
                        #         if not len(self.fr_data.cropped_faces[self.cam_id][track_id])<1:
                        #             self.fr_data.cropped_faces[self.cam_id][track_id].pop(0)
                        #         else:
                        #             self.fr_data.cropped_faces[self.cam_id].pop(track_id)
                            
                        #     # poped_crop_face =  cropped_face.#cropped_face_dataset[track_id].pop(j)
                        #     encoded, buffer = cv2.imencode('.jpg', cropped_face)
                        #     img_b64 = base64.b64encode(buffer)

                        #     data_to_send = {
                        #         "id": track_id,
                        #         "edit": False,
                        #         # "camera_id": self.cam_id,
                        #         "file": img_b64.decode('UTF-8')
                        #     }
                            
                        #     response = request(method="POST", url=self.face_search_api, json= data_to_send)
                            
                        #     if response.status_code == 200:
                        #         data = response.json()

                        #         if data["success"] is not False:

                                    # print(data)

                                    # index_id = data["indexid"]

                                    # poped_crop_face =  cropped_face_dataset.pop(track_id)
                            

                            encoded, buffer = cv2.imencode('.jpg', cropped_face)
                            img_b64 = base64.b64encode(buffer)

                            data_to_send = {
                                "edit": False,
                                "id": int(track_id),
                                "file": img_b64.decode('UTF-8')
                            }

                            response = request(method="POST", url=self.face_search_api, json= data_to_send)
                            
                            if response.status_code == 200:

                                result = response.json()
                                # if data["employeeName"] is not False:
                                #     print(data)
                                print(result)
                                if result == None: continue
                                data = result['result']
                                if not data["success"]: continue
                                self.fr_data.processed_tracks[self.cam_id].append(track_id)

                                # limit_dict(self.fr_data.recognized_faces[self.cam_id], track_id, data["employeeName"], self.common_class.Logic.max_name_store)
                                if len(self.fr_data.recognized_faces[self.cam_id]) > self.common_class.Logic.max_name_store - 1:
                                    self.fr_data.recognized_faces[self.cam_id].pop(list(self.fr_data.recognized_faces[self.cam_id].keys())[0])

                                    
                                self.fr_data.recognized_faces[self.cam_id][track_id] = data["name"]
                                
                                if data["name"] == "" : continue
                                
                                fr_data ={
                                    "index_id": data["indexid"],
                                    "camId": "01",
                                    # "imageData": img_b64.decode('UTF-8')
                                }

                                headers={
                                    'Content-type':'application/json', 
                                    'Accept':'application/json'
                                }
                                try:
                                    response = request(method="POST", url=self.face_log_api, json=fr_data, headers=headers, verify=False)
                                    
                                    # response = request(method="POST", url=self.config.FrServer.fr_log_api, data=fr_data, verify=False)
                                    if response.status_code == 200:
                                        print(f"Logged {data['name']}")
                                except Exception as e:
                                    print(e)

                        except Exception as e:
                            print(e)
                            # None
