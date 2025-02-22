#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib, sys, getopt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

def disp_help():
    proname = (sys.argv[0]).strip().split('/')
    print ('This a pyhton template for using smtplib to send emails. \
For more information please go to the offical site of smtplib "https://docs.python.org/3.5/library/smtplib.html"\n\
Sender\'s address and password must be set manually within the script.\n\
Author: Yi Zhang (zhangyi.cugwuhan@gmail.com)\n')
    print ('Usage: '+proname[-1]+' [-a<to_address>,<to_address>,...|-A<address-file>] [-s<subject>] [-t<text>|-T<text-file>] [-f<attached_file>,<attached_file>,...] [-h] [-d]\n\n\
-a --to-address\tA list of receiving addresses separated by commas. Default addresses could be set manually within the script.\n\
-A --ads-file\tRead receiving addresses from a file. Different addresses should be separated by commas.\n\
-s --subject\tSubject of the email. The default is \"This is automatic message, please do not reply.\".\n\
-t --text\tText message of the email. The default is \"No content.\".\n\
-T --text-file\tRead text message from a file.\n\
-f --attached-file\tFile attachments separated by commas.\n\
-h --help\tShow this information\n\
-d --defaults\tShow default settings')

'''
用户名 密码(应用专用密码)
发件邮箱(一般等于用户名) 收件邮箱(列表)
主题 文字 文件(地址列表) 默认收件地址
'''
def send_mail(hostname: str, portid: str, usrname: str, passwd: str, 
    send_from: str, send_to: list,
    subject: str, text: str, files= None):
    #初始化邮件头信息
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Subject'] = subject
    #添加文件信息
    msg.attach(MIMEText(text))
    #添加附件文件
    for f in files or []:
        with open(f, "rb") as fil: 
            ext = f.split('.')[-1:]
            attachedfile = MIMEApplication(fil.read(), _subtype = ext)
            attachedfile.add_header(
                'content-disposition', 'attachment', filename=basename(f) )
        msg.attach(attachedfile)
    #发送文件
    try:
        #邮箱服务器SMTP配置 服务器地址 端口
        smtp = smtplib.SMTP(host = hostname, port = portid) 
        smtp.starttls()
        smtp.login(usrname,passwd)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
    except Exception:
        print("fail to sent mail.")

def main(argv):
    # 从文本里读入邮箱设置信息 你也可以直接在此脚本设置 从文件读入只是更加安全一点
    with open("/Users/zhangyi/.zy_setup/icloud_smtp_info.txt", 'r', encoding='utf-8') as f:
        dic=[]
        for line in f.readlines():
            line=line.strip('\n') #去掉换行符\n
            b=line.split('=') #将每一行以等号为分隔符转换成列表
            dic.append(b)
    dic=dict(dic)

    userName = dic.get('username')
    passWord = dic.get('passwd')
    hostName = dic.get('server')
    portName = dic.get('port')
    toAddress = ['792779110@qq.com']
    #toPresons = ['Dr. Zhang']
    #signature = ['pymail']
    adsFile = 'null'
    subJect = 'This is automatic message, please do not reply.'
    textMsg = 'No content.'
    textFile = 'null'
    attachFile = None

    try:
        opts, args = getopt.getopt(argv,"hda:A:s:t:T:f:",["help","defaults","to-address=","ads-file=","subject=","text=","text-file=","att-file="])
    except getopt.GetoptError:
        disp_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            disp_help()
            sys.exit()
        elif opt in ("-d", "--defaults"):
            print("username: %s\npassword: %s\nto-address: %s\nsubject: %s\ntext: %s"
            % (userName,passWord,toAddress,subJect,textMsg))
            sys.exit()
        elif opt in ("-a", "--to-address"):
            toAddress = list(map(str,arg.strip().split(',')))
        elif opt in ("-A", "--ads-file"):
            adsFile = arg
        elif opt in ("-s", "--subject"):
            subJect = arg
        elif opt in ("-t", "--text"):
            textMsg = arg
        elif opt in ("-T", "--text-file"):
            textFile = arg
        elif opt in ("-f", "--att-file"):
            attachFile = list(map(str,arg.strip().split(',')))

    if adsFile != 'null':
        fa = open(adsFile,'r')
        toAddress = list(map(str,fa.read().strip().split(',')))
        fa.close()
        pass

    if textFile != 'null':
        fp = open(textFile,'r')
        textMsg = fp.read()
        fp.close()
        pass

    send_mail(hostName,portName,userName,passWord,userName,toAddress,subJect,textMsg,attachFile)

if __name__ == "__main__":
    main(sys.argv[1:])