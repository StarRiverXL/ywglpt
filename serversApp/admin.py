from django.contrib import admin

# Register your models here.
from .models import viewlog, appmanagement


class ViewLogAdmin(admin.ModelAdmin):
    list_display = ['env', 'IP', 'username', 'passwd']


class AppManagementAdmin(admin.ModelAdmin):
    list_display = ['env', 'appName', 'code', 'operationsPersonnel',
                    'state', 'ipOut', 'ipIn', 'path', 'deployName', 'port', 'urlLink']


admin.site.register(viewlog, ViewLogAdmin)
admin.site.register(appmanagement, AppManagementAdmin)


