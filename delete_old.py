import requests
from code.parse_files.parse import parse_response_list


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
