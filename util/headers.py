import json
import os
import random
from urllib.parse import quote
import requests
import hashlib
import execjs

# user_agents = [
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"]

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



def gen_header(url_part,d_c0='"AHCfcI0r9BKPTowWLggkfMGi5uRMk3Xf-rw=|1618403625"', is_signature=True):
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
        # 'cookie': 'd_c0={}'.format(d_c0),
        # "x-api-version": "3.0.91",
        # "accept":"*/*",
        # "accept-encoding":"gzip, deflate, br",2.0_aXY8c7X06M2pS_F0ZCFqNgeqcLxxHqtqzBO8Ser0SXOf
        # "accept-language":"zh-CN,zh;q=0.9",
        # "accept":"",
        # "sec-ch-ua-platform": "Windows",
        # "referer":"https://www.zhihu.com/people/chen-shao-neo/answers",
        # "sec-ch-ua-mobile": "?0",
        # "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        # "sec-fetch-dest": "empty",
        # "x-ab-pb":"CtoBOwIpBZQGaQHBBHwGVgxSCz8AZASiBkAB4AQUBWALGwAzBVIFVQUwBsIFQQaEAtgFKgZ9AvMDDgU0DIkM+AO0Ck8DQgTXC7ULjASABewK4AtWBasGWwYHDKEDtwOmBBwGdQQRBTEGfwUBBlwGjQQYBtcC6QSyBecFxgYBC0cAtABABuQKFQUZBYkGPwamBlADogOxBeMFOQbcCyoDMgM0BIwFrAbMAs8LNwz0AwoERQQ3BXQBCwTaBDIFngX0C0MAagF+BrkCDwvYAqADUQUKBhYGmwszBFcEiwUSbQAAAAAAAAEBAAEAAQICAAACAAAAAAAAAAABAAAAAAEAAAMAAwQAAQAAAAABAAAAAAAAAAAAAAQAAAEKAAAAAAAAAAIAAQEAAAADAAAAAgAAAAEACwEAAQAEAAABAAEAFQAAFQEAAAEBAAAAAQA=",
        # "sec-fetch-dest": "empty",
        # "sec-fetch-mode": "cors",
        # "sec-fetch-site":"same-origin",
        # "x-requested-with":"fetch",
        "x-zse-93": "101_3_2.0",
        "x-zse-96": "2.0_{}".format(encrypt_str)
        # "x-zse-96": "2.0_aXY8c7X06M2pS_F0ZCFqNgeqcLxxHqtqzBO8Ser0SXOf"
    }
    return header

if __name__ == '__main__':
    headers = gen_header(
        "/api/v4/members/chen-shao-neo/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,excerpt,is_labeled,label_info,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,is_recognized;data[*].vessay_info;data[*].author.badge[?(type=best_answerer)].topics;data[*].author.vip_info;data[*].question.has_publishing_draft,relationship&offset=0&limit=20&sort_by=created",
        "")