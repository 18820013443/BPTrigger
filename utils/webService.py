import requests
from requests.auth import HTTPBasicAuth
# url = "http://azw-rpadeva-001:8181/ws/zkktest"
# url = "http://137.182.193.146:8181/ws/zkktest"
# url = "http://137.182.193.234:8181/ws/zkktest"
# headers={
#     'Authorization':'Basic dGFuZy5rLjVAcGcuY29tOk1ydGtrIzAw',
#     'Content-Type':'text/xml; charset="UTF-8"',
# }

# r = requests.post(url,headers=headers, data=message.encode())


def TriggerProcess(server, functionName, postBody):
    headers = {
        'Content-Type': 'text/xml; charset="UTF-8"',
    }
    url = f'http://{server}/ws/{functionName}'
    r = requests.post(url, headers=headers, data=postBody.encode(), auth=HTTPBasicAuth('tang.k.5@pg.com', 'Mrtkk#00'))
    print(r.text)


if __name__ == '__main__':
    server = '137.182.193.146:8181'
    functionName = 'zkktest'
    postBody = '<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/"><Body><zkktest ' \
               'xmlns="urn:blueprism:webservice:zkktest"/></Body></Envelope> '
    TriggerProcess(server, functionName, postBody)
