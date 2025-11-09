from typing import BinaryIO

from openai import AsyncOpenAI

from app.main.config import WhisperConfig


class SpeechToTextService:
    def __init__(self, whisper_config: WhisperConfig):
        self._config = whisper_config
        self._client = AsyncOpenAI(
            api_key=whisper_config.groq_api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    async def transcribe(self, audio_file: BinaryIO, filename: str = "audio.ogg") -> str:
        transcript = await self._client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=(filename, audio_file, "audio/ogg"),
            language="ru"
        )
        return transcript.text
