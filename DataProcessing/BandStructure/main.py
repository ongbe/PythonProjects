#!usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Shufei Lei"
__version__ = "0.3"


import csv
import numpy as np
from matplotlib import pyplot as plt
from tkinter import *
from tkinter import messagebox
from TkinterDnD2 import *
import re
import os


class Bands(object):
    """能带文件处理类"""
    def __init__(self, file_path, energy_step_length):
        # 如果拖进去的文件路径中含有空格会产生一对花括号{}，这里先把它删除掉
        if "{" and "}" in file_path:
            self.bands_file_path = file_path.strip("{").strip("}")
        else:
            self.bands_file_path = file_path
        self.energy_step_length = energy_step_length

    def extract_band_line(self):
        """提取能带数据"""
        bands_file_path = self.bands_file_path
        file = open(bands_file_path, "r")

        lines = file.readlines()
        k_points = int(re.search(r"\d+", lines[0])[0])  # 获取 k 点数值 (type: int)
        fermi_energy = float(
            re.search(r"[-+]?[0-9]*\.?[0-9]+", lines[4])[0])  # 获取费米能级数值 (type: float)

        tmp1 = 0
        tmp2 = 0
        global row1, row2  # row1 是截取的分界线，row2 是每个 k 点下的数据长度
        for each_line in lines:
            if "K-point     1 " != each_line[:14]:  # 从文件第一行开始计数，直到出现第一个 K-point
                tmp1 += 1
            else:
                row1 = tmp1

            if "K-point     2 " != each_line[:14]:  # 从文件第一行开始计数，直到出现第二个 K-point
                tmp2 += 1
            else:
                row2 = tmp2 - row1
                break

        lines = lines[row1:]
        k_point_index = 1
        bulk_list = []
        # 将每个 k 点下的数据从文件中分离出来
        while k_point_index <= k_points:
            bulk_data = lines[row2 * (k_point_index - 1) + 2:  # 2 是每个 k 点下第一个数据的索引值
                              row2 * (k_point_index - 1) + row2]
            bulk = {
                "k_point_index": k_point_index,
                "energy_data": bulk_data
            }
            k_point_index += 1
            bulk_list.append(bulk)

        max_energy_at_each_k_point = []
        min_energy_at_each_k_point = []
        for bulk in bulk_list:
            # print(bulk["energy_data"])
            if "Spin component 2\n" in bulk["energy_data"]:
                messagebox.showerror("错误", "自旋数不为 1，无法计算")
            bulk["energy_data"] = [round(
                (float(each.strip()) - fermi_energy) * 27.2114, 6) for each in bulk["energy_data"]]  # 将 Ha 转换为 eV
            max_energy_at_each_k_point.append(max(bulk["energy_data"]))
            min_energy_at_each_k_point.append(min(bulk["energy_data"]))

        # 最小值和最大值的精度对交点个数的获取有一点影响
        ultimate_max_energy = round(float(max(max_energy_at_each_k_point)), 6)
        ultimate_min_energy = round(float(min(min_energy_at_each_k_point)), 6)

        each_line_data = []
        lines_data = []
        # len(bulk_list[0]["energy_data"]为每个k点下的点数
        for row_index in range(len(bulk_list[0]["energy_data"])):
            for column_index in range(k_points):
                each_line_data.append(
                    bulk_list[column_index]["energy_data"][row_index])
            lines_data.append([each for each in each_line_data]
                              )  # 不能直接用append(line_data)
            each_line_data.clear()

        file.close()

        return lines_data, ultimate_min_energy, ultimate_max_energy

    def generate_energy_scan_values(self):
        """生成能量扫描值"""
        energy_values = [round(each, 6) for each in list(
            np.arange(self.extract_band_line()[1], self.extract_band_line()[2], float(self.energy_step_length)))]

        return energy_values

    def get_intersection_point_number(self):
        """获取扫描能量与每条能带的交点数"""
        results = []

        # 如果输入的路径为空，则报错
        if self.bands_file_path == "":
            messagebox.showerror("错误", "路径为空")
            return
        else:
            # 如果输入的路径不为空，但不是绝对路径，则报错
            if not os.path.isabs(self.bands_file_path):
                messagebox.showerror("错误", "请输入 .bands 文件的绝对路径")
                return
            else:
                # 如果输入的路径不为空且为绝对路径，但不存在，则报错
                if not os.path.exists(self.bands_file_path):
                    messagebox.showerror("错误", "路径不存在")
                    return
                # 如果输入的路径为绝对路径且存在，但后缀名不是 .bands ，则报错
                if self.bands_file_path.split(".")[1] != "bands":
                    messagebox.showerror("错误", "请输入后缀名为 .bands 的文件的路径")
                    return
        # 如果输入的能量扫描步长为空，则报错
        if self.energy_step_length != "":
            pass
        else:
            messagebox.showerror("错误", "请输入能量扫描的步长值，建议取值在 0.1 eV 附近")
            return

        Save(self.bands_file_path).write_header()

        for each_energy in self.generate_energy_scan_values():
            intersection_point_number = 0
            for array in self.extract_band_line()[0]:
                for i in range(len(array) - 1):
                    # 能量值有正、负，用 2 种判别进行区分
                    if array[i] < array[i + 1]:
                        if array[i] <= each_energy <= array[i + 1]:
                            intersection_point_number += 1
                    else:
                        if array[i] >= each_energy >= array[i + 1]:
                            intersection_point_number += 1
            result = {
                "energy_value": each_energy,
                "intersection_point_number": intersection_point_number
            }
            results.append(result)
            Save(self.bands_file_path).write_data([each_energy, intersection_point_number])
        messagebox.showinfo("提示", "计算完成")
        Plot.draw(results)
        Save(self.bands_file_path).save_image()


class Save(object):
    """数据保存类"""
    def __init__(self, file_path):
        self.csv_file_path = file_path.split(".")[0] + ".csv"
        self.image_file_path = file_path.split(".")[0] + ".png"

    def write_header(self):
        """写入表头"""
        with open(self.csv_file_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerows([["能量值 (eV)", "交点数"]])

    def write_data(self, content):
        """写入数据"""
        with open(self.csv_file_path, "a", newline="", encoding="utf-8") as f1:
            writer = csv.writer(f1)
            with open(self.csv_file_path, "r", newline="", encoding="utf-8") as f2:
                rows = csv.reader(f2)
                if not [row for row in rows]:
                    writer.writerrow(["Energy (eV)", "Value"])
                    writer.writerow(content)
                else:
                    writer.writerow(content)

    def save_image(self):
        """保存结果图片"""
        plt.savefig(self.image_file_path)

        if " " in self.image_file_path:
            self.image_file_path = self.image_file_path.replace(" ", "\" \"")
        os.system("start {}".format(self.image_file_path))


class Plot(object):
    """绘图类"""
    @staticmethod
    def draw(results):
        energy_values = []
        intersection_point_numbers = []
        for each in results:
            energy_value = each["energy_value"]
            intersection_point_number = each["intersection_point_number"]
            energy_values.append(energy_value)
            intersection_point_numbers.append(intersection_point_number)

        plt.cla()  # 清空图片数据
        plt.plot(energy_values, intersection_point_numbers)
        plt.xlim(energy_values[0], energy_values[-1])
        plt.ylim(-1, max(intersection_point_numbers) + 1)
        plt.xlabel("Energy (eV)")
        plt.ylabel("Intersection point numbers")
        # plt.show()


class Window(object):
    """窗口类"""
    def __init__(self):
        self.window = TkinterDnD.Tk()
        self.entry_sv = StringVar()

    def set_labels(self):
        """设置标签"""
        label1 = Label(self.window, text=".bands 文件路径：", font=("微软雅黑", 12))
        label1.grid(row=0, column=0, sticky=E)

        label2 = Label(self.window, text="扫描能量步长 (eV)：", font=("微软雅黑", 12))
        label2.grid(row=1, column=0, sticky=E)

        label3 = Label(self.window, text="（建议取值在 0.1 eV 附近）", font=("微软雅黑", 12))
        label3.grid(row=2, column=0, sticky=E)

        label4 = Label(self.window, text="注意：", font=("微软雅黑", 12))
        label4.grid(row=3, column=0, sticky=E)

        label5 = Label(self.window, text="1.本程序仅适用于 DMol 计算的结果，且自旋数必须为 1！", font=("微软雅黑", 12))
        label5.grid(row=3, column=1, sticky=W)

        label6 = Label(self.window, text="2.步长取得越小精度越高，但所需花费的时间越长！", font=("微软雅黑", 12))
        label6.grid(row=4, column=1, sticky=W)

        label7 = Label(self.window, text="3.程序计算完成后会在 .bands 文件所在的目录下生成 ", font=("微软雅黑", 12))
        label7.grid(row=5, column=1, sticky=W)

        label8 = Label(self.window, text="  .png 图片和 .csv 文件，请注意查看！", font=("微软雅黑", 12))
        label8.grid(row=6, column=1, sticky=W)

    def set_entry(self):
        """设置输入框"""
        global entry1, entry2
        self.entry_sv.set("可以直接将 .bands 文件拖进来")
        entry1 = Entry(self.window, textvar=self.entry_sv, width=60)  # .bands 文件路径输入框
        entry1.grid(row=0, column=1)
        entry1.drop_target_register(DND_FILES)
        entry1.dnd_bind("<<Drop>>", self.drop)

        entry2 = Entry(self.window, width=60)  # 扫描能量步长
        entry2.grid(row=1, column=1)

    def set_button(self):
        """设置按钮"""
        calc_button = Button(self.window,
                             text="点击计算",
                             command=lambda: Bands(entry1.get(), entry2.get()).get_intersection_point_number())
        calc_button.grid(row=2, column=1)

    def drop(self, event):
        """拖拽文件扩展"""
        self.entry_sv.set(event.data)

    def execute(self):
        """执行窗口"""
        self.window.title("计算能带交点")  # 设置窗口标题
        self.window.geometry("650x220+500+200")  # 设置窗口尺寸，550x200 表示窗口宽度x高度，+500+200表示窗口显示位置
        self.set_labels()
        self.set_entry()
        self.set_button()
        self.window.mainloop()


if __name__ == "__main__":
    window = Window()
    window.execute()
