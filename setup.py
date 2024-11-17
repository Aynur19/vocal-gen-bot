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

    # Ответ пользователю с фиктивным файлом
    await update.message.reply_text(
        f"Ваша заявка:\n\nТекст: {song_text}\nСтиль: {vocal_style}\n\nГенерация файла..."
    )

    # Вместо реальной генерации — возвращаем фиксированный файл
    await update.message.reply_document(open("sample.wav", "rb"))
    
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




# # Начальное сообщение с описанием функционала
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [["Сгенерировать вокал"]]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
#     await update.message.reply_text(
#         f"Привет, {update.effective_user.first_name}!\n\n"
#         "Я помогу вам создать вокал. Вот что я могу:\n"
#         "- Нажмите 'Сгенерировать вокал', чтобы начать процесс.\n\n"
#         "Команды:\n"
#         "/start — перезапустить бота\n"
#         "/cancel — отменить процесс",
#         reply_markup=reply_markup,
#     )
#     return ConversationHandler.END

# # Обработка кнопки "Сгенерировать вокал"
# async def ask_for_song_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [["Отменить"]]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
#     await update.message.reply_text(
#         "Пожалуйста, отправьте текст песни.", reply_markup=reply_markup
#     )
#     return ASK_TEXT

# # Получение текста песни и запрос стиля
# async def ask_for_vocal_style(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["song_text"] = update.message.text

#     keyboard = [["Отменить"]]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
#     await update.message.reply_text(
#         "Теперь укажите стиль исполнения вокала и ваши пожелания.", reply_markup=reply_markup
#     )
#     return ASK_STYLE

# # Завершение процесса: обработка данных
# async def generate_vocal(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     vocal_style = update.message.text
#     song_text = context.user_data["song_text"]

#     # Здесь можно вызвать функцию обработки данных
#     # Например, функцию заглушки
#     # generate_mock_audio(song_text, vocal_style)

#     # Ответ пользователю с фиктивным файлом
#     await update.message.reply_text(
#         f"Ваша заявка:\n\nТекст: {song_text}\nСтиль: {vocal_style}\n\nГенерация файла..."
#     )

#     # Вместо реальной генерации — возвращаем фиксированный файл
#     await update.message.reply_document(open("sample.wav", "rb"))
    
#     # Возвращаем пользователя в начальное состояние
#     return await start(update, context)

# # Обработка команды "Отменить"
# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         "Процесс отменён. Возвращаюсь в главное меню.", reply_markup=ReplyKeyboardRemove()
#     )
#     return await start(update, context)

# # Основная функция для запуска бота
# def main():
#     app = Application.builder().token(TOKEN).build()

#     # Определение диалога
#     conv_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.Regex("^(Сгенерировать вокал)$"), ask_for_song_text)],
#         states={
#             ASK_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_vocal_style)],
#             ASK_STYLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, generate_vocal)],
#         },
#         fallbacks=[CommandHandler("cancel", cancel), MessageHandler(filters.Regex("^(Отменить)$"), cancel)],
#     )

#     # Регистрация обработчиков
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(conv_handler)

#     # Запуск бота
#     app.run_polling()

# if __name__ == "__main__":
#     main()


# # from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
# # from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes, ConversationHandler
# # import os
# # import time

# # from config import config

# # TOKEN = config.TELEGRAM_BOT_TOKEN

# # # Этапы взаимодействия
# # GREETING, SONG_TEXT, VOCAL_STYLE = range(3)

# # # Путь к аудиофайлу (заглушка для демонстрации)
# # MOCK_AUDIO_PATH = "demo_audio.wav"


# # # 1. Приветствие пользователя
# # async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user_name = update.effective_user.first_name
# #     await update.message.reply_text(
# #         f"Привет, {user_name}! Я бот для генерации вокала. Вот что я умею:\n\n"
# #         "📋 **Функционал**:\n"
# #         "- Сгенерировать вокал из текста песни\n"
# #         # "- Указать стиль вокала\n\n"
# #         "Чтобы начать, нажмите на кнопку ниже.",
# #         reply_markup=ReplyKeyboardMarkup([["🎤 Сгенерировать вокал"]], resize_keyboard=True)
# #     )
# #     return GREETING


# # # 2. Просьба указать текст песни
# # async def ask_for_song_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     await update.message.reply_text(
# #         "Пожалуйста, введите текст песни, которую хотите озвучить.",
# #         reply_markup=ReplyKeyboardRemove()
# #     )
# #     return SONG_TEXT


# # # 3. Просьба указать стиль вокала
# # async def ask_for_vocal_style(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     context.user_data['song_text'] = update.message.text.strip()
# #     await update.message.reply_text(
# #         "Теперь укажите стиль исполнения вокала и любые пожелания.\nПример: \"Весёлый, с акцентом на припеве\"."
# #     )
# #     return VOCAL_STYLE


# # # 4. Генерация заглушки
# # async def process_vocal_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     context.user_data['vocal_style'] = update.message.text.strip()
# #     song_text = context.user_data['song_text']
# #     vocal_style = context.user_data['vocal_style']

# #     # Здесь можно передать song_text и vocal_style в вашу функцию обработки.
# #     print(f"Получен текст: {song_text}")
# #     print(f"Получен стиль: {vocal_style}")

# #     # Эмуляция задержки обработки
# #     time.sleep(3)

# #     # Отправка аудиофайла
# #     await update.message.reply_audio(audio=open(MOCK_AUDIO_PATH, 'rb'))
# #     await update.message.reply_text(
# #         "Ваш вокал сгенерирован! Если хотите попробовать снова, нажмите кнопку ниже.",
# #         reply_markup=ReplyKeyboardMarkup([["🎤 Сгенерировать вокал"]], resize_keyboard=True)
# #     )
# #     return GREETING


# # # Завершение диалога
# # async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     await update.message.reply_text("Диалог завершён. Нажмите /start, чтобы начать заново.")
# #     return ConversationHandler.END


# # def main():
# #     app = Application.builder().token(TOKEN).build()

# #     # Определение обработчика диалога
# #     conv_handler = ConversationHandler(
# #         entry_points=[CommandHandler("start", start)],
# #         states={
# #             GREETING: [MessageHandler(filters.Regex("🎤 Сгенерировать вокал"), ask_for_song_text)],
# #             SONG_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_vocal_style)],
# #             VOCAL_STYLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_vocal_request)],
# #         },
# #         fallbacks=[CommandHandler("cancel", cancel)]
# #     )

# #     # Добавление обработчиков
# #     app.add_handler(conv_handler)

# #     # Запуск бота
# #     app.run_polling()


# # if __name__ == "__main__":
# #     main()
