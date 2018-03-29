"""bx_econ URL Configuration

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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static


from apps.core.views import (
    login_view, logout_view, register_profile, update_profile)
from apps.purchase_task.views import (mock_form)


urlpatterns = [
    url(r'^', include('apps.core.urls')),
    url(r'^/', include('apps.core.urls')),
    url(r'^/task', include('apps.purchase_task.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login_view, name='login_view'),
    url(r'^logout/', logout_view, name='logout_view'),
    url(r'^register/', register_profile, name='register_view'),
    url(r'^update_profile/', update_profile, name='update_view'),
    url(r'^mock/', mock_form, name='mock_form'),
    url(r'^task/', include('apps.purchase_task.urls')),
]
