# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InlineQueryResultAudio, InputTextMessageContent
import logging

links_file = open('links.txt', 'r')
phrases = eval(links_file.read())

def search(str_to_search):
    print(str_to_search.lower())
    results = list()
    for phrase in phrases:
        if str_to_search.lower() in phrase['name'].lower():
            print('Found:', phrase['name'])
            results.append(phrase)
    return results

updater = Updater(token='204151153:AAH5AsfOBJ34oiF2GGHGD9Yr-Jz1r4d3QqY')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Привет! Бот работает в inline режиме. Т.е. в любом чате введи моё имя и команду для поиска и выбирай фразу среди найденых (\"@HStone_bot фраза\")")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('help', start)
dispatcher.add_handler(start_handler)

def echo(bot, update):
    print(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text + ' OK?!')

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

def inline_caps(bot, update):
    query = update.inline_query.query
    print(update.inline_query.query, update.inline_query.from_user.first_name, update.inline_query.from_user.last_name)
    if not query:
        return
    results = list()
    print('searchin\'...')
    phrases_results = search(query)
    i = 0
    for phrase in phrases_results:
        results.append(
            InlineQueryResultAudio(
                id = i,
                title=phrase['name'][:-4],
                audio_url=phrase['link']
            )
        )
        i += 1
        if i >= 50:
            break
    bot.answer_inline_query(update.inline_query.id, results)

    

inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()