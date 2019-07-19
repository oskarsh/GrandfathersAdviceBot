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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, RegexHandler, Filters
import db

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

reply_keyboard = [['Life', 'Health'],
                  ['Work', 'Friends'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def advice(update, context):
    keyboard = [[InlineKeyboardButton("Life", callback_data='1'),
                 InlineKeyboardButton("Health", callback_data='2'),
                 InlineKeyboardButton("Work", callback_data='3'),
                 InlineKeyboardButton("Friends", callback_data='4')
                 ],
]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose Category:', reply_markup=reply_markup)

def start(update, context):
    update.message.reply_text("Type /advice to get started")
    update.message.reply_text("Type /add to add your own advice")
    update.message.reply_text("Type /help to get help")
    update.message.reply_text("Type /life to get Life Advice")
    update.message.reply_text("Type /health to get Well being and Health Advice")
    update.message.reply_text("Type /work to get Work and Carrer Advice")
    update.message.reply_text("Type /friends to get Family and Friends Advice")
    update.message.reply_text("Type /donate to donate a penny for a coffee")


def lifeadvice(update, context):
    logger.info("sending Life Advice")
    life=db.getLifeAdvicesFromDb()
    advice=random.choice(life)
    logger.info(advice)
    update.message.reply_text(text="Grandfather Life advice is: \n \n \n "+ advice + " \n \n \n Get another /advice \n \n Get another /life advice")


def healthadvice(update, context):
    logger.info("sending Well Being and Health Advice")
    health=db.getHealthAdvicesFromDb()
    advice=random.choice(health)
    logger.info(advice)
    update.message.reply_text(text="Grandfather Well being and Health advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /health advice")


def workadvice(update, context):
    logger.info("sending Work and Carrer Advice")
    carrer=db.getCarrerAdvicesFromDb()
    advice=random.choice(carrer)
    logger.info(advice)
    update.message.reply_text(text="Grandfather Work and Carrer advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /work advice")



def friendsadvice(update, context):
    logger.info("sending Family and Friends Advice")
    family = db.getFamilyAdvicesFromDb()
    advice=random.choice(family)
    logger.info(advice)
    update.message.reply_text(text="Grandfather Family and Friends advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /friends advice")


def addAdvice(update, context):
    logger.info("ADDING ADVICE")
    update.message.reply_text(text="You can now tell me what you learned as a life lesson", reply_markup=markup)
    return CHOOSING

def donate(update, context):
    update.message.reply_text(text="If you like my Grandson´s work consider helping him out by donating a small dime \n \n https://liberapay.com/daehruoydeef")


def button(update, context):
    query = update.callback_query
    data = query.data
    logger.info("data: " + str(data))
    if data == "1":
        logger.info("sending Life Advice")
        life=db.getLifeAdvicesFromDb()
        advice=random.choice(life)
        logger.info(advice)
        query.edit_message_text(text="Grandfather Life advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /life advice")
    elif data == "2":
        logger.info("sending Well Being and Health Advice")
        health=db.getHealthAdvicesFromDb()
        advice=random.choice(health)
        logger.info(advice)
        query.edit_message_text(text="Grandfather Well being and Health advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /health advice")
    elif data == "3":
        logger.info("sending Work and Carrer Advice")
        carrer=db.getCarrerAdvicesFromDb()
        advice=random.choice(carrer)
        logger.info(advice)
        query.edit_message_text(text="Grandfather Work and Carrer advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /work advice")
    elif data == "4":
        logger.info("sending Family and Friends Advice")
        family = db.getFamilyAdvicesFromDb()
        advice=random.choice(family)
        logger.info(advice)
        query.edit_message_text(text="Grandfather Family and Friends advice is: \n \n \n"+ advice + " \n \n \n Get another /advice \n \n Get another /friends advice")

def custom_choice(update, context):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE

def regular_choice(update, context):
    logger.info("REGULAR CHOICE")
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Your {}? Yes, I would love to hear about that!'.format(text.lower()))

    return TYPING_REPLY

def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "\n"
                              "{}"
                              "\n"
                              "Let me think a Day or two about this. Thanks for sharing your knowledge".format(
                                  facts_to_str(user_data)) + 
                                  "\n"
                              "You can tell me more " + category + " Advices if you like. Simply /addAdvice again")

    data = {category: user_data[category]}

    # writing the advice to a user queue
    db.writeToUserAdviceJson(data)
    
    return ConversationHandler.END


def showAllUserAdvices(update, context):
    feeds = db.getAllUserAdvices()
    logger.info(feeds)
    update.message.reply_text(text=feeds)


def addAllUserAdvices(update, context):
    userAdvices = db.getAllUserAdvices()
    for advice in userAdvices:
        for key in advice:
            if key == "Life":
                db.insertIntoLifeAdvices(advice[key])
            if key == "Friends":
                db.insertIntoFamilyAdvices(advice[key])
            if key == "Work":
                db.insertIntoCarrerAdvices(advice[key])
            if key == "Health":
                db.insertIntoHealthAdvices(advice[key])

def getAllUserAdvices():
    db.getLifeAdvicesFromDb()

def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("Until next time!")

    user_data.clear()
    return ConversationHandler.END

def help(update, context):
    update.message.reply_text("Type /advice to get started")
    update.message.reply_text("Type /add to add your own advice")
    update.message.reply_text("Type /help to get help")
    update.message.reply_text("Type /life to get Life Advice")
    update.message.reply_text("Type /health to get Well being and Health Advice")
    update.message.reply_text("Type /work to get Work and Carrer Advice")
    update.message.reply_text("Type /friends to get Family and Friends Advice")
    update.message.reply_text("Type /donate to donate a penny for a coffee")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    logger.info("BOT STARTED")
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("TOKEN", use_context=True)
    logger.info("TOKEN SET")
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('advice', advice))
    updater.dispatcher.add_handler(CommandHandler('donate', donate))
    updater.dispatcher.add_handler(CommandHandler('life', lifeadvice))
    updater.dispatcher.add_handler(CommandHandler('health', healthadvice))
    updater.dispatcher.add_handler(CommandHandler('work', workadvice))
    updater.dispatcher.add_handler(CommandHandler('showAllUserAdvices', showAllUserAdvices))
    updater.dispatcher.add_handler(CommandHandler('addAllUserAdvices', addAllUserAdvices))
    updater.dispatcher.add_handler(CommandHandler('friends', friendsadvice))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    logger.info("HANDLER LINKED")

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', addAdvice)],

        states={
            CHOOSING: [RegexHandler('^(Life|Work|Health|Friends)$',
                                    regular_choice,
                                    pass_user_data=True),
                       RegexHandler('^Something else...$',
                                    custom_choice),
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    logger.info("STARTED POLLING")
    
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
    logger.info("WAITING FOR REQUESTS")


if __name__ == '__main__':
    main()
