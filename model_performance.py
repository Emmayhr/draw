import sys
from statistics import mean

sys.path.append('../')
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from db import *


def get_evaluation_result_port():
    result = {
              'AUC': [],
              'Precision': [],
              'F1': [],
              'Recall': []
              }
    try:
        windows = 540
        for port_num in range(3, 33, 3):
            auc_list = []
            precision_list = []
            f1_list = []
            recall_list = []

            res = Evaluation_result.select(fn.AVG(Evaluation_result.AUC), fn.AVG(Evaluation_result.F1),
                                           fn.AVG(Evaluation_result.Recall), fn.AVG(Evaluation_result.Precision)).where(
                (Evaluation_result.port_num == port_num) & (Evaluation_result.continue_time == windows))
            print(res.dicts()[0])
            result['AUC'].append(res.dicts()[0]['AUC'])
            result['Precision'].append(res.dicts()[0]['Precision'])
            result['F1'].append(res.dicts()[0]['F1'])
            result['Recall'].append(res.dicts()[0]['Recall'])

        print(result)


    except Exception as e:
        print(e)
        return


def draw_bars(result):
    x = np.arange(len(result['windows']))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x, height=result['AUC'], width=width, label='Men', color='whitesmoke', linestyle='-',
                    linewidth='0.5', edgecolor='black', align='center')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('AUC')
    # ax.set_title('Scores by group and gender')
    ax.set_xticks(x)
    ax.set_xticklabels(result['windows'])
    ax.legend()
    # ax.axis('off')
    autolabel(rects1, ax)
    plt.ylim(top=0.983, bottom=0.975)
    plt.show()

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, height=result['Precision'], width=width, label='Men', color='whitesmoke', linestyle='-',
                    linewidth='0.5', edgecolor='black', align='center')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Precision')
    # ax.set_title('Scores by group and gender')
    ax.set_xticks(x)
    ax.set_xticklabels(result['windows'])
    ax.legend()
    # ax.axis('off')
    autolabel(rects1, ax)
    plt.ylim(top=0.93, bottom=0.86)
    plt.show()

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, height=result['F1'], width=width, label='Men', color='whitesmoke', linestyle='-',
                    linewidth='0.5', edgecolor='black', align='center')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('F1')
    # ax.set_title('Scores by group and gender')
    ax.set_xticks(x)
    ax.set_xticklabels(result['windows'])
    ax.legend()
    # ax.axis('off')
    autolabel(rects1, ax)
    # plt.ylim(top = 0.93, bottom = 0.86)
    plt.show()


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


get_evaluation_result_port()

