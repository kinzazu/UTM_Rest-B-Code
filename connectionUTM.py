import requests
from log_n_save2file import save_xml, config_file

import time
from xml_create import compilation_doc


def get_sent_doc(ip_port):
    url = ip_port
    xml_container = requests.get(url)
    print(xml_container.text)
    return xml_container


def send_response(ip: str, port: str, xml_string):
    fake_xml = {'xml_file': ('QueryRestBCode.xml', xml_string)}
    url = 'http://{}:{}/opt/in/QueryRestBCode'.format(ip, port)
    print(url)
    poster = requests.post(url, files=fake_xml)
    print(poster.status_code, poster.text)


def send_ttn_response(ip: str, port: str, xml_string):
    fake_xml = {'xml_file': ('QueryResendDoc.xml', xml_string)}
    url = 'http://{}:{}/opt/in/QueryResendDoc'.format(ip, port)
    # print(url)
    poster = requests.post(url, files=fake_xml)
    print(poster.status_code)


# get_rests_response – запрос всех ответов УТМ на запросы марок по справке Б. Нужно для проверки наличия марок в справке
# rests_bcode – запрос на конкретный ответ по остаткам марки. Далее парс, -
# - если файл пустой, то делаем DELETE для удаления из БД УТМ.
# большая проблема, что он удаляет документы, при данном запросе.
# нужно это либо решать, либо вообще другой метод придумывать.
def get_rests_response(ip, port: str):
    zapros = requests.get('http://{}:{}/opt/out/ReplyRestBCode'.format(ip, port))
    save_xml(zapros.text)
    return zapros.text


def rest_bcode(list_response: list):
    list_of_xml = []
    for element in list_response:
        post_element = requests.post(element)
        print(post_element)
        list_of_xml.append(post_element.text)
        # time.sleep(5)
    return list_of_xml



# 212.119.253.130:8081 - Green Villa    109.226.229.29:4545 - Brugge
# xml = compilation_doc('020000190211', 'FB-000002712629120')
# get_sent_doc('http://109.226.229.29:4545/opt/in')
# # send_response('109.226.229.29:4545', xml)
# xml_string = get_rests_response('212.119.253.130:8081')
# container = rest_bcode(prr(xml_string))
# print(container)


# ip = config_file('ini/conf.ini','ip')
# # port = config_file('ini/conf.ini','port')
# # get_rests_response(ip,port)