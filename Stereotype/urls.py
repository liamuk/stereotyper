from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from Stereotype_app import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.s_index),
    url(r'^explore/', views.s_explore),
    url(r'^search_helper', views.s_search_helper),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # TODO: find a better way of serving static files
