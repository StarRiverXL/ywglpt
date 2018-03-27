from django.db import models

# Create your models here.


class viewlog(models.Model):
    """
        日志查看服务器数据表
    """
    env = models.CharField('环境', max_length=3)
    IP = models.GenericIPAddressField('IP')
    SSHport = models.CharField('SSH端口', max_length=5)
    username = models.CharField('登陆用户', max_length=30)
    passwd = models.CharField('登陆密码', max_length=50)

    def __str__(self):
        return self.env


class appmanagement(models.Model):
    """
        应用管理明细表
    """
    env = models.CharField('环境', max_length=3)
    appName = models.CharField('应用名称', max_length=25)
    code = models.CharField('应用编码', max_length=10)
    operationsPersonnel = models.CharField('运维人员', max_length=25)
    state_CHOICE = {
        ('1', '启用'),
        ('2', '停用')
    }
    state = models.CharField(max_length=2, verbose_name="状态", choices=state_CHOICE, default='1')
    ipOut = models.GenericIPAddressField('外网IP', blank=True, null=True)
    ipIn = models.GenericIPAddressField('内网IP', blank=True, null=True)
    path = models.CharField('应用部署路径', max_length=50)
    deployName = models.CharField('应用部署名称', max_length=25)
    port = models.IntegerField('监听端口', default=0)
    urlLink = models.CharField('访问地址', max_length=50)
    modified_time = models.DateTimeField('修改时间', auto_now_add=True)
    code_state_CHOICE = {
        ('1', "None"),
        ('2', "start"),
        ('3', "stop"),
        ('4', "restart")
    }
    code_state = models.CharField(max_length=10, verbose_name="操作动作", choices=code_state_CHOICE, default='1')
    code_update_time = models.DateTimeField('更新时间', blank=True, null=True)
    code_content = models.CharField("验证码", max_length=6, blank=True, null=True)
    code_send_content = models.CharField('发送内容', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.appName








