from bs4 import BeautifulSoup
import urllib.request
import http.cookiejar
import urllib.parse


def get_cookie(USERNAME, PASSWD):
    LOGIN_URL = "http://auth.bupt.edu.cn/authserver/login?service=http%3a%2f%2fyjxt.bupt.edu.cn%2fULogin.aspx"

    cookiejar = http.cookiejar.LWPCookieJar(USERNAME)
    cookiehandle = urllib.request.HTTPCookieProcessor(cookiejar)
    httphandle = urllib.request.HTTPHandler()

    opener = urllib.request.build_opener(cookiehandle, httphandle)

    html = opener.open(LOGIN_URL)
    soup = BeautifulSoup(html.read().decode("utf-8"),'lxml')
    lt_node = soup.find(nameislt)
    lt = lt_node['value']

    exec_node = soup.find(nameisexecution)
    exec_str = exec_node['value']

    data = {
        'lt': lt,
        'username': USERNAME,
        'password': PASSWD,
        'execution': exec_str,
        '_eventId': 'submit',
        'rmShown': '1'
    }
    opener.open(LOGIN_URL,urllib.parse.urlencode(data).encode())

    return cookiejar


def nameislt(tag):
    if tag.has_attr('name')and tag['name'] == 'lt':
        return True
    else:
        return False


def nameisexecution(tag):
    if tag.has_attr('name')and tag['name'] == 'execution':
        return True
    else:
        return False
