import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update
from utils import get_reply

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
TOKEN = "1722999171:AAG7TUqAQ7vJJbSrZKOOGMd-LaXfizZSuMA"

@app.route('/')
def index():
    return "Hello!"

@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "OK!"


def start(update, context):
    author = update.message.from_user.first_name
    reply = "Hi! {}".format(author)
    update.message.reply_text('Hi {}'.format(author))


def help(update, context):
    help_txt = "Hey! This is help section. Tell me what you need?"
    update.message.reply_text(help_txt)


def reply_text(bot, update):
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news":
        reply_text = "OK! I will show you news with {}".format(reply)
        bot.send_message(chat_id=update.message.chat_id, text=reply_text)
    else:
        bot.send_message(chat_id=update.message.chat_id, text=reply)

def echo_sticker(bot, update):
    sticker=update.message.sticker.file_id
    update.message.reply_text(sticker)


def error(bot, update):
    logger.error("Updated '%s' caused error '%s'", update, update.error)


if __name__ == '__main__':

    bot = Bot(TOKEN)
    bot.set_webhook("https://2dc44ed84087.ngrok.io/" + TOKEN)
    dp = Dispatcher(bot, None)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, reply_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    dp.add_error_handler(error)
    app.run(port=8443)
