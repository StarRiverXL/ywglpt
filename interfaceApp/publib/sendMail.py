#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 2017/08/28
# Email：
import smtplib, logging
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
logger = logging.getLogger('django')

MAIL_SERVER = "xxxxxxxxxxxxxxxxxxx"             # 设置服务器
MAIL_PORT = 25                                  # 设置发送邮件服务器端口,默认为 25
MAIL_USER = "test@xxxxxxxxxxxxxxxx.com"         # 用户名
MAIL_PASS = "xxxxxxxxxx"                        # 口令


class SendMail(object):
    def __init__(self, mail_server, mail_port, mail_user, mail_pass):
        self.mail_server = mail_server
        self.mail_port = mail_port
        self.mail_user = mail_user
        self.mail_pass = mail_pass

    def __send_mail(self, msg_instance, to_list_mail, sub1):
        msg_instance['Subject'] = Header(sub1, "utf-8")               # 设置邮件主题
        msg_instance['From'] = self.mail_user                         # 设置邮件发送人,注意：设置格式以后会出现代发现象
        msg_instance['To'] = Header(";".join(to_list_mail), "utf-8")  # 设置邮件接收人
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_server, port=self.mail_port)
            server.login(self.mail_user, self.mail_pass)
            logger.info("用户 [{0}] 成功登陆邮件服务器：{1}".format(self.mail_user, self.mail_server))
            server.sendmail(self.mail_user, to_list_mail, msg_instance.as_string())
            server.quit()
            return "邮件发送成功"
        except Exception as e:
            return "邮件发送异常，具体原因为: %s" % e

    def send_mail_text_or_html(self, to_list, sub, mail_sub_type, content):
        """
            发送邮件，以text或html格式。
            : param to_list: 需要发送的人，列表格式
            : param sub: 邮件发送主题
            : param mail_sub_type: 邮件发送格式 text/plain（普通文本邮件），html/plain(html邮件)
            : param content: 邮件发送内容,如果邮件发送格式为 html，内容传递也需要为 html 内容格式
            : return: True
        """
        msg = MIMEText(content, _subtype=mail_sub_type, _charset="utf-8")
        logger.info("本次接收参数为：[主题] {0}, [内容] {1}, [接收人] {2}".format(sub, content, to_list))
        return self.__send_mail(msg, to_list, sub)

    def send_mail_attachment(self, to_list, sub, filepath, file_show_name, content):
        """
            发送邮件，以附件的形式
            : param to_list: 需要发送的人，列表格式
            : param sub: 邮件发送主题
            : param filepath:发送的附件在本地的路径
            : param file_show_name: 发送的附件在邮件中显示的名称
            : return: True
        """
        msg = MIMEMultipart()                                                      # 创建一个带附件的实例
        att1 = MIMEText(open(filepath, 'rb').read(), 'base64', 'gb2312')           # 除路径以外其他暂时不懂
        att1["Content-Type"] = 'application/octet-stream'                          # 暂时不懂
        att1["Content-Disposition"] = 'attachment; filename=%s' % file_show_name   # filename 邮件中显示附近名称
        msg.attach(att1)                                       # 添加附件1   注：添加附件2 方式相同 msg.attach(att2)
        txt = MIMEText(content, 'plain', 'utf-8')
        msg.attach(txt)                                                            # 添加邮件说明内容
        # 以下是添加图片的方式，实验失败
        # file1 = "D:\\1.jpg"
        # image = MIMEImage(open(file1, 'rb').read())
        # image.add_header('Content-ID', '<image>')
        # msg.attach(image)
        logger.info("本次接收参数为：[主题] {0}, [接收人] {1}, [附件路径] {2}".format(sub, to_list, filepath))
        return self.__send_mail(msg, to_list, sub)


def mailMain(mail_to_list, mail_subject, mail_content):
    mail_type = "plain"
    mail = SendMail(MAIL_SERVER, MAIL_PORT, MAIL_USER, MAIL_PASS)
    return mail.send_mail_text_or_html(mail_to_list, mail_subject, mail_type, mail_content)


def userSendmail(subject, to_list, content):
    logger.info("本次发送邮件主题: %s" % subject)
    logger.info("本次发送邮件收件人列表： %s" % to_list)
    logger.info("本次发送邮件内容：%s" % content)
    if subject == None or content == None or to_list == None:
        logger.error("邮件主题、内容或收件人不能为空")
        return "邮件主题、内容或收件人不能为空"
    mail_to_list = []
    mail_to_list.append(to_list)
    result = mailMain(mail_to_list, str(subject), str(content))
    if result:
        logger.info("本次邮件发送结果: %s" % result)
        return result
    else:
        logger.info("本次邮件发送发生异常")
        return "发送异常"


# if __name__ == '__main__':
#     """
#         注意在较短时间内不要发送 主题相同的邮件，否则不成功。
#     """
#     mail_to_list = ["923912578@qq.com", "2637828320@qq.com"]    # 收件人列表
#     mail_subject = "hello17"                                    # 邮件主题
#
#     # 实例化对象
#     mail = SendMail(MAIL_SERVER, MAIL_PORT, MAIL_USER, MAIL_PASS)
#
#     # 发送普通文本邮件
#     mail_type = "plain"  # 邮件发送格式 text/plain（普通文本邮件），html/plain(html邮件)
#     mail_content = "hello world！"  # 邮件内容
#     result = mail.send_mail_text_or_html(mail_to_list, mail_subject, mail_type, mail_content)
#
#     # html邮件的发送
#     # mail_type = "html"
#     # mail_content = "<a href='https://www.baidu.com'> 点我跳转，说明为 html 内容 </a>"
#     # result = mail.send_mail_text_or_html(mail_to_list, mail_subject, mail_type, mail_content)
#
#     # 发送附件
#     # file_path = "D:\\a.txt"
#     # file_name = "a.txt"
#     # mail_content = "邮件说明内容，带有附件"  # 邮件内容
#     # result = mail.send_mail_attachment(mail_to_list, mail_subject, file_path, file_name, mail_content)
#
#     print result




