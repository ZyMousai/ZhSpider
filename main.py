"""zh spider 入口"""
from core.handle_file import HandleFile
from core.spider import ZhSpider


def main():
    # 1. 获取模式 并且整理url

    while True:
        print("1.单链接模式")
        print("2.文件导入批量模式,(读取文件路径为：./template/zh.template)")
        spider_mode = input("请输入想要的爬虫模式：")
        if spider_mode in ["1", "2"]:
            print(f"----程序获取到的模式为：{spider_mode}")
            if spider_mode == "1":
                url = input("请输入链接：")
                urls = [url]
            else:
                print("----开始批量读取")
                urls = HandleFile.read_file()
            break
        else:
            print("****输入有误，请重新输入")

    print("----开始运行。。。")

    # 2. 开始爬取
    ax = ZhSpider()
    ax.run(urls)
    # 3. 输出


if __name__ == '__main__':
    main()
