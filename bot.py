# -*- coding: utf-8 -*-
import config
import telebot
from get_data import *
from get_class import *
import threading
from telebot import types
import random
import os
import sqlite3
from get_all_schools import *
from db_processing import *


'''import logging

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)'''

bot = telebot.TeleBot(config.token)
day = ''
set_school = False
chat_id = ''
g_school_name = ''


    
@bot.message_handler(commands=['tomorrow'])
def handle_tomorrow(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, 'Введите класс', reply_markup=markup)
    global day
    day = 'tomorrow'
    print('tomorrow')


@bot.message_handler(commands=['set_school'])
def handle_set_school(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, 'Введите город/назание школы', reply_markup=markup)
    global set_school
    set_school = True
    #bot.send_message(message.chat.id, 'Got it!')
   
@bot.message_handler(regexp="[А-Яа-я\s]*\/[А-Яа-я\s\№\d\"]*")
def handle_city_school(message):
    global set_school
    if not set_school:
        return None
    text = message.text.split('/')
    city_name = text[0]
    school_name = text[1]

    global g_school_name
    g_school_name = message.text
    
    sc_id = get_school_id(city_name, school_name )
    if sc_id:
        bot.send_message(message.chat.id, 'Школа выбрана')
        db_update(message.chat.id, sc_id)
        print("SCHOOL ID = " + sc_id)
    else:
        bot.send_message(message.chat.id, 'Школа не выбрана, корректно вводите данные')
    set_school = False
    
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Приветствую, введите класс для получения расписания')



@bot.message_handler(regexp="[\d]+[а-яА-Я]")
def handle_test(message):
    chat_id = str(message.chat.id)
    print("CHAT ID = " + chat_id)
    global day
    global g_school_name
    #if message.chat.type == 'group' and day != 'tomorrow':
        #text = message.text.split()[1]
    #else:
    text = message.text
    print(text)
    if message.content_type == 'text':
        if class_checker(text, chat_id ) != None:
            if day != 'tomorrow':
                print('today ' + ' ' + text + ' ' + g_school_name)
                bot.send_message(message.chat.id,Make_a_message(class_checker(text, chat_id)))
            else:
                global day
                bot.send_message(message.chat.id,Make_a_message(class_checker(text, chat_id),day))
                print('Завтра ' + ' ' + text + ' ' + g_school_name)
        else:
            bot.send_message(message.chat.id,'В нашей школе нет такого класса')
            sticker_number = random.randint(1,10)
            sti = open('stickers/%s.webp' % str(sticker_number), 'rb')
            bot.send_sticker(message.chat.id, sti)
    day = ''


'''@bot.message_handler(func=lambda message: True)
def handle_no_class(message):
    #print(message.text)
    bot.send_message(message.chat.id,'В нашей школе нет такого класса')
    sticker_number = random.randint(1,10)
    sti = open('stickers/%s.webp' % str(sticker_number), 'rb')
    bot.send_sticker(message.chat.id, sti)
    #bot.send_sticker(message.chat.id, "FILEID")'''


        #time.sleep(3)

def class_checker(classname, chat_id):
    school_id = db_check(chat_id)
    print('school_id = ' + school_id)
    class_list = get_class_list(school_id)
    #print(class_list)
    for item in class_list:
        if item['classname'] == classname.lower():
            return item['classid']
    return None

if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        os.startfile('bot.py')
        print("Here's an ERROR")
