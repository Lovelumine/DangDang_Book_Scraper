import csv
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

# 存储所有图书的信息


def save_to_csv(books_info):
    Tk().withdraw()  # 关闭Tk的主窗口
    filename = asksaveasfilename(defaultextension=".csv")  # 弹出保存文件对话框
    if not filename:  # If the user cancelled the dialog
        return
    try:  # 如果用户输入了文件名
        # 将所有书的信息写入CSV文件
        with open(filename, 'w', newline='', encoding='gbk', errors='ignore') as csvfile:
            fieldnames = ['书名', '作者', '出版社', '定价', 'ISBN', '出版时间', '内容']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for book_info in books_info:
                writer.writerow(book_info)
    except PermissionError:
        print("文件保存失败，可能是由于文件已经被其他程序打开，或者没有足够的权限来保存文件。请重新选择文件路径。")
        save_to_csv()  # 如果保存失败，重新调用函数让用户选择文件路径
