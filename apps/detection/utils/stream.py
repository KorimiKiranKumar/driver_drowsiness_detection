from .camera import start_camera
from .pipeline import process_frame

def generate_frames():
    return start_camera(process_frame)