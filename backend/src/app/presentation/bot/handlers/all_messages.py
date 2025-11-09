import io

from aiogram import F, Router
from aiogram.types import Message
from dishka import FromDishka

from app.application.usecases.answer_question import AnswerQuestionUsecase
from app.application.usecases.transcribe_voice import TranscribeVoiceUsecase

all_messages_router = Router()


@all_messages_router.message(F.voice)
async def handle_voice(
    message: Message,
    answer_usecase: FromDishka[AnswerQuestionUsecase],
    transcribe_usecase: FromDishka[TranscribeVoiceUsecase],
) -> None:
    status_msg = await message.answer("🎤 Распознаю голосовое сообщение...")

    try:
        file = await message.bot.get_file(message.voice.file_id)
        audio_data = io.BytesIO()
        await message.bot.download_file(file.file_path, audio_data)
        audio_data.seek(0)

        text = await transcribe_usecase(audio_data, "voice.ogg")

        if not text or not text.strip():
            await status_msg.edit_text(
                "Не удалось распознать речь."
            )
            return

        await status_msg.edit_text(
            f"Распознано: «{text}»\n\n🔍 Ищу ответ в документах..."
        )

        answer = await answer_usecase(text)
        await message.answer(answer)

    except Exception:
        await status_msg.edit_text(
            "Произошла ошибка при обработке голосового сообщения."
        )


@all_messages_router.message(F.text)
async def handle_text(
    message: Message,
    answer_usecase: FromDishka[AnswerQuestionUsecase],
) -> None:
    if not message.text or not message.text.strip():
        return

    status_msg = await message.answer("Ищу ответ в документах...")

    try:
        answer = await answer_usecase(message.text)
        await status_msg.delete()
        await message.answer(answer)

    except Exception:
        await status_msg.edit_text(
            "Произошла ошибка при обработке вашего запроса."
        )

