class CommonClass:
    
    camera_class = {}
    face_detection_class = {}
    tracker_class = {}
    visualize = {}
    server_class = {}

    
    class FrDetectorConfig:
        model = './model/model.pb'
        gpu_memory_fraction = 0.70
        visible_device_list = ''
        threshold = 0.6

    class TrackerConfig:
        ids_to_decay_age = 100
        max_age = 20
        min_hits = 3

    class FrameData:
        frame = {}
        
    class FrConfig:
        face_padding = 10
        skip_frames = 3
    
    class FrData:
        recognized_faces = {}
        unrecognized_faces = {}
        cropped_faces = {}
        processed_tracks = {}
        
    class Logic:
        
        max_person_store = 10
        max_face_store = 5
        max_name_store = 3

        process_for_every_track_age = 3
        ids_to_decay_age = 100