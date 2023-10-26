from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.ext import Updater
from telegram.utils.helpers import escape_markdown
import threading
import config

# Вставьте ваш токен сюда
TOKEN = config.tgtoken
WEBHOOK_URL = config.webhookurl  # URL, на который Телеграм будет отправлять обновления

def start(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение при запуске бота."""
    user = update.effective_user
    update.message.reply_text(f'Привет, {escape_markdown(user.first_name)}!')

def handle_photos(update: Update, context: CallbackContext) -> None:
    """Обрабатывает полученные фотографии."""
    file = update.message.photo[-1].get_file()
    
    threading.Thread(target=download_photo, args=(file, update)).start()

def download_photo(file, update):
    file.download('received_photo.jpg')
    update.message.reply_text('Фотография успешно получена и сохранена.')

def main() -> None:
    """Запуск бота."""
    # Создание Updater и передача токена бота.
    updater = Updater(TOKEN)

    # Получение диспетчера для регистрации обработчиков
    dp = updater.dispatcher

    # Регистрация обработчиков
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo & ~Filters.command, handle_photos))

    # Установка вебхука
    updater.start_webhook(listen="0.0.0.0",
                          port=8443,
                          url_path=TOKEN,
                          webhook_url=f"{WEBHOOK_URL}/{TOKEN}")

    updater.idle()

if __name__ == '__main__':
    main()
