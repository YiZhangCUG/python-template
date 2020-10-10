#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, string
import random
import sys, getopt
import numpy as np
import pyshtools

def disp_help():
	proname = (sys.argv[0]).strip().split('/')
	print ('This is a python template generates a series of random distributed spherical harmonic coefficients.\n\
For more information please go to the offical site of shtools "https://shtools.oca.eu/shtools/"\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)\n')
	print ('Usage: '+proname[-1]+' [-d<order-num>] [-o<out-file>] [-p<power-factor>] [-h]\n\
-d --order-num\tset order number of the output spherical harmonic coefficients, the default is 180\n\
-o --ofile\toutput name, the default is \'XXXXXXXX.SHcoeffs\' in which Xs are replaced by random symbols\n\
-p --power\tset multiply factor of the power spectrum, the default is 1.0\n\
-h --help\tshow this information')

def randomCoeffs(orderNum,fileName,powerFactor):
	proName = (sys.argv[0]).strip().split('/')

	degrees = np.arange(orderNum, dtype=float)
	degrees[0] = np.inf
	power = powerFactor*degrees**(-2)

	clm = pyshtools.SHCoeffs.from_random(power)
	#clm.to_file(fileName)
	coeffs = clm.to_array()
	fp = open(fileName,'w')
	outstr = '# This file is generated by '+proName[-1]+' on '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n'
	fp.write(outstr)
	outstr = '# number of orders = '+str(orderNum-1)+'\n'
	fp.write(outstr)
	for i in range(coeffs.shape[1]):
		for j in range(i+1):
			outstr = str(i)+' '+str(j)+' '+str(coeffs[0][i][j])+' '+str(coeffs[1][i][j])+'\n'
			fp.write(outstr)
		pass
	pass
	fp.close()

def main(argv):
	#定义参数初始值
	numOrder = 181
	nameFile = ''.join(random.sample(string.ascii_letters + string.digits, 8))+".SHcoeffs"
	factorPower = 1.0
	#提取命令行参数
	try:
		opts, args = getopt.getopt(argv,"hd:o:p:",["help","order-num=","ofile=","power="])
	except getopt.GetoptError:
		disp_help()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			disp_help()
			sys.exit()
		elif opt in ("-d", "--order-num"):
			numOrder = int(arg)
			numOrder = numOrder + 1
		elif opt in ("-p", "--power"):
			factorPower = float(arg)
		elif opt in ("-o", "--ofile"):
			nameFile = arg
	#执行函数
	randomCoeffs(numOrder,nameFile,factorPower)

if __name__ == "__main__":
	main(sys.argv[1:])