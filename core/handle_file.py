"""操作输入和输出"""
import pandas


class HandleFile(object):
    def __init__(self):
        pass

    @staticmethod
    def read_file():
        p = pandas.read_excel("../template/zh.xlsx")
        return [row for index, row in p.itertuples()]

    def writ_file(self):
        pass
