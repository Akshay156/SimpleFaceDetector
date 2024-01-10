import requests
import cv2
import numpy as np
import base64

class FrServerHandler():
    def __init__(self) -> None:
        self.face_enroll_url = "http://localhost:5100/enroll-face/"
        self.face_search_url = "http://localhost:5100/search-face/"

    # def get_name(self, cropped_face):
    #     # Your face recognition logic goes here
    #     response = "FR response"
    #     return "Name"

    def enroll_faces(self, cropped_faces, person_data):
        try:
            # Convert faces to base64
            cropped_faces_b64 = [self.image_to_b64(face) for face in cropped_faces]

            data = {
                "personal_details": person_data,
                "face_data": cropped_faces_b64
            }

            # Send data to the face enroll URL
            response = self.post_request(self.face_enroll_url, data)

            if response.status_code == 200:
                return True
            else:
                print(f"Failed to enroll faces. Server response: {response.text}")
                return False

        except Exception as e:
            print(e)
            return "Failed"
        
    def search_face(self, current_frame):
        try:
            # Convert current frame to base64
            face_b64 = self.image_to_b64(current_frame)

            # Prepare data for face search
            data_to_verify = {
                "edit": True,  # Adjust accordingly
                "id": 0,  # Adjust accordingly
                "file": face_b64
            }

            # Send data to the face search URL
            response = self.post_request(self.face_search_url, data_to_verify)

            if response.status_code == 200:
                search_result = response.json()
                # Process the search result as needed
                return search_result
            else:
                print(f"Failed to search for faces. Server response: {response.text}")
                return None

        except Exception as e:
            print(e)
            return None
    
    
    def image_to_b64(self, image):
        # Convert cv::Mat to NumPy array
        image_np = np.asarray(image)

        # Convert NumPy array to base64
        _, buffer = cv2.imencode('.jpg', image_np)
        return base64.b64encode(buffer.tobytes()).decode('utf-8')

    def post_request(self, url, data):
        # Send a POST request to the specified URL with data
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
        return response
