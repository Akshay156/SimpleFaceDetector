from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import uvicorn
import cv2
import base64
import numpy as np
import requests

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/FaceEnrollCompunnel"

Base = declarative_base()

class FaceEnrollment(Base):
    __tablename__ = "face_enrollment"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    image_path = Column(String)
    index_id = Column(String)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


# Placeholder function to simulate fetching data from the database
def get_data_from_database(index_id):
    # Replace this with your actual database query
    # For now, returning placeholder data
    return {
        "database_field_1": "value_1",
        "database_field_2": "value_2"
    }

# Placeholder function to simulate fetching name, email, and phone number
def get_name_email_phone_from_indexid(index_id):
    try:
        db = SessionLocal()
        # Fetch data from the FaceEnrollment table based on index_id
        face_enrollment = db.query(FaceEnrollment).filter(FaceEnrollment.index_id == index_id).first()

        if face_enrollment:
            # Return the fetched data
            return {
                "name": face_enrollment.name,
                "email": face_enrollment.email,
                "phone": face_enrollment.phone,
                "image_path": face_enrollment.image_path
            }
        else:
            # Return placeholder data if not found (you can adjust this logic)
            return {
                "name": "",
                "email": "",
                "phone": "",
                "image_path": ""
            }
    except Exception as e:
        print(f"Error fetching data from the database: {e}")
        # Return placeholder data in case of an error
        return {
            "name": "",
            "email": "",
            "phone": "",
            "image_path": ""
        }
    finally:
        db.close()


def get_cv2images_from_arrayofb64(face_data):
    images = []

    for face_b64 in face_data:
        try:
            # Decode base64 string to bytes
            face_bytes = base64.b64decode(face_b64)

            # Convert bytes to numpy array
            face_np = np.frombuffer(face_bytes, dtype=np.uint8)

            # Decode numpy array to image
            face_image = cv2.imdecode(face_np, cv2.IMREAD_COLOR)

            images.append(face_image)
        except Exception as e:
            print(f"Error decoding face image: {e}")

    return images


def add_to_milvus_fr_server(imageb64, identity_id):
    face_enroll_api = "http://localhost:5105/compunnel_facerec/face-enroll"

    data = {
        "data": [
            {
                "edit": True,
                "id": identity_id,
                "file": imageb64
            }
        ]
    }

    try:
        response = requests.post(face_enroll_api, json=data["data"], headers={'Content-Type': 'application/json'})
        response.raise_for_status()  # Check for HTTP errors

        result = response.json()
        # Process the result if needed

        return result
    except requests.exceptions.RequestException as e:
        print(f"Error sending request to Milvus Face Recognition Server: {e}")
        return None


@app.post("/search-face/")
async def search_face(search_data: dict):
    try:
        # Assuming search_data has keys "edit", "id", and "file"
        if "edit" not in search_data or "id" not in search_data or "file" not in search_data:
            raise HTTPException(status_code=400, detail="Invalid search data format")

        # Assuming search_data["file"] contains the base64 image string
        image_base64 = search_data["file"]

        # Assuming search_data["id"] is the image ID
        image_id = search_data["id"]

        # Assuming search_data["edit"] is a boolean indicating edit mode
        edit_mode = search_data["edit"]

        # Prepare data in the format expected by the /face-search endpoint
        search_request_data = {
            "edit": edit_mode,
            "id": image_id,
            "file": image_base64
        }

        # Make a POST request to the /face-search endpoint
        face_search_url = "http://localhost:5105/compunnel_facerec/face-search"
        response = requests.post(face_search_url, json=search_request_data, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            search_result = response.json()
            if search_result["success"]:

                # Placeholder data from the database
                data_from_db = get_data_from_database(search_result["indexid"])

                # Placeholder data for name, email, and phone number
                name_email_phone = get_name_email_phone_from_indexid(search_result["indexid"])

                # Include the fetched data in the response
                search_result.update(data_from_db)
                search_result.update(name_email_phone)

                return JSONResponse(content={"result": search_result})
        
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Search failed: {response.text}")

    except Exception as e:
        return JSONResponse(content={"result": f"Search Failed: {e}"})


@app.post("/enroll-face/")
async def enroll_face(
    enrollment_data: dict,
):
    name = enrollment_data["personal_details"]["Name"]
    phone = enrollment_data["personal_details"]["Phone"]
    email = enrollment_data["personal_details"]["Email"]

    if not all([name, phone, email]):
        raise HTTPException(status_code=400, detail="Name, phone, and email are required fields")

    image_data_array = get_cv2images_from_arrayofb64(enrollment_data.get("face_data"))

    image_folder = "./Images"
    image_path_array = []
    failed_image_index = []

    for idx, image in enumerate(image_data_array):

        data = {"name": name, "phone": phone, "email": email, "image_path": "", "index_id": ""}

        db = SessionLocal()
        face_enrollment = FaceEnrollment(**data)

        milvus_response = add_to_milvus_fr_server(enrollment_data["face_data"][idx], idx)
        single_response = milvus_response[0]

        if single_response["success"]:
            print(single_response)
            index_id = single_response["indexid"]

        else:
            failed_image_index.append(idx)
            print(single_response["error"])

        # print(index_id)

        image_path = os.path.join(image_folder, f"{name}_{idx}.jpg")
        # image_path_array.append(image_path)

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        cv2.imwrite(image_path, image)

        db.add(face_enrollment)
        db.commit()
        face_enrollment.image_path = image_path
        face_enrollment.index_id = index_id
        db.commit()
        db.refresh(face_enrollment)

    return JSONResponse(content={"Success": "True"})


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5100, reload=True)
