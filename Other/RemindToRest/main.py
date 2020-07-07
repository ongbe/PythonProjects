#!usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import *
import time


def show_message():
    root = Tk()  # 建立主窗口
    root.title("Tips")
    root.withdraw()  # 隐藏窗口

    # 获取屏幕的宽度和高度，并且在高度上考虑到底部的任务栏，为了是弹出的窗口在屏幕中间
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight() - 100
    root.resizable(False, False)

    # 添加组件
    frame = Frame(root, relief=RIDGE, borderwidth=3)
    frame.pack(fill=BOTH, expand=1)  # pack() 放置组件若没有则组件不会显示

    # 窗口显示的文字、并设置字体、字号
    label = Label(frame, text="你已经工作 1 个小时了，请休息一下吧！", font="微软雅黑 -25 bold")
    label.pack(fill=BOTH, expand=1)

    # 设置按钮
    button = Button(frame, text="OK", font="微软雅黑 -25 bold", fg="red", command=root.destroy)
    button.pack(side=BOTTOM)

    root.update_idletasks()
    root.deiconify()  # 计算窗口的大小
    root.withdraw()  # 再次隐藏窗口，防止窗口出现被拖动的感觉

    root.geometry('%sx%s+%s+%s' % (root.winfo_width() + 10, root.winfo_height() + 10,
                                   int((screenwidth - root.winfo_width()) / 2),
                                   int((screenheight - root.winfo_height()) / 2)))
    root.deiconify()
    root.mainloop()


if __name__ == '__main__':
    times = 1
    while True:
        if times % 3600 == 0:  # 每隔 1 个小时提醒一次，可以根据你自己的需求更改
            show_message()
        time.sleep(1)
        times += 1
