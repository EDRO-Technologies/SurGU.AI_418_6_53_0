from dishka import Provider, Scope, provide

from app.application.services.speech_to_text import SpeechToTextService
from app.main.config import WhisperConfig


class SpeechProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_speech_to_text(
        self,
        whisper_config: WhisperConfig
    ) -> SpeechToTextService:
        return SpeechToTextService(whisper_config)
