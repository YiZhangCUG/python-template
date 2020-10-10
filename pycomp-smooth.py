#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, getopt
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack
import copy

def disp_help():
    proname = (sys.argv[0]).strip().split('/')
    print ('This is a pyhton template preforming the smooth process of a set of data points or multiple sets using the FFT transform.\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)\n')
    print ('Usage: '+proname[-1]+' -i<inputfile> -o<outputfile>|-s [-j<head-record>] [-w<window-low>,<window-high>] [-e<xmin>,<xmax>,<dx>|-f<referfile>] [-r<rmin>,<ramx>] [-d<x-row>,<y-row1>,<y-row2>,...] [-l<legend>,...] [-a<x-label>,<y-label>]\n\
-i --ifile\tinput-file name (*.txt *.xyz *.dat)\n\
-f --referfile\ttake a one columon file that indicates special locations for extrapolation\n\
-d --data-line\tselect x row and y rows, the default is 0 for x, 1 for y\n\
-j --jump-head\tskip head records as indicated by the parameter, the default is zero\n\
-w --window\tpass window the FFT transform, the minimal and maximal value is 0 and 1, respectively\n\
-e --extralimit\tthe range of extrapolation, the default with use what -r option indicates\n\
-r --rows\tset begining and ending rows of data that used to plot, the default will use all data\n\
-o --ofile\toutput-file name without extensions, the default formats are .png for figures and .txt for data\n\
-l --legend\tset data legends, the default is \'data\'. The number of legends must equal the number of y rows\n\
-a --axis-label\tset x and y axises\' labels, the default are \'x\' and \'y\'\n\
-s --screen\tonly show the figure on screen and do not save the figure\n\
-h --help\tshow this information')

def poly_extrapolate(infile,outfile,refile,lines,rows,window,sline,elimit,legend,labels,ifSavefig):
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
            # 确定插值范围 首先尝试从-e命令获取插值范围 然后再尝试从文件获取 最后使用-r指定的范围
            if elimit[0] != -1:
                polateX = np.linspace(elimit[0],elimit[1],np.floor((elimit[1]-elimit[0])/elimit[2])+1)
                fitY = np.zeros(len(polateX))
            elif refile != '':
                file2 = open(refile,'r')
                polateList = file2.readlines()
                polateX = map(float,polateList)
                fitY = np.zeros(len(polateX))
                file2.close()
            else:
                polateX = xValues
                fitY = np.zeros(len(lineList))
        else:
            oneY = np.zeros(len(lineList[rows[0]:rows[1]])) #创建Y数组和fit数组
            # 确定插值范围 首先尝试从-e命令获取插值范围 然后再尝试从文件获取 最后使用-r指定的范围
            if elimit[0] != -1:
                polateX = np.linspace(elimit[0],elimit[1],np.floor((elimit[1]-elimit[0])/elimit[2])+1)
                fitY = np.zeros(len(polateX))
            elif refile != '':
                file2 = open(refile,'r')
                polateList = file2.readlines()
                polateX = map(float,polateList)
                fitY = np.zeros(len(polateX))
                file2.close()
            else:
                polateX = xValues
                fitY = np.zeros(len(lineList[rows[0]:rows[1]]))

        oneY = map(float,[x[f] for x in yValues])
        # 执行圆滑
        comp_oneY = scipy.fftpack.rfft(oneY)
        frequency = scipy.fftpack.rfftfreq(len(oneY), polateX[1]-polateX[0])
        spectrum = comp_oneY**2
        cutoff_idx = (window[0]) < spectrum < (window[1])
        comp_oneY2 = w.copy()
        comp_oneY2[cutoff_idx] = 0
        smooth_oneY = scipy.fftpack.irfft(comp_oneY2)
        # 绘图
        screen.plot(polateX,smooth_oneY,'--',label=legend[f]+"-smoothed")
        screen.scatter(xValues,oneY,label=legend[f],marker='.',color="grey")
        screen.legend(loc='best', fontsize='large')
        # 按label绘制轴的单位
        screen.set_xlabel(labels[0])
        screen.set_ylabel(labels[1])
        # 绘制图名
        plt.title(infile)
        if not ifSavefig:
            fig.savefig(outfile[f]+".png")
            fp = open(outfile[f]+".txt",'w')
            outhead = '# '+labels[0]+' '+labels[1]+'\n'
            fp.write(outhead)
            for x in range(len(polateX)):
                outstr = str(polateX[x])+' '+str(smooth_oneY[x])+'\n'
                fp.write(outstr)
            fp.close()
    plt.show()

def main(argv):
    # initialize parameters
    inputFile = ''
    outputFile = ''
    referFile = ''
    onlyScreen = False
    dataLine = [0,1]
    dataRow = [-1,-1]
    extraLimit = [-1,-1,-1]
    dataLegend = ['data']
    axisLabel = ['x','y']
    startLine = 0
    passWindow = [0.0,1.0]
    # get option
    try:
        opts, args = getopt.getopt(argv,"hi:o:sj:d:l:a:r:w:e:f:",["help","ifile=","ofile=","screen","jump-head=","data-line=","legend=","axis-label=","rows=","window=","extralimit=","referfile="])
    except getopt.GetoptError:
        disp_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            disp_help()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt in ("-o", "--ofile"):
            outputFile = map(str,arg.strip().split(','))
        elif opt in ("-f", "--referfile"):
            referFile = arg
        elif opt in ("-s", "--screen"):
            onlyScreen = True
        elif opt in ("-j", "--jump-head"):
            startLine = int(arg)
        elif opt in ("-w", "--window"):
            passWindow = map(float,arg.strip().split(','))
        elif opt in ("-r", "--rows"):
            dataRow = map(int,arg.strip().split(','))
        elif opt in ("-d", "--data-line"):
            dataLine = map(int,arg.strip().split(','))
        elif opt in ("-l", "--legend"):
            dataLegend = map(str,arg.strip().split(','))
        elif opt in ("-a", "--axis-label"):
            axisLabel = map(str,arg.strip().split(','))
        elif opt in ("-e","--extrapolate"):
            extraLimit = map(float,arg.strip().split(','))
    # check for necessary paremeters
    if inputFile == '':
        print("error: no input-file name")
        disp_help()
        sys.exit()
    if onlyScreen == False and outputFile == '':
        print("error: no ouput-file name")
        sys.exit()
    if onlyScreen == True and outputFile != '':
        print("error: -o and -s can not be used at the same time")
        sys.exit()
    # runtine
    poly_extrapolate(inputFile,outputFile,referFile,dataLine,dataRow,passWindow,startLine,extraLimit,dataLegend,axisLabel,onlyScreen)

if __name__ == "__main__":
    main(sys.argv[1:])