import xml.etree.ElementTree as ET
from xml_create import compile_ttn_request
from connectionUTM import send_ttn_response
import datetime
import time


def parse_ttn(file_path: str, x_day: str):
    tree =ET.parse(file_path)
    root = tree.getroot()
    ttn_unread_list = root[1][0][2]
    ttn_data = []
    x_day = datetime.datetime.strptime(x_day, '%Y-%m-%d')
    x_day = x_day.date()
    for node in ttn_unread_list:
        print(node.tag)
        ttn_index = node[0]
        raw_data = datetime.datetime.strptime(node[2].text, '%Y-%m-%d')
        y = raw_data.date()
        if y >= x_day:
            if node[0].text != 'TTN-0347192075':
                ttn_data.append(node[0].text)
        else:
            continue
    print('{}/{}'.format(len(ttn_data), len(ttn_unread_list)))
    print(ttn_data)
    return ttn_data


listik = parse_ttn('xml/TTN.xml', '2019-12-19')
counter = 0
for ttn in listik:
    counter += 1
    print('\n {}/10 \t {}'.format(counter, ttn))
    xml_string = compile_ttn_request('020000190211', ttn)
    send_ttn_response('109.226.229.29:4545', xml_string)

    for i in range(610):
        print('\r{}/610 сек.'.format(i), end='')
        time.sleep(1)
