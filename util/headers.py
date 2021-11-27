import json
import os
import random
from urllib.parse import quote
import hashlib
import execjs

user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"]

ua_list = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3975.2 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4183.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5'
]



def gen_header(url_part,cookie,d_c0='"ACDXfhlXcBKPThgCFcQdt5d4_bWmqk79pmQ=|1609556670"', is_signature=True):
    """
        init:
            cd x-zse-96/
            npm install jsdom

        refer document:
            https://blog.csdn.net/qq_26394845/article/details/118183245
    """
    f = "+".join(["101_3_2.0", url_part, d_c0])
    fmd5 = hashlib.new('md5', f.encode()).hexdigest()

    _cur_dir = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(_cur_dir, 'x-zse-96/g_encrypt.js'), 'r') as f:
        ctx1 = execjs.compile(f.read(), cwd=r'{}'.format(os.path.join(_cur_dir, 'x-zse-96')))
    encrypt_str = ctx1.call('b', fmd5)
    header = {
        # "referer": "https://www.zhihu.com/search?type={}&q={}".format(type, q),
        "user-agent": random.choice(ua_list),
        'cookie': 'd_c0={}'.format(d_c0),
        "x-api-version": "3.0.91",
        "x-zse-93": "101_3_2.0",
        "x-zse-96": "2.0_{}".format(encrypt_str)
    }
    return header
