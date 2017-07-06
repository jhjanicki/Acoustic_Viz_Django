"""acoustic_viz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


import queries.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^get-data/$', queries.views.get_data),
    url(r'^get-sites/$', queries.views.get_sites),
    url(r'^site/(?P<id>\D+)/', queries.views.site),
    url(r'^site/', queries.views.site),
    url(r'^$', queries.views.hello_peeg),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# r'^site/\D+/'
# /(?P<site_id>[a-zA-Z0-9_]+)/