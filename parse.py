import xml.etree.ElementTree as ET


def apply_parse(url):  # берет XML файл из урл(или файла) и парсит его.
    list_alc = []
    tree = ET.parse(url)
    root = tree.getroot()
    fsrar_id = root[0][0].text
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


def alc_name_n_ect(list_alc: list, tag: str): # возращает имя/справку_Б/количество в зависимости от переменной tag
    for iteration in range(len(list_alc)):
        if tag == 'rst:InformF2RegId':
            # print('form.b', list_alc[2].text)
            return list_alc[2].text
        elif tag == 'pref: FullName':
            # print('NAME', list_alc[3][0].text)
            return list_alc[3][0].text
        elif tag == 'pref:ProductVCode':
            # print('code V', list_alc[3][5].text)
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


def creating_list_of_class(class_object, stock_list):
    alc_list = []
    for x in stock_list:
        alc_list.append(class_object(x))
    return alc_list


def parse_response_list(xml): #анлиз для файла со ссылками
    xml_link_list = []
    tree = ET.parse(xml)
    root = tree.getroot()
    for link in root:
        xml_link_list.append(link.text)
    xml_link_list.pop()
    print(xml_link_list)

# парсит лист ссылок хмл, в которых могут быть марки, а может и не быть. после должна возращать либо марки либо ноль
# которые падают в бд
def parse_element_from_list(xml):   # изменить с xml на url потом и запрашивать документы
    tree = ET.parse(xml)
    root = tree.getroot()
    #
    try:
        for tag in root[1][0][2]:
           print(tag.text)
    # вернуть тупл с проблеькиком на конце и вернуть марки в одну таблицу, а во второй таблице поменять значение
    #  формБ = 1
    except IndexError:
        print('изменить значение "Have FORMB" на 0!')


parse_element_from_list('xml/sample_with_mark.xml')


# 'xml/sample_with_mark.xml'
# пример использования, который нужно перенести в мейн.
# def insert_data(db_name: str, ins_alc_class_list: list):  # если повторить, на заполненных значениях, то данные задублируются, аккуратне!
#     connect = sqlite3.connect(db_name)                    # сделал условие, вроде избавил его от дублирования.
#     cursor = connect.cursor()
#     for data in ins_alc_class_list:
#         symbol = (data.alc_form,)
#         print(symbol)
#         a = input('стоять боятся')
#         selec = [data.alc_name, data.alc_code, data.alc_form, 0]
#         # checking = 'SELECT * FROM alc_data WHERE form_b=?'
#         cursor.execute('SELECT * FROM alc_data WHERE form_b=?', symbol)
#         print('1', cursor.fetchone())
#         # print('2',cursor.fetchall())
#         if cursor.fetchone() is None:
#             cursor.execute('INSERT INTO alc_data VALUES (?,?,?,?)', selec)
#         else:
#             '{} already exist'.format(selec[2])
#             continue

        # print(cursor.fetchone())
    # connect.commit()

# create_db('test.db')


