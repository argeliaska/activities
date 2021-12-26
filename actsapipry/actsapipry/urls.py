from django.conf.urls import url, include
from actsapi import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^admin/', admin.site.urls),
    url(r'^properties/$', views.PropertyList.as_view()),
    url(r'^properties/(?P<pk>[0-9]+)$', views.PropertyDetail.as_view()),
    url(r'activities/$', views.ActivityList.as_view()),
    url(r'activities/(?P<pk>[0-9]+)$', views.ActivityDetail.as_view()),
]
