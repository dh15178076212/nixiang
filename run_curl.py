# coding=utf-8
"""
作者: 浩, Administrator
日期: 2023年11月14日--09-40
"""
import re, subprocess

fp = open('./linshi.py', 'w', encoding='utf-8')


def eval_curl(text):
    text = (text.replace('\\', ''))
    url = re.findall("curl '(.*?)'", text)[0]
    head_list = re.findall("-H '(.*?): (.*?)'", text)
    head = dict(head_list)
    if (re.findall('-X POST', text)):
        method = 'post'
    else:
        method = 'GET'.lower()

    if method == 'post':
        json_ = (re.findall("--json '(.*?)'", text))
        data_ = (re.findall('--data-raw "(.*?)"', text))
        if json_:
            source = 'import requests \nheaders = ' + str(head) + '\n' + 'json_data = ' + json_[
                0] + '\n' + 'response = requests.' + method + f'(\'{url}\', headers=headers, json=json_data).text' + '\nprint(response)'
            fp.write(source)
        else:
            source = 'import requests \nheaders = ' + str(head) + '\n' + 'data = ' + data_[
                0] + '\n' + 'response = requests.' + method + f'(\'{url}\', headers=headers, data=data).text' + '\nprint(response)'
            fp.write(source)

    else:
        source = 'import requests \nheaders = ' + str(
            head) + '\n' + 'response = requests.' + method + f'(\'{url}\', headers=headers).text' + '\nprint(response)'
        fp.write(source)

    fp.close()
    path = r"./linshi.py"
    subprocess.Popen("python %s %s" % (path, url), shell=True, stdout=None, stderr=None).wait()


curltext = '''
curl 'http://mobile-cdn.tianyancha.com/appsource/android/dimen_bubble_sfjx.webp' \
 -X GET \
 -H 'User-Agent: Dalvik/2.1.0 (Linux; U; Android 10; Pixel 3 Build/QQ3A.200805.001)' \
 -H 'Host: mobile-cdn.tianyancha.com' \
 -H 'Connection: Keep-Alive' \
 -H 'Accept-Encoding: gzip'
 '''

if __name__ == '__main__':
    eval_curl(curltext)
