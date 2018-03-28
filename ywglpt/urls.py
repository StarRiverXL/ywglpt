"""ywglpt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from publicApp import views as pub_index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^public/', include('publicApp.urls')),
    url(r'^index/', pub_index.indexpage),
    url(r'^$', pub_index.checkuser),
    url(r'^asset/', include('assetApp.urls')),
    url(r'^servers/', include('serversApp.urls')),
    url(r'^ywdocument/', include('ywdocumentApp.urls')),
    url(r'^samllfun/', include('smallfunApp.urls')),
    url(r'^interface/', include('interfaceApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 图片访问地址




