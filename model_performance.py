import sys
from statistics import mean

sys.path.append('../')
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from db import *


def get_evaluation_result_port(ceil_rate):
    result = {
        'AUC': [],
        'Precision': [],
        'F1': [],
        'Recall': []
    }
    try:
        windows = 540
        for port_num in range(3, 33, 3):
            res = Evaluation_result.select(fn.AVG(Evaluation_result.AUC), fn.AVG(Evaluation_result.F1),
                                           fn.AVG(Evaluation_result.Recall), fn.AVG(Evaluation_result.Precision)).where(
                (Evaluation_result.port_num == port_num) & (Evaluation_result.continue_time == windows) &
                (Evaluation_result.ceil_rate > ceil_rate - 0.05) & (Evaluation_result.ceil_rate < ceil_rate + 0.05))
            result['AUC'].append(res.dicts()[0]['AUC'])
            result['Precision'].append(res.dicts()[0]['Precision'])
            result['F1'].append(res.dicts()[0]['F1'])
            result['Recall'].append(res.dicts()[0]['Recall'])
        return result
    except Exception as e:
        print(e)
        return None


def get_evaluation_result_windows(ceil_rate, threshold):
    result = {
        'AUC': [],
        'Precision': [],
        'F1': [],
        'Recall': []
    }
    try:
        port_num = 20
        for windows in range(120, 960, 60):
            res = Evaluation_result.select(fn.AVG(Evaluation_result.AUC), fn.AVG(Evaluation_result.F1),
                                           fn.AVG(Evaluation_result.Recall), fn.AVG(Evaluation_result.Precision)).where(
                (Evaluation_result.port_num == port_num) & (Evaluation_result.continue_time == windows) &
                (Evaluation_result.ceil_rate > ceil_rate - 0.05) & (Evaluation_result.ceil_rate < ceil_rate + 0.05) &
                (Evaluation_result.threshold > threshold - 0.05) & (Evaluation_result.threshold < threshold + 0.05))
            print(res)
            result['AUC'].append(res.dicts()[0]['AUC'])
            result['Precision'].append(res.dicts()[0]['Precision'])
            result['F1'].append(res.dicts()[0]['F1'])
            result['Recall'].append(res.dicts()[0]['Recall'])
        return result
    except Exception as e:
        print(e)
        return None


def draw_bars_port(result, x):
    width = 1  # the width of the bars
    ax = plt.subplot(2, 2, 1)
    ax.set_ylabel('AUC')
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    plt.ylim(top=1, bottom=0.5)
    rects1 = ax.bar(x, height=result['AUC'], width=width, color='whitesmoke', linestyle='-',
                    linewidth='0.5', edgecolor='black', align='center')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax = plt.subplot(2, 2, 2)
    ax.set_ylabel('Precision')
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    plt.ylim(top=1, bottom=0.5)
    rects1 = ax.bar(x, height=result['Precision'], width=width, color='whitesmoke', linestyle='-',
                    linewidth='0.5', edgecolor='black', align='center')

    ax = plt.subplot(2, 2, 3)
    ax.set_ylabel('F1')
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    plt.ylim(top=1, bottom=0.5)
    rects1 = ax.bar(x, height=result['F1'], width=width, color='whitesmoke', linestyle='-',
                    linewidth='0.5', edgecolor='black', align='center')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax = plt.subplot(2, 2, 4)
    ax.set_ylabel('Recall')
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    plt.ylim(top=1, bottom=0.5)
    rects1 = ax.bar(x, height=result['Recall'], width=width, color='whitesmoke', linestyle='-',
                    linewidth='0.5', edgecolor='black', align='center')
    plt.show()


def draw_bars_windows(result, x):
    print(result['AUC'])
    print(x)
    width = 54  # the width of the bars
    # ax = plt.subplot(2, 2, 1)
    ax = plt.subplot()
    ax.set_ylabel('ACC')
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    plt.ylim(top=0.84, bottom=0.76)
    rects1 = ax.bar(x, height=result['AUC'], width=width, color='whitesmoke', linestyle='-',
                    linewidth='0.5', edgecolor='black', align='center')
    plt.show()

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax = plt.subplot(2, 2, 2)
    ax = plt.subplot()
    ax.set_ylabel('Precision')
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    plt.ylim(top=0.75, bottom=0.6)
    rects1 = ax.bar(x, height=result['Precision'], width=width, color='whitesmoke', linestyle='-',
                    linewidth='0.5', edgecolor='black', align='center')
    plt.show()

    ax = plt.subplot()
    ax.set_ylabel('F1')
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    plt.ylim(top=1, bottom=0.6)
    rects1 = ax.bar(x, height=result['F1'], width=width, color='whitesmoke', linestyle='-',
                    linewidth='0.5', edgecolor='black', align='center')
    plt.show()

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax = plt.subplot(2, 2, 4)
    ax = plt.subplot()
    ax.set_ylabel('Recall')
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    plt.ylim(top=0.76, bottom=0.6)
    rects1 = ax.bar(x, height=result['Recall'], width=width, color='whitesmoke', linestyle='-',
                    linewidth='0.5', edgecolor='black', align='center')
    plt.show()


# port_avr_list = get_evaluation_result_port(0.2)
# draw_bars_port(port_avr_list, np.arange(3, 33, 3))
windows_avr_list = get_evaluation_result_windows(0.2, threshold=0.3)
draw_bars_windows(windows_avr_list, np.arange(120, 960, 60))
