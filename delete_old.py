import requests
from parse import parse_response_list
from log_n_save2file import config_file
import time


def delete_history(ip:str, port:str):
    url = f'http://{ip}:{port}/opt/out/ReplyHistoryFormB'
    get_list = requests.post(url).text
    list_res = parse_response_list(get_list)
    print(list_res)
    for i in list_res:
        pip = requests.delete(i)




ip = config_file('ini/conf.ini', 'ip')
port = config_file('ini/conf.ini', 'port')

delete_history(ip, port)
