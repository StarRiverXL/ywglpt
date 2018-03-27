#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 2017/12/28
# Email：
import logging
import paramiko
# paramiko.util.log_to_file('/tmp/sshout.log')  # 日志记录，开启可看到类似于debug的输出
logger = logging.getLogger('django')


class SSHConnection(object):
    """
        基于用户名和密码的连接
        通过传入基础参数完成相关服务器操作，及返回响应结果
        涉及的操作包含：命令执行、文件上传和下载
    """
    
    def __init__(self, hostip, username, password, port=22):
        self.hostip = hostip
        self.port = port
        self.username = username
        self.password = password
        
    def __sshconnet(self):
        """
        : return: 连接对象,失败返回 False
        """
        try:
            self.obj = paramiko.SSHClient()
            self.obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 设置允许连接不在know_host文件中的机器
            self.obj.connect(self.hostip, self.port, self.username, self.password)
        except Exception as e:
            logger.error("远程连接主机失败，错误详情如下：IP [{0}], 失败具体原因：[{1}]".format(self.hostip, e))
            return False
        return self.obj
    
    def __objsftp(self):
        """
        : return: sftp连接对象
        """
        self.obj = self.__sshconnet()
        self.objsftp = self.obj.open_sftp()
        return self.objsftp
    
    def __sshconnet_close(self):
        self.obj.close()

    def __objsftp_close(self):
        self.objsftp.close()
        
    def run_cmd(self, cmd):
        """
        : param cmd: 需要运行的命令,请确保参数命令正确无误
        : return: 运行正常的结果数据
        """
        obj = self.__sshconnet()
        result_list_out = []
        result_list_err = []
        stdin, stdout, stderr = obj.exec_command(cmd)
        for i in stdout.readlines():
            result_list_out.append(i)
        for i in stderr.readlines():
            result_list_err.append(i)
        if len(result_list_err) > 0:
            result_list = result_list_err
            logger.warning("执行命令时发生错误，错误IP：[{0}],错误命令：[{1}],错误详情为：[{2}]".format(self.hostip, cmd, result_list))
        else:
            result_list = result_list_out
        return result_list

    def run_cmdlist(self, cmdlist):
        """
        : param cmdlist: 需要运行的多条命令
        : return: 以列表形势返回执行正确的结果
        """
        # 需要参照上面修改。
        result_list = []
        obj = self.__sshconnet()
        for cmd in cmdlist:
            stdin, stdout, stderr = obj.exec_command(cmd)
            if len(stderr.readline()) <= 0:
                # stdin.write("Y")  # 简单交互，输入 ‘Y’
                for i in stdout.readlines():
                    result_list.append(i)
            else:
                logger.warning("执行多条命令时发生错误，错误IP：[%s],错误命令：[%s]" % (self.hostip, cmd))
                for i in stderr.readlines:
                    result_list.append(i)
        return result_list

    def get_file(self, remotepath, localpath):
        """
        : param remotepath: 远程机器目录路径
        : param localpath: 本地机器目录路径
        : return: 成功或失败的字典数据  True 为成功， False 失败，
        """
        data = {"result": "返回获取文件执行结果"}
        objsftp = self.__objsftp()
        objsftp.get(remotepath, localpath)
        return data

    def put_file(self, localpath, remotepath):
        """
        : param remotepath: 远程机器目录路径
        : param localpath: 本地机器目录路径
        : return: 成功或失败的字典数据  True 为成功， False 失败，
        """
        data = {"result": "返回上传文件执行结果"}
        objsftp = self.__objsftp()
        objsftp.put(localpath, remotepath)
        return data
    

