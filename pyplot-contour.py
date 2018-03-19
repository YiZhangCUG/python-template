#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import sys, getopt
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.mlab as mlab

def disp_help():
	proname = (sys.argv[0]).strip().split('/')
	print ('This a pyhton template for using matplotlib to plot a contour map of random distributed data. \
For more information please go to the offical site of matplotlib "http://matplotlib.org/"\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)\n')
	print ('Usage: '+proname[-1]+' -i<inputfile> [-d<line1,line2,line3>] [-j<head-record>] -o<outputfile>|-s\n\
-i --ifile\tinput-file name (*.txt *.xyz *.dat)\n\
-d --data-line\tselect two lines as input data, defaults are the first two lines\n\
-j --jump-head\tskip head records as indicated by the parameter, the default is zero\n\
-o --ofile\toutput-file name (*.jpg *.png *.pdf *.eps ...)\n\
-s --screen\tonly show the figure on screen and do not save the figure\n\
-h --help\tshow this information')

def plot_random(infile,outfile,lines,sline,ifSavefig):
	file = open(infile,'r')
	lineList = file.readlines()
	lineList = [line.strip().split( ) for line in lineList[sline:]]
	file.close()

	xValues = [float(x[lines[0]]) for x in lineList]
	yValues = [float(x[lines[1]]) for x in lineList]
	zValues = [float(x[lines[2]]) for x in lineList]

	fig, screen = plt.subplots()
	tri.Triangulation(xValues, yValues)
	plt.tricontour(xValues, yValues, zValues, 15, linewidths=0.8, colors='k')
	plt.tricontourf(xValues, yValues, zValues, 15, cmap=cm.rainbow)
	plt.colorbar()
	plt.plot(xValues, yValues, 'ko', ms=0.5)
	plt.title(infile)
	plt.show()
	if not ifSavefig: fig.savefig(outfile)

def main(argv):
	inputfile = ''
	outputfile = ''
	onlyScreen = False
	dataLine = [0,1,2]
	startLine = 0

	try:
		opts, args = getopt.getopt(argv,"hi:o:sd:j:",["help","ifile=","ofile=","screen","data-line=","jump-head"])
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
		elif opt in ("-d", "--data-line"):
			dataLine = map(int,arg.strip().split(','))
		elif opt in ("-j", "--jump-head"):
			startLine = int(arg)

	if inputfile == '':
		disp_help()
		sys.exit()

	if onlyScreen == False and outputfile == '':
		print("error: no ouput-file name")
		sys.exit()

	if onlyScreen == True and outputfile != '':
		print("error: -o and -s can not be used at the same time")
		sys.exit()

	plot_random(inputfile,outputfile,dataLine,startLine,onlyScreen)

if __name__ == "__main__":
	main(sys.argv[1:])