"""zh spider 入口"""
from core.handle_file import HandleFile
from core.spider import ZhSpider
import os


def main():
    # 1. 获取模式 并且整理url

    while True:
        print("1.单链接模式")
        print("2.文件导入批量模式,(读取文件路径为：./template/zh.xlsx)")
        print("cookie文件请放入./template/路径下,名字为cookie.txt")
        spider_mode = input("请输入想要的爬虫模式：")
        if spider_mode in ["1", "2"]:
            print(f"----程序获取到的模式为：{spider_mode}")
            if os.path.exists("./template/cookie.txt"):
                with open('./template/cookie.txt', "r", encoding="utf-8") as f:
                    cookie = f.read()
                if spider_mode == "1":
                    url = input("请输入链接:")
                    urls = [url]
                else:
                    print("----开始批量读取")
                    urls = HandleFile.read_file()
                break
            else:
                print("请尽快放入cookie文件到指定目录中")
                continue
        else:
            print("****输入有误，请重新输入")

    print("----开始运行。。。")
    print("----开始读取cookie-----")
    # 2. 开始爬取
    ax = ZhSpider()
    ax.run(urls, cookie)


if __name__ == '__main__':
    main()
