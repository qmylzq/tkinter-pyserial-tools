from tkinter import *
import re
class MY_CODE():
    #构造函数
    def __init__(self,ser,text,functionandparam):
        self.ser=ser
        self.text=text
        self.functionandparam=functionandparam

    #解析指令，并选择对应函数去执行
    def function_choose_do(self,functionname):
        result=0
        if functionname == 'uboot_in_cmd':
            result=self.uboot_in_cmd()
        elif functionname == 'uboot_dbg_set':
            param=int(self.functionandparam[1])
            result=self.uboot_dbg_set(param)
        elif functionname == 'uboot_reset':
            result =self.uboot_reset()
        elif functionname == 'reboot':
            result =self.reboot()
        elif functionname == 'nfs_cmd':
            deviceip=self.functionandparam[1]
            nfsdir=self.functionandparam[2]
            result=self.nfs_cmd(deviceip,nfsdir)
        elif functionname == 'cd_dav':
            if len(self.functionandparam)> 1:
                filename = self.functionandparam[1]
                result = self.cd_dav(filename)
            else:
                result = self.cddav()
        elif functionname == 'file_move':
            ori_dir=self.functionandparam[1]
            des_dir=self.functionandparam[2]
            mod=int(self.functionandparam[3])
            result=self.file_move(ori_dir,des_dir,mod)
        elif functionname == 'dir_move':
            ori_dir=self.functionandparam[1]
            des_dir=self.functionandparam[2]
            mod=int(self.functionandparam[3])
            result=self.dir_move(ori_dir,des_dir,mod)
        elif functionname == 'file_del':
            filename=self.functionandparam[1]
            result=self.file_del(filename)
        elif functionname == 'dir_del':
            dirname=self.functionandparam[1]
            result=self.dir_del(dirname)
        elif functionname == 'file_cp':
            ori_dir=self.functionandparam[1]
            des_dir=self.functionandparam[2]
            mod=int(self.functionandparam[3])
            result=self.file_cp(ori_dir,des_dir,mod)
        elif functionname == 'dir_cp':
            ori_dir=self.functionandparam[1]
            des_dir=self.functionandparam[2]
            mod=int(self.functionandparam[3])
            result=self.dir_cp(ori_dir,des_dir,mod)
        return result

    #ctrl+u,进入uboot
    def uboot_in_cmd(self):
        self.waitforlong('Ctrl+u to stop')
        self.ser.write(chr(0x15).encode())
        self.waitforstring('HKVS #')
        isok =1
        return isok

    #设置dbg等级
    def uboot_dbg_set(self,num):
        self.ser.write(('set dbg '+str(num)+'\n').encode())
        self.waitforstring('HKVS #')
        self.ser.write(('sa'+'\n').encode())
        self.waitforstring('HKVS #')
        isok =1
        return isok

    #uboot重启
    def uboot_reset(self):
        self.ser.write(('re'+'\n').encode())
        self.waitforlong('built-in commands')
        self.waitforlong('#')
        isok=1
        return isok

    #内核重启
    def reboot(self):
        self.ser.write(('reboot'+'\n').encode())
        self.waitforlong('built-in commands')
        self.waitforlong('#')
        isok=1
        return isok

    #切换到dav目录，并查验所需操作的文件是否存在
    def cd_dav(self,filename):
        self.ser.write(('cd dav'+'\n').encode())
        self.waitforstring('#')
        self.ser.write(('ls'+'\n').encode())
        if self.waitforstring(filename) > 0:
            isok =1
        else:
            isok =0
        self.waitforstring('#')
        return isok

    #仅切换到dav目录
    def cddav(self):
        self.ser.write(('cd dav'+'\n').encode())
        self.waitforstring('#')
        self.ser.write(('ls'+'\n').encode())
        self.waitforstring('#')
        isok =1
        return isok

    #挂载
    def nfs_cmd(self,deviceip,nfsdir):
        pattern =re.compile('[0-9]+',re.S)
        dev=re.findall(pattern,deviceip)
        gw=str(dev[0])+'.'+str(dev[1])+'.'+str(dev[2])+'.'+'254'
        self.ser.write(('ifconfig eth0 down'+'\n').encode())
        self.waitforstring('#')
        self.ser.write(('ifconfig eth0 hw ether 00:0C:33:44:55:a6'+'\n').encode())#修改mac地址防止冲突
        self.waitforstring('#')
        self.ser.write(('ifconfig eth0 up'+'\n').encode())
        self.waitforstring('Link is Up')
        self.waitforstring('IPv6 routers')
        self.ser.write(('ifconfig eth0 '+deviceip+' netmask 255.255.255.0 broadcast 255.255.255.255'+'\n').encode())
        self.waitforstring('#')
        self.ser.write(('route add default gw '+gw+'\n').encode())
        self.waitforstring('#')
        self.ser.write(('mount -t nfs '+nfsdir+' /mnt -o nolock'+'\n').encode())
        isok1=self.waitforstring('#')
        self.ser.write(('mount'+'\n').encode())
        isok2=self.waitforstring('on /mnt type nfs')
        if isok1 >0 & isok2 > 0:
            isok =1
        else:
            isok =0
        return isok

    #移动文件，并修改dav目录
    def file_move(self,ori_dir,des_dir,mod):
        self.ser.write(('mv '+ori_dir+' '+des_dir+'\n').encode())
        isok1=self.waitTorF('#','mv:')
        self.ser.write(('chmod '+mod+' '+des_dir+'\n').encode())
        isok2=self.waitTorF('#','chmod:')
        if isok1 +isok2 ==2:
            isok =1
        else:
            isok =0
        return isok

    #移动目录并修改文件
    def dir_move(self,ori_dir,des_dir,mod):
        self.ser.write(('mv '+ori_dir+' '+des_dir+'\n').encode())
        isok1=self.waitTorF('#','mv:')
        self.ser.write(('chmod -R '+mod+' '+des_dir+'\n').encode())
        isok2=self.waitTorF('#','chmod:')
        if isok1 +isok2 ==2:
            isok =1
        else:
            isok =0
        return isok

    #删除指定文件
    def file_del(self,filename):
        self.ser.write(('rm '+filename+'\n').encode())
        isok = self.waitTorF('#','rm:')
        return  isok

    #删除指定目录
    def dir_del(self,dirname):
        self.ser.write(('rm -r '+dirname+'\n').encode())
        isok = self.waitTorF('#','rm:')
        return  isok

    #文件复制，并修改文件权限
    def file_cp(self,ori_dir,des_dir,mod):
        self.ser.write(('cp '+ori_dir+' '+des_dir+'\n').encode())
        isok1=self.waitTorF('#','cp:')
        self.ser.write(('chmod '+str(mod)+' '+des_dir+'\n').encode())
        isok2=self.waitTorF('#','chmod:')
        if isok1 +isok2 ==2:
            isok =1
        else:
            isok =0
        return isok

    #目录复制，并修改权限
    def dir_cp(self,ori_dir,des_dir,mod):
        self.ser.write(('cp '+ori_dir+' '+des_dir+'\n').encode())
        isok1=self.waitTorF('#','cp:')
        self.ser.write(('chmod -R '+str(mod)+' '+des_dir+'\n').encode())
        isok2=self.waitTorF('#','chmod:')
        if isok1 +isok2 ==2:
            isok =1
        else:
            isok =0
        return isok

    #有限时间内等待关键句
    def waitforstring(self,string):
        recv=self.ser.readline()
        self.text.insert(END,recv)
        self.text.see(END)
        self.text.update()
        timer = 60
        while timer:
            recv=self.ser.readline()
            self.text.insert(END,recv)
            self.text.see(END)
            self.text.update()
            if string in str(recv):
                break
            else:
                timer -=1
        return timer

    #无限时间内等待关键句
    def waitforlong(self,string):
        while True:
            recv=self.ser.readline()
            self.text.insert(END,recv)
            self.text.see(END)
            self.text.update()
            if string in str(recv):
                break

    #等待关键句，并判断执行成功or执行失败
    def waitTorF(self,true,false):
        recv=self.ser.readline()
        self.text.insert(END,recv)
        self.text.see(END)
        self.text.update()
        isok = 0
        timer =30
        while timer:
            recv=self.ser.readline()
            self.text.insert(END,recv)
            self.text.see(END)
            self.text.update()
            if false in str(recv):
                isok =0
                break
            elif true in str(recv):
                isok = 1
                break
            else:
                isok =0
                timer -=1
        return isok