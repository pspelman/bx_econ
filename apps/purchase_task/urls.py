from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static


import views

print "reached purchase_task urls"

urlpatterns = [
    # url(r'^', views.task_form_view),
    url(r'^$', views.welcome_vew),
    url(r'^begin_task', views.begin_task),
    url(r'^task', views.task_view),
    url(r'^process_form', views.process_form_data),
    url(r'^completion', views.task_complete_view),
    url(r'^logout', views.logout_view),
    # url(r'^question_validate/', views.question_validate),


]
