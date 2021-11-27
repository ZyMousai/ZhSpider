"""zh spider 核心爬虫"""
import requests
from util.headers import gen_header
from lxml import etree
import json


class ZhSpider(object):

    def __init__(self):
        pass

    def zhihui_user_info_spider(self, url):
        url = "https://www.zhihu.com/people/chen-shao-neo"
        # headers = gen_header()
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "cookies": '_xsrf=Q3z0aZyl1V0QtE2Cgh10mewWEGOiZGuZ; _zap=9d18523a-fdaa-47cf-ba87-7ed9e4ededae; d_c0="AJCQRMQFsBOPTi8EM_O35D-gKCa_1Uu9Sc4=|1631010186"; ISSW=1; l_n_c=1; o_act=login; r_cap_id="N2NjY2ZiMTc5Y2E3NDBhZGJjODdhNWZmNGRiNDljOTU=|1637895868|de25f1c3ae4632e326c1a198895af8cf2e5d0974"; cap_id="MWUzNGUxNmFkMWEzNDVhNGE3MzU5MGJmMzkxZGQ1NTE=|1637895868|f3b324cc3650256f691b29d11785fa5484d45121"; l_cap_id="N2I1ODRmZWIzMTg4NGI0YTllN2VhNDE5Y2MwMzBmMWE=|1637895868|a40ab4f643dfb59ad6a7e919efeeacd1d28c1959"; n_c=1; z_c0="2|1:0|10:1637896321|4:z_c0|92:Mi4xVjFSSkF3QUFBQUFBa0pCRXhBV3dFeVlBQUFCZ0FsVk5nSjZOWWdDcDJtWE9vaXo2LWhvdHVQSWpZV0s4dlhEWWxB|4d28da47cf209b373e909c404409f7dcfce255642f09e0ff32ba206ffd5a57a1"; captcha_session_v2="2|1:0|10:1637896870|18:captcha_session_v2|88:ZzA3U2pLNTAzdUtLMS9qTjNtaTFvQkcrNm9DQjIxci9sbTlkZkVJczEzcERSNTRTQi92Sm9GOStuek9RayswZA==|064adc71a81dad37d07147335e06ade67ac615eea65aa31692d3427e6404f2ec"; captcha_ticket_v2="2|1:0|10:1637896884|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfckRvUTF2NkFoUUZHNE15aVJqb1hjenQwUDJlQTdEd1lxcmp3UF84RUhwODZpckJIenVMeUV0c0d5d05wV0tsQUs2Q29ZR1hrZjBDMDdSMWVmR2dTS3VMeDQ3ZnFIX01OR3pnWmVzNjBrbkRybHNDNkg0Vmg4QmxuWXNDVk1GSm03SnBGRDlDb3g0Wk43eXdOSFNSNk5ZMEwwNlhRY08uc3o0WUJyZVV2bzVwX1dqbGpRelhPSlI1VUpacWJneEkuN0Fua2VCYVdncXZRcS5YemYxeUVjRE9xU1QuTmV1VWN4cGFET3dnSWppazg4bnRnd1h6V21wcEZDUWE2RGVMZUNkNERUTEI5VFJqUWhsLmItYkRlOUtMTUpGVEZQdEVxcGtwaXJzRlYtZUNDMWxfd1c4dXQ0VHhKdy1sS2guNjg0aDF6Tnc4ZjJ4ZUg5aV9RZGg3WkV2T21senBSZU1PMnctWTRwSS5NaVVDbW9jcnBBT0hzbTIwbEY4OFouWXRiU0tIWFVMMkIwSUpLNkJWcS1FVThUMTRVMHlvaENPQ0gxdlpta284Umhhb3guQjJqQzVZSHdYZjJiTnBJLXJWbHBhaEt6dXprQjV5cFJzT0JGejFhZ09zSHhVOUFCb2Nxbk5Ic1NYOGQ3MGxVQUYuN24xUWhFc0hLU2FwMyJ9|822582ea9962fd09ccb07c3d0946bc3c7cbbcf8216db13e1737348966752e5eb"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1637551899,1637803777,1637894009,1637994569; KLBRSID=57358d62405ef24305120316801fd92a|1637995065|1637994567; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1638009464; NOT_UNREGISTER_WAITING=1'
        }
        req = requests.get(url, headers=headers)
        comtent = etree.HTML(req.text)
        user_info = comtent.xpath('//*[@id="js-initialData"]/text()')[0]
        user_info_json = json.loads(user_info)
        people_info = list(user_info_json["initialState"]["entities"]["users"].values())[0]
        account_name = people_info["name"]
        employment_record = [{"job_name": i["job"]["name"], "company_name": i["company"]["name"]} for i in
                             people_info["employments"]]
        description = people_info['description']
        followersCount = people_info['followerCount']
        # 点赞总数
        like_total_count = people_info['voteupCount']
        authentication_info = people_info['badgeV2']["mergedBadges"][0]["description"]
        articles_count = people_info['articlesCount']
        answer_count = people_info['answerCount']

        print(account_name, employment_record, description, followersCount, like_total_count, authentication_info,
              articles_count, answer_count)
        # print(req.text)

    def run(self, urls):
        if len(urls) >= 10:
            thread_num = 10
        else:
            thread_num = len(urls)


if __name__ == '__main__':
    zs = ZhSpider()
    zs.zhihui_user_info_spider("")
