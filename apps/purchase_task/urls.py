from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

import apt_logic
import views
from data_management import send_results, make_csv


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
    url(r'^(?P<researcher_email>[0-9]+)/(begin_task_with_url_params)', views.begin_task_with_url_params),
    url(ur'^task/(?P<researcher_email>.*)/$', views.begin_task_with_url_params),
    url(ur'^task/(?P<researcher_email>.*)/(?P<participant_id>[0-9]+)', views.begin_task_with_url_params),
    url(ur'^task/?researcher_email=(?P<researcher_email>.*)&participant_id=(?P<participant_id>[0-9]+)', views.begin_task_with_url_params),
    url(ur'^task/manual_input', views.manual_input),
    # url(r'^(?P<researcher_email>[A-Za-z0-9!@#$%^&*()-_]+)/(begin_task_with_url_params)', views.begin_task_with_url_params),
    # url(r'^(?P<researcher_email>[\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b]+)/(begin_task_with_url_params)', views.begin_task_with_url_params),
    # url(r'^instructions_view', views.instructions_view),
    url(r'^favicon\.ico$', favicon_view),
    url(r'send_results', send_results, name='send_results'),
    url(r'make_csv', make_csv, name='make_csv'),
    # url(r'^question_validate/', views.question_validate),

]

handler404 = views.error404
handler500 = views.error404

# handler404 = error.error_handler
# handler500 = error.error_handler