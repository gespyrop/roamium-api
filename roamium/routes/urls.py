from django.urls import path, include
from rest_framework import routers
from .views import RouteViewSet, VisitViewSet

router = routers.DefaultRouter()
router.register('routes', RouteViewSet)
router.register('visits', VisitViewSet)

urlpatterns = [
    path('', include(router.urls))
]
