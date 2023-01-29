# !/usr/bin/python3.7
# coding:utf-8
# 合并PDF文件
# pip install PyPDF2 -i https://pypi.tuna.tsinghua.edu.cn/simple
import os
import time

from PyPDF2 import PdfFileMerger


# 格式化时间
def get_datetime():
    return time.strftime('%Y%m%d%H%M%S')


class PDFmerge:
    def __init__(self, pdfiles):
        self.pdfiles = pdfiles

    def run(self):
        # 获取指定目录下的所有PDF文件并组成列表
        pdf_lst = [f for f in os.listdir(self.pdfiles) if f.endswith('.pdf')]
        # 生成PDF文件目录地址并组成列表
        pdfadd_lst = [os.path.join(target_path, filename) for filename in pdf_lst]
        # 实例化
        file_merger = PdfFileMerger(strict=False)
        # 初始化页数
        page = 0
        for pdf in pdfadd_lst:
            # 判断文件页码，从0页开始
            if page < 1:
                file_merger.append(pdf)
            else:
                # 文件页码大于0，从最后页插入新文件
                file_merger.merge(page, pdf)
            page += 1
            time.sleep(0.1)
        # 写入合并文件
        file_merger.write(f'合并文件_{get_datetime()}.pdf')


if __name__ == "__main__":
    # 获取目录下所有PDF文件
    target_path = input("指定PDF文件目录，当前目录按回车：")
    if target_path:
        pass
    else:
        target_path = './'
    pdfmerger = PDFmerge(target_path)
    pdfmerger.run()
