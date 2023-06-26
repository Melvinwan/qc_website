from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('status/', views.status, name='status'),
    path('laser/', views.laser_page_view, name='laser_page'),
    path('rfsoc/', views.rfsoc_page_view, name='rfsoc_page'),
    path('mercury/', views.mercury_page_view, name='mercury_page'),
    path('caylar/', views.caylar_page_view, name='caylar_page'),
    re_path(r'^.*\.*', views.pages, name='pages'),
]
