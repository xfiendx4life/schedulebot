
import requests
import xml.etree.ElementTree  as ET
def get_class_list():
        r = requests.post('http://sgo.volganet.ru/lacc.asp?Function=GetClassListForSchool&SchoolID=1460')
        root = ET.fromstring(r.text)
        class_list = []
        for child in root[0]:
                class_voc = {}
                class_voc['classid'] = child.find('classid').text
                class_voc['classname'] = child.find('classname').text
                class_list.append(class_voc)
        return class_list
