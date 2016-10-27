# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree  as ET
import datetime
import sys
import time

cache = {}

def url_request(url,payload=None):
        x = 0
        f = False
        while not f:
                try:
                        response = requests.post(url, payload)
                        f = True
                except :
                        time.sleep(x)
                        print(sys.exc_info()[0])
                        x += 1
        return response


def set_dates(*day):
    now  = datetime.date.today()
    if not day:
        now_str = now.strftime("%d.%m.%Y.")
        StartDate = now_str
        EndDate = now_str 
    else:
        date = now + datetime.timedelta(days=1)
        StartDate = date.strftime("%d.%m.%Y.")
        EndDate = date.strftime("%d.%m.%Y.")
    return StartDate, EndDate

def check_and_clear():
    global cache
    if not cache:
        cache['expire'] = datetime.datetime.now()+ datetime.timedelta(minutes=1)
    else:
        if cache['expire'] <= datetime.datetime.now():
            cache = {}
            cache['expire'] = datetime.datetime.now()+ datetime.timedelta(minutes=1)
     
def check_cache(ClassID, *day):
    global cache
    StartDate, EndDate = set_dates(*day)
    ClassID_Date = ClassID + '|' + StartDate
    if ClassID_Date not in cache:
        d = get_schedule_for_class(ClassID, *day)
        cache[ClassID_Date] = d
        #print(d)
        return d
    else:
        print('From Cache %s'% ClassID_Date)
        return cache[ClassID_Date]
#75265
def get_schedule_for_class(ClassID, *day):
    if not day:
        StartDate, EndDate = set_dates()
    else:
        StartDate, EndDate = set_dates(day)
    payload = {"Function":"GetScheduleForClass","ClassID":ClassID,
               "StartDate":StartDate, "EndDate":EndDate}
    r = requests.post("http://sgo.volganet.ru/lacc.asp", params = payload)
    doc = ET.fromstring(r.text)
    week = []
    for child in doc[0]:
        lessons  = {}
        lessons['Subject'] = child.find('subjname').text
        lessons['Date'] = child.find('day').text
        lessons['Start_time'] = child.find('starttime').text
        lessons['Teacher'] = '%s %s %s' %(child.find('tlastname').text,
         child.find('tfirstname').text, child.find('tmidname').text )
        lessons['Room'] = child.find('roomname').text
        week.append(lessons)
    return week


def check_weekday(*day):
    #today = datetime.date.today().weekday()
    now = datetime.date.today()
    if day:
        weekday = (now + datetime.timedelta(days=1)).weekday()
    else:
        weekday = now.weekday()
    if weekday == 6:
        return True
    return False

            
def Make_a_message(ClassID, *date):
    #day = get_schedule_for_class(ClassID, *day)
    print('here')
    try:
        check_and_clear()
        day = check_cache(ClassID, *date)
        if not check_weekday(*date):
            message = day[0]['Date'] + '\n'
            for lesson in day:
                message += '%s %s %s %s %s.%s. \n' % (lesson['Start_time'],lesson['Subject'],
                                            lesson['Room'],lesson['Teacher'].split()[0],
                                                      lesson['Teacher'].split()[1][0],
                                                      lesson['Teacher'].split()[2][0])
        else:
            message = "Похоже в этот день нет уроков, братишка"
    except:
        message = "Похоже произошла ошибка, братишка"
        print(sys.exc_info())
    return message
