from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

import views
from views import send_results


print "reached purchase_task urls"

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

# urlpatterns = patterns(
#     url(r'^favicon\.ico$', favicon_view),
# )
#

urlpatterns = [
    # url(r'^', views.task_form_view),
    url(r'^$', views.welcome_vew),
    url(r'^instructions', views.instructions_view),
    url(r'^begin_task', views.begin_task),
    url(r'^task_view', views.task_view),
    # url(r'^task', views.task_view),
    url(r'^process_form', views.process_form_data),
    url(r'^completion', views.task_complete_view),
    url(r'^logout', views.logout_view),
    url(r'^(?P<results_email>[0-9]+)/(task_with_url_params)', views.task_with_url_params),
    url(ur'^task/(?P<results_email>.*)/$', views.task_with_url_params),
    url(ur'^task/(?P<results_email>.*)/(?P<participant_id>[0-9]+)', views.task_with_url_params),
    # url(r'^(?P<results_email>[A-Za-z0-9!@#$%^&*()-_]+)/(task_with_url_params)', views.task_with_url_params),
    # url(r'^(?P<results_email>[\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b]+)/(task_with_url_params)', views.task_with_url_params),
    # url(r'^instructions_view', views.instructions_view),
    url(r'^favicon\.ico$', favicon_view),
    url(r'send_results', send_results, name='send_results'),
    # url(r'^question_validate/', views.question_validate),



]
