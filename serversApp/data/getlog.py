#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 2017/12/18
# Email：

import paramiko
from .server_opt import SSHConnection
import logging
import string
import time
import re
import platform
logger = logging.getLogger('django')


class GetServerData(object):
    def __init__(self, **search_messages):
        self.IP = search_messages['IP']
        self.logpath = search_messages['logpath']
        self.viewtype = search_messages['viewtype']                     # 查看方式 tail head grep sed
        self.viewkeyword = search_messages['viewkeyword']               # 查询关键字
        self.viewnumber = search_messages['viewnumber']                 # 显示行数
        self.viewnumber_type = search_messages['viewnumber_type']       # 查看方式grep 默认、前、后、前后
        self.download_start_n = search_messages['download_start_n']     # 下载时开始行号
        self.download_end_n = search_messages['download_end_n']         # 下载时开始行号

    def parameter_hand(self):
        """
            输入参数处理，检查是否合法等。
        : return: 一条合法的命令
        """
        search_messages = {}
        search_messages["safe"] = False
        # 检查路径是否合法
        un_safety_commands = ["|", ">", ">>", "#", "@", "$"]  # 定义不安全的字符
        if self.logpath == "":
            logger.info('获取日志,日志路径不能为空')
            search_messages['safe'] = ["日志路径不能为空"]
            return search_messages
        for i in un_safety_commands:
            if self.logpath.find(i) != -1:
                logger.info('获取日志,输入路径中含有非法字符[ %s ]' % i)
                search_messages["safe"] = ['输入路径中含有非法字符[ %s ]' % i]
                return search_messages
        t = self.logpath[-4:]
        if t != ".out" and t != ".log":
            logger.info("获取日志,文件名不对,必须以 .out  或  .log 结尾")
            search_messages["safe"] = ["文件名不对,必须以 .out  或  .log 结尾"]
            return search_messages
        # 检查输入方式
        if self.viewtype == "tail" or self.viewtype == "head":
            if self.viewnumber_type != "" or self.download_start_n != "" or self.download_end_n != "":
                logger.info("获取日志,赞不支持该条件查询，当查询方式为 head 或 tail 时, [viewnumber_type] "
                            "[download_start_n] [download_end_n] 应为空")
                search_messages["safe"] = ["赞不支持该条件查询，当查询方式为 head 或 tail 时,"
                                           "[grep显示方式为],[下载时开始行号],[下载时开始行号]应为空"]
                return search_messages
            if self.viewnumber == "":
                logger.info("获取日志,赞不支持该条件查询，当查询方式为 head 或 tail 时, [viewnumber] 不能为空")
                search_messages["safe"] = ["赞不支持该条件查询，当查询方式为 head 或 tail 时, [显示行数]不能为空"]
                return search_messages

            else:
                search_messages["commend"] = "%s -%s %s" % (self.viewtype, self.viewnumber, self.logpath)
        if self.viewtype == "grep":
            if self.viewkeyword == "" or self.viewnumber_type == "":
                logger.info("获取日志,赞不支持该条件查询，当查询方式为 grep 时, [ %s ] [ %s ] "
                            "不能为空" % (self.viewkeyword, self.viewnumber_type))
                search_messages["safe"] = ["赞不支持该条件查询，当查询方式为 grep 时, [关键字] [查看方式grep]不能为空"]
                return search_messages
            else:
                search_messages["commend"] = "grep -n '{0}' -{1} 10 '{2}' | tail -{3} "\
                    .format(self.viewkeyword, self.viewnumber_type, self.logpath, self.viewnumber)
        # 返回合法命令及安全标识
        return search_messages

    def hand_data(self, usernaem, passwd, port):
        """
            数据逻辑处理，主要入口
        : return:  数据逻辑处理结果
        """
        logger.info('获取日志,进入数据逻辑处理函数')
        data = []       # 服务器返回信息
        search_messages = self.parameter_hand()
        if not search_messages["safe"]:
            logger.info("获取日志,生成正确的执行命令: [ %s ]" % search_messages['commend'])
        else:
            logger.info("获取日志,输入参数错误，返回提示：[ %s ]" % search_messages['safe'])
            return search_messages['safe']

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            logger.info("获取日志,尝试连接服务器: IP [%s] 用户名：[%s] " % (self.IP, usernaem))
            ssh.connect(self.IP, port, usernaem, passwd)
        except:
            logger.error('获取日志,服务器连接失败')
            data.append('服务器连接失败')
            search_messages["grepvalue"] = data
            return search_messages['grepvalue']
        stdin, stdout, stderr = ssh.exec_command('ls %s' % self.logpath)

        if len(stderr.readline()) <= 0:
            try:
                stdin, stdout, stderr = ssh.exec_command(search_messages['commend'])
                for i in stdout.readlines():
                    data.append(i)
            except Exception as e:
                logger.error("获取日志,命令执行失败： 服务器IP [{0}] 用户：[{1}] 执行命令: "
                             "[{2}]".format(self.IP, usernaem, search_messages['commend']))
                logger.error("获取日志,执行命令异常详情为：%s " % e)
                data.append('执行命令失败,请联系管理员紧急处理.谢谢!!!')
        else:
            logger.info('获取日志,输入的文件不存在，请重新输入! IP: %s  path: %s'.format(self.IP, self.logpath))
            data.append("输入的文件不存在，请重新输入!")
        search_messages["grepvalue"] = data
        ssh.close()
        logger.info('获取日志,数据处理函数结束,处理结果： %s' % search_messages['grepvalue'])
        return search_messages['grepvalue']


class ServerOptControl(object):
    """
    服务器操作参数控制
    """
    def __init__(self, **opt_base_messages):
        self.ip = opt_base_messages['ip']
        self.ip_username = opt_base_messages['ip_username']
        self.ip_passwd = opt_base_messages['ip_passwd']
        self.ip_port = opt_base_messages['ip_port']

    def __cmd(self, cmd_content):
        """
        : param cmd_content: 需要执行的命令
        : return: 命令执行的结果
        """
        logger.info("获取日志,开始执行命令： %s" % cmd_content)
        cmd_ssh = SSHConnection(self.ip, self.ip_username, self.ip_passwd, self.ip_port)
        data = cmd_ssh.run_cmd(cmd_content)
        logger.info("获取日志,命令执行完成： %s" % cmd_content)
        return data

    def bash_cmd_control(self, cmd, cmd_content):
        """
            基础命令操作控制主函数
        : return: 基础命令操作之后的结果
        """
        messages = {}
        messages["safe"] = False
        cmd_control_list = ["ping", "ls", "telnet", "curl"]     # 定义可执行的命令列表
        if cmd in cmd_control_list:     # 判断命令是否在可执行命令列表中
            cmd_messages = cmd_content.split(" ")   # 对传入进来的命令进行分割判断
            # logger.info("----调试使用----- %s------%s----%s" %(len(cmd_messages),cmd_messages, cmd_messages[1]))

            # 对输入的结果进行判断整理，过滤成合法命令。
            if cmd == "ping" and cmd_messages[0] == "ping":
                if cmd_messages[1] != "-c":
                    messages["result"] = ["ping 命令必须携带参数 -c，请参照说明填写。"]
                elif not cmd_messages[2].isdigit() or int(cmd_messages[2]) <= 0 or int(cmd_messages[2]) >= 10:
                    logger.info("----调试使用----- %s -----------" % cmd_messages[2])
                    messages["result"] = ["ping 命令中-c 参数必须未 1 - 9 中任意数据，数字过大返回结果时间过长。"]
                elif len(cmd_messages) >= 5:
                    messages["result"] = ["ping 命令参数过长，请参照说明执行。"]
                    logger.warning("ping 命令执行中含有非法参数，命令详情为：%s" % cmd_content)
                else:
                    messages["result"] = self.__cmd(cmd_content)
                messages["safe"] = True
            elif cmd == "ls" and cmd_messages[0] == "ls":
                # 检查路径是否合法
                un_safety_commands = ["|", ">", ">>", "&", "&&"]  # 定义不安全的字符
                if len(cmd_messages) != 2:
                    messages["result"] = ["ls 命令参数过长，只允许查看单个目录，请参照说明执行。"]
                    logger.warning("ls 命令执行中含有非法参数或目录过多，命令详情为：%s" % cmd_content)
                elif cmd_messages[1]:
                    for i in un_safety_commands:
                        if cmd_messages[1].find(i) != -1:
                            logger.info('获取日志,输入路径中含有非法字符[ %s ]' % i)
                            messages["result"] = ['输入路径中含有非法字符[ %s ]' % i]
                            messages["safe"] = True
                    if len(cmd_messages[1]) >= 120:
                        messages["result"] = ['查看的目录不能超过120个字符，如有需要请联系管理员，谢谢。']
                        messages["safe"] = True
                    elif not messages['safe']:
                        messages["result"] = self.__cmd(cmd_content)
                messages["safe"] = True
            elif cmd == "telnet" and cmd_messages[0] == "telnet":
                messages["result"] = ["telnet 参数规则暂未确认，任在开发中。"]
                #  下面代码需要解决 telnet成功后如何结束的问题
                # if len(cmd_messages) != 3:
                #     messages["result"] = ["telnet 命令格式错误，参照: telnet xx.xx.xx.xx 22  or  telnet www.baidu.com 80"]
                # elif not cmd_messages[2].isdigit():
                #     messages["result"] = ["telnet 命令格式错误,指定端口必须为数字,你的输入端口为：%s" % cmd_messages[2]]
                # else:
                #     messages["result"] = self.__cmd(cmd_content)
                messages["safe"] = True
            elif cmd == "curl" and cmd_messages[0] == "curl":
                messages["safe"] = True
                messages["result"] = ["curl 参数规则暂未确认，任在开发中。"]
            else:
                logger.info("获取日志,需要执行的命令与实际输入命令不符合，请检查。")
                messages["safe"] = True
                messages["result"] = ["需要执行的命令与实际输入命令不符合，请检查。选择的命令为："
                                      "[{0}],实际执行的命令为：[{1}]".format(cmd, cmd_messages[0])]
        else:
            logger.info("获取日志,输入为参数：[{0}]，其中命令：[{1}] 不能为空 或 不允许的操作,如有必要请联系管理员.".format(cmd_content, cmd))
            messages["safe"] = True
            messages["result"] = ["输入为参数：[{0}]，其中命令：[{1}] 不能为空 或 不允许的操作,如有必要请联系管理员.".format(cmd_content, cmd)]
        return messages

    def log_query_control(self, query_type, query_cmd_content):
        """
            日志查询操作主控函数
        : return: 日志查询操作之后的结果
        """
        messages = {}
        messages["safe"] = False
        query_type_list = ["grep", "tail", "head"]     # 定义可执行的命令列表
        if query_type in query_type_list:     # 判断命令是否在可执行命令列表中
            query_messages = query_cmd_content.split(" ")   # 对传入进来的命令进行分割判断
            # logger.info("%s------%s----%s" %(len(query_messages), query_type, query_messages[3]))   # 调试使用
            if query_type == "grep" and query_messages[0] == "grep":
                # grep 'xxxx' -C 10 /xxx/xxx.log | head -100
                # 检查路径是否合法
                un_safety_commands = ["|", ">", ">>", "&", "&&"]  # 定义不安全的字符
                if len(query_messages) != 8:
                    messages["result"] = ["grep 命令格式不对，请参照说明填写：grep 'xxxxx' -C 10 /xxx/xxx.log | head -100"]
                elif query_messages[2] != "-C" and query_messages[2] != "-B" and query_messages[2] != "-A":
                    messages["result"] = ["grep 命令第二参数必须为 -C | -A | -B ，请参照说明填写,默认可以选 -C 0"]
                elif query_messages[4][-4:] != ".out" and query_messages[4][-4:] != ".log":
                    messages["result"] = ["文件名不对,必须以 .out  或  .log 结尾"]
                elif not query_messages[3].isdigit():
                    messages["result"] = ["grep 命令格式不对，参数 -C | -A | -B 必须指定查看行数"]
                elif query_messages[5] != "|":
                    messages["result"] = ["grep 命令格式不对,请参照说明填写：grep 'xxxx' -C 10 /xxx/xxx.log | head -100"]
                elif query_messages[6] != "head" and query_messages[6] != "tail":
                    messages["result"] = ["grep 命令格式不对,请参照说明填写：grep 'xxx' -C 10 /xxx/xxx.log | head -100"]
                elif query_messages[7][0] != "-" and query_messages[7][1:].isdigit() and int(query_messages[7][1:]) >= 500:
                    messages["result"] = ["grep 命令格式不对,请参照说明填写，必须限定查看行数,且小于500行，如 -100"]
                elif query_messages[1][0] != "'" and query_messages[1][0] != '"' \
                        or query_messages[1][-1] != "'" and query_messages[1][-1] != '"':
                    messages["result"] = ["grep 命令格式不对,请参照说明填写，查询的关键字必须使用引号"]
                elif query_messages[4]:
                    for i in un_safety_commands:
                        if query_messages[4].find(i) != -1:
                            logger.info('获取日志,输入路径中含有非法字符[ %s ]' % i)
                            messages["result"] = ['输入路径中含有非法字符[ %s ]' % i]
                            messages["safe"] = True
                    if len(query_messages[4]) >= 120:
                        messages["result"] = ['查看的目录不能超过120个字符，如有需要请联系管理员，谢谢。']
                        messages["safe"] = True
                    #     感觉有问题，需要调试
                    elif not messages['safe']:
                        logger.info("获取日志,grep 查询规则通过，命令详情：%s" % query_cmd_content)
                        # 添加默认参数 -n
                        query_cmd_content_tmp = list(query_cmd_content)
                        query_cmd_content_tmp.insert(4, " -n")
                        query_cmd_content = "".join(query_cmd_content_tmp)
                        messages["result"] = self.__cmd(query_cmd_content)
                messages["safe"] = True
            elif query_type == "tail" and query_messages[0] == "tail":
                # tail -n xx /xxx/xxx.log
                if len(query_messages) != 4:
                    messages["result"] = ["tail 命令格式不正确，请参照说明填写：tail -n xx /xxx/xxx.log"]
                elif query_messages[1] != "-n":
                    messages["result"] = ["tail 命令参数不正确，请参照说明填写：tail -n x /xxx/xxx.log"]
                elif not query_messages[2].isdigit() and int(query_messages[2]) > 500:
                    messages["result"] = ["tail 命令参数不正确，请参照说明填写：-n 指定行数需小于500行"]
                elif query_messages[3][-4:] != ".out" and query_messages[3][-4:] != ".log":
                    messages["result"] = ["文件名不对,必须以 .out  或  .log 结尾"]
                else:
                    logger.info("获取日志,tail 查询规则通过，命令详情：%s" % query_cmd_content)
                    messages["result"] = self.__cmd(query_cmd_content)
                messages["safe"] = True
            elif query_type == "head" and query_messages[0] == "head":
                # head -n xx /xxx/xxx.log
                if len(query_messages) != 4:
                    messages["result"] = ["head 命令格式不正确，请参照说明填写：head -n xx /xxx/xxx.log"]
                elif query_messages[1] != "-n":
                    messages["result"] = ["head 命令参数不正确，请参照说明填写：head -n x /xxx/xxx.log"]
                elif not query_messages[2].isdigit() and int(query_messages[2]) > 500:
                    messages["result"] = ["head 命令参数不正确，请参照说明填写：-n 指定行数需小于500行"]
                elif query_messages[3][-4:] != ".out" and query_messages[3][-4:] != ".log":
                    messages["result"] = ["文件名不对,必须以 .out  或  .log 结尾"]
                else:
                    logger.info("获取日志,head 查询规则通过，命令详情：%s" % query_cmd_content)
                    messages["result"] = self.__cmd(query_cmd_content)
                messages["safe"] = True
            else:
                logger.info("获取日志,需要执行的命令与实际输入命令不符合，请检查。")
                messages["safe"] = True
                messages["result"] = ["需要执行的命令与实际输入命令不符合，请检查。选择的命令为："
                                      "[{0}],实际执行的命令为：[{1}]".format(query_type, query_messages[0])]
        else:
            logger.info("获取日志,输入为参数：[{0}]，其中命令：[{1}] 不能为空 或 不允许的操作,如有必要请联系管理员.".format(query_cmd_content, query_type))
            messages["safe"] = True
            messages["result"] = ["输入为参数：[{0}]，其中命令：[{1}] 不能为空 或 不允许的操作,如有必要请联系管理员.".format(query_cmd_content, query_type)]
        return messages

    def log_download_control(self, download_path, download_begin_line, download_end_line):
        """
            日志下载操作主控函数,先通过sed命令下载需要的日志在服务器上,然后通过远程获取到平台服务器,再通过web下载给用户.
        : return:
        """
        messages = {}
        messages["safe"] = False
        messages["safe_number"] = False
        un_safety_commands = ["|", ">", ">>", "&", "&&"]  # 定义不安全的字符
        # __cmd
        if not download_begin_line.isdigit() and not download_end_line.isdigit():
            messages["result"] = ["开始行号或结束行号必须为数字"]
            messages["safe"] = True
        elif int(download_begin_line) >= int(download_end_line):
            messages["result"] = ["开始行号必须小于结束行号"]
            messages["safe"] = True
        elif download_path[-4:] != ".out" and download_path[-4:] != ".log":
            messages["result"] = ["文件名不对,必须以 .out  或  .log 结尾"]
            messages["safe"] = True
        elif download_path:
            for i in un_safety_commands:
                if download_path.find(i) != -1:
                    logger.info('获取日志,输入路径中含有非法字符[ %s ]' % i)
                    messages["result"] = ['输入路径中含有非法字符[ %s ]' % i]
                    messages["safe"] = True
            if len(download_path) >= 120:
                messages["result"] = ['查看的目录不能超过120个字符，如有需要请联系管理员，谢谢。']
                messages["safe"] = True
            logger.info("获取日志,查看路径[{0}]在服务器[{1}]是否存在".format(download_path, self.ip))
            messages["view_download_path"] = self.__cmd("ls %s" % download_path)
            logger.info("%s" % messages["view_download_path"])
            if messages["view_download_path"][0] == "%s\n" % download_path:
                messages["sed_mkdir_tmp"] = self.__cmd("test -d /tmp/yunwei_platform_special_tmp "
                                                       "|| mkdir /tmp/yunwei_platform_special_tmp")
                logger.info("创建目录的信息: %s" % messages["sed_mkdir_tmp"])
                try:
                    download_path_name = download_path.split("/")[-1][:-4]
                    localtime_download = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                    download_file_name = "%s_%s.log" % (download_path_name, localtime_download)
                except Exception as e:
                    logger.warning("获取日志,文件中必须是/xx/xx/x.log,具体错误详情: %s" % e)
                    messages["result"] = ["文件中必须是/xx/xx/x.log,具体错误详情: %s" % e]
                #  sed -n '100,130p' /xxx/xxx/a.log >> /tmp/xxx.log
                messages["sed_download_file"] = self.__cmd("sed -n '{0},{1}p' {2} >> /tmp/yunwei_platform_"
                                                           "special_tmp/{3}".format(download_begin_line,
                                                                                    download_end_line,
                                                                                    download_path,
                                                                                    download_file_name))
                logger.info("获取日志,在服务器上使用sed命令重定向日志到/tmp/yunwei_platform_special_tmp/{0},"
                            "返回详细信息:{1}".format(download_file_name, messages["sed_download_file"]))
                logger.info("获取日志,开始执行下载命令,文件名: %s" % download_file_name)
                cmd_ssh = SSHConnection(self.ip, self.ip_username, self.ip_passwd, self.ip_port)
                system_version = platform.system()
                if system_version == "Windows":
                    data = cmd_ssh.get_file("/tmp/yunwei_platform_special_tmp/%s" %
                                            download_file_name, "data\\downloadlog\\%s" % download_file_name)
                elif system_version == "Linux":
                    data = cmd_ssh.get_file("/tmp/yunwei_platform_special_tmp/%s" %
                                            download_file_name, "data/downloadlog/%s" % download_file_name)
                logger.info("获取日志,下载文件返回详细信息: %s" % data)
                logger.info("获取日志,下载命令执行完成文件名: %s" % download_file_name)
                messages["result"] = ["%s_%s" % (download_path_name, localtime_download)]
                messages["safe"] = True
                messages["safe_number"] = True
            else:
                messages["safe"] = True
                messages["result"] = ["需要下载的日志文件在服务器上不存在,请使用基础命令ls先检查确认."]
        else:
            messages["result"] = ["参数不正确..."]
            messages["safe"] = True
        return messages
