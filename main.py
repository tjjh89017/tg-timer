#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import datetime

from flask import Flask, request

import telegram
from telegram.ext import Dispatcher, MessageHandler, CommandHandler, Filters

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', None)

app = Flask(__name__)
bot = telegram.Bot(TELEGRAM_TOKEN)

# Enable logging
logger = app.logger

last_reply_time = datetime.datetime.min

@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'

def reply_handler(bot, update):
    """Reply message."""
    """check with from id"""
    global last_reply_time
    username = update.message.from_user.username
    text = update.message.text
    logger.info(text)
    logger.info(username)
    if username == 'cming_ou':
        now = datetime.datetime.now()
        diff = now - last_reply_time
        logger.info(repr(diff))
        logger.info(repr(diff > datetime.timedelta(hours=12)))
        if diff > datetime.timedelta(hours=12):
            logger.info("reply")
            last_reply_time = now
            remain_time = datetime.datetime(2021, 3, 4) - now
            pass_time = now - datetime.datetime(2020, 1, 27)
            #update.message.reply_text("距離Jimmy退伍與Edgecore過勞者聯盟解散還有{}天\nAweimeow都已經退伍{}天了".format(remain_time.days, pass_time.days))

def command_handler(bot, update):
    logger.info('command')
    logger.info(update.message.from_user.username)
    logger.info(update.message.text)
    logger.info(type(bot))
    logger.info(type(update))
    #update.message.reply_text("test")
    now = datetime.datetime.now()
    remain_time = datetime.datetime(2021, 3, 4) - now
    pass_time = now - datetime.datetime(2020, 1, 27)
    update.message.reply_text("距離Jimmy退伍與Edgecore過勞者聯盟解散還有{}天\nAweimeow都已經退伍{}天了".format(remain_time.days, pass_time.days))

dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))
dispatcher.add_handler(CommandHandler('show', command_handler))

if __name__ == '__main__':
    app.run(debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
