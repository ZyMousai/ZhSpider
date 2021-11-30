"""操作输入和输出"""
import pandas as pd
import os


class HandleFile(object):
    def __init__(self):
        pass

    @staticmethod
    def read_file():
        p = pd.read_excel("./template/zh.xlsx")
        return [row for index, row in p.itertuples()]

    def writ_file(self, data, file_name):
        _cur_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        account_info_path = os.path.join(_cur_dir, "results/{}.xlsx".format(file_name))
        if os.path.exists(account_info_path):
            vaildip_data = pd.read_excel(account_info_path)
            append_data = vaildip_data.append(data, ignore_index=True)
            append_data.to_excel(account_info_path, index=False)
        else:
            pd_data = pd.DataFrame(data)
            pd_data.to_excel(account_info_path, index=False)

