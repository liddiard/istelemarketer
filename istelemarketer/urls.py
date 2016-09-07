from django.conf.urls import include, url

from verdict import views

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'istelemarketer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', views.FrontPageView.as_view(), name='front'),
    url(r'^api/check/$', views.CheckPhoneNumberView.as_view(), name='check'),

    # url(r'^admin/', include(admin.site.urls)),
]