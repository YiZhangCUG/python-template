#!/bin/bash
# 获取当前文件夹地址
folderAddress=`pwd`
# 指定安装地址 若不存在则建立 同时将路径添加到环境变量中
objectAddress="/usr/local/sbin"
if [[ ! -d $objectAddress ]]; then
	mkdir $objectAddress
	export PATH=$PATH:$objectAddress
fi
#找到所有后缀名为.py的脚本名称 存入数组
scriptName=( `ls *.py` )
for element in ${scriptName[@]}; do
	objectName=${element%.*}
	#若链接不存在 则建立
	if [[ ! -L ${objectAddress}/${objectName} ]]; then
		printf "creating links for "$objectName"... "
		ln -s ${folderAddress}/${element} ${objectAddress}/${objectName}
		printf "done\n"
	fi
done