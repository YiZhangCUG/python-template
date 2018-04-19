#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import sys, getopt
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import copy

# 显示帮助信息
def disp_help():
    proname = (sys.argv[0]).strip().split('/')
    print ('This a pyhton template for using matplotlib to plot a histogram figure. \
For more information please go to the offical site of matplotlib "http://matplotlib.org/"\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)\n')
    print ('Usage: '+proname[-1]+' -i<inputfile> -o<outputfile>|-s [-j<head-record>] [-n<num1>,<num2>,...] [-d<y-row1>,<y-row2>,...] [-l<legend1>,<legend2>,...] [-a<x-label>,<y-label>]\n\
-i --ifile\tinput-file name (*.txt *.xyz *.dat)\n\
-d --data-line\tselect data rows, the default is 0\n\
-j --jump-head\tskip head records as indicated by the parameter, the default is zero\n\
-o --ofile\toutput-file name (*.jpg *.png *.pdf *.eps ...)\n\
-n --bar-num\tspecify bar numbers, which should equals the number of y-rows. The default is 50\n\
-l --legend\tset data legends, the default is \'data\'. The number of legends must equal the number of y rows\n\
-a --axis-label\tset x and y axises\' labels, the default are \'value\' and \'count\'\n\
-s --screen\tonly show the figure on screen and do not save the figure\n\
-h --help\tshow this information')

def plot_lines(infile,outfile,lines,sline,legend,labels,bars,ifSavefig):
    # 按行读取文件 从sline开始按空格分割数据
    file = open(infile,'r')
    lineList = file.readlines()
    # 默认忽略#号开头的行
    lineList_orig = copy.deepcopy(lineList)
    for line in lineList_orig:
        if line.startswith('#'):
            lineList.remove(line)
    lineList = [line.strip().split( ) for line in lineList[sline:]]
    file.close()
    # 初始化yValues
    yValues = np.zeros((len(lineList),len(lines)))
    # 按lines提取lineList中的特定列
    count = 0
    for l in map(int,lines[:]):
        for h in range(len(lineList)):
            yValues[h][count] = float(lineList[h][l])
        count += 1
    #复制默认bar数量到每一个
    if len(bars) == 1 and len(lines) != 1:
        for l in range(len(lines)-1):
            bars.append(bars[0])
    #复制默认legend到每一个
    if len(legend) == 1 and len(lines) != 1:
        for l in range(len(lines)-1):
            legend.append(legend[0])
    # 循环绘图 按legend绘制图例
    fig, screen = plt.subplots()
    oneY = np.zeros(len(lineList))
    for l in range(len(lines)):
        oneY = list(map(float,[x[l] for x in yValues]))
        #screen.hist(oneY, bars[l], normed=1,label=legend[l])
        screen.hist(oneY, bars[l],label=legend[l])
    screen.legend(loc='upper right', fontsize='large')
    # 按label绘制轴的单位
    screen.set_xlabel(labels[0])
    screen.set_ylabel(labels[1])
    # 绘制图名
    plt.title(infile)
    # 显示 保存
    plt.show()
    if not ifSavefig: fig.savefig(outfile)

def main(argv):
    # 定义参数初始值
    inputfile = ''
    outputfile = ''
    onlyScreen = False
    dataLine = [0]
    dataLegend = ['data']
    axisLabel = ['value','count']
    startLine = 0
    barNum = [50]
    # 提取命名行参数
    try:
        opts, args = getopt.getopt(argv,"hi:o:sj:d:l:a:n:",["help","ifile=","ofile=","screen","jump-head=","data-line=","legend=","axis-label=","bar-num="])
    except getopt.GetoptError:
        disp_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            disp_help()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-s", "--screen"):
            onlyScreen = True
        elif opt in ("-j", "--jump-head"):
            startLine = int(arg)
        elif opt in ("-d", "--data-line"):
            dataLine = list(map(int,arg.strip().split(',')))
        elif opt in ("-n", "--bar-num"):
            barNum = list(map(int,arg.strip().split(',')))
        elif opt in ("-l", "--legend"):
            dataLegend = list(map(str,arg.strip().split(',')))
        elif opt in ("-a", "--axis-label"):
            axisLabel = list(map(str,arg.strip().split(',')))
    # 检查参数
    if inputfile == '':
        disp_help()
        sys.exit()

    if onlyScreen == False and outputfile == '':
        print("error: no ouput-file name")
        sys.exit()

    if onlyScreen == True and outputfile != '':
        print("error: -o and -s can not be used at the same time")
        sys.exit()
    # 执行函数
    plot_lines(inputfile,outputfile,dataLine,startLine,dataLegend,axisLabel,barNum,onlyScreen)

if __name__ == "__main__":
    main(sys.argv[1:])