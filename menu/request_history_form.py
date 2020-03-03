import time
import xml.etree.ElementTree as ET

from requests import get

from DB import DB_solver
from http_work.connectionUTM import get_rest_list, send_formb_history_response, get_link_from_replyid, send_ttn_response
from menu.stopwatch import timer
from parse_files.parse import parse_rest_list, get_reply_id, response_history_b
from parse_files.xml_create import compile_formb_history, compile_ttn_request
from work_with_files.config_worker import Config
from work_with_files.delete_used_docs import delete_history
from work_with_files.log_n_save2file import save_xml
from work_with_files.path_class import Path2File

path = Path2File()

config = Config(path.set_path_file(subfolder='ini', file='conf.ini'))


def test_parse(url):
    list_reply_id = []
    root = ET.fromstring(get(url).text)
    for child in root[1][0][1]:
        form_b = child[2].text
        xml_string = compile_formb_history(form_b, config.fsrar_id)
        save_xml(xml_string.decode('utf-8'), 3)
        return_id = send_formb_history_response(config.ip, config.port, xml_string)
        reply_id = get_reply_id(return_id)
        list_reply_id.append(reply_id)
        yes_counter = 0
        print(f'\r{len(list_reply_id)}', end='')
        iteration = 0
        if len(list_reply_id) % 120 == 0 and len(list_reply_id) != 0 or child == root[1][0][1][-1]:
            print('\n')
            timer(121)
            if iteration != 0:
                for replyID in list_reply_id[step::]:
                    xml = get_link_from_replyid(config.ip, config.port, replyID)
                    semi_result = get_reply_id(xml)
                    # print(semi_result)
                    while True:
                        if semi_result == '1':
                            time.sleep(5)
                            xml = get_link_from_replyid(config.ip, config.port, replyID)
                            semi_result = get_reply_id(xml)
                            continue
                        elif 'http://' in semi_result :
                            some_name = get(semi_result)
                            fb = response_history_b(some_name.text)
                            DB_solver.add_ttn_info(config.DB_name, fb)
                            yes_counter += 1

                        break
                    step = len(list_reply_id) - step
            elif iteration == 0:
                for replyID in list_reply_id:
                    xml = get_link_from_replyid(config.ip, config.port, replyID)
                    semi_result =get_reply_id(xml)
                    # print(semi_result)
                    while True:
                        if semi_result == '1':
                            time.sleep(5)
                            xml = get_link_from_replyid(config.ip, config.port, replyID)
                            semi_result = get_reply_id(xml)
                            continue
                        elif 'http://' in semi_result :
                            some_name = get(semi_result)
                            fb = response_history_b(some_name.text)
                            DB_solver.add_ttn_info(config.DB_name, fb)
                            yes_counter += 1
                        break
                step = len(list_reply_id)
                if yes_counter == len(list_reply_id):
                    print(f'\nуспешно получено {len(list_reply_id)} документов на запрос номера ТТН по справке Б')
                else:
                    print(f'получено {yes_counter}/{len(list_reply_id)}')
            iteration += 1


def DB_ttn():
    sum_strings = DB_solver.get_data_db(config.DB_name, 'summary_ttn')
    for num in range(sum_strings):
        print('\n----{}/{}---- :'.format(num, sum_strings))
        ttn = DB_solver.get_data_db(config.DB_name, 'ttn')
        print('---- {} ----'.format(ttn))
        xml = compile_ttn_request(config.fsrar_id, ttn)
        send_ttn_response(ip=config.ip, port=config.port, xml_string=xml)
        timer(config.timeout)
        DB_solver.change_status(config.DB_name, ttn, 'ttn_list', 'ttn')


# delete_history(ip, port)
DB_solver.create_table_ttn(config.DB_name)
x = get_rest_list(config.ip, config.port)
test_parse(parse_rest_list(x))
delete_history(config.ip, config.port)
DB_ttn()