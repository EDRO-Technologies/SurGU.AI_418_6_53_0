from aiogram import Bot, Dispatcher
from dishka import Provider, Scope, from_context
from dishka.dependency_source.composite import CompositeDependencySource


class BotProvider(Provider):
    scope = Scope.APP
    bot: CompositeDependencySource = from_context(
        provides=Bot,
    )
    dp: CompositeDependencySource = from_context(
        provides=Dispatcher,
    )
