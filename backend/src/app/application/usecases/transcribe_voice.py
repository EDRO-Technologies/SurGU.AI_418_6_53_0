from typing import BinaryIO

from app.application.services.speech_to_text import SpeechToTextService


class TranscribeVoiceUsecase:
    def __init__(self, speech_to_text: SpeechToTextService):
        self._speech_to_text = speech_to_text

    async def __call__(self, audio_file: BinaryIO, filename: str = "voice.ogg") -> str:
        return await self._speech_to_text.transcribe(audio_file, filename)
