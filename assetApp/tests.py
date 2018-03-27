from django.test import TestCase

# Create your tests here.
import math

pk = 3
page_num = 2    # 分页时每页的页数
page = 1    # 设置需要请求的页

if int(pk) >= int(page_num):
    print('----')
    page = pk / page_num
else:
    print('===')
print("原数据: %s" % page)
print("round: %s" % round(page))
print("int: %s" % int(page))
print("ceil: %s " % math.ceil(page))









