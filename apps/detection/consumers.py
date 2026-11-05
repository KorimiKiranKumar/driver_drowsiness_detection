import json
import base64
import cv2
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import DetectionLog

class DetectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)

        image_data = data.get("image")

        if not image_data:
            return

        # Decode base64 image
        img_bytes = base64.b64decode(image_data.split(',')[1])
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            await self.send(text_data=json.dumps({
                "status": "Error: Invalid image"
            }))
            return

        # ---- SIMPLE DETECTION LOGIC ----
        # (replace with your ML model later)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        status = "Awake"
        if np.mean(gray) < 50:
            status = "Drowsy"

        # Save to DB
        await self.save_log(status)

        # Send result back
        await self.send(text_data=json.dumps({
            "status": status
        }))

    @sync_to_async
    def save_log(self, status):
        DetectionLog.objects.create(status=status)
