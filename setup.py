from config import config
TOKEN = config.TELEGRAM_BOT_TOKEN

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes


# Шаги для состояния диалога
ASK_TEXT, ASK_STYLE = range(2)


# Начальное сообщение с описанием функционала
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Сгенерировать вокал"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}!\n\n"
        "Я помогу вам создать вокал. Вот что я могу:\n"
        "- Нажмите 'Сгенерировать вокал', чтобы начать процесс.\n\n"
        "Команды:\n"
        "/start — перезапустить бота\n"
        "/cancel — отменить процесс",
        reply_markup=reply_markup,
    )
    return ConversationHandler.END

# Обработка кнопки "Сгенерировать вокал"
async def ask_for_song_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Убираем кнопку "Сгенерировать вокал" после того как она была нажата
    await update.message.reply_text(
        "Пожалуйста, отправьте текст песни. Для отмены используйте команду /cancel.",
        reply_markup=ReplyKeyboardRemove()  # Убираем клавиатуру
    )
    return ASK_TEXT

# Получение текста песни и запрос стиля
async def ask_for_vocal_style(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["song_text"] = update.message.text

    # Убираем кнопку "Отменить"
    await update.message.reply_text(
        "Теперь укажите стиль исполнения вокала и ваши пожелания. Для отмены используйте команду /cancel."
    )
    return ASK_STYLE

# Завершение процесса: обработка данных
async def generate_vocal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vocal_style = update.message.text
    song_text = context.user_data["song_text"]

    # Сообщение о начале генерации
    await update.message.reply_text("Начинаю генерацию вокала... Это может занять некоторое время.")

    try:
        # Здесь можно вызвать функцию обработки данных
        # Например, функцию заглушки
        # generate_mock_audio(song_text, vocal_style)

        # Вместо реальной генерации — возвращаем фиктивный файл
        await update.message.reply_document(open("sample.wav", "rb"))
        
        # Сообщение об успешной генерации
        await update.message.reply_text(f"Ваша заявка:\n\nТекст: {song_text}\nСтиль: {vocal_style}\n\nГенерация завершена.")

    except Exception as e:
        # Если генерация не удалась, отправляем сообщение об ошибке
        await update.message.reply_text(
            f"Произошла ошибка при генерации вокала: {str(e)}. Пожалуйста, попробуйте снова."
        )
        return await start(update, context)

    return await start(update, context)

# Обработка команды "Отменить"
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Процесс отменён. Возвращаюсь в главное меню.", reply_markup=ReplyKeyboardRemove()
    )
    return await start(update, context)

# Основная функция для запуска бота
def main():
    app = Application.builder().token(TOKEN).build()

    # Определение диалога
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^(Сгенерировать вокал)$"), ask_for_song_text)],
        states={
            ASK_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_vocal_style),
                CommandHandler("cancel", cancel),
            ],
            ASK_STYLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, generate_vocal),
                CommandHandler("cancel", cancel),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
