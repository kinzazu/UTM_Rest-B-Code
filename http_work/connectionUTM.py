import requests

<<<<<<< Updated upstream:connectionUTM.py
from log_n_save2file import save_xml
from parse import parse_element_from_list
=======
from work_with_files.log_n_save2file import save_xml
from parse_files.parse import parse_element_from_list
>>>>>>> Stashed changes:http_work/connectionUTM.py


def get_rest_list(ip,port):
    url = f'http://{ip}:{port}/opt/out/ReplyRests_v2'
    get_list = requests.get(url)
    return get_list.text


def send_response(ip: str, port: str, xml_string):
    fake_xml = {'xml_file': ('QueryRestBCode.xml', xml_string)}
    url = 'http://{}:{}/opt/in/QueryRestBCode'.format(ip, port)
    print(url)
    poster = requests.post(url, files=fake_xml)
    print(poster.status_code)


def send_ttn_response(ip: str, port: str, xml_string):
    fake_xml = {'xml_file': ('QueryResendDoc.xml', xml_string)}
    url = 'http://{}:{}/opt/in/QueryResendDoc'.format(ip, port)
    # print(url)
    poster = requests.post(url, files=fake_xml)
    print(poster.status_code)


def send_formb_history_response(ip: str, port: str, xml_string):
    fake_xml = {'xml_file': ('QueryHistoryFormB.xml', xml_string)}
    url = 'http://{}:{}/opt/in/QueryHistoryFormB'.format(ip, port) #
    # print(url)
    poster = requests.post(url, files=fake_xml)
    # print(poster.status_code)
    return poster.text


def send_transfer(ip: str, port: str, xml_string):
    fake_xml = {'xml_file': ('TransferToShop.xml', xml_string)}
    url = 'http://{}:{}/opt/in/TransferToShop'.format(ip, port) #
    # print(url)
    poster = requests.post(url, files=fake_xml)
    # print(poster.status_code)
    return poster.text

def get_link_from_replyid(ip,port,reply_id):
    url = f'http://{ip}:{port}/opt/out?replyId={reply_id}'
    poster = requests.post(url)
    return poster.text

# get_rests_response – запрос всех ответов УТМ на запросы марок по справке Б. Нужно для проверки наличия марок в справке
# rests_bcode – запрос на конкретный ответ по остаткам марки. Далее парс, -
# - если файл пустой, то делаем DELETE для удаления из БД УТМ.
# большая проблема, что он удаляет документы, при данном запросе.
# нужно это либо решать, либо вообще другой метод придумывать.
def get_rests_response(ip, port: str):
    zapros = requests.get('http://{}:{}/opt/out/ReplyRestBCode'.format(ip, port))
    save_xml(zapros.text, 1)
    return zapros.text


def rest_bcode(list_response: list, db_name):
    for element in list_response:
        post_element = requests.post(element)
        save_xml(post_element.text, 2)
        parse_element_from_list(post_element.text, db_name)
        # time.sleep(5)



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