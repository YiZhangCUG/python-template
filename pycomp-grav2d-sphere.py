#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, getopt
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.io import netcdf

constant_G = 6.67191e-3

def convert2DListTo1DList(list):
	result = []
	for element in list:
		for subElement in element:
			result.append(subElement)
	return result

def disp_help():
	proname = (sys.argv[0]).strip().split('/')
	print ('This a pyhton template for forward calculating a shpere\'s gravitational field on a plane.\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)\n')
	print ('Usage: '+proname[-1]+' -o<outputfile>|-s [-r<xmin>/<xmax>/<ymin>/<ymax>] [-d<x_num>/<y_num>] [-p<sph-posi-x>/<sph-posi-y>/<sph-depth>/<sph-radius>/<sph-rho>]\n\
-r --range\tcomputation area. default values are 0/1000/0/1000\n\
-d --dimension\tobservation points in x and y directions. default values are 101/101\n\
-p --parameter\tgeometric and physcial parameters of a sphere. default values are 500/500/200/50/1.0\n\
-o --ofile\toutput-file name. The programe will save a .png image file and a .nc grid file\n\
-s --screen\tonly show the figure on screen and do not save the figure and data\n\
-h --help\tshow this information')

def sub_figure(fig,ax,data,title,unit,dataRange):
	cax = ax.imshow(data,cmap=cm.rainbow,
					origin='lower',extent=dataRange,
					vmax=data.max(),vmin=data.min())
	ax.set_title(title)
	ax.set_xlabel('y (m)')
	ax.set_ylabel('x (m)')
	cbar = fig.colorbar(cax, ax=ax, shrink=0.6, ticks=np.linspace(data.min(),data.max(),num=5))
	cbar.ax.set_yticklabels(map(str,np.round(np.linspace(data.min(),data.max(),num=5),2)))
	cbar.ax.set_ylabel(unit)

	for item in ([ax.title, ax.xaxis.label, ax.yaxis.label, cbar.ax.yaxis.label] + cbar.ax.get_yticklabels() + ax.get_xticklabels() + ax.get_yticklabels()):
		item.set_fontsize(8)

def sphere_gravity(Area,Dimension,Sphere,ifSavefig,filename,scripts):
	xArray, yArray = np.meshgrid(np.linspace(Area[0],Area[1],Dimension[0]),np.linspace(Area[2],Area[3],Dimension[1]),sparse=False,indexing='ij')
	values = constant_G*(4/3)*np.pi*(Sphere[3]**3)*Sphere[4]*Sphere[2]/(((xArray-Sphere[0])**2+(yArray-Sphere[1])**2+(Sphere[2])**2)**(3/2))
	values_gx = -3e+4*constant_G*(4/3)*np.pi*(Sphere[3]**3)*Sphere[4]*Sphere[2]*(xArray-Sphere[0])/(((xArray-Sphere[0])**2+(yArray-Sphere[1])**2+(Sphere[2])**2)**(5/2))
	values_gy = -3e+4*constant_G*(4/3)*np.pi*(Sphere[3]**3)*Sphere[4]*Sphere[2]*(yArray-Sphere[1])/(((xArray-Sphere[0])**2+(yArray-Sphere[1])**2+(Sphere[2])**2)**(5/2))
	values_gz = 1e+4*constant_G*(4/3)*np.pi*(Sphere[3]**3)*Sphere[4]*(2*Sphere[2]**2+(xArray-Sphere[0])**2+(yArray-Sphere[1])**2)/(((xArray-Sphere[0])**2+(yArray-Sphere[1])**2+(Sphere[2])**2)**(5/2))
	
	fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
	Info = 'Parameters: '
	for str in convert2DListTo1DList(scripts):
		Info = Info + str + ' '
	fig.suptitle(Info,fontsize=9)
	sub_figure(fig,ax1,values,'gravity','mGal',Area)
	sub_figure(fig,ax2,values_gz,'vertical gradient','Eo',Area)
	sub_figure(fig,ax3,values_gx,'horizontal gradient x','Eo',Area)
	sub_figure(fig,ax4,values_gy,'horizontal gradient y','Eo',Area)
	plt.tight_layout()
	plt.margins(tight=True)

	if not ifSavefig:
		plt.savefig(filename+'.png')

		file = netcdf.netcdf_file(filename+'.nc','w')
		file.history = 'gravity data of a sphere'
		file.createDimension('x_axis', int(Dimension[0]))
		file.createDimension('y_axis', int(Dimension[1]))
		x = file.createVariable('x_axis','d',('x_axis',))
		x.units = 'm'
		y = file.createVariable('y_axis','d',('y_axis',))
		y.units = 'm'
		d = file.createVariable('g','d',('x_axis','y_axis'))
		d.units = 'mGal'
		dx = file.createVariable('gx','d',('x_axis','y_axis'))
		dx.units = 'Eo'
		dy = file.createVariable('gy','d',('x_axis','y_axis'))
		dy.units = 'Eo'
		dz = file.createVariable('gz','d',('x_axis','y_axis'))
		dz.units = 'Eo'
		x[:] = np.linspace(Area[0],Area[1],Dimension[0])
		y[:] = np.linspace(Area[2],Area[3],Dimension[1])
		d[:] = values
		dx[:] = values_gx
		dy[:] = values_gy
		dz[:] = values_gz
		file.close()

	plt.show()
	

def main(argv):
	area = [0,1000,0,1000]
	dimension = [101,101]
	sphere = [500,500,200,50,1.0]
	onlyScreen = False
	outputfile = ''

	try:
		opts, args = getopt.getopt(argv,"hr:d:p:o:s",["help","range=","dimension=","parameter=","ofile=","screen="])
	except getopt.GetoptError:
		disp_help()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			disp_help()
			sys.exit()
		elif opt in ("-r", "--range"):
			area = map(float, arg.strip().split('/'))
		elif opt in ("-d", "--dimension"):
			dimension = map(float, arg.strip().split('/'))
		elif opt in ("-p", "--parameter"):
			sphere = map(float, arg.strip().split('/'))
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-s", "--screen"):
			onlyScreen = True

	if outputfile == '' and onlyScreen == False:
		disp_help()
		sys.exit()

	sphere_gravity(area,dimension,sphere,onlyScreen,outputfile,opts)

if __name__ == "__main__":
	main(sys.argv[1:])