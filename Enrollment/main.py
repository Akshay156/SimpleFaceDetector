from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from QtEnroller import Ui_Form
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
import os
from helper import FrServerHandler
import requests
class Camera:
    
    def __init__(self, camera):
        self.camera = camera

    def open(self):
        cap = cv2.VideoCapture(self.camera)
        return cap
    
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of the UI
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.cam_class = Camera('/dev/video0')
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.view_cam)  

        # Connect signals and slots here if needed
        self.ui.button_start.clicked.connect(self.btn_start)
        self.ui.button_enroll.clicked.connect(self.btn_enroll)
        self.ui.button_reset.clicked.connect(self.btn_reset)
        self.ui.button_verify.clicked.connect(self.btn_verify)

        # Initialize a variable to track the button state (toggle)
        self.toggle_start = False
        self.toggle_enroll = False
        self.toggle_verify = False
        self.face_detector = None
        
        # script_dir = os.path.dirname(__file__)
        self.face_detector = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")
        self.recognized_name = ""
        
        self.face_slots = {
            1: self.ui.label_face_1,
            2: self.ui.label_face_2,
            3: self.ui.label_face_3,
            4: self.ui.label_face_4,
            5: self.ui.label_face_5,
        }
        
        self.cropped_faces = []
        
        if self.face_detector is None:
            print("Failed to load face detector model.")
        else:
            print(f"Model file not found ")   
            
        self.frame_counter = 0
        
        self.fr_server_handler = FrServerHandler()
        
        self.current_frame = None
        self.current_bbox = None
    
    def btn_verify(self):
        
        if self.ui.button_verify.text() == "Cancel":
            self.reset()
            self.ui.button_verify.setText("Verify")
            self.clear_all_images()
            self.toggle_verify = False
            self.recognized_name = ""

            
        elif self.ui.button_verify.text() == "Verify":
            self.toggle_verify = True
            self.toggle_enroll = False
            self.toggle_start = True
            self.ui.button_verify.setText("Cancel")
            
            
            
    
    def reset(self):
        self.toggle_enroll = False
        self.toggle_start = True
        
        self.ui.button_start.show()
        # self.ui.button_verify.show()
        self.ui.button_enroll.setText("Enroll")
        self.ui.button_start.setText("Start")
        self.ui.button_reset.setText("Reset")
        self.clear()
        if self.timer.isActive():
            self.timer.stop()
    
    def clear_all_images(self):
        for slot in self.face_slots:
            self.face_slots[slot].clear()
            self.toggle_enroll = True
            self.cropped_faces = []
            
        self.ui.label_view_cam.clear()
        
                
    def btn_reset(self):
        
        if self.ui.button_reset.text() == "Retry":
            self.clear_all_images()
                
        elif self.ui.button_reset.text() == "Reset":
            if self.timer.isActive():
                self.toggle_enroll = False
                self.toggle_start = False

                self.timer.stop()
                self.ui.button_start.show()
                # self.ui.button_verify.show()
                self.ui.button_enroll.setText("Enroll")
                self.ui.button_start.setText("Start")
    
    def btn_enroll(self):
        
        if self.ui.button_enroll.text() == "Enroll":
            self.toggle_enroll = not self.toggle_enroll
            self.ui.button_start.hide()
            # self.ui.button_verify.hide()
            self.ui.button_enroll.setText("Submit")
            self.ui.button_reset.setText("Retry")
            self.ui.button_verify.setText("Cancel")
            return
            
        if self.ui.button_enroll.text() == "Submit":
            name = self.ui.line_edit_name.text()
            phone = self.ui.line_edit_phone.text()
            email = self.ui.line_edit_email.text()

            if not name or not phone or not email:
                QMessageBox.warning(
                    None, "Warning", "Please fill in all the required fields.", QMessageBox.Ok
                )
            else:
                print("Name:", name)
                print("Phone:", phone)
                print("Email:", email)
                
                person_data = {
                    "Name" : name,
                    "Phone" : phone,
                    "Email" : email
                }
                success = self.fr_server_handler.enroll_faces(self.cropped_faces, person_data)
                if success:
                    QMessageBox.information(
                    None, "Info", f"{name} has been enrolled", QMessageBox.Ok
                    )
                    self.reset()
                    self.ui.button_reset.click()
                    return
        
    
    def btn_start(self):
        # Toggle the state
        self.toggle_start = not self.toggle_start
        self.toggle_enroll = False
        
        if self.toggle_start:
            
            self.ui.button_start.setText("Stop")
            self.cap = self.cam_class.open()    
            self.timer.start(20)
            
        else:
            self.ui.button_start.setText("Start")
            self.toggle_enroll = False
            
            try:
                self.cap.release()
            except:
                print("capture function is already empty")

            
    def detect_face(self, frame):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        self.face_detector.setInput(blob)
        detections = self.face_detector.forward()
        confidence = detections[0, 0, 0, 2]

        if confidence < 0.5:
            return frame, []

        box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        
        try:
            frame_to_crop = frame.copy()
            
            if self.toggle_verify:
                if self.current_bbox is not None and self.current_frame is not None:
                    cropped_face = self.crop_detected_faces(self.current_frame, self.current_bbox)
                    response = self.fr_server_handler.search_face(cropped_face)
                    if response is not None:
                        if "result" in response:
                            if response["result"]["success"]:
                                result_name = response["result"]["name"]
                                if result_name != "Unknown":
                                    self.recognized_name = result_name
                    else:
                        self.recognized_name = ""                            
                                
                    
            
            cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 123, 0), 3)
            
            # Crop and resize the detected face
            # cropped_face = self.crop_detected_faces(frame_to_crop, box)
            if len(self.recognized_name)>1:
                # Define the position and font for putting text
                text_position = (startX, startY - 10)
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                font_color = (255, 255, 255)
                font_thickness = 2

                # Put text on the frame
                cv2.putText(frame, self.recognized_name, text_position, font, font_scale, font_color, font_thickness)
            self.current_frame = frame.copy()
            self.current_bbox = box.copy()

        except Exception as e:
            return None, []

        return frame, box

    def crop_detected_faces(self, frame, box, padding_ratio=0.2, target_height=480):
        (startX, startY, endX, endY) = box.astype("int")

        # Apply padding to the face region
        padding_horizontal = int(padding_ratio * (endX - startX))
        padding_vertical = int(padding_ratio * (endY - startY))
        
        startX_with_padding = max(0, startX - padding_horizontal)
        startY_with_padding = max(0, startY - padding_vertical)
        endX_with_padding = min(frame.shape[1], endX + padding_horizontal)
        endY_with_padding = min(frame.shape[0], endY + padding_vertical)

        # Extract the face region with padding
        face_region_with_padding = frame[startY_with_padding:endY_with_padding, startX_with_padding:endX_with_padding]

        # Resize the face region
        r = target_height / float(face_region_with_padding.shape[0])
        dim = (int(face_region_with_padding.shape[1] * r), target_height)
        cropped_face = cv2.resize(face_region_with_padding, dim)

        return cropped_face

    def clear(self):
        pass
    
    def view_cam(self):
        skip_frame_while_enroll = 10
        
        # Check if the camera is started or the timer is active
        if self.toggle_start or self.timer.isActive():
            # Read a frame from the camera
            ret, frame = self.cap.read()

            if ret:
                frame_to_enroll = frame.copy()
                # Increment the frame counter
                self.frame_counter += 1
                
                # Perform face detection and get the detected face box
                frame, box = self.detect_face(frame)
                
                if len(box)> 0:
                    if self.toggle_enroll and self.frame_counter % skip_frame_while_enroll == 0:
                        # If in enrollment mode and it's time to process a frame, crop the detected face and display in available slots
                        self.enroll_faces(frame_to_enroll, box)
                        if all(self.face_slots[slot].pixmap() is not None for slot in self.face_slots):
                            self.toggle_enroll = False
                    else:
                        # If not in enrollment mode or it's not time to process a frame, clear the slots
                        self.clear()
                
                # Display the processed frame in the main view
                self.view_image(frame, self.ui.label_view_cam)

    # Helper function for enrolling faces into available slots
    def enroll_faces(self, frame, box):
        if self.toggle_enroll:
            cropped_face = self.crop_detected_faces(frame, box)
            
            if cropped_face is not None:
                # Iterate through available face slots
                for slot in self.face_slots:
                    if self.face_slots[slot].pixmap() is None:
                        self.view_image(cropped_face, self.face_slots[slot])
                        self.cropped_faces.append(cropped_face)
                        break

    # Helper function for clearing face slots
    def clear_face_slots(self):
        for slot in self.face_slots:
            self.face_slots[slot].clear()
            self.cropped_faces = []


    def view_image(self, image, label_variable):
        """
        Displays image 
        @param:
        input - cv::Mat Image, variable of the label and size of that label
        """

        rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        h, w, ch = rgbImage.shape
        bytes_per_line = ch * w
        cv_to_qt = QImage(rgbImage.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Calculate the aspect ratio
        aspect_ratio = w / h
        
        # Calculate the available size in the label
        available_width = label_variable.width()
        available_height = label_variable.height()
        
        # Calculate the size for keeping the aspect ratio
        new_width = min(available_width, int(available_height * aspect_ratio))
        new_height = min(available_height, int(available_width / aspect_ratio))
        
        # Calculate the position to center the image
        x_position = (available_width - new_width) // 2
        y_position = (available_height - new_height) // 2
        
        # Scale and display the image in the center
        scaled_image = cv_to_qt.scaled(new_width, new_height, Qt.KeepAspectRatio)
        label_variable.setPixmap(QPixmap.fromImage(scaled_image))
        label_variable.setGeometry(x_position, y_position, new_width, new_height)


if __name__ == "__main__":
    app = QApplication([])
    main_window = MyMainWindow()
    main_window.show()
    app.exec()
