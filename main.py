import re

import requests
from telegram.ext import Updater, CommandHandler


def get_url():
    contents = requests.get('https://api.thecatapi.com/v1/images/search').json()
    url = contents[0]['url']  # Ответ представляет собой список, поэтому обращаемся к первому элементу
    return url


def get_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search(r"([^.]*)$", url).group(1).lower()
    return url


def bop(update, context):
    url = get_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


def start(update, context):
    update.message.reply_text("Привет! Я бот с котиками. Чтобы получить котика, используйте команду /cat.")


def stop(update, context):
    update.message.reply_text("До свидания! Чтобы запустить бота снова, используйте команду /start.")
    context.bot.stop()


def error(update, context):
    print(f'Обновление {update} вызвало ошибку {context.error}')


def main():
    updater = Updater('6411686334:AAFKh6FwdRb6Y_x5cxL0NC7p_Bmo_I51qZk')
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('cat', bop))

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('cat', bop))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()