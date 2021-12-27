from django.conf.urls import url, include
from actsapi import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^admin/', admin.site.urls),
    url(r'^api/v1/properties/$', views.PropertyList.as_view()),
    url(r'^api/v1/properties/(?P<pk>[0-9]+)$', views.PropertyDetail.as_view()),
    url(r'^api/v1/activities/$', views.ActivityList.as_view()),
    url(r'^api/v1/activities/(?P<pk>[0-9]+)$', views.ActivityDetail.as_view()),
    url(r'^api/v1/cancel_activity/(?P<pk>[0-9]+)$', views.CancelActivity.as_view()),
    url(r'^api/v1/resc_activity/(?P<pk>[0-9]+)$', views.RescheduleActivity.as_view()),
    url(r'^api/v1/survey/(?P<pk>[0-9]+)$', views.SurveyDetail.as_view(),name='survey-detail'),    
]
