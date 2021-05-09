"""roamium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, \
                                            TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import routers

# Aggregate all apps in custom API root
@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'places': reverse('place-list', request=request, format=format),
        'login': reverse('token_obtain_pair', request=request, format=format),
        'refresh_token': reverse('token_refresh', request=request, format=format),
    })

# Custom Admin Panel
admin.site.site_header = 'Roamium Admin Panel'
admin.site.site_title = 'Roamium Admin Panel'
admin.site.index_title = 'Welcome to Roamium'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('api/user/', include('users.urls')),
    path('api/place/', include('places.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
