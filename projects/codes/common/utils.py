#!/usr/bin/env python
# coding=utf-8
'''
Author: John
Email: johnjim0816@gmail.com
Date: 2021-03-12 16:02:24
LastEditor: John
LastEditTime: 2022-08-15 18:11:27
Discription: 
Environment: 
'''
import os
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import json

from matplotlib.font_manager import FontProperties  # 导入字体模块

def chinese_font():
    ''' 设置中文字体，注意需要根据自己电脑情况更改字体路径，否则还是默认的字体
    '''
    try:
        font = FontProperties(
        fname='/System/Library/Fonts/STHeiti Light.ttc', size=15) # fname系统字体路径，此处是mac的
    except:
        font = None
    return font

def plot_rewards_cn(rewards, ma_rewards, cfg, tag='train'):
    ''' 中文画图
    '''
    sns.set()
    plt.figure()
    plt.title(u"{}环境下{}算法的学习曲线".format(cfg.env_name,
              cfg.algo_name), fontproperties=chinese_font())
    plt.xlabel(u'回合数', fontproperties=chinese_font())
    plt.plot(rewards)
    plt.plot(ma_rewards)
    plt.legend((u'奖励', u'滑动平均奖励',), loc="best", prop=chinese_font())
    if cfg.save:
        plt.savefig(cfg.result_path+f"{tag}_rewards_curve_cn")
    # plt.show()
def smooth(data, weight=0.9):  
    '''用于平滑曲线，类似于Tensorboard中的smooth

    Args:
        data (List):输入数据
        weight (Float): 平滑权重，处于0-1之间，数值越高说明越平滑，一般取0.9

    Returns:
        smoothed (List): 平滑后的数据
    '''
    last = data[0]  # First value in the plot (first timestep)
    smoothed = list()
    for point in data:
        smoothed_val = last * weight + (1 - weight) * point  # 计算平滑值
        smoothed.append(smoothed_val)                    
        last = smoothed_val                                
    return smoothed

def plot_rewards(rewards,cfg,path=None,tag='train'):
    sns.set()
    plt.figure()  # 创建一个图形实例，方便同时多画几个图
    plt.title(f"{tag}ing curve on {cfg.device} of {cfg.algo_name} for {cfg.env_name}")
    plt.xlabel('epsiodes')
    plt.plot(rewards, label='rewards')
    plt.plot(smooth(rewards), label='smoothed')
    plt.legend()
    if cfg.save_fig:
        plt.savefig(f"{path}/{tag}ing_curve.png")
    if cfg.show_fig:
        plt.show()

def plot_losses(losses, algo="DQN", save=True, path='./'):
    sns.set()
    plt.figure()
    plt.title("loss curve of {}".format(algo))
    plt.xlabel('epsiodes')
    plt.plot(losses, label='rewards')
    plt.legend()
    if save:
        plt.savefig(path+"losses_curve")
    plt.show()

def save_results(dic, tag='train', path = None):
    ''' 保存奖励
    '''
    Path(path).mkdir(parents=True, exist_ok=True)
    for key,value in dic.items():
        np.save(path+'{}_{}.npy'.format(tag,key),value)
    print('Results saved！')


def make_dir(*paths):
    ''' 创建文件夹
    '''
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)


def del_empty_dir(*paths):
    ''' 删除目录下所有空文件夹
    '''
    for path in paths:
        dirs = os.listdir(path)
        for dir in dirs:
            if not os.listdir(os.path.join(path, dir)):
                os.removedirs(os.path.join(path, dir))

def save_args(args,path=None):
    # 保存参数   
    args_dict = vars(args)  
    Path(path).mkdir(parents=True, exist_ok=True) 
    with open(f"{path}/params.json", 'w') as fp:
        json.dump(args_dict, fp)   
    print("参数已保存！")
