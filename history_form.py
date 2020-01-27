from connectionUTM import get_rest_list, send_formb_history_response, get_link_from_replyid, send_ttn_response
from log_n_save2file import config_file, save_xml
from parse import parse_rest_list, get_reply_id, response_history_b
from requests import get, post
from xml_create import compile_formb_history, compile_ttn_request
import time
import xml.etree.ElementTree as ET
import DB_solver
from delete_old import delete_history

ip = config_file('ini/conf.ini', 'ip')
port = config_file('ini/conf.ini', 'port')
fsrar_id = config_file('ini/conf.ini', 'fsrar_id')
db_name = f"DB/{config_file('ini/conf.ini', 'db_name')}"
timeout = config_file('ini/conf.ini', 'timeout')


def test_parse(url):
    list_reply_id = []
    root = ET.fromstring(get(url).text)
    for child in root[1][0][1]:
        form_b = child[2].text
        xml_string = compile_formb_history(form_b, fsrar_id)
        save_xml(xml_string.decode('utf-8'), 3)
        return_id = send_formb_history_response(ip, port, xml_string)
        reply_id = get_reply_id(return_id)
        list_reply_id.append(reply_id)
        yes_counter = 0
        print(f'\r{len(list_reply_id)}', end='')
        step = len(list_reply_id) - 1
        iteration = 0
        if len(list_reply_id) % 120 == 0 and len(list_reply_id) != 0 or child == root[1][0][1][-1]:
            print('\n')
            iteration += 1
            for i in range(125):
                print(f'\rTimer: {i+1}/125 сек.', end='')
                time.sleep(1)
            if iteration != 0:
                for replyID in list_reply_id[step::]:
                    xml = get_link_from_replyid(ip, port, replyID)
                    semi_result =get_reply_id(xml)
                    # print(semi_result)
                    while True:
                        if semi_result == '1':
                            time.sleep(5)
                            xml = get_link_from_replyid(ip, port, replyID)
                            semi_result = get_reply_id(xml)
                            continue
                        elif 'http://' in semi_result :
                            some_name = get(semi_result)
                            fb = response_history_b(some_name.text)
                            DB_solver.add_ttn_info(db_name, fb)
                            yes_counter += 1

                        break
            elif iteration == 0:
                for replyID in list_reply_id:
                    xml = get_link_from_replyid(ip, port, replyID)
                    semi_result =get_reply_id(xml)
                    # print(semi_result)
                    while True:
                        if semi_result == '1':
                            time.sleep(5)
                            xml = get_link_from_replyid(ip, port, replyID)
                            semi_result = get_reply_id(xml)
                            continue
                        elif 'http://' in semi_result :
                            some_name = get(semi_result)
                            fb = response_history_b(some_name.text)
                            DB_solver.add_ttn_info(db_name, fb)
                            yes_counter += 1

                        break

                if yes_counter == len(list_reply_id):
                    print(f'\nуспешно получено {len(list_reply_id)} документов на запрос номера ТТН по справке Б')
                else:
                    print(f'получено {yes_counter}/{len(list_reply_id)}')


def DB_ttn():
    sum_strings = DB_solver.get_data_db(db_name, 'summary_ttn')
    for num in range(sum_strings):
        print('\n----{}/{}---- :'.format(num, sum_strings))
        ttn = DB_solver.get_data_db(db_name, 'ttn')
        print('---- {} ----'.format(ttn))
        xml = compile_ttn_request(fsrar_id, ttn)
        send_ttn_response(ip=ip, port=port, xml_string=xml)
        for i in range(int(timeout)):  # TODO: подумать над таймаутом!!!
            print('\r{}/{} сек.'.format(i, timeout), end='')
            time.sleep(1)
        DB_solver.change_status(db_name, ttn, 'ttn_list', 'ttn')


# delete_history(ip, port)
DB_solver.create_table_ttn(db_name)
x = get_rest_list(ip, port)
test_parse(parse_rest_list(x))
delete_history(ip, port)
DB_ttn()
