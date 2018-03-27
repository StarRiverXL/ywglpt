from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.
from .models import AddressYunwei
import logging
logger = logging.getLogger('django')


def address(request):
    logger.info("获取运维通讯录")
    address_yunwei_list = AddressYunwei.objects.all()
    logger.info("返回运维通讯录结果成功")
    return render(request, 'smallfunApp/address.html', {"address_yunwei_list": address_yunwei_list})
    # return render(request, 'smallfunApp/address.html')



