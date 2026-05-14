from aiogram import Router
from aiogram.types import (
    Message,
    FSInputFile
)

from aiogram import F

from app.export.excel_exporter import (
    export_to_excel
)

router = Router()


@router.message(
    F.text == "📤 Экспорт Excel"
)
async def export_handler(
    message: Message
):

    await message.answer(
        "📤 Создаю Excel..."
    )

    file_path = export_to_excel()

    excel_file = FSInputFile(
        file_path
    )

    await message.answer_document(
        excel_file,
        caption="📊 Экспорт объявлений"
    )