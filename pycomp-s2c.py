#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, getopt
import numpy as np
import copy

def disp_help():
	proname = (sys.argv[0]).strip().split('/')
	print ('This a pyhton template for translate spherical coordinates to the Cartesian coordinates\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)\n')
	print ('Usage: '+proname[-1]+' -p<longitude>,<latitude>,<radius>|-P<coordinates> [-h]\n\n\
-p --point\tSpherical coordinates of a point\n\
-P --point-file\tRead spherical coordinates from a file.\n\
-h --help\tShow this information')

def s2c(coor):
	print("x\ty\tz")
	for i in range(len(coor)):
		x = coor[i][2]*np.sin((0.5 - coor[i][1]/180.0)*np.pi)*np.cos((2.0 + coor[i][0]/180.0)*np.pi);
		y = coor[i][2]*np.sin((0.5 - coor[i][1]/180.0)*np.pi)*np.sin((2.0 + coor[i][0]/180.0)*np.pi);
		z = coor[i][2]*np.cos((0.5 - coor[i][1]/180.0)*np.pi);
		print("%.12f %.12f %.12f" % (x,y,z))
'''
Coordiante = [[45,30,310]]
s2c(Coordiante)
'''

def main(argv):
	Coor_file = 'null'
	try:
		opts,args = getopt.getopt(argv,"hp:P:",["help","point","Point"])
	except getopt.GetoptError:
		disp_help()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h","--help"):
			disp_help()
			sys.exit()
		elif opt in ("-p","--point"):
			Coordiante = [list(map(float,arg.strip().split(',')))]
		elif opt in ("-P","--Point"):
			Coor_file = arg
			file = open(Coor_file,'r')
			lineList = file.readlines()
			# 默认忽略#号开头的行
			lineList_orig = copy.deepcopy(lineList)
			for line in lineList_orig:
				if line.startswith('#'):
					lineList.remove(line)
			Coordiante = [list(map(float,line.strip().split(','))) for line in lineList]
			file.close()
	s2c(Coordiante)

if __name__ == "__main__":
	main(sys.argv[1:])