"""zh spider 核心爬虫"""


class ZhSpider(object):

    def __init__(self):
        pass

    def run(self, urls):
        if len(urls) >= 10:
            thread_num = 10
        else:
            thread_num = len(urls)
