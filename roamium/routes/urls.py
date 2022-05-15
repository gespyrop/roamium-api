from django.urls import path, include
from rest_framework import routers
from .views import RouteViewSet, VisitViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register('routes', RouteViewSet)
router.register('visits', VisitViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls))
]
