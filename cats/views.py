from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import filters

from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .throttling import WorkingHoursRateThrottle
from .pagination import CatsPagination


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (
        AnonRateThrottle, WorkingHoursRateThrottle, ScopedRateThrottle)
    # подключаем кастомный лимит
    throttle_scope = 'low_request'
    # Если нужно выключить пагинацию, то нужно так pagination_class = None
    # pagination_class = None
    pagination_class = LimitOffsetPagination

    # Указываем фильтрующий бэкенд DjangoFilterBackend
    # Из библиотеки django-filter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    # Временно отключим пагинацию на уровне вьюсета,
    # так будет удобнее настраивать фильтрацию
    pagination_class = None
    # Фильтровать будем по полям color и birth_year модели Cat
    # Фильтр
    filterset_fields = ('color', 'birth_year', 'name')
    # Поиск
    search_fields = ('=name', '=achievements__name', '=owner__username')
    # Сортировка
    ordering_fields = ('name', 'birth_year')
    # Сортировка по умолчанию
    ordering = ('-id',)

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CatViewSetPaginator(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (
        AnonRateThrottle, WorkingHoursRateThrottle, ScopedRateThrottle)
    # подключаем кастомный лимит
    throttle_scope = 'low_request'
    # Если нужно выключить пагинацию, то нужно так pagination_class = None
    pagination_class = PageNumberPagination

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Вот он наш собственный класс пагинации с page_size=20
    pagination_class = CatsPagination


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
