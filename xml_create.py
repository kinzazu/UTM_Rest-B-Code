import xml.etree.ElementTree as ET


def compilation_doc(fsrar_id, form_b):
    root = ET.Element("ns:Documents")
    root.set('xmlns:ns', 'http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01')
    root.set('xmlns:qp', 'http://fsrar.ru/WEGAIS/QueryParameters')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('Version', '1.0')
    owner_query = ET.SubElement(root, "ns:Owner")
    fsrar = ET.SubElement(owner_query, 'ns:FSRAR_ID')
    fsrar.text = fsrar_id
    doc = ET.SubElement(root, 'ns:Document')
    query_restB = ET.SubElement(doc, "ns:QueryRestBCode")
    parameters = ET.SubElement(query_restB, 'qp:Parameters')
    parameter = ET.SubElement(parameters, "qp:Parameter")
    name = ET.SubElement(parameter, 'qp:Name')
    name.text = "ФОРМА2"
    value = ET.SubElement(parameter, 'qp:Value')
    value.text = form_b
    message = ET.tostring(root, "utf-8")
    # document = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + message.decode('utf-8')
    document: bytes = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'.encode('utf-8')
    document += message
    return document


def compile_ttn_request(fsrar_id, ttn_id):
    root = ET.Element("ns:Documents")
    root.set('xmlns:ns', 'http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01')
    root.set('xmlns:qp', 'http://fsrar.ru/WEGAIS/QueryParameters')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('Version', '1.0')
    owner_query = ET.SubElement(root, "ns:Owner")
    fsrar = ET.SubElement(owner_query, 'ns:FSRAR_ID')
    fsrar.text = fsrar_id
    doc = ET.SubElement(root, 'ns:Document')
    query_rest_b = ET.SubElement(doc, "ns:QueryResendDoc")
    parameters = ET.SubElement(query_rest_b, 'qp:Parameters')
    parameter = ET.SubElement(parameters, "qp:Parameter")
    name = ET.SubElement(parameter, 'qp:Name')
    name.text = "WBREGID"
    value = ET.SubElement(parameter, 'qp:Value')
    value.text = ttn_id
    message = ET.tostring(root, "utf-8")
    # document = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + message.decode('utf-8')
    document = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'.encode('utf-8')
    document += message
    return document
