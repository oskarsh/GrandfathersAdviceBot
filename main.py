#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
Basic example for a bot that uses inline keyboards.
"""
import logging
import requests
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Ask the API to get the all the Data
r = requests.get('https://my-json-server.typicode.com/daehruoydeef/GrandfathersAdviceBot/life')
logger.info(r.json())
life = r.json()


def start(update, context):
    keyboard = [[InlineKeyboardButton("Life Advice", callback_data='1'),
                 InlineKeyboardButton("Well Being and Health ", callback_data='2'),
                 InlineKeyboardButton("Work and Carrer", callback_data='3'),
                 InlineKeyboardButton("Family and Friends", callback_data='4')
                 ],
]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose Time:', reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    data = query.data
    logger.info("data: " + str(data))
    if data == "1":
        logger.info("sending Family and Friends Advice")
        advice=random.choice(life)
        logger.info(advice)
        query.edit_message_text(text=advice)
    elif data == "2":
        logger.info("sending Well Being and Health Advice")
    elif data == "3":
        logger.info("sending Work and Carrer Advice")
    elif data == "4":
        logger.info("sending Family and Friends Advice")

    
    # query.edit_message_text(text="Selected option: {}".format(query.data))


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():



    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("TOKEN", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()