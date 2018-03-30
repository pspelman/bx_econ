from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static


import views


urlpatterns = [
    url(r'^', views.task_form_view),
    url(r'^/', views.task_form_view),
    url(r'^question_validate/', views.question_validate),

    #     # url(r'^register', views.register),
    # url(r'^login$', views.login),
    # url(r'^new$', views.register),
    # # url(r'^buy', views.buy_product),
    # url(r'success', views.purchase_success),
    # url(r'start_over', views.clear_order_history),
    # url(r'^success$', views.submission_success),
    # url(r'^reset$', views.reset),
    # url(r'^(?P<item_number>[0-9]+)/$', views.show),
    # url(r'^(?P<item_number>[0-9]+)/$', views.get_number),
    # url(r'^(?P<item_number>[0-9]+)/(edit)$', views.edit),
    # url(r'^(?P<item_number>[0-9]+)/(delete)$', views.delete),
    # url(r'^(P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views_month_archive),


]
