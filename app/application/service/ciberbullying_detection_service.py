from app.domain.model.model import Model
from app.domain.model.message import Message

class CiberbullyingDetectionService:
    def __init__(self, model: Model):
        self.model = model

    def analize_message(self, message: str):
        msg = Message(message=message)
        processed_message = msg.process()
        return self.model.predict(processed_message)