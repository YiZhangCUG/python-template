#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import sys, getopt
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

def disp_help():
	print 'This a pyhton template for using matplotlib to plot a figure or figures for a xyz data set. \
For more information please go to the offical site of matplotlib "http://matplotlib.org/"\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)\n\
Usage: pyplot-plane -i<file> -s|-o<file>,<file>,... [-j<head-record>] [-t<xmin>/<dx>/<xmax>/<ymin>/<dy>/<ymax>] [-a<x-label>,<y-label>] [{-d<data-row>,<data-row>,... -l<legend>,... -u<unit>,...}]\n\
-i --ifile\tinput-file name (*.txt *.xyz *.dat)\n\
-d --data-line\tselect data rows, the default is 2 for data values\n\
-j --jump-head\tskip head records as indicated by the parameter, the default is 0\n\
-o --ofile\toutput-file name (*.jpg *.png *.pdf *.eps ...)\n\
-t --tick\tset data intervals, the default is 0/10/1000/0/10/1000\n\
-u --unit\tset unit labels for color bar, the default is \'value\'\n\
-l --legend\tset figure titles, the default is \'data\'. The number of legends must equal the number of data rows\n\
-a --axis-label\tset x and y axises\' labels, the default are \'x (m)\' and \'y (m)\'\n\
-s --screen\tonly show the figure on screen and do not save the figure\n\
-h --help\tshow this information'

def single_figure(fig,ax,data,title,unit,dataRange):
	cax = ax.imshow(data,cmap=cm.rainbow,
					origin='lower',extent=dataRange,
					vmax=data.max(),vmin=data.min())
	ax.set_title(title)
	cbar = fig.colorbar(cax, ax=ax, shrink=0.6, ticks=np.linspace(data.min(),data.max(),num=5))
	cbar.ax.set_yticklabels(map(str,np.round(np.linspace(data.min(),data.max(),num=5),2)))
	cbar.ax.set_ylabel(unit)

def plot_planes(ifile,ofile,lines,sline,interval,legend,labels,unit,ifSavefig):
	file = open(ifile,'r')
	lineList = file.readlines()
	lineList = [line.strip().split( ) for line in lineList[sline:]]
	file.close()

	hlnum = [0,0]
	hlnum[0] = int ((interval[2] - interval[0])/interval[1] + 1)
	hlnum[1] = int ((interval[5] - interval[3])/interval[4] + 1)
	datarange = [0.0,0.0,0.0,0.0]
	datarange[0] = interval[0]
	datarange[1] = interval[2]
	datarange[2] = interval[3]
	datarange[3] = interval[5]

	zValues = np.zeros((hlnum[1],hlnum[0]))
	zArray = np.zeros((hlnum[0]*hlnum[1],len(lines)))

	count = 0
	for l in map(int,lines[:]):
		for h in range(len(lineList)):
			zArray[h][count] = float(lineList[h][l])
		count += 1

	for f in range(len(lines)):
		for l in range(hlnum[1]):
			for h in range(hlnum[0]):
				zValues[l][h] = zArray[l*hlnum[0]+h][f]
		fig, ax = plt.subplots()
		ax.set_xlabel(labels[0])
		ax.set_ylabel(labels[1])
		single_figure(fig,ax,zValues,legend[f],unit[f],datarange)
		if not ifSavefig: fig.savefig(ofile[f])
	plt.show()

def main(argv):
	inputFile = ''
	outputFile = ['']
	onlyScreen = False
	dataLine = [2]
	dataLegend = ['data']
	dataUnit = ['value']
	dataInterval = [0,10,1000,0,10,1000]
	axisLabel = ['x (m)','y (m)']
	startLine = 0

	try:
		opts, args = getopt.getopt(argv,"hi:o:sj:d:l:a:t:u:",["help","ifile=","ofile=","screen","jump-head=","data-line=","legend=","axis-label=","tick=","unit="])
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
		elif opt in ("-s", "--screen"):
			onlyScreen = True
		elif opt in ("-j", "--jump-head"):
			startLine = int(arg)
		elif opt in ("-d", "--data-line"):
			dataLine = map(int,arg.strip().split(','))
		elif opt in ("-l", "--legend"):
			dataLegend = map(str,arg.strip().split(','))
		elif opt in ("-a", "--axis-label"):
			axisLabel = map(str,arg.strip().split(','))
		elif opt in ("-t", "--tick"):
			dataInterval = map(float,arg.strip().split('/'))
		elif opt in ("-u", "--unit"):
			dataUnit = map(str,arg.strip().split(','))

	if inputFile == '':
		disp_help()
		sys.exit()

	if onlyScreen == False and outputFile[0] == '':
		print 'error: no output-file name'
		sys.exit()

	if onlyScreen == True and outputFile[0] != '':
		print 'error: -o and -s can not be used at the same time'
		sys.exit()

	plot_planes(inputFile,outputFile,dataLine,startLine,dataInterval,dataLegend,axisLabel,dataUnit,onlyScreen)

if __name__ == "__main__":
	main(sys.argv[1:])