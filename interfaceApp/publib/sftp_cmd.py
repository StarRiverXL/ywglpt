#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko
import os
import re
import sys


class RemoteConnection(object):
    """
    Upload files or execute shell commands
    """
    def __init__(self, ssh_ip, ssh_port, ssh_user, ssh_passwd):
        self.ip = ssh_ip
        self.port = ssh_port
        self.user = ssh_user
        self.passwd = ssh_passwd

    def checkIp(self, ip):
        """
        Check for IPV4 address type
        :param ip: 192.168.0.0
        :return: False || True
        """
        p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if p.match(ip):
            return True
        else:
            return False

    def checkType(self, **parameter):
        """
        Check that the health value type in the dictionary is the same
        :param parameter: {"str": "str", int: 1,}
        :return: if error,return 1
        """
        para = parameter
        for k, v in para.values()[0].items():
            if type(k) != type(v):
                print("Parameter type error: key[ {0} ] ,value[ {1} ]".format(k, v))
                return 1

    def cmdExecute(self, exe_cmd):
        """
        Execute the shell command, return the execution result, default 10 timeout
        :return: result
        """
        p = {self.ip: "str", self.port: 1, self.user: "str", self.passwd: "str", exe_cmd: "str"}
        self.checkType(parameter=p)
        ip = self.checkIp(self.ip)
        if ip == False:
            print('The ip "{0}" you entered is not IPV4 type, please check.'.format(self.ip))
            return 1
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(self.ip, self.port, self.user, self.passwd, timeout=10)
                stdin, stdout, stderr = ssh.exec_command(exe_cmd, timeout=10)
                error = stderr.readlines()
                result = stdout.readlines()
                if error:
                    print('Command "{0}" fails, for the following reasons.'.format(exe_cmd))
                    for i in range(len(error)):
                        print(error[i]),
                    return 1
                else:
                    print('Command "{0}" performs successfully, and the result is as follows.'.format(exe_cmd))
                    for i in range(len(result)):
                        print(result[i]),
                    return 0
                    # for i in stdout:
                    #     print(i.strip("\n")
                    #     if "a" in str(i):
                    #         print("aaaaa"
                    #         exit(0)
                    #     else:
                    #         print("bbbbb"
            except Exception as e:
                print('The instantiation parameter is: ip "{0}"、 port "{1}"、 user "{2}"、 passwd "{3}"、 ' \
                      'cmd [ {4} ]'.format(self.ip, self.port, self.user, self.passwd, exe_cmd))
                info = sys.exc_info()
                print("Exception types: ", info[0], ":", info[1])
                print("The instantiation of the connection is abnormal, for the following reasons.")
                print(e)
            finally:
                 ssh.close()

    def uploadFiles(self, local_file, remote_file):
        p = {self.ip: "str", self.port: 1, self.user: "str", self.passwd: "str", local_file: "str", remote_file: "str"}
        self.checkType(parameter=p)
        if os.path.exists(local_file) == False:
            print("The local file %s does not exist. Please check it." % (local_file))
            return 1
        ip = self.checkIp(self.ip)
        if ip == False:
            print('The ip "{0}" you entered is not IPV4 type, please check.'.format(self.ip))
            return 1
        else:
            try:
                ssh_sftp = paramiko.Transport(self.ip, self.port)
                ssh_sftp.connect(username=self.user, password=self.passwd)
                sftp = paramiko.SFTPClient.from_transport(ssh_sftp)
                a = sftp.put(local_file, os.path.join(os.path.split(remote_file)[0], remote_file))
                print(a)
            except IOError as io:
                print("The remote object should be specified to the file, not just the directory," \
                      " or other IO errors. For example: /home/tmp/a.txt")
                print(io)
            except Exception as e:
                print('The instantiation parameter is: ip "{0}"、 port "{1}"、 user "{2}"、 passwd "{3}"、 ' \
                      'local_file [ {4} ]、remote_file [ {5} ]'.format(self.ip, self.port, self.user, self.passwd,
                                                                       local_file, remote_file))
                info = sys.exc_info()
                print("Exception types: ", info[0], ":", info[1])
                print("The instantiation of the connection is abnormal, for the following reasons.")
                print(e)
            finally:
                ssh_sftp.close()

if __name__ == '__main__':
    a = RemoteConnection("192.168.78.19", 22, "root", "123123")
    a.cmdExecute("bash /root/a.sha")
    a.uploadFiles("D:\\a.txt", "/root/a.txt")



