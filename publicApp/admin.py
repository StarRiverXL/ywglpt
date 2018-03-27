from django.contrib import admin
from .models import Navigation, SiteNavigation, MonitorPlatform
# Register your models here.


class NavigationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'upper_business', 'remark']


class SiteNavigationAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'business_type', 'img', 'introduction']
    search_fields = ['name']


class MonitorPlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'remark']
    search_fields = ['name', 'url']


admin.site.register(Navigation, NavigationAdmin)
admin.site.register(SiteNavigation, SiteNavigationAdmin)
admin.site.register(MonitorPlatform)

# 账号密码   admin/1234qwer



