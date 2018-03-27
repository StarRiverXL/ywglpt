from django.db import models


# Create your models here.


class AddressYunwei(models.Model):
    name = models.CharField('姓名', max_length=30)
    phone = models.CharField('电话', max_length=30)
    email = models.EmailField('邮箱')
    position = models.CharField('岗位', max_length=30)
    QQ = models.CharField('QQ', max_length=30)
    note = models.CharField('备注', max_length=30)




