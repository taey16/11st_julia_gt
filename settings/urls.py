
from django.conf.urls import patterns, include, url
from main.views import main, update

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', main),
  url(r'^update/', update),
  # Examples:
  # url(r'^$', 'illy_gt.views.home', name='home'),
  # url(r'^illy_gt/', include('illy_gt.foo.urls')),

  # Uncomment the admin/doc line below to enable admin documentation:
  # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  # url(r'^admin/', include(admin.site.urls)),
)
