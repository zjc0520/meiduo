"""meiduo_1 URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^', include('meiduo_1.apps.users.urls')),
    url('^', include('meiduo_1.apps.verifications.urls')),
    url(r'^oauth/',include('meiduo_1.apps.oauth.urls')),
    url(r'^',include('meiduo_1.apps.areas.urls')),
    url(r'^',include('meiduo_1.apps.goods.urls')),
    url(r'^',include('meiduo_1.apps.contents.urls')),
    url(r'^ckeditor/',include('ckeditor_uploader.urls'))
]
