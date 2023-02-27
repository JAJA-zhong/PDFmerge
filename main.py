# !/usr/bin/python3.7
# coding:utf-8
# 合并PDF文件
# pip install PyPDF2 -i https://pypi.tuna.tsinghua.edu.cn/simple
import os
import time

from PyPDF2 import PdfFileMerger, PdfFileReader,PdfFileWriter


# 格式化时间
def get_datetime():
    return time.strftime('%Y%m%d%H%M%S')


class PDFmerge:
    def __init__(self, pdfiles):
        self.pdfiles = pdfiles

    def run(self):
        # 获取指定目录下的所有PDF文件并组成列表
        pdf_lst = [files for files in os.listdir(self.pdfiles) if files.endswith('.pdf')]
        print(pdf_lst)
        # 生成PDF文件目录地址并组成列表并去除水印文件
        pdfadd_lst = [os.path.join(target_path, filename) for filename in pdf_lst if filename !="watermark.pdf"]
        print(pdfadd_lst)
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
        print("PDF合并完成。")
        return f'合并文件_{get_datetime()}.pdf'

    def add_watermark(self,pdf_file_in, pdf_file_mark, pdf_file_out):#输入文件，水印文件，输出文件
        """把水印添加到pdf中"""
        pdf_output = PdfFileWriter()
        input_stream = open(pdf_file_in, 'rb')
        pdf_input = PdfFileReader(input_stream, strict=False)
        # 获取PDF文件的页数
        pageNum = pdf_input.getNumPages()
        # 读入水印pdf文件
        pdf_watermark = PdfFileReader(open(pdf_file_mark, 'rb'), strict=False)
        # 给每一页打水印
        for i in range(pageNum):
            page = pdf_input.getPage(i)
            page.mergePage(pdf_watermark.getPage(0))
            page.compressContentStreams()  # 压缩内容
            pdf_output.addPage(page)
        pdf_output.write(open(pdf_file_out, 'wb'))
        print("水印合并完成。")


if __name__ == "__main__":
    # 获取目录下所有PDF文件
    target_path = input("指定PDF文件目录，当前目录按回车：")
    if target_path:
        pass
    else:
        target_path = './'
    pdfmerger = PDFmerge(target_path)
    pdf_file_in=pdfmerger.run()
    pdf_file_mark=f'{target_path}watermark.pdf'
    water_file=f"{target_path}水印文件_{pdf_file_in[-18:]}"
    water_path=input("是否添加水印(1)：")
    if water_path=='1':
        print(f"{target_path}{pdf_file_in}", pdf_file_mark, water_file)
        pdfmerger.add_watermark(f"{target_path}{pdf_file_in}",pdf_file_mark,water_file)
