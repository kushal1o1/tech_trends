"""
URL configuration for tech_trends project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from trends.views import TechNewsViewSet, NewsSourcesViewSet
from mailApp.views import SubscriberViewSet,SubscribedCategoryViewSet,VerifyEmailView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

schema_view =get_schema_view(
    openapi.Info(
        title="Tech Trends",
        default_version="v1",
        description="My api",
        terms_of_service="https://www.google.com/kushal1o1",
        contact=openapi.Contact(email="share.kushal@gmail.com"),
        license=openapi.License(name="MIT"),),
        public=True,
        permission_classes=(permissions.AllowAny,),
        
    )

router = DefaultRouter()
router.register(r'trends', TechNewsViewSet)
router.register(r'subscribers', SubscriberViewSet, basename='subscribers')
router.register(r"categories",SubscribedCategoryViewSet,basename="categories")
router.register(r'sources', NewsSourcesViewSet, basename='sources')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('verify-email/<uuid:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='scheme-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
