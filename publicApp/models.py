from django.db import models


# Create your models here.


class Navigation(models.Model):
    """
    左侧导航
    """
    name = models.CharField('导航名称', max_length=20)
    upper_business = models.IntegerField('上级id', blank=True, null=True)
    remark = models.CharField('备注', max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name


class SiteNavigation(models.Model):
    """
    站点导航
    """
    BUSINESS_TYPE_CHOICE = (
        ('A', 'A'),
        ('B', 'B'),
        ('other', 'other')
    )
    name = models.CharField('网站名', max_length=255)
    url = models.URLField('url地址')
    created_time = models.DateTimeField(auto_now_add=True)
    business_type = models.CharField('业务类型', max_length=5, choices=BUSINESS_TYPE_CHOICE, default=3)
    img = models.ImageField(upload_to='img/siteIndex/', default='img/siteIndex/default.jpg')    # 上传的图片
    introduction = models.CharField(max_length=255, default=None, null=True, blank=True)
    
    def __str__(self):
        return self.name


class MonitorPlatform(models.Model):
    """
    监控平台
    """
    GENDER_CHOICE = (
        (u'1', u'正常'),
        (u'2', u'异常'),
    )
    name = models.CharField('网站名', max_length=255)
    url = models.URLField()
    state = models.CharField('状态', max_length=2, choices=GENDER_CHOICE)
    remark = models.CharField('备注', max_length=255)
    
    def __str__(self):
        return self.name


