from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', views.index),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^main/$', views.main, name='main'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^confirm/$', views.confirm, name='confirm'),
    url(r'^lock/$', views.lock, name='lock'),
    url(r'^unlock/$', views.unlock, name='unlock'),
    url(r'^newreport/$', views.newreport, name='newreport'),
    url(r'^savereport/$', views.savereport, name='savereport'),
    url(r'^unfixed/$',views.unfixed,name='unfixed'),
    url(r'^fixed/$', views.fixed, name='fixed'),
]