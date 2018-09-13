# coding=gbk
from bs4 import BeautifulSoup
from xyw2 import get_cookie
import time
import requests
import re


def login(user, pwd):
    cookiejar = get_cookie(user, pwd)

    cookie = [item.name + "=" + item.value for item in cookiejar]
    cookie.append('Hm_lvt_41e71a1bb3180ffdb5c83f253d23d0c0=1536203509')
    cookie.append('DropDownListXqu=DropDownListXqu=')
    cookie.append('OnlineSelXQ=OnlineSelXQ=30')
    cookie.append('DropDownListYx_xsbh=DropDownListYx_xsbh=331000')
    cookiestr = ';'.join(item for item in cookie)

    UA = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 " \
         "Safari/537.36 "
    header = {
        "User-Agent": UA,
        "Host": "yjxt.bupt.edu.cn",
        "Referer": "http://yjxt.bupt.edu.cn/Gstudent/leftmenu.aspx?UID={}".format(user),
        "Upgrade-Insecure-Requests": "1",
        "Cookie": cookiestr
    }

    return header


def get_class_page(header):
    list_url = 'http://yjxt.bupt.edu.cn/Gstudent/Course/PlanCourseOnlineSel.aspx?EID=9kWb0OKGTBF2KzmBt5QNDZLXYu1Fldi6xwxV6Yb1wPA1TrsnKBRXgg==&UID={}'.format(USER)
    req = requests.get(list_url, headers=header)
    soup = BeautifulSoup(req.text, 'lxml').find_all('tr', onmouseout="SetRowBgColor(this,false)" )
    return soup


def xuanke(html):
    eid = re.findall(r'EID=(.*?)&amp;UID', html)[0].replace('==', '%3d%3d')
    class_url = 'http://yjxt.bupt.edu.cn/Gstudent/Course/PlanSelClass.aspx?EID={}&UID={}'.format(eid, USER)

    req = requests.get(class_url, headers=header)
    source = req.text

    __EVENTVALIDATION = re.findall(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />', source)[0]
    __VIEWSTATE = re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)"', source)[0]

    payload = {
        'ctl00$ScriptManager1': 'ctl00$contentParent$UpdatePanel2 | ctl00$contentParent$dgData$ctl02$ImageButton1',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATEGENERATOR': '6BAD22EE',
        '__VIEWSTATEENCRYPTED': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__EVENTVALIDATION': __EVENTVALIDATION,
        'ctl00$contentParent$drpXqu$drpXqu': '',
        '__ASYNCPOST': 'true',
        'ctl00$contentParent$dgData$ctl02$ImageButton1.x': '11',  ### 这两个值 是变化的 不知道怎么获得 有这两个值就可以自动选择了
        'ctl00$contentParent$dgData$ctl02$ImageButton1.y': '8'
    }

    req = requests.post(class_url, headers=header, data=payload)
    if 'frameElement.api.close()' in req.text:
        return True
    else:
        print(req.text)
        return False

if __name__ == "__main__":
    global USER
    USER = 'user'              # 自己填
    PWD = 'pwd'                # 自己填

    header = login(USER, PWD)
    ids = ['课程编号']          # 自己填

    counter = 1
    while True:
        print(counter)
        classes = get_class_page(header)

        if len(ids) == 0:
            print('选课完成')
            break

        for id in ids:
            for s in classes:
                html = str(s)
                if id in html:
                    if '正在选课' in html:
                        if xuanke(html):
                            print('选课成功 {}'.format(id))
                            ids.remove(id)
                        else:
                            print('选课失败 {}'.format(id))
                            ids.remove(id)
                    else:
                        print('无法选课 {}'.format(id))
                    break
            else:
                print('课程id不存在 {}'.format(id))
                ids.remove(id)
        time.sleep(1)
        counter += 1
