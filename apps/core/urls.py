from django.conf.urls import url, include
from . import views

print "reached core urls.py"

urlpatterns = [
    url(r'^', views.index),
    url(r'^begin', views.login_view),
    url(r'^login', views.login_view),
    url(r'^home', views.home),
    # url(r'^logout', views.logout_view),

]
