#!usr/python 3/bin
# -*- coding: utf-8 -*-
'''
脚本功能：计算y轴每个能量值下有每条能带有多少个交点，并导出数据
'''
import re
import numpy as np
import csv


def get_each_line_data(file_path):
    file = open(file_path, 'r')
    lines = file.readlines()
    k_points = int(re.search(r'\d+', lines[0])[0])  # 获取k点数值
    fermi_energy = float(
        re.search(r'[-+]?[0-9]*\.?[0-9]+', lines[4])[0])  # 获取费米能级数值

    lines = lines[9:]
    k_point_index = 1
    bulk_list = []
    while k_point_index <= k_points:
        bulk_data = lines[62 * (k_point_index - 1) + 2:
                          62 * (k_point_index - 1) + 62]
        bulk = {
            'k_point_index': k_point_index,
            'energy_data': bulk_data
        }
        k_point_index += 1
        bulk_list.append(bulk)

    max_energy_list = []
    min_energy_list = []
    for bulk in bulk_list:
        bulk['energy_data'] = [round(
            (float(each.strip()) - fermi_energy) * 27.2114, 6) for each in bulk['energy_data']]
        max_energy_list.append(max(bulk['energy_data']))
        min_energy_list.append(min(bulk['energy_data']))
    max_energy = round(float(max(max_energy_list)), 6)
    min_energy = round(float(min(min_energy_list)), 6)

    line_data = []
    lines_data = []
    # len(bulk_list[0]['energy_data']为每个k点下的点数
    for row_index in range(len(bulk_list[0]['energy_data'])):
        for column_index in range(k_points):
            line_data.append(bulk_list[column_index]['energy_data'][row_index])
        lines_data.append([each for each in line_data]
                          )  # 不能直接用append(line_data)
        line_data.clear()  # 每次将line_data加进lines_data后要清除数据以进行下次操作

    file.close()
    return lines_data, min_energy, max_energy


def get_intersection_point_number(lines_array, energy_values):
    result = []
    total_intersection_point_number = 0
    write_header()
    print('')
    for each_energy in energy_values:
        intersection_point_number = 0
        for array in lines_array:
            for i in range(len(array) - 1):
                if array[i] < array[i + 1]:
                    if array[i] <= each_energy and each_energy <= array[i + 1]:
                        print('{} <--{}--> {}'.format(array[i], array[i + 1], each_energy))
                        intersection_point_number += 1
                        total_intersection_point_number += 1
                else:
                    if array[i] >= each_energy and each_energy >= array[i + 1]:
                        print('{} <--{}--> {}'.format(array[i], array[i + 1], each_energy))
                        intersection_point_number += 1
                        total_intersection_point_number += 1
        result.append({
            'energy_value': each_energy,
            'intersection_point_number': intersection_point_number
        })
        save_to_csv([[each_energy, intersection_point_number]], file_path)


def save_to_csv(content, file_path):
    with open('.' + file_path.split('/')[-1].split('.')[0] + '.csv', 'a+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(content)


def write_header():
    with open('.' + file_path.split('/')[-1].split('.')[0] + '.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows([['y值 (eV)', '交点数']])


if __name__ == '__main__':
    file_path = './Substrate_BandStr.bands'  # 指定.bands文件所在的路径
    lines_data, min_energy, max_energy = get_each_line_data(file_path)
    step = float(input('输入一个合适的步长：'))
    energy_values = [round(each, 6) for each in list(
        np.arange(min_energy, max_energy, step))]
    get_intersection_point_number(lines_data, energy_values)
