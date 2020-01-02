import re
import tkinter as tk


existing_element_list = [
    {"element": "H", "mass": "1.0079"},
    {"element": "He", "mass": "4.0026"},
    {"element": "Li", "mass": "6.941"},
    {"element": "Be", "mass": "9.0122"},
    {"element": "B", "mass": "10.811"},
    {"element": "C", "mass": "12.0107"},
    {"element": "N", "mass": "14.0067"},
    {"element": "O", "mass": "15.9994"},
    {"element": "F", "mass": "18.9984"},
    {"element": "Ne", "mass": "20.1797"},
    {"element": "Na", "mass": "22.9897"},
    {"element": "Mg", "mass": "24.305"},
    {"element": "Al", "mass": "26.9815"},
    {"element": "Si", "mass": "28.0855"},
    {"element": "P", "mass": "30.9738"},
    {"element": "S", "mass": "32.065"},
    {"element": "Cl", "mass": "35.453"},
    {"element": "Ar", "mass": "39.948"},
    {"element": "K", "mass": "39.0983"},
    {"element": "Ca", "mass": "40.078"},
    {"element": "Sc", "mass": "44.9559"},
    {"element": "Ti", "mass": "47.867"},
    {"element": "V", "mass": "50.9415"},
    {"element": "Cr", "mass": "51.9961"},
    {"element": "Mn", "mass": "54.938"},
    {"element": "Fe", "mass": "55.845"},
    {"element": "Co", "mass": "58.9332"},
    {"element": "Ni", "mass": "58.6934"},
    {"element": "Cu", "mass": "63.546"},
    {"element": "Zn", "mass": "65.39"},
    {"element": "Ga", "mass": "69.723"},
    {"element": "Ge", "mass": "72.64"},
    {"element": "As", "mass": "74.9216"},
    {"element": "Se", "mass": "78.96"},
    {"element": "Br", "mass": "79.904"},
    {"element": "Kr", "mass": "83.8"},
    {"element": "Rb", "mass": "85.4678"},
    {"element": "Sr", "mass": "87.62"},
    {"element": "Y", "mass": "88.9059"},
    {"element": "Zr", "mass": "91.224"},
    {"element": "Nb", "mass": "92.9064"},
    {"element": "Mo", "mass": "95.94"},
    {"element": "Tc", "mass": "98"},
    {"element": "Ru", "mass": "101.07"},
    {"element": "Rh", "mass": "102.9055"},
    {"element": "Pd", "mass": "106.42"},
    {"element": "Ag", "mass": "107.8682"},
    {"element": "Cd", "mass": "112.411"},
    {"element": "In", "mass": "114.818"},
    {"element": "Sn", "mass": "118.71"},
    {"element": "Sb", "mass": "121.76"},
    {"element": "Te", "mass": "127.6"},
    {"element": "I", "mass": "126.9045"},
    {"element": "Xe", "mass": "131.293"},
    {"element": "Cs", "mass": "132.9055"},
    {"element": "Ba", "mass": "137.327"},
    {"element": "La", "mass": "138.9055"},
    {"element": "Ce", "mass": "140.116"},
    {"element": "Pr", "mass": "140.9077"},
    {"element": "Nd", "mass": "144.24"},
    {"element": "Pm", "mass": "145"},
    {"element": "Sm", "mass": "150.36"},
    {"element": "Eu", "mass": "151.964"},
    {"element": "Gd", "mass": "157.25"},
    {"element": "Tb", "mass": "158.9253"},
    {"element": "Dy", "mass": "162.5"},
    {"element": "Ho", "mass": "164.9303"},
    {"element": "Er", "mass": "167.259"},
    {"element": "Tm", "mass": "168.9342"},
    {"element": "Yb", "mass": "173.04"},
    {"element": "Lu", "mass": "174.967"},
    {"element": "Hf", "mass": "178.49"},
    {"element": "Ta", "mass": "180.9479"},
    {"element": "W", "mass": "183.84"},
    {"element": "Re", "mass": "186.207"},
    {"element": "Os", "mass": "190.23"},
    {"element": "Ir", "mass": "192.217"},
    {"element": "Pt", "mass": "195.078"},
    {"element": "Au", "mass": "196.9665"},
    {"element": "Hg", "mass": "200.59"},
    {"element": "Tl", "mass": "204.3833"},
    {"element": "Pb", "mass": "207.2"},
    {"element": "Bi", "mass": "208.9804"},
    {"element": "Po", "mass": "209"},
    {"element": "At", "mass": "210"},
    {"element": "Rn", "mass": "222"},
    {"element": "Fr", "mass": "223"},
    {"element": "Ra", "mass": "226"},
    {"element": "Ac", "mass": "227"},
    {"element": "Th", "mass": "232.0381"},
    {"element": "Pa", "mass": "231.0359"},
    {"element": "U", "mass": "238.0289"},
    {"element": "Np", "mass": "237"},
    {"element": "Pu", "mass": "244"},
    {"element": "Am", "mass": "243"},
    {"element": "Cm", "mass": "247"},
    {"element": "Bk", "mass": "247"},
    {"element": "Cf", "mass": "251"},
    {"element": "Es", "mass": "252"},
    {"element": "Fm", "mass": "257"},
    {"element": "Md", "mass": "258"},
    {"element": "No", "mass": "259"},
    {"element": "Lr", "mass": "262"},
    {"element": "Rf", "mass": "261"},
    {"element": "Db", "mass": "262"},
    {"element": "Sg", "mass": "266"},
    {"element": "Bh", "mass": "264"},
    {"element": "Hs", "mass": "277"},
    {"element": "Mt", "mass": "268"},
]


def main():
    def extract_element_and_number():
        '''提取每个元素和与之对应的化学计量比。'''
        _str = entry1.get()  # 获取用户输入的内容
        # x?-->匹配x字符 0 次或 1 次
        # x*-->匹配x字符0次或多次
        re_str = re.findall(r"[A-Z][a-z]?[\d+\.?\d*]*", _str)  # 将元素和化学计量比组全部匹配出来，例如 Na2, B2, S

        for i in range(len(re_str)):
            if re_str[i][-1] not in [str(x) for x in range(10)]:
                re_str[i] += "1"  # 为没有对应化学计量比的元素符号设置为 1，如 S1

        global extracted_element_list  # 设置为全局变量
        extracted_element_list = []
        for each in re_str:
            # 将上述提取到的 Na2, B2, S1之类的组再拆分成 Na 2, B 2, S 1
            element = re.findall(r"[A-Z][a-z]?", each)[0]
            num = float(re.findall(r"\d+\.?\d*", each)[0])
            extracted_element_list.append(
                {
                    "element": element,
                    "num": num
                }
            )

        return extracted_element_list

    def get_reference_value(metal_atom):
        '''判断应该取哪一个标准电极电势。'''
        if metal_atom == "Li":
            referenece_value = 3.045
            return referenece_value
        if metal_atom == "Na":
            referenece_value = 2.714
            return referenece_value
        if metal_atom == "K":
            referenece_value = 2.928
            return referenece_value
        if metal_atom == "Ca":
            referenece_value = 2.868
            return referenece_value
        if metal_atom == "Mg":
            referenece_value = 2.372
            return referenece_value
        if metal_atom == "Al":
            referenece_value = 2.069
            return referenece_value

        return None


    def calc_with_metal_atom_mass():
        '''计算考虑金属原子质量后的分子质量、比容量和能量密度（如果给出了 OCV）。'''
        OCV = entry2.get()  # 获取用户输入的开路电压值
        extracted_element_list = extract_element_and_number()
        total_mass_with_metal_atom_mass = 0
        metal_atom_num = extracted_element_list[0]["num"]  # 获得金属元素对应的化学计量比

        for each in extracted_element_list:
            extracted_element = each["element"]  # 从用户输入的化学式获取每个元素符号
            extracted_num = each["num"]  # 从用户输入的化学式获取每个元素符号的化学计量比
            for each in existing_element_list:
                existing_element = each["element"]  # 从已有的元素列表中获取元素符号

                if extracted_element == existing_element:
                    mass = extracted_num * float(each["mass"])  # 计算每个提取元素的质量
                    total_mass_with_metal_atom_mass += mass  # 计算总的分子质量

        total_mass_with_metal_atom_mass = round(total_mass_with_metal_atom_mass, 2)
        print("考虑金属质量的分子质量：", str(total_mass_with_metal_atom_mass) + "g/mol")

        # 计算比容量，公式：C=nF/M，C--比容量，n--金属原子化学计量比，F--法拉第常数，M--总的分子质量
        specific_capacity_with_metal_atom_mass = round(metal_atom_num * 26801 / total_mass_with_metal_atom_mass, 2)
        print("考虑金属质量的比容量：", str(specific_capacity_with_metal_atom_mass) + "mAh/g")

        if OCV:  # 判断用户是否输入了开路电压值（判断用户是否需要计算能量密度）
            metal_atom = extracted_element_list[0]["element"]  # 获取金属元素符号
            reference_value = get_reference_value(metal_atom)  # 获取参考标准电极电势
            # 计算能量密度
            energy_density_with_metal_atom_mass = round(specific_capacity_with_metal_atom_mass * (reference_value - float(OCV)), 2)
            print("考虑金属质量的能量密度：", str(energy_density_with_metal_atom_mass) + "mWh/g")

            text2.delete('1.0', 'end')  # 清除输出框内的数据
            text2.insert("insert", energy_density_with_metal_atom_mass)  # 在输出框内插入数据（即输出数据）

        text1.delete('1.0', 'end')
        text1.insert("insert", specific_capacity_with_metal_atom_mass)

        return None

    def calc_without_metal_atom_mass():
        '''计算不考虑金属原子质量后的分子质量、比容量和能量密度（如果给出了 OCV）。'''
        OCV = entry2.get()
        extracted_element_list = extract_element_and_number()
        total_mass_without_atom_mass = 0
        metal_atom_num = extracted_element_list[0]["num"]

        for each in extracted_element_list[1:]:
            extracted_element = each["element"]
            extracted_num = each["num"]
            for each in existing_element_list:
                existing_element = each["element"]
                if extracted_element == existing_element:
                    mass = extracted_num * float(each["mass"])
                    total_mass_without_atom_mass += mass

        total_mass_without_atom_mass = round(total_mass_without_atom_mass, 2)
        print("考虑金属质量的分子质量：", str(total_mass_without_atom_mass) + "g/mol")

        specific_capacity_without_metal_atom_mass = round(metal_atom_num * 26801 / total_mass_without_atom_mass, 2)
        print("不考虑考虑金属质量的比容量：", str(specific_capacity_without_metal_atom_mass) + "mAh/g")

        if OCV:
            metal_atom = extracted_element_list[0]["element"]
            reference_value = get_reference_value(metal_atom)
            energy_density_without_metal_atom_mass = round(specific_capacity_without_metal_atom_mass * (reference_value - float(OCV)), 2)
            print("不考虑金属质量的能量密度：", str(energy_density_without_metal_atom_mass) + "mWh/g")

            text4.delete('1.0', 'end')
            text4.insert("insert", energy_density_without_metal_atom_mass)

        text3.delete('1.0', 'end')
        text3.insert("insert", specific_capacity_without_metal_atom_mass)

        return None

    window = tk.Tk()  # 创建 GUI 窗口
    window.title("比容量、能量密度计算器")  # 设置标题
    window.geometry("700x200+400+200")  # 设置窗口大小和显示位置

    entry1 = tk.Entry(window, width=30)  # 设置第一个输入框
    entry1.grid(row=0, column=1)  # 设置输入框位置

    entry2 = tk.Entry(window, width=30)  # 设置第二个输入框
    entry2.grid(row=1, column=1)

    # tk.Label-->设置标签，tk.E设置右对齐
    label1 = tk.Label(window, text="请输入化学式，示例：Na2B2S（大小写要注意！）", font=("微软雅黑", 12))
    label1.grid(row=0, column=0, sticky=tk.E)

    label2 = tk.Label(window, text="开路电压（V）", font=("微软雅黑", 12))
    label2.grid(row=1, column=0, sticky=tk.E)

    label3 = tk.Label(window, text="考虑金属原子质量的比容量（mAh/g）", font=("微软雅黑", 12))
    label3.grid(row=2, column=0, sticky=tk.E)

    label4 = tk.Label(window, text="考虑金属原子质量的能量密度（mWh/g）", font=("微软雅黑", 12))
    label4.grid(row=3, column=0, sticky=tk.E)

    label5 = tk.Label(window, text="不考虑金属原子质量的比容量（mAh/g）", font=("微软雅黑", 12))
    label5.grid(row=4, column=0, sticky=tk.E)

    label6 = tk.Label(window, text="不考虑金属原子质量的能量密度（mWh/g）", font=("微软雅黑", 12))
    label6.grid(row=5, column=0, sticky=tk.E)

    text1 = tk.Text(window, width=30, height=1.5)  # 设置输出框宽度和高度
    text1.grid(row=2, column=1)  # 设置输出框位置

    text2 = tk.Text(window, width=30, height=1.5)
    text2.grid(row=3, column=1)

    text3 = tk.Text(window, width=30, height=1.5)
    text3.grid(row=4, column=1)

    text4 = tk.Text(window, width=30, height=1.5)
    text4.grid(row=5, column=1)

    button1 = tk.Button(  # 设置点击按钮
        window,
        text="点击计算",
        command=calc_with_metal_atom_mass)
    button1.grid(row=2, column=2, sticky=tk.W)  # 设置点击按钮位置

    button2 = tk.Button(
        window,
        text="点击计算",
        command=calc_without_metal_atom_mass)
    button2.grid(row=4, column=2, sticky=tk.W)

    window.mainloop()  # 窗口循环（不自动关闭窗口）


if __name__ == "__main__":
    main()
