from django.conf.urls import patterns, include, url

from verdict import views

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'istelemarketer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', views.front, name='front'),

    # url(r'^admin/', include(admin.site.urls)),
)
