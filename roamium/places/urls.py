from django.urls import path, include
from rest_framework import routers
from .views import PlaceViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register('places', PlaceViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]
