from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="API for Banner Service",
      contact=openapi.Contact(url="https://t.me/id_egoyan"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('user_banner/', views.UserBannerView.as_view(), 
         name='user_banner_view'),
    path('banner/', views.BannersView.as_view(),
         name='banners_view'),
    path('banner/<int:id>/', views.BannerView.as_view(),
         name='banner_view'),

    path('token/', views.TokenCreateView.as_view(),
         name='token_obtain_pair'),

    path('swagger/', 
         schema_view.with_ui('swagger', cache_timeout=0), 
         name='schema-swagger-ui'),
]
