#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys, getopt
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

def disp_help():
	proname = (sys.argv[0]).strip().split('/')
	print ('This a pyhton template for using matplotlib to plot a figure or figures for a xyz data set. \
For more information please go to the offical site of matplotlib "http://matplotlib.org/"\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)\n')
	print ('Usage: '+proname[-1]+' -i<file> -s|-o<file>,<file>,... [-j<head-record>] [-t<xmin>/<dx>/<xmax>/<ymin>/<dy>/<ymax>] [-a<x-label>,<y-label>] [{-d<data-row>,<data-row>,... -l<legend>,... -u<unit>,...}]\n\
-i --ifile\tinput-file name (*.txt *.xyz *.dat)\n\
-d --data-line\tselect data rows, the default is 2 for data values\n\
-j --jump-head\tskip head records as indicated by the parameter, the default is 0\n\
-o --ofile\toutput-file name (*.jpg *.png *.pdf *.eps ...)\n\
-t --tick\tset data intervals, the default is 0/10/1000/0/10/1000\n\
-u --unit\tset unit labels for color bar, the default is \'value\'\n\
-l --legend\tset figure titles, the default is \'data\'. The number of legends must equal the number of data rows\n\
-a --axis-label\tset x and y axises\' labels, the default are \'x (m)\' and \'y (m)\'\n\
-s --screen\tonly show the figure on screen and do not save the figure\n\
-p --polygon\tdraw polygons on the figure\n\
-h --help\tshow this information')

def tellme(s):
	plt.title(s, fontsize=14)
	plt.draw()

def single_figure(fig,ax,data,title,unit,dataRange):
	cax = ax.imshow(data,cmap=cm.rainbow,
					origin='lower',extent=dataRange,
					vmax=data.max(),vmin=data.min())
	ax.set_title(title)
	cbar = fig.colorbar(cax, ax=ax, shrink=0.6, ticks=np.linspace(data.min(),data.max(),num=5))
	cbar.ax.set_yticklabels(map(str,np.round(np.linspace(data.min(),data.max(),num=5),2)))
	cbar.ax.set_ylabel(unit)

def plot_planes(ifile,ofile,lines,sline,interval,legend,labels,unit,ifSavefig, ifPoly):
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

	if (ifPoly):
		tellme('Click to start draw polygons.\nleft->add right->pop mid->stop')
		while True:
			pts = []
			pts = np.asarray(plt.ginput(-1, timeout=-1))

			if (len(pts) >= 3):
				ph = plt.fill(pts[:, 0], pts[:, 1], 'green', alpha = 0.3, lw=2)

			if (len(pts) >= 1):
				print(">")
				for i in range(len(pts)):
					print("%lf %lf" % (pts[i][0], pts[i][1]))

			tellme('Press any key to quit drawing polygons.\nleft->add right->pop mid->stop')

			if plt.waitforbuttonpress():
				tellme('Done drawing polygons.')
				break

	plt.show()

def main(argv):
	inputFile = ''
	outputFile = ['']
	onlyScreen = False
	drawPoly = False
	dataLine = [2]
	dataLegend = ['data']
	dataUnit = ['value']
	dataInterval = [0,10,1000,0,10,1000]
	axisLabel = ['x (m)','y (m)']
	startLine = 0

	try:
		opts, args = getopt.getopt(argv,"hi:o:sj:d:l:a:t:u:p",["help","ifile=","ofile=","screen","polygon","jump-head=","data-line=","legend=","axis-label=","tick=","unit="])
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
			outputFile = list(map(str,arg.strip().split(',')))
		elif opt in ("-s", "--screen"):
			onlyScreen = True
		elif opt in ("-p", "--polygon"):
			drawPoly = True
		elif opt in ("-j", "--jump-head"):
			startLine = int(arg)
		elif opt in ("-d", "--data-line"):
			dataLine = list(map(int,arg.strip().split(',')))
		elif opt in ("-l", "--legend"):
			dataLegend = list(map(str,arg.strip().split(',')))
		elif opt in ("-a", "--axis-label"):
			axisLabel = list(map(str,arg.strip().split(',')))
		elif opt in ("-t", "--tick"):
			dataInterval = list(map(float,arg.strip().split('/')))
		elif opt in ("-u", "--unit"):
			dataUnit = list(map(str,arg.strip().split(',')))

	if inputFile == '':
		disp_help()
		sys.exit()

	if onlyScreen == False and outputFile[0] == '':
		print ('error: no output-file name')
		sys.exit()

	if onlyScreen == True and outputFile[0] != '':
		print ('error: -o and -s can not be used at the same time')
		sys.exit()

	plot_planes(inputFile,outputFile,dataLine,startLine,dataInterval,dataLegend,axisLabel,dataUnit,onlyScreen,drawPoly)

if __name__ == "__main__":
	main(sys.argv[1:])