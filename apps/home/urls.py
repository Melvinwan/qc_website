from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('status/', views.status, name='status'),
    path('status-caylar/', views.statusCaylar, name='statuscaylar'),
    path('status-laser/', views.statusLaser, name='statuslaser'),
    path('status-mercury/', views.statusMercury, name='statusmercury'),
    path('status-rfsoc/', views.statusRFSoC, name='statusrfsoc'),
    path('plot/', views.update_live_plot, name='plot'),
    path('laser/', views.laser_page_view, name='laser_page'),
    path('rfsoc/', views.rfsoc_page_view, name='rfsoc_page'),
    path('mercury/', views.mercury_page_view, name='mercury_page'),
    path('caylar/', views.caylar_page_view, name='caylar_page'),
    path('live-data-rfsoc/', views.get_live_data_and_run_rfsoc, name='live_data_rfsoc'),
    path('start-experiment/', views.start_experiment, name='start_experiment'),
    path('stop-experiment/', views.stop_experiment, name='stop_experiment'),
    re_path(r'^.*\.*', views.pages, name='pages'),
]
