#!/bin/bash
# 获取当前文件夹地址
folderAddress=`pwd`
# 获取当前用户的根目录
userAddress=`echo $HOME`
# 指定安装地址 若不存在则建立
objectAddress="/usr/local/sbin/python-scripts"
if [[ ! -d $objectAddress ]]; then
	sudo mkdir $objectAddress
fi
# 添加安装路径到环境变量中 首先获取当前的环境变量 若安装路径已存在于环境变量中则跳过 否则添加安装地址到环境变量中
allPATH=`echo $PATH`
if [[ `echo ${allPATH} | grep "${objectAddress}"` ]]; then
	echo "The installation address is already added to \$PATH. Nothing to be done."
else
	breaked=no
	# 几个经常使用的用户配置文件
	profileAddress=("${userAddress}/.zshrc" "${userAddress}/.bash_profile" "${userAddress}/.profile")
	for one_address in ${profileAddress[@]}; do
		if [[ -f ${one_address} ]]; then
			echo "adding the installation address to ${one_address}"
			cat <<- EOF >> ${one_address}
				# this is added by configure.sh of python-template (zhangyi.cugwuhan@gmail.com)
				export PATH="${objectAddress}:\$PATH"
			EOF
			source ${one_address}
			breaked=yes
			break
		fi
	done
	# 预设的用户配置文件都不存在 则新建一个.bash_profile文件 添加环境变量
	if [[ ${breaked} == "no" ]]; then
		echo "made file ${userAddress}/.bash_profile"
		echo "adding the installation address to ${userAddress}/.bash_profile"
		cat <<- EOF > ${userAddress}/.bash_profile
			# this is added by configure.sh of python-template (zhangyi.cugwuhan@gmail.com)
			export PATH=${objectAddress}:\$PATH
		EOF
		source ${userAddress}/.bash_profile
	fi
fi

#找到所有后缀名为.py的脚本名称 存入数组
scriptName=( `ls *.py` )
for element in ${scriptName[@]}; do
	objectName=${element%.*}
	#若链接不存在 则建立
	if [[ ! -L ${objectAddress}/${objectName} ]]; then
		printf "creating links for "$objectName"... "
		sudo ln -s ${folderAddress}/${element} ${objectAddress}/${objectName}
		printf "done\n"
	fi
done