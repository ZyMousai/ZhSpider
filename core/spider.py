"""zh spider 核心爬虫"""
from concurrent.futures._base import ALL_COMPLETED, wait
import time
import requests
from util.headers import gen_header, ua_list
from lxml import etree
import json
import math
import random
from util.BoundedThreadPool import BoundedThreadPoolExecutor
from core.handle_file import HandleFile

# from concurrent.futures.thread import ThreadPoolExecutor
zhihu_spider_pool = BoundedThreadPoolExecutor(max_workers=10)


class ZhSpider(object):

    def __init__(self):
        self.hf = HandleFile()

    def zhihu_user_info_spider(self, url, cookie):
        # url = "https://www.zhihu.com/people/chen-shao-neo"
        # headers = gen_header()
        self.article_infos = {"articles": [], "answers": []}

        print("开始抓取当前url:" + url)
        headers = {
            "user-agent": random.choice(ua_list),
            "cookie": cookie
        }
        req = requests.get(url, headers=headers)
        comtent = etree.HTML(req.text)
        user_info = comtent.xpath('//*[@id="js-initialData"]/text()')[0]
        user_info_json = json.loads(user_info)
        people_info = user_info_json["initialState"]["entities"]["users"][url.split("/")[-1]]
        url_token = people_info["urlToken"]
        self.account_name = people_info["name"]
        employment_record = [{"job_name": i["job"]["name"], "company_name": i["company"]["name"]} for i in
                             people_info["employments"]]
        description = people_info['description']
        followersCount = people_info['followerCount']
        # 点赞总数
        like_total_count = people_info['voteupCount']
        if people_info['badgeV2']["mergedBadges"]:
            authentication_info = people_info['badgeV2']["mergedBadges"][0]["description"]
        else:
            authentication_info = ""
        articles_count = people_info['articlesCount']
        answer_count = people_info['answerCount']
        print("抓取{}基础信息成功！".format(self.account_name))
        user_data = {
            "账号名称": [self.account_name],
            "职业经历": [str(employment_record)],
            "个人简介": [description],
            "粉丝数": [followersCount],
            "点赞总数": [like_total_count],
            "认证状态": [authentication_info],
            "文章总数": [articles_count],
            "回答总数": [answer_count],
        }
        self.hf.writ_file(user_data, "account_info")
        self.write_data(answer_count, url_token, articles_count, cookie)

    def write_data(self, answer_count, url_token, articles_count, cookie):
        answer_pool = []
        print("开始抓取回答问题数据,总共{}页".format(str(math.ceil(answer_count / 20))))
        for i in range(math.ceil(answer_count / 20)):
            answers_url = "https://www.zhihu.com/api/v4/members/{}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cexcerpt%2Cis_labeled%2Clabel_info%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B*%5D.author.vip_info%3Bdata%5B*%5D.question.has_publishing_draft%2Crelationship&offset={}&limit=20&sort_by=created".format(
                url_token, 20 * i)
            answer_pool.append(zhihu_spider_pool.submit(self.zhihu_user_answer_info, answers_url, cookie, i))
        wait(answer_pool, return_when=ALL_COMPLETED)
        print("回答问题数据抓取成功!")
        articles_pool = []
        print("开始抓取文章数据,总共{}页".format(str(math.ceil(articles_count / 20))))
        for i in range(math.ceil(articles_count / 20)):
            articles_url = "https://www.zhihu.com/api/v4/members/{}/articles?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cexcerpt%2Cis_labeled%2Clabel_info%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B*%5D.author.vip_info%3Bdata%5B*%5D.question.has_publishing_draft%2Crelationship&offset={}&limit=20&sort_by=created".format(
                url_token, 20 * i)
            articles_pool.append(zhihu_spider_pool.submit(self.zhihu_user_articles_info, articles_url, cookie, i))
        wait(articles_pool, return_when=ALL_COMPLETED)
        print("文章数据抓取成功!")
        article_pool = []
        answers = self.article_infos['answers']
        self.article_infos['answers'] = []
        print("开始抓取回答问题文章内容,总共{}个".format(str(len(answers))))
        for i, article in enumerate(answers):
            article_pool.append(zhihu_spider_pool.submit(self.zhihu_article_info, article, cookie, i))
        wait(article_pool, return_when=ALL_COMPLETED)
        print("获取回答问题成功！")
        # print("开始获取作者回答排名") (暂时不用)
        # for index, data in enumerate(self.article_infos['answers']):
        #     self.author_answer_ranking = []
        #     author_answer_ranking_pool = []
        #     for i in range(math.ceil(data["article_answerCount"] / 5)):
        #         articles_url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&platform=desktop&sort_by=default".format(
        #             str(data["article_user_id"]), 5 * i)
        #         author_answer_ranking_pool.append(
        #             zhihu_spider_pool.submit(self.zhihu_answer_ranking, articles_url, cookie))
        #     wait(author_answer_ranking_pool, return_when=ALL_COMPLETED)
        #     answer_ranking = sorted(self.author_answer_ranking, key=lambda x: x["voteup_count"], reverse=True)
        #     for i, answer_info in enumerate(answer_ranking):
        #         if str(answer_info["user_id"]) == str(data['article_url']).split("/")[-1]:
        #             self.article_infos["answers"][index]["author_answer_ranking"] = i + 1
        # print("获取作者回答排名成功！！")
        # 3. 输出
        article_titles = []
        article_urls = []
        voteup_counts = []
        comment_counts = []
        author_answer_ranking = []
        visit_counts = []
        article_answerCounts = []
        article_follower_counts = []
        for data in self.article_infos["answers"]:
            article_titles.append(data.get("article_title", ""))
            article_urls.append(data.get("article_url", ""))
            voteup_counts.append(data.get("voteup_count", 0))
            comment_counts.append(data.get("comment_count", 0))
            author_answer_ranking.append(data.get("author_answer_ranking", 0))
            visit_counts.append(data.get("visit_count", 0))
            article_answerCounts.append(data.get("article_answerCount", 0))
            article_follower_counts.append(data.get("article_follower_count", 0))

        for data in self.article_infos["articles"]:
            article_titles.append(data.get("article_title", ""))
            article_urls.append(data.get("article_url", ""))
            voteup_counts.append(data.get("voteup_count", 0))
            comment_counts.append(data.get("comment_count", 0))
            author_answer_ranking.append(data.get("author_answer_ranking", 0))
            visit_counts.append(data.get("visit_count", 0))
            article_answerCounts.append(data.get("article_answerCount", 0))
            article_follower_counts.append(data.get("article_follower_count", 0))

        writ_data = {
            "内容标题": article_titles,
            "内容链接": article_urls,
            "点赞数": voteup_counts,
            "评论数": comment_counts,
            "作者回答排名": author_answer_ranking,
            "问题浏览量": visit_counts,
            "问题关注数": article_answerCounts,
            "问题回答数": article_follower_counts,
        }
        self.hf.writ_file(writ_data, self.account_name)

    def zhihu_user_answer_info(self, url, cookie, i):
        try:
            print("开始抓取第{}页用户回答内容".format(str(i + 1)))
            url_port = url.split(".com")[1]
            headers = gen_header(url_port)
            headers["cookie"] = cookie
            req = requests.get(url, headers=headers, timeout=15)
            answer_info_json_data = req.json()["data"]
            for json_data in answer_info_json_data:
                json_dict = {
                    "article_title": json_data["question"]['title'],
                    "article_url": "https://www.zhihu.com/question/{}/answer/{}".format(json_data["question"]['id'],
                                                                                        json_data["id"]),
                    "article_user_id": json_data["question"]['id'],
                    "voteup_count": json_data['voteup_count'],
                    'comment_count': json_data['comment_count']
                }
                self.article_infos["answers"].append(json_dict)
        except Exception as e:
            print(e)

    def zhihu_user_articles_info(self, url, cookie, i):
        try:
            print("开始抓取第{}页用户文章内容".format(str(i + 1)))
            url_port = url.split(".com")[1]
            headers = gen_header(url_port)
            headers["cookie"] = cookie
            req = requests.get(url, headers=headers, timeout=15)
            articles_info_json_data = req.json()["data"]
            for json_data in articles_info_json_data:
                json_dict = {
                    "article_title": json_data['title'],
                    "article_url": json_data['url'],
                    "voteup_count": json_data['voteup_count'],
                    'comment_count': json_data['comment_count']
                }
                self.article_infos["articles"].append(json_dict)
        except:
            pass

    def zhihu_article_info(self, article, cookie, i):
        try:
            print("开始抓取第{}页文章内容".format(str(i + 1)))
            headers = {
                "user-agent": random.choice(ua_list),
                "cookie": cookie
            }
            req = requests.get(article['article_url'], headers=headers, timeout=15)
            comtent = etree.HTML(req.text)
            user_info = comtent.xpath('//*[@id="js-initialData"]/text()')[0]
            user_info_json = json.loads(user_info)
            article_info = user_info_json["initialState"]["entities"]["questions"][str(article["article_user_id"])]
            article["visit_count"] = article_info['visitCount']
            article["article_answerCount"] = article_info['answerCount']
            article["article_follower_count"] = article_info['followerCount']
            self.article_infos["answers"].append(article)
        except:
            pass

    # def zhihu_answer_ranking(self, url, cookie):
    #     try:
    #         time.sleep(1)
    #         url_port = url.split(".com")[1]
    #         headers = gen_header(url_port)
    #         headers["cookie"] = cookie
    #         req = requests.get(url, headers=headers, timeout=15)
    #         answer_info_json_data = req.json()["data"]
    #         for json_data in answer_info_json_data:
    #             json_dict = {
    #                 "user_id": json_data['id'],
    #                 "voteup_count": json_data['voteup_count'],
    #             }
    #             self.author_answer_ranking.append(json_dict)
    #     except Exception as e:
    #         print(e)

    def run(self, urls, cookie):
        for url in urls:
            self.zhihu_user_info_spider(url, cookie)
        # if len(urls) >= 10:
        #     thread_num = 10
        # else:
        #     thread_num = len(urls)

# if __name__ == '__main__':
#     zs = ZhSpider()
# _zap=29c72fff-022b-449e-bb02-3b2a617a0ad0; d_c0="AHCfcI0r9BKPTowWLggkfMGi5uRMk3Xf-rw=|1618403625"; _9755xjdesxxd_=32; YD00517437729195%3AWM_TID=U4VYLawMe4tFRQEBERY6thCW5xjMcZFF; _xsrf=bdd0faf3-f29c-48f8-b6d0-8b00d9db95c9; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1636547336,1637502034,1638016430; gdxidpyhxdE=ThDtiXp%5CRj%2FNt%2BkQldqQP5mQ9kYJlTubQRSk1%2B27PEVG43wt%2B9crl9LWSL98bL%2Fw23VV1AZPXYrCWybQrL%2FSHyBcA7z%2BHcqkxiT50rqDbt4XHsPTrX8fIMTsNwIy6qNRTXt%5CCiEWUX8e2KLwdf9ObNWrPMe%2FbcsA%2B9UBLNcpp5RvkHha%3A1638017332139; YD00517437729195%3AWM_NI=U65x3wh2yZ4EFPa8t3R%2BGfXOsA6eUZOMAqYgh38kbhuxodUCYnTbDzibBCxmgCpvle2ClLdStneymtGRMCB01JbMilzfbgAWnWHGTIJ1VgCJr6Fp9lxUeuyF6x9rOzR6ZjE%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee97c44a86a69d83e867bc9a8ba2d55b868b8faef565f1b49883c540a7eca1bbf82af0fea7c3b92a97eafb99b27daceeb7bbb74f8690afd9f73992f58987db45b19ffa86d8528d938f92dc6dacedf88ce164b7a8a185d8499bb29c83c772abbe8ea4fb67a59dc097ef6ff29da4ade759b8b2ab9af080858e83a4c13cf396aeaeec68babaae88c45dae8988a8d7438aef9a88c242b2ea8a91bc68bc8bab96fc4ef6a8f793ce7292ea968bc837e2a3; captcha_session_v2="2|1:0|10:1638016733|18:captcha_session_v2|88:eWpsQUVzdlJaOWwvTENVVHFGNlNKWU1uT3J2c1ROR29EeUdZQlp0VjA4bk9Vcm5idW93Y1Z2RklGeWhaMUJMZg==|a7beb7de9655c9b7e73cf598813899ebb9fa839550316b12a87c27e15d763aa0"; captcha_ticket_v2="2|1:0|10:1638016741|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfd2MxcVRaZVBROFMxVndqWmo3RmVZNTVYVW1RNzE4TzZQaHBhX3Vlc21vRTZhT2RhNDllYmxBX18yV2RDdWx5T0I2dHpEb1dqZEJPZk5aV3A5ZjdYeVI1RGo2bFpGMklfTTdaMUg0cURXejRCUFJpSXI1OTh5SllwLWd5U25uRkdDMjJKUGhaTjhHUlRxVkFuRkRWbmF3NHBMUEpINWp0TXcybUtBS2t1VllKY05KcFhZUmltbVdoOUpObGFUczdJaDlCNURCTVEuVXByNHdGelV0NTdQWUpGcC5FTFJXMGxnNU81V2VubG82VnJfeWZyaXc0dGNXN0lIZDJqakM0MmgwRFE3Z3h5MmN0Z2NzQmFLRkpRbUJvOFFxdy1CVEJYbGR1ZjFzejlib1ZzNEY4MmlueS1WU2NLYlM4a0JxYnVmN1dtamg5cV9vOVVDajQxZ2RkZlFHS3hGNVI2ZDFDdU1saV9CQ2RyenBobEpwbGF2Zk1oaU5EZGpyZFk4TUM5aW9reTdsVU5pdkguRFlwck5ub3VnME1sdWhGOUdrVVR1LVpHWHNYZzVrS3pMb3hab2FnbGlNZ2FuLTZ3ejBFVHdObENoekZyRGlOV3ZLYWt5b2h4NHNYZzhOWU1vanM3ZnVhV2o0bWFoZE1CSUpNZFMySE9XeFhIWnpYMyJ9|a4f9ed4d1c834a0c353121aad139a02b9658ed81fc205004bcb0552d76f12758"; z_c0="2|1:0|10:1638016760|4:z_c0|92:Mi4xVjFSSkF3QUFBQUFBY0o5d2pTdjBFaVlBQUFCZ0FsVk4tSFNQWWdCWnU5dG44bVFWLWpyY3E3Ykh5MkRWb19GMF9B|6a2bf59a0106c8fb12ce5915a003d23d8a91bcf496b347fc76d4e45b25a42776"; unlock_ticket="ADAAezpzSAomAAAAYAJVTQAuomEEDU_dm5yTbKURZ__JDlb4Gki0mg=="; NOT_UNREGISTER_WAITING=1; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1638016858; KLBRSID=0a401b23e8a71b70de2f4b37f5b4e379|1638016961|1638016429
#     zs.zhihu_user_info_spider("https://www.zhihu.com/people/chen-shao-neo", cookie)
