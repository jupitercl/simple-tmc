from django.conf.urls import url
from django.contrib import admin
from sitio import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.tmc_view, name='index'),
]
