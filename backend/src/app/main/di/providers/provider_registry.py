from dishka.integrations.fastapi import FastapiProvider

from app.main.di.providers.auth import AuthProvider
from app.main.di.providers.bot import BotProvider
from app.main.di.providers.config import ConfigProvider
from app.main.di.providers.rag import RAGProvider
from app.main.di.providers.speech import SpeechProvider
from app.main.di.providers.sqla import SqlaProvider
from app.main.di.providers.usecases import UseCaseProvider

PROVIDERS = [
    ConfigProvider(),
    SqlaProvider(),
    AuthProvider(),
    UseCaseProvider(),
    BotProvider(),
    RAGProvider(),
    FastapiProvider(),
    SpeechProvider(),
]


def get_providers():
    return PROVIDERS
