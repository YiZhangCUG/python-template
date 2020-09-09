#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys, getopt
import matplotlib.pyplot as plt
import numpy as np

def disp_help():
	proname = (sys.argv[0]).strip().split('/')
	print ('This is a pyhton template preforming the extrapolation of a set of data points or multiple sets using the least squares polynomial fit. \
For more information please go to the offical site of matplotlib "http://matplotlib.org/"\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)\n')
	print ('Usage: '+proname[-1]+' -i<inputfile> -o<outputfile>|-s [-j<head-record>] [-p<deg>] [-e<xmin>,<xmax>,<dx>|-f<referfile>] [-r<rmin>,<ramx>] [-d<x-row>,<y-row1>,<y-row2>,...] [-l<legend>,...] [-a<x-label>,<y-label>]\n\
-i --ifile\tinput-file name (*.txt *.xyz *.dat)\n\
-f --referfile\ttake a one columon file that indicates special locations for extrapolation\n\
-d --data-line\tselect x row and y rows, the default is 0 for x, 1 for y\n\
-j --jump-head\tskip head records as indicated by the parameter, the default is zero\n\
-p --polynomial\tdegree of the fitting polynomial, the default value is 1\n\
-e --extralimit\tthe range of extrapolation, the default with use what -r option indicates\n\
-r --rows\tset begining and ending rows of data that used to plot, the default will use all data\n\
-o --ofile\toutput-file name without extensions, the default formats are .png for figures and .txt for data\n\
-l --legend\tset data legends, the default is \'data\'. The number of legends must equal the number of y rows\n\
-a --axis-label\tset x and y axises\' labels, the default are \'x\' and \'y\'\n\
-s --screen\tonly show the figure on screen and do not save the figure\n\
-h --help\tshow this information')

def poly_extrapolate(infile,outfile,refile,lines,rows,degrees,sline,elimit,legend,labels,ifSavefig):
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
		# 执行多项式拟合
		polyline = np.poly1d(np.polyfit(xValues,oneY,degrees))
		fitY = polyline(polateX)
		# 绘图
		screen.plot(polateX,fitY,'--',label=legend[f]+"-extrapolated")
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
				outstr = str(polateX[x])+' '+str(fitY[x])+'\n'
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
	polyDeg = 1
	# get option
	try:
		opts, args = getopt.getopt(argv,"hi:o:sj:d:l:a:r:p:e:f:",["help","ifile=","ofile=","screen","jump-head=","data-line=","legend=","axis-label=","rows=","polynomial=","extralimit=","referfile="])
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
		elif opt in ("-p", "--polynomial"):
			polyDeg = int(arg)
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
	poly_extrapolate(inputFile,outputFile,referFile,dataLine,dataRow,polyDeg,startLine,extraLimit,dataLegend,axisLabel,onlyScreen)

if __name__ == "__main__":
	main(sys.argv[1:])