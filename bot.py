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
    if str(type(sc_id)) != "<class 'list'>" and sc_id != None:
        markup = types.ReplyKeyboardHide(selective=False)
        bot.send_message(message.chat.id, 'Школа выбрана', reply_markup = markup)
        db_update(message.chat.id, sc_id)
        print("SCHOOL ID = " + sc_id)
        set_school = False
    elif str(type(sc_id)) == "<class 'list'>":
        markup = types.ReplyKeyboardMarkup(row_width = 1)
        itembtn = 0
        school_list = sc_id
        for item in school_list:
            sch = '%s/%s' % (city_name,item)
            print(sch)
            itembtn = types.KeyboardButton(sch)
            markup.add(itembtn)
        bot.send_message(message.chat.id,'Попробуйте один из следующих вариантов /set_school', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Школа не выбрана, корректно вводите данные')
    
    
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Приветствую, выберите город и школу для получения расписания')



@bot.message_handler(regexp="[\d]+[а-яА-Я]*")
def handle_test(message):
    try:
        markup = types.ReplyKeyboardHide(selective=False)
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
                    bot.send_message(message.chat.id,Make_a_message(class_checker(text, chat_id)), reply_markup = markup)
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
    except:
        bot.send_message(message.chat.id,"Сначала выберите школу используя /set_school")


'''@bot.message_handler(func=lambda message: True)
def handle_no_class(message):
    #print(message.text)
    text = message.text
    try:
        markup = types.ReplyKeyboardMarkup(row_width = 3)
        itembtn = 0
        school_list = get_school_list(get_city_id(text))
        for item in school_list:
            itembtn = types.KeyboardButton(item['schoolname'])
            markup.add(itembtn)
    except:
        print('markup error')
    bot.send_message(message.chat.id,'keyboard test', reply_markup=markup)
    #sticker_number = random.randint(1,10)
    #sti = open('stickers/%s.webp' % str(sticker_number), 'rb')
    #bot.send_sticker(message.chat.id, sti)
    #bot.send_sticker(message.chat.id, "FILEID")'''


        #time.sleep(3)

def class_checker(classname, chat_id):
    school_id = db_check(chat_id)
    if school_id != None:
        print('school_id = ' + school_id)
        class_list = get_class_list(school_id)
        #print(class_list)
        for item in class_list:
            if item['classname'] == classname.lower():
                return item['classid']
        return None
    else:
        return None

if __name__ == '__main__':
    timer = 0
    flag = True
    while True:
        try:
            time.sleep(timer)
            bot.polling(none_stop=True)
        except Exception as e:
            if flag:
                bot.send_message('43037893', 'Houston we have problems: ' + str(e))
                flag = False
            #print(str(e))
            timer += 1
