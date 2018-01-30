from django.conf.urls import url, include  
from rest_framework import routers

from .views import JobViewSet


router = routers.DefaultRouter()  
# register job endpoint in the router
router.register(r'jobs', JobViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [  
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]