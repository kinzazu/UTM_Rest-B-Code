import xml.etree.ElementTree as ET

from DB.DB_solver import change_have_form
from work_with_files.log_n_save2file import log_file


def apply_parse(url):  # берет XML файл из урл(или файла) и парсит его.
    list_alc = []
    tree = ET.parse(url)
    root = tree.getroot()
    rests = root[1][0][1]
    for child in rests:
        list_alc.append(child)
    return list_alc


def parse_response_rests(xml: str):
    list_urls = []
    root = ET.fromstring(xml)
    for child in root:
        if child.tag == 'url':
            list_urls.append(child.text)
        else:
            continue
    print(list_urls)
    return list_urls


def alc_name_n_ect(list_alc: list, tag: str):  # возращает имя/справку_Б/количество в зависимости от переменной tag
    for iteration in range(len(list_alc)):
        if tag == 'rst:InformF2RegId':
            # print('form.b', list_alc[2].text)
            return list_alc[2].text
        elif tag == 'pref: FullName':
            # print('NAME', list_alc[3][0].text)
            return list_alc[3][0].text
        elif tag == 'pref:ProductVCode':
            # print('my_code V', list_alc[3][5].text)
            return list_alc[3][5].text
# тэги из хемеэля
    # rst:InformF2RegId - справка Б
    # rst:Product - общий тэг для доступа к следующим
    #     pref: FullName - тэг имени алкоголя
    #     pref:ProductVCode - тэг алкокода для сортировки и исключения не нужного


class AlcForm:
    def __init__(self, list_acl):
        self.alc_name = alc_name_n_ect(list_acl, 'pref: FullName')
        self.alc_code = alc_name_n_ect(list_acl, 'pref:ProductVCode')
        self.alc_form = alc_name_n_ect(list_acl, 'rst:InformF2RegId')

    def __str__(self):
        return "FORM-B: {}".format(self.alc_code)

    def __repr__(self):
        try:
            return self.alc_code
        except TypeError:
            print('проблема с GUID заказа')


class Only_Form:
    def __init__(self, form_b):
        self.alc_form = self.class_form_input(form_b)
        self.alc_name = 0
        self.alc_code = 0

    def class_form_input(self, form_b_object):
        return form_b_object

    def __str__(self):
        return "FORM-B: {}".format(self.alc_form)

    def __repr__(self):
        try:
            return self.alc_form
        except TypeError:
            print('проблема с FORM-B запроса')


def creating_list_of_class(class_object, stock_list):
    alc_list = []
    for x in stock_list:
        alc_list.append(class_object(x))
    return alc_list


def parse_response_list(xml):  # анлиз для файла со ссылками
    xml_link_list = []
    # tree = ET.parse(xml)
    root = ET.fromstring(xml)
    for link in root:
        xml_link_list.append(link.text)
    xml_link_list.pop()
    return xml_link_list


# парсит лист ссылок хмл, в которых могут быть марки, а может и не быть. после должна возращать либо марки либо ноль
# которые падают в бд
def parse_element_from_list(xml, db_name):   # изменить с xml на url потом и запрашивать документы

    root = ET.fromstring(xml)
    form_b = root[1][0][1].text
    try:
        for tag in root[1][0][2]:
            print(tag.text)
            change_have_form(db_name, form_b, 1, tag.text)
            event = f'Added mark {tag.text} for {form_b}'
            log_file(event)
    except IndexError:
        print('have mark = 0')
        change_have_form(db_name, form_b, 0, None)


def parse_rest_list(xml):
    root = ET.fromstring(xml)
    print(root[-2].tag, root[-2].text)
    return root[-2].text


def get_reply_id(xml):
    root = ET.fromstring(xml)
    return root[0].text


def response_history_b(xml_string):
    fb_ttn_dict = dict()
    root = ET.fromstring(xml_string)
    fb_ttn_dict['form_b'] = root[1][0][0].text
    fb_ttn_dict['ttn'] = root[1][0][2][0][1].text
    return fb_ttn_dict
