#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import datetime
import random
import requests
import json

from flask import Flask, request

import telegram
from telegram.ext import Dispatcher, MessageHandler, CommandHandler, Filters

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', None)

app = Flask(__name__)
bot = telegram.Bot(TELEGRAM_TOKEN)

# Enable logging
logger = app.logger

last_reply_time = datetime.datetime.min

quote_last_reply_time = datetime.datetime.min
quote_cache = ""

lunch = [
    '智邦美味一樓餐廳',
    '早餐店(拉雅漢堡,小籠湯包)',
    '四海遊龍',
    '大籠包(鼎福大碗麵)',
    '高峰路熱炒',
    '義大利麵(功夫茶)',
    '僑記刀切麵食館',
    '重慶孫子文牛肉麵',
    '佳香牛排館',
    '六家麵店',
    '21金小火鍋',
    '雲南泰式小吃',
    '跟昨天一樣!',
    '跟明天一樣!',
    '歐哥請我們吃什麼就吃什麼',
    '歐哥說吃什麼就吃什麼',
    '巨城',
    '走下去吃清大南大校區',
    '你自己決定吧!',
]

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
    health_time = now - datetime.datetime(2020, 3, 10)
    update.message.reply_text("距離Jimmy退伍與Edgecore過勞者聯盟解散還有{}天\nAweimeow都已經退伍{}天了\n每日關心Jimmy健康狀態,已經自主隔離{}天了".format(remain_time.days, pass_time.days, health_time.days))

def lunch_handler(bot, update):
    logger.info('lunch')
    logger.info(update.message.from_user.username)
    logger.info(update.message.text)
    update.message.reply_text("吃{}".format(random.choice(lunch)))

def jianhaoch_handler(bot, update):
    logger.info('jianhaoch')
    logger.info(update.message.from_user.username)
    logger.info(update.message.text)
    update.message.reply_text("@jianhaoch 世界越快·豪·則慢-士豪說說哥參上!")

def quote_handler(bot, update):
    global quote_last_reply_time
    global quote_cache
    logger.info('quote')
    logger.info(update.message.from_user.username)
    logger.info(update.message.text)
    # get data from wikiquote
    try:
        # if timeout > 15min, renew the quote
        now = datetime.datetime.now()
        diff = now - quote_last_reply_time
        if diff > datetime.timedelta(minutes=15):
            quote_last_reply_time = now
            raw_data = requests.get('https://zh.wikiquote.org/w/api.php?action=parse&format=json&formatversion=2&prop=wikitext&page=Wikiquote:每日名言/{}月{}日'.format(now.month, now.day)).text
            data = json.loads(raw_data)
            quote_cache = data['parse']['wikitext']

        update.message.reply_text(quote_cache)
    except Exception as e:
        logger.info('except in quote, but ingore')
        logger.info(e)
        pass

dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))
dispatcher.add_handler(CommandHandler('show', command_handler))
dispatcher.add_handler(CommandHandler('lunch', lunch_handler))
dispatcher.add_handler(CommandHandler('jianhaoch', jianhaoch_handler))
dispatcher.add_handler(CommandHandler('quote', quote_handler))

if __name__ == '__main__':
    app.run(debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
