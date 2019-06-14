#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# LICENSE: MIT
# AUTHOR: daeh@tuta.io
# TITLE: GrandfathersAdviceBot
# DESCRIPTION: Grandfather will tell you Advice he learned throughout his Life. 
# NOTES: t.me/GrandfathersAdviceBot
#
#

import logging
import json
import os
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Ask the API to get the all the Data
with open('db.json') as json_file:  
    data = json.load(json_file)
    life = data["life"]
    health = data["health"]
    carrer = data["carrer"]
    family = data["family"]

def advice(update, context):
    keyboard = [[InlineKeyboardButton("Life Advice", callback_data='1'),
                 InlineKeyboardButton("Health", callback_data='2'),
                 InlineKeyboardButton("Work", callback_data='3'),
                 InlineKeyboardButton("Friends", callback_data='4')
                 ],
]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose Category:', reply_markup=reply_markup)

def start(update, context):
    update.message.reply_text("Type /advice to get started")
    update.message.reply_text("Type /help to get help")
    update.message.reply_text("Type /life to get Life Advice")
    update.message.reply_text("Type /health to get Well being and Health Advice")
    update.message.reply_text("Type /work to get Work and Carrer Advice")
    update.message.reply_text("Type /friends to get Family and Friends Advice")
    update.message.reply_text("Type /donate to donate a penny for a coffee")


def lifeadvice(update, context):
    logger.info("sending Life Advice")
    advice=random.choice(life)
    logger.info(advice)
    update.message.reply_text(text="Grandfather Life advice is: \n \n \n "+ advice + " \n \n \n Get another /advice \n \n Get another /life advice")


def healthadvice(update, context):
    logger.info("sending Well Being and Health Advice")
    advice=random.choice(health)
    logger.info(advice)
    update.message.reply_text(text="Grandfather Well being and Health advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /health advice")


def workadvice(update, context):
    logger.info("sending Work and Carrer Advice")
    advice=random.choice(carrer)
    logger.info(advice)
    update.message.reply_text(text="Grandfather Work and Carrer advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /work advice")



def friendsadvice(update, context):
    logger.info("sending Family and Friends Advice")
    advice=random.choice(family)
    logger.info(advice)
    update.message.reply_text(text="Grandfather Family and Friends advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /friends advice")



def button(update, context):
    query = update.callback_query
    data = query.data
    logger.info("data: " + str(data))
    if data == "1":
        logger.info("sending Life Advice")
        advice=random.choice(life)
        logger.info(advice)
        query.edit_message_text(text="Grandfather Life advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /life advice")
    elif data == "2":
        logger.info("sending Well Being and Health Advice")
        advice=random.choice(health)
        logger.info(advice)
        query.edit_message_text(text="Grandfather Well being and Health advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /health advice")
    elif data == "3":
        logger.info("sending Work and Carrer Advice")
        advice=random.choice(carrer)
        logger.info(advice)
        query.edit_message_text(text="Grandfather Work and Carrer advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /work advice")
    elif data == "4":
        logger.info("sending Family and Friends Advice")
        advice=random.choice(family)
        logger.info(advice)
        query.edit_message_text(text="Grandfather Family and Friends advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /friends advice")

def help(update, context):
    update.message.reply_text("Use /advice to get some advice.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("TOKEN", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('advice', advice))
    updater.dispatcher.add_handler(CommandHandler('life', lifeadvice))
    updater.dispatcher.add_handler(CommandHandler('health', healthadvice))
    updater.dispatcher.add_handler(CommandHandler('work', workadvice))
    updater.dispatcher.add_handler(CommandHandler('friends', friendsadvice))
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
