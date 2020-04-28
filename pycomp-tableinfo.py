#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import sys, getopt
import numpy as np
import copy

def disp_help():
	proname = (sys.argv[0]).strip().split('/')
	print ('A pyhton template for statistics of a table data.\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)\n')
	print ('Usage: '+proname[-1]+' -i<infile> [-j<head-record>] [-c<column1>,<column2>...] [-s<split-symbol>] [-r<row-min>,<row-max>,<row-min2>,<row-max2>...]\n\
-i --ifile\tinput table name\n\
-j --jumphead\tskip head records. the default value is 0. NOTE: any line starts with # will be skipped automatically.\n\
-c --column\tdata columns. the default value is 1 which represents the third column of a input table\n\
-s --symbol\tline spliting symbol. the default values are space and tab\n\
-r --rows\tset begining and ending rows of data that used for calculation, the default will will all data.\n\
\t\tNote that this option may take multiple row indices groups that each of them has a strart and end indice\n\
-h --help\tshow this information')

def tableinfo(infile,sline,lines,rows,ssymbol):
	# 按行读取文件 从sline开始按空格分割数据
	file = open(infile,'r')
	lineList = file.readlines()
	# 默认忽略#号开头的行
	lineList_orig = copy.deepcopy(lineList)
	for line in lineList_orig:
		if line.startswith('#'):
			lineList.remove(line)
	# 按分隔符解析每行的数据
	if ssymbol == 'space' or ssymbol == 'tab':
		lineList = [line.strip().split( ) for line in lineList[sline:]]
	else:
		lineList = [line.strip().split(ssymbol) for line in lineList[sline:]]
	file.close()

	if rows[0] == -1:
		yValues = np.zeros((len(lineList),len(list(lines))))
		count = 0
		for l in list(map(int,lines)):
			for h in range(len(lineList)):
				yValues[h][count] = float(lineList[h][l])
			count += 1
		oneY = np.zeros(len(lineList))
		for l in range(len(list(lines))):
			oneY = list(map(float,[x[l] for x in yValues]))
			print('statistics of data column: '+str(lines[l])+"\n")
			print('number of inputs: '+str(len(list(oneY))))
			print('-------------------------------')
			print('minima\t|\t'+str(np.nanmin(list(oneY))))
			print('maxima\t|\t'+str(np.nanmax(list(oneY))))
			print('range\t|\t'+str(np.ptp(list(oneY))))
			print('median\t|\t'+str(np.nanmedian(list(oneY))))
			print('mean\t|\t'+str(np.nanmean(list(oneY))))
			print('std\t|\t'+str(np.nanstd(list(oneY))))
			print('var\t|\t'+str(np.nanvar(list(oneY))))
			print('rms\t|\t'+str(np.sqrt(np.nanmean(np.power(oneY,2)))))
			print('-------------------------------')
	else:
		index = []
		for r in range(len(rows)/2):
			for h in range(rows[2*r],rows[2*r+1]+1):
				index.append(h)

		count = 0
		yValues = np.zeros((len(index),len(lines)))
		for l in map(int,lines[:]):
			count2 = 0
			for h in index:
				yValues[count2][count] = float(lineList[h][l])
				count2 += 1
			count += 1
		oneY = np.zeros(len(index))
		for l in range(len(lines)):
			oneY = map(float,[x[l] for x in yValues])
			print('statistics of data column: '+str(lines[l]))
			print('-------------------------------')
			print('minima\t|\t'+str(np.nanmin(oneY)))
			print('maxima\t|\t'+str(np.nanmax(oneY)))
			print('range\t|\t'+str(np.ptp(oneY)))
			print('median\t|\t'+str(np.nanmedian(oneY)))
			print('mean\t|\t'+str(np.nanmean(oneY)))
			print('std\t|\t'+str(np.nanstd(oneY)))
			print('var\t|\t'+str(np.nanvar(oneY)))
			print('-------------------------------')

def main(argv):
	inputFile = ''
	startLine = 0
	dataLine = [1]
	dataRow = [-1,-1]
	splitSymbol = 'space'

	try:
		opts, args = getopt.getopt(argv,"hi:j:c:r:s:",["help","ifile=","jumphead=","column=","rows=","symbol="])
	except getopt.GetoptError:
		disp_help()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h","--help"):
			disp_help()
			sys.exit()
		elif opt in ("-i","--ifile"):
			inputFile = arg
		elif opt in ("-j","--jumphead"):
			startLine = int(arg)
		elif opt in ("-c","--column"):
			dataLine = list(map(int,arg.strip().split(',')))
		elif opt in ("-r","--rows"):
			dataRow = list(map(int,arg.strip().split(',')))
		elif opt in ("-s","-symbol"):
			splitSymbol = arg

	if inputFile == '':
		print('error: no input-file name')
		disp_help()
		sys.exit()
	# runtine
	tableinfo(inputFile,startLine,dataLine,dataRow,splitSymbol)

if __name__ == "__main__":
	main(sys.argv[1:])