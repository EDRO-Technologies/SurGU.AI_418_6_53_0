from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

start_router = Router()

@start_router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Добро пожаловать.\n\n"
        "Я консультирую по вопросам охраны труда на основе актуальной нормативной базы.\n"
        "Задайте ваш вопрос."
    )

@start_router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "Как использовать бота:\n\n"
        "• Напишите вопрос текстом\n"
        "• Отправьте голосовое сообщение\n\n"
        "Бот проанализирует запрос и предоставит ответ на основе нормативной документации."
    )