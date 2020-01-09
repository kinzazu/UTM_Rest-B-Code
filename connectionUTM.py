import requests
from xml_create import compilation_doc
from requests.auth import HTTPBasicAuth


def get_orders(ip_port):
    url = ip_port
    xml_container = requests.get(url)
    print(xml_container.text)
    return xml_container


def send_response(ip_port, xml_string):
    fake_xml = {'xml_file': ('QueryRestBCode.xml', xml_string)}
    url = 'http://' + ip_port + '/opt/in/QueryRestBCode'
    print(url)
    poster = requests.post(url, files=fake_xml)
    print(poster.status_code, poster.text)


# get_orders('http://109.226.229.29:4545/opt/in')
# xml = compilation_doc('020000190211', 'FB-000001952584827')
# send_response('109.226.229.29:4545', xml)