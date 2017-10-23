#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import sys, getopt
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.font_manager as font_manager
import numpy as np
import copy

a_very_big_int = 1e+30

# 显示帮助信息
def disp_help():
    proname = (sys.argv[0]).strip().split('/')
    print 'This a pyhton template for using matplotlib to plot a one line or multiple lines figure. \
For more information please go to the offical site of matplotlib "http://matplotlib.org/"\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)'
    print 'Usage: '+proname[-1]+' -i<inputfile> -o<outputfile>|-s [-t<fig-title>] [-j<head-record>] [-f<ref-col>,<ref-index>,<ref-index>...] [-r<rmin>,<ramx>,<rmin2>,<rmax2>....] [-d<x-col>,<y-col1>,<y-col2>,...] [-l<legend>,...] [-a<x-label>,<y-label>] [-y<layout>,<layout>...]\n\
-i --ifile\tinput-file name (*.txt *.xyz *.dat).\n\
-o --ofile\toutput-file name (*.jpg *.png *.pdf *.eps ...).\n\
-s --screen\tonly show the figure on screen and do not save the figure.\n\
-d --data-line\tselect x column and y columns, the default is 0 for x, 1 for y. If x-col less than zero,\n\
\t\ta number array will be used as x axis.\n\
-t --title\tset figure title, the default will use the input-file name. use -t\" \" to disable the title.\n\
-j --jump-head\tskip head records as indicated by the parameter, the default is zero. Note that all data rows start with # are ingored by default.\n\
-f --ref-index\tset a column as reference with at least one reference index. the template will plot\n\
\t\trows equal the reference indices.\n\
-r --rows\tset begining and ending rows of data that used to plot, the default will will all data.\n\
\t\tNote that this option may take multiple index-groups that each of them has a strart and end indice.\n\
-l --legend\tset lines\' legend. round a legend with \$\$ to use the MathTex expression.\n\
-a --axis-label\tset x and y axises\' labels, the default are \'x\' and \'y\'. round a legend with \$\$ to\n\
\t\tuse the MathTex expression.\n\
-y --layout\tset figure\'s layout. The default is 0 for my everyday use.\n\
\t\t0 everyday use\n\
\t\t1 article\n\
\t\t2 use white color for ticks and tick labels\n\
-h --help\tshow this information.'

def plot_lines(infile,outfile,figtitle,lines,refers,rows,sline,legend,labels,ifSavefig,style):
    # 循环绘图 按legend绘制图例
    fig, ax = plt.subplots()
    # 设置布局 部分参数设置在函数最后完成 如图例参数 图片保存参数 注意这个参数会循环所有参数并覆盖
    for s in style:
        if s == 0:
            # everyday use
            title_font = {'fontname':'Arial','size':'14','color':'black','weight':'normal','verticalalignment':'bottom'}
            axis_font = {'fontname':'Arial','size':'12'}
            legend_size = 12
            line_widths = 1.5
            save_dpi = 300
            # 按label绘制轴的单位
            for l in (ax.get_xticklabels() + ax.get_yticklabels()):
                l.set_fontname('Arial')
                l.set_fontsize(12)
            ax.set_xlabel(labels[0],**axis_font)
            ax.set_ylabel(labels[1],**axis_font)
            ax.yaxis.set_ticks_position('both')
            ax.autoscale(tight=True)
            ax.spines['left'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.grid(color='lightgrey',linestyle='--',linewidth=0.5)
            # 绘制图名
            if figtitle == '': plt.title(infile,**title_font)
            else: plt.title(figtitle,**title_font)
            # 注意adjust和tight_layout不要同时使用 或者可以保存为eps文件 在别的处理软件里处理边框
            #fig.subplots_adjust(left=0.14,right=0.99,bottom=0.18)
            plt.tight_layout()
        elif s == 1:
            # article
            fig.set_size_inches(3,1.854) #文章中使用的大小 英寸 平时不需要使用
            title_font = {'fontname':'Arial','size':'7','color':'black','weight':'normal','verticalalignment':'bottom'}
            axis_font = {'fontname':'Arial','size':'6.5'}
            legend_size = 6.5
            line_widths = 1
            save_dpi = 300
            # 按label绘制轴的单位
            for l in (ax.get_xticklabels() + ax.get_yticklabels()):
                l.set_fontname('Arial')
                l.set_fontsize(6.5)
            ax.set_xlabel(labels[0],**axis_font)
            ax.set_ylabel(labels[1],**axis_font)
            ax.yaxis.set_ticks_position('both')
            ax.autoscale(tight=True)
            ax.spines['left'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.grid(color='lightgrey',linestyle='--',linewidth=0.5)
            # 绘制图名
            if figtitle == '': plt.title(infile,**title_font)
            else: plt.title(figtitle,**title_font)
            plt.tight_layout(pad=0)
        elif s == 2:
            ax.tick_params(axis='both',colors='w')
            ax.xaxis.label.set_color('w')
            ax.yaxis.label.set_color('w')
        else:
            print 'error: wrong layout style'
            sys.exit()
#############以下是数据提取处理部分#####################
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
    # 按lines提取lineList中的特定列
    if rows[0] == a_very_big_int:
        if refers[0] == a_very_big_int:
            xValues = np.zeros(len(lineList))
            if lines[0] < 0:
                xValues = range(1,len(lineList)+1)
                yValues = np.zeros((len(lineList),len(lines)-1))

                count = 0
                for l in map(int,lines[1:]):
                    for h in range(len(lineList)):
                        yValues[h][count] = float(lineList[h][l])
                    count += 1

                oneY = np.zeros(len(lineList))
                for l in range(len(lines)-1):
                    oneY = map(float,[x[l] for x in yValues])
                    ax.plot(xValues,oneY,linewidth=line_widths)
            else:
                xValues = map(float,[x[lines[0]] for x in lineList])
                yValues = np.zeros((len(lineList),len(lines)-1))

                count = 0
                for l in map(int,lines[1:]):
                    for h in range(len(lineList)):
                        yValues[h][count] = float(lineList[h][l])
                    count += 1

                oneY = np.zeros(len(lineList))
                for l in range(len(lines)-1):
                    oneY = map(float,[x[l] for x in yValues])
                    ax.plot(xValues,oneY,linewidth=line_widths)
        else:
            for r in map(float,refers[1:]):
                index = []
                for h in range(len(lineList)):
                    if float(lineList[h][int(refers[0])]) == r:
                        index.append(h)

                xValues = np.zeros(len(index))
                if lines[0] < 0:
                    xValues = range(1,len(index)+1)
                    yValues = np.zeros((len(index),len(lines)-1))

                    count = 0
                    for l in map(int,lines[1:]):
                        count2 = 0
                        for h in index:
                            yValues[count2][count] = float(lineList[h][l])
                            count2 += 1
                        count += 1

                    oneY = np.zeros(len(index))
                    for l in range(len(lines)-1):
                        oneY = map(float,[x[l] for x in yValues])
                        ax.plot(xValues,oneY,linewidth=line_widths)
                else:
                    count = 0
                    for h in index:
                        xValues[count] = float(lineList[h][lines[0]])
                        count += 1
                    yValues = np.zeros((len(index),len(lines)-1))

                    count = 0
                    for l in map(int,lines[1:]):
                        count2 = 0
                        for h in index:
                            yValues[count2][count] = float(lineList[h][l])
                            count2 += 1
                        count += 1

                    oneY = np.zeros(len(index))
                    for l in range(len(lines)-1):
                        oneY = map(float,[x[l] for x in yValues])
                        ax.plot(xValues,oneY,linewidth=line_widths)
    else:
        if refers[0] == a_very_big_int:
            for r in range(len(rows)/2):
                if lines[0] < 0:
                    xValues = range(1,len(lineList[rows[2*r]:rows[2*r+1]])+1)
                    yValues = np.zeros((len(lineList[rows[2*r]:rows[2*r+1]]),len(lines)-1))

                    count = 0
                    for l in map(int,lines[1:]):
                        for h in range(len(lineList[rows[2*r]:rows[2*r+1]])):
                            yValues[h][count] = float(lineList[h+rows[2*r]][l])
                        count += 1

                    oneY = np.zeros(len(lineList))
                    for l in range(len(lines)-1):
                        oneY = map(float,[x[l] for x in yValues])
                        ax.plot(xValues,oneY,linewidth=line_widths)
                else:
                    xValues = np.zeros(len(lineList[rows[2*r]:rows[2*r+1]]))
                    xValues = map(float,[x[lines[0]] for x in lineList[rows[2*r]:rows[2*r+1]]])
                    yValues = np.zeros((len(lineList[rows[2*r]:rows[2*r+1]]),len(lines)-1))

                    count = 0
                    for l in map(int,lines[1:]):
                        for h in range(len(lineList[rows[2*r]:rows[2*r+1]])):
                            yValues[h][count] = float(lineList[h+rows[2*r]][l])
                        count += 1

                    oneY = np.zeros(len(lineList))
                    for l in range(len(lines)-1):
                        oneY = map(float,[x[l] for x in yValues])
                        ax.plot(xValues,oneY,linewidth=line_widths)
        else:
            for r in map(float,refers[1:]):
                index = []
                for e in range(len(rows)/2):
                    for h in range(rows[2*e],rows[2*e+1]+1):
                        if float(lineList[h][int(refers[0])]) == r:
                            index.append(h)

                xValues = np.zeros(len(index))
                if lines[0] < 0:
                    xValues = range(1,len(index)+1)
                    yValues = np.zeros((len(index),len(lines)-1))

                    count = 0
                    for l in map(int,lines[1:]):
                        count2 = 0
                        for h in index:
                            yValues[count2][count] = float(lineList[h][l])
                            count2 += 1
                        count += 1

                    oneY = np.zeros(len(index))
                    for l in range(len(lines)-1):
                        oneY = map(float,[x[l] for x in yValues])
                        ax.plot(xValues,oneY,linewidth=line_widths)
                else:
                    count = 0
                    for h in index:
                        xValues[count] = float(lineList[h][lines[0]])
                        count += 1
                    yValues = np.zeros((len(index),len(lines)-1))

                    count = 0
                    for l in map(int,lines[1:]):
                        count2 = 0
                        for h in index:
                            yValues[count2][count] = float(lineList[h][l])
                            count2 += 1
                        count += 1

                    oneY = np.zeros(len(index))
                    for l in range(len(lines)-1):
                        oneY = map(float,[x[l] for x in yValues])
                        ax.plot(xValues,oneY,linewidth=line_widths)
    # 绘制图例在曲线绘制之后 这样才能知道是哪些曲线
    if legend[0] != 'null':
        ax.legend(legend,loc='best', fontsize=legend_size, facecolor='2', edgecolor='2')
    plt.show()
    if not ifSavefig:
        fig.savefig(outfile,dpi=save_dpi,transparent=True,bbox_inches='tight',pad_inches=0)

def main(argv):
    # 定义参数初始值
    inputfile = ''
    outputfile = ''
    figTitle = ''
    onlyScreen = False
    dataLine = [0,1]
    dataRow = [a_very_big_int,a_very_big_int*2]
    refIndex = [a_very_big_int]
    dataLegend = ['null']
    axisLabel = ['x','y']
    startLine = 0
    defaultLayout = [0]
    # 提取命名行参数
    try:
        opts, args = getopt.getopt(argv,"hi:o:sj:d:l:a:r:t:f:y:",\
            ["help","ifile=","ofile=","screen=","jump-head=","data-line=","legend=","axis-label=","rows=","title=","ref-index=","layout="])
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
        elif opt in ("-t", "--title"):
            figTitle = arg
        elif opt in ("-s", "--screen"):
            onlyScreen = True
        elif opt in ("-j", "--jump-head"):
            startLine = int(arg)
        elif opt in ("-r", "--rows"):
            dataRow = map(int,arg.strip().split(','))
        elif opt in ("-f", "--ref-index"):
            refIndex = map(float,arg.strip().split(','))
        elif opt in ("-d", "--data-line"):
            dataLine = map(int,arg.strip().split(','))
        elif opt in ("-l", "--legend"):
            dataLegend = map(str,arg.strip().split(','))
        elif opt in ("-a", "--axis-label"):
            axisLabel = map(str,arg.strip().split(','))
        elif opt in ("-y", "--layout"):
            defaultLayout = map(int,arg.strip().split(','))
    # 检查参数
    if inputfile == '':
        print("error: no input-file name")
        disp_help()
        sys.exit()

    if onlyScreen == False and outputfile == '':
        print("error: no ouput-file name")
        sys.exit()

    if onlyScreen == True and outputfile != '':
        print("error: -o and -s options can not be used at the same time")
        sys.exit()

    if startLine < 0:
        print("error: -j option does not take a negtive value")
        sys.exit()

    for i in dataRow:
        if i < 0:
            print("error: -r option does not take a negtive value")
            sys.exit()
    if len(dataRow)%2:
        print("error: -r option only takes an even number of values")
        sys.exit()
    for i in range(len(dataRow)/2):
        if dataRow[2*i] >= dataRow[2*i+1]:
            print("error: wrong -r option values: "+str(dataRow[2*i])+" "+str(dataRow[2*i+1]))
            sys.exit()

    if refIndex[0] < 0:
        print("error: -f option does not take a negtive value")
        sys.exit()

    for i in dataLine[1:]:
        if i < 0:
            print("error: -d option does not take a negtive value")
            sys.exit()
    # 执行函数
    plot_lines(inputfile,outputfile,figTitle,dataLine,refIndex,dataRow,startLine,dataLegend,axisLabel,onlyScreen,defaultLayout)

if __name__ == "__main__":
    main(sys.argv[1:])