from django.urls import path
from . import views

urlpatterns = [
    path('user_banner/', views.user_banner_view),
    path('banner/', views.banners_view),
    path('banner/<int:id>/', views.banner_view),
]
