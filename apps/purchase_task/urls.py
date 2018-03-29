from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns = [
    url(r'^', include('apps.core.urls')),
    url(r'^/', include('apps.core.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login_view, name='login_view'),
    url(r'^logout/', logout_view, name='logout_view'),
    url(r'^register/', register_profile, name='register_view'),
    url(r'^update_profile/', update_profile, name='update_view'),

]
