#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import sys, getopt
import matplotlib.pyplot as plt
import numpy as np

# 显示帮助信息
def disp_help():
    print 'This is a pyhton template preforming the least squares polynomial fit of a set of data points or multiple sets. \
For more information please go to the offical site of matplotlib "http://matplotlib.org/"\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)\n\
Usage: pyplot-polyfit -i<inputfile> -o<outputfile>|-s [-j<head-record>] [-p<deg>] [-r<rmin>,<ramx>] [-d<x-row>,<y-row1>,<y-row2>,...] [-l<legend>,...] [-a<x-label>,<y-label>]\n\
-i --ifile\tinput-file name (*.txt *.xyz *.dat)\n\
-d --data-line\tselect x row and y rows, the default is 0 for x, 1 for y\n\
-j --jump-head\tskip head records as indicated by the parameter, the default is zero\n\
-p --polynomial\tdegree of the fitting polynomial, the default value is 1\n\
-r --rows\tset begining and ending rows of data that used to plot, the default will use all data\n\
-o --ofile\toutput-file name (*.jpg *.png *.pdf *.eps ...)\n\
-l --legend\tset data legends, the default is \'data\'. The number of legends must equal the number of y rows\n\
-a --axis-label\tset x and y axises\' labels, the default are \'x\' and \'y\'\n\
-s --screen\tonly show the figure on screen and do not save the figure\n\
-h --help\tshow this information'

def plot_lines(infile,outfile,lines,rows,degrees,sline,legend,labels,ifSavefig):
    # 按行读取文件 从sline开始按空格分割数据
    file = open(infile,'r')
    lineList = file.readlines()
    lineList = [line.strip().split( ) for line in lineList[sline:]]
    file.close()
    # 初始化数组 默认第一列为x轴
    if rows[0] == -1:
        xValues = np.zeros(len(lineList))
        xValues = map(float,[x[lines[0]] for x in lineList])
        yValues = np.zeros((len(lineList),len(lines)-1))
    else:
        xValues = np.zeros(len(lineList[rows[0]:rows[1]]))
        xValues = map(float,[x[lines[0]] for x in lineList[rows[0]:rows[1]]])
        yValues = np.zeros((len(lineList[rows[0]:rows[1]]),len(lines)-1))
    # 按lines提取lineList中的特定列
    if rows[0] == -1:
        count = 0
        for l in map(int,lines[1:]):
            for h in range(len(lineList)):
                yValues[h][count] = float(lineList[h][l])
            count += 1
    else:
        count = 0
        for l in map(int,lines[1:]):
            for h in range(len(lineList[rows[0]:rows[1]])):
                yValues[h][count] = float(lineList[h+rows[0]][l])
            count += 1
    # 确定拟合多项式 循环绘图 按legend绘制图例
    for f in range(len(lines)-1):
        fig, screen = plt.subplots()
        if rows[0] == -1:
            oneY = np.zeros(len(lineList)) #创建Y数组和fit数组
            fitY = np.zeros(len(lineList))
        else:
            oneY = np.zeros(len(lineList[rows[0]:rows[1]])) #创建Y数组和fit数组
            fitY = np.zeros(len(lineList[rows[0]:rows[1]]))

        oneY = map(float,[x[f] for x in yValues])
        # 执行多项式拟合
        polyline = np.poly1d(np.polyfit(xValues,oneY,degrees))
        fitY = polyline(xValues)
        # 计算均方根
        diff = np.sqrt(np.sum((oneY-fitY)**2))
        # 绘图
        screen.plot(xValues,oneY,'-',label=legend[f])
        screen.plot(xValues,fitY,'--',label=legend[f]+"-polyfit")
        # 定位显示均方根的位置
        xMin = np.min(xValues)
        xMax = np.max(xValues)
        yMin = np.min(oneY)
        yMax = np.max(oneY)
        screen.text(xMin+0.618*(xMax-xMin),yMin+0.618*(yMax-yMin),"RMS = "+str(diff))
        screen.legend(loc='upper right', fontsize='large')
        # 按label绘制轴的单位
        screen.set_xlabel(labels[0])
        screen.set_ylabel(labels[1])
        # 绘制图名
        plt.title(infile)
        if not ifSavefig: fig.savefig(outfile[f])
    plt.show()

def main(argv):
    # 定义参数初始值
    inputfile = ''
    outputfile = ''
    onlyScreen = False
    dataLine = [0,1]
    dataRow = [-1,-1]
    dataLegend = ['data']
    axisLabel = ['x','y']
    startLine = 0
    polydeg = 1
    # 提取命名行参数
    try:
        opts, args = getopt.getopt(argv,"hi:o:sj:d:l:a:r:p:",["help","ifile=","ofile=","screen","jump-head=","data-line=","legend=","axis-label=","rows=","polynomial="])
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
            outputfile = map(str,arg.strip().split(','))
        elif opt in ("-s", "--screen"):
            onlyScreen = True
        elif opt in ("-j", "--jump-head"):
            startLine = int(arg)
        elif opt in ("-p", "--polynomial"):
            polydeg = int(arg)
        elif opt in ("-r", "--rows"):
            dataRow = map(int,arg.strip().split(','))
        elif opt in ("-d", "--data-line"):
            dataLine = map(int,arg.strip().split(','))
        elif opt in ("-l", "--legend"):
            dataLegend = map(str,arg.strip().split(','))
        elif opt in ("-a", "--axis-label"):
            axisLabel = map(str,arg.strip().split(','))
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
    plot_lines(inputfile,outputfile,dataLine,dataRow,polydeg,startLine,dataLegend,axisLabel,onlyScreen)

if __name__ == "__main__":
    main(sys.argv[1:])