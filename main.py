import logging
from datetime import datetime
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Настройки логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    """Отправляет инструкции по использованию бота"""
    instructions = "Привет! Я бот-записная книжка. Просто отправь мне сообщение, и я запишу его в файл с датой и временем.\n\n" \
                   "Доступные команды:\n" \
                   "/info - инструкции по использованию\n" \
                   "/note - получить файл с записями\n" \
                   "/clear - очистить файл\n" \
                   "/delete - удалить последнюю запись"
    update.message.reply_text(instructions)


# Обработчик команды /info
def info(update: Update, context: CallbackContext) -> None:
    """Отправляет инструкции по использованию бота"""
    instructions = "Просто отправь мне сообщение, и я запишу его в файл с датой и временем.\n\n" \
                   "Доступные команды:\n" \
                   "/info - инструкции по использованию\n" \
                   "/note - получить файл с записями\n" \
                   "/clear - очистить файл\n" \
                   "/delete - удалить последнюю запись"
    update.message.reply_text(instructions)


# Обработчик команды /note
def note(update: Update, context: CallbackContext) -> None:
    """Отправляет пользователю файл с записями"""
    chat_id = update.effective_chat.id

    # Имя файла для пользователя
    file_name = f"notes_{chat_id}.txt"

    try:
        with open(file_name, 'r') as file:
            notes = file.read()

        if notes:
            update.message.reply_document(document=open(file_name, 'rb'), filename='notes.txt')
        else:
            update.message.reply_text("У вас еще нет записей.")
    except FileNotFoundError:
        update.message.reply_text("У вас еще нет записей.")


# Обработчик команды /clear
def clear(update: Update, context: CallbackContext) -> None:
    """Очищает файл с записями"""
    chat_id = update.effective_chat.id

    # Имя файла для пользователя
    file_name = f"notes_{chat_id}.txt"

    try:
        # Открываем файл в режиме записи, очищаем его и закрываем
        with open(file_name, 'w') as file:
            file.write('')
        update.message.reply_text("Файл с записями очищен.")
    except FileNotFoundError:
        update.message.reply_text("У вас еще нет записей.")


# Обработчик команды /delete
def delete(update: Update, context: CallbackContext) -> None:
    """Удаляет последнюю запись из файла"""
    chat_id = update.effective_chat.id

    # Имя файла для пользователя
    file_name = f"notes_{chat_id}.txt"

    try:
        # Открываем файл в режиме чтения
        with open(file_name, 'r') as file:
            lines = file.readlines()

        if lines:
            # Удаляем последнюю запись из списка
            lines.pop()

            # Открываем файл в режиме записи, записываем измененные записи и закрываем
            with open(file_name, 'w') as file:
                file.writelines(lines)

            update.message.reply_text("Последняя запись удалена.")
        else:
            update.message.reply_text("Файл с записями пуст.")
    except FileNotFoundError:
        update.message.reply_text("У вас еще нет записей.")


# Обработчик сообщений
def echo(update: Update, context: CallbackContext) -> None:
    """Записывает сообщение пользователя в файл с датой и временем"""
    chat_id = update.effective_chat.id
    message = update.message.text
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
    note = f"{timestamp} {message}\n"

    # Имя файла для пользователя
    file_name = f"notes_{chat_id}.txt"

    # Добавляем запись в файл
    with open(file_name, 'a') as file:
        file.write(note)

    update.message.reply_text("Запись сохранена!")


def main() -> None:
    """Запуск бота"""
    # Токен вашего бота
    token = '***********************************'

    # Создаем объект бота и передаем ему токен
    updater = Updater(token)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("note", note))
    dispatcher.add_handler(CommandHandler("clear", clear))
    dispatcher.add_handler(CommandHandler("delete", delete))

    # Регистрируем обработчик сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запускаем бота
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl + C
    updater.idle()


if __name__ == '__main__':
    main()
