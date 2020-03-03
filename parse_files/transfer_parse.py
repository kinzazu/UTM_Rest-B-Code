import datetime
import xml.etree.ElementTree as ET

from http_work.connectionUTM import send_transfer


class ImportFB:
    def __init__(self, code, qnt, fb):
        self.fb = fb
        self.code = code
        self.qnt = qnt


today = datetime.date.today()


def transfer2shop(fsrar_id, fb_list):
    root = ET.Element("ns:Documents")
    root.set('xmlns:ns', 'http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01')
    root.set('xmlns:pref', "http://fsrar.ru/WEGAIS/ProductRef_v2")
    root.set('xmlns:tts', "http://fsrar.ru/WEGAIS/TransferToShop")
    root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
    root.set('Version', '1.0')
    owner_query = ET.SubElement(root, "ns:Owner")
    fsrar = ET.SubElement(owner_query, 'ns:FSRAR_ID')
    fsrar.text = fsrar_id
    doc = ET.SubElement(root, 'ns:Document')
    trans2shop = ET.SubElement(doc, 'ns:TransferToShop')
    ttshead = ET.SubElement(trans2shop, 'tts:Header')
    ttsnum = ET.SubElement(ttshead, 'tts:TransferNumber')
    ttsnum.text = input('введите номер документа')
    ttsdate = ET.SubElement(ttshead, 'tts:TransferDate')
    ttsdate.text = f'{today.isoformat()}'
    ttscontent = ET.SubElement(trans2shop, 'tts:Content')
    num = 1
    for fb in fb_list:
        ttsposition = ET.SubElement(ttscontent, 'tts:Position')
        ttsindent = ET.SubElement(ttsposition, 'tts:Identity')
        ttsindent.text = str(num)
        ttsprodeuctcode = ET.SubElement(ttsposition, 'tts:ProductCode')
        ttsprodeuctcode.text = fb.code
        ttsquanity = ET.SubElement(ttsposition, 'tts:Quantity')
        ttsquanity.text = fb.qnt
        ttsinf = ET.SubElement(ttsposition, 'tts:InformF2')
        preff2 = ET.SubElement(ttsinf, 'pref:F2RegId')
        preff2.text = fb.fb
        num += 1
    message = ET.tostring(root, "utf-8")
    document: bytes = '<?xml version="1.0" encoding="UTF-8"?>'.encode('utf-8')
    document += message
    return document


def parse_transfer(xml, ignore_list):
    class_list = []
    tree = ET.parse(xml)
    root = tree.getroot()
    content = root[1][0][1]
    for position in content:
        if position[3][0].text in ignore_list:
            print('yes')
        else:
            print('no')
        try:
            ignore_list.index(position[3][0].text)
            continue
        except ValueError:
            print(position[1].text)
            class_list.append(ImportFB(position[1].text, position[2].text,position[3][0].text ))
    return class_list


def create_ignore_list(txt_path):
    listik = []
    f = open(txt_path, 'r')
    for line in f:
        x = line.split(', ')
        for fb in x:
            if fb is not '\n':
                listik.append(fb)
        print(listik)
    return listik


ignor_list = create_ignore_list('fb_ignore.txt')
print(len(ignor_list))
# print(os.getcwd())
#
class_list = parse_transfer('Transfer_vodka.xml', ignor_list)
doc = transfer2shop('020000190211', class_list)
x = send_transfer('109.226.229.29', '4545', doc)
print(x)