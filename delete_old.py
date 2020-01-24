import requests
from parse import parse_response_list
from log_n_save2file import config_file
import time


def delete_history(ip:str, port:str):
    url = f'http://{ip}:{port}/opt/out/ReplyHistoryFormB'
    get_list = requests.post(url).text
    list_res = parse_response_list(get_list)
    # print(list_res)
    num = 1
    for i in list_res:
        print(f'\r {num}\\{len(list_res)}', end='')
        pip = requests.delete(i)
        num += 1
