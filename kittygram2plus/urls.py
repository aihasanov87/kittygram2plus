from rest_framework import routers

from django.contrib import admin
from django.urls import include, path

from cats.views import (AchievementViewSet, CatViewSet,
                        UserViewSet, CatViewSetPaginator)


router = routers.DefaultRouter()
router.register(r'cats', CatViewSet)
router.register(r'v2/cats', CatViewSetPaginator)
router.register(r'users', UserViewSet)
router.register(r'achievements', AchievementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
