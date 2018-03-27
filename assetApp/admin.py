from django.contrib import admin
from mptt.admin import MPTTModelAdmin
# Register your models here.
from .models import AssetManagement


class AssetManagementAdmin(admin.ModelAdmin):
    list_display = ['ip', 'host_name', 'project', 'system', 'cpu', 'memory', 'hard', 'remark']
    search_fields = ['ip']


admin.site.register(AssetManagement, AssetManagementAdmin)

# 账号密码   admin/1234qwer




