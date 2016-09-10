#https://sgo.volganet.ru/lacc.asp?Function=GetCityList2&StateID=34
#https://sgo.volganet.ru/lacc.asp?Function=GetSchools&city=216
import requests
import xml.etree.ElementTree  as ET

def get_city_list():
    r = requests.post('https://sgo.volganet.ru/lacc.asp?Function=GetCityList2&StateID=34')
    #r.encoding = 'utf-8'
    root = ET.fromstring(r.text)
    city_list = []
    for child in root[0]:
        city_dict = {}
        city_dict['cityid'] = child.find('cityid').text
        city_dict['city'] = child.find('city').text
        city_list.append(city_dict)
    return city_list
    
def get_city_id(name):
    lst = get_city_list()
    for item in lst:
        if item['city'] == name:
            return item['cityid']

def get_school_list(cityid):
    r = requests.post('https://sgo.volganet.ru/lacc.asp?Function=GetSchools&city=%s' % cityid)
    root = ET.fromstring(r.text)
    school_list = []
    for child in root[0]:
        school_dict = {}
        school_dict['schoolid'] = child.find('schoolid').text
        school_dict['schoolname'] = child.find('schoolname').text
        school_list.append(school_dict)
    return school_list

def get_school_id(city_name, school_name):
    try:
        lst = get_school_list(get_city_id(city_name))
        for item in lst:
            if item['schoolname'].lower() == school_name.lower():
                return item['schoolid']
        possible_list = []
        for item in lst: #makes list if there's no name
            for word in school_name.lower().split():
                if word in item['schoolname'] and word != '№':
                    possible_list.append(item['schoolname'])
        return possible_list
                        
                    
    except:
        return None
