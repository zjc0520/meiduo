from django.conf.urls import url
from oauth import views

urlpatterns = [
    url(r'^qq/authorization/$', views.QQURLView.as_view()),
    url(r'^qq/user/$',views.QQloginView.as_view())
]