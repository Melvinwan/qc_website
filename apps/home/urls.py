from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('status/', views.status, name='status'),
    path('laser/', views.laser_page_view, name='laser_page'),
    re_path(r'^.*\.*', views.pages, name='pages'),
]
