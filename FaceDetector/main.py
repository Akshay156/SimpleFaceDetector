# main.py
from src.server_inference import ServerConfigurator
from typing import List, Dict
from pydantic import BaseModel
from src.camera.set_sources import ConfigureCam
from src.detector.face_detector_thread import ConfigureFaceDetector
import json
from src.common_class import CommonClass

config_path = "./config.json"

with open(config_path) as f:
    config = json.load(f)

class CameraProcessConfig(BaseModel):
    name: str
    skip_frames: int
    max_person_to_recognise: int

class CameraConfig(BaseModel):
    type: str
    uri: str
    resolution: List[int]
    fps: int
    process: CameraProcessConfig

class CameraConfiguration(BaseModel):
    camera_1: CameraConfig

class ConfigData(BaseModel):
    camera_configuration: CameraConfiguration

def get_model_data_from(config):
    try:
        return ConfigData(**config)
    except Exception as e:
        print(f"Error parsing config data: {e}")
        return None

camera_config = get_model_data_from(config)

if camera_config:
    common_class = CommonClass()
    multicam = ConfigureCam(camera_config.camera_configuration, common_class)
    detection = ConfigureFaceDetector(config, common_class)
    server = ServerConfigurator(config, common_class)
    
    print("Configured multicam")
else:
    print("Invalid configuration data.")
