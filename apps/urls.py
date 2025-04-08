from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TestViewSet, UserTestResultViewSet, UserSubscriptionViewSet
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.include_root_view = False

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('', include(router.urls)),

   path('categorys/', CategoryViewSet.as_view({'get': 'list','post':'create'})),
   path('category/<int:id>',CategoryViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
   path('tests/', TestViewSet.as_view({'get': 'list','post':'create'})),
   path('test/<int:id>',TestViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
   path('user-test-result/', UserTestResultViewSet.as_view({'get': 'list','post':'create'})),
   path('user-test-result/<int:id>',UserTestResultViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
   path('user-subscription', UserSubscriptionViewSet.as_view({'get': 'list','post':'create'})),
   path('user-subscript/<int:id>',UserSubscriptionViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

   path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
