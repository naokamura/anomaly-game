from django.urls import path
from . import views

app_name = "records"

urlpatterns = [
    path('', views.start_view, name='start'),
    path('start/', views.start_game, name='start_game'),
    path('list/', views.record_list, name='list'),
    path('<int:pk>/', views.record_detail, name='detail'),
    path('analysis/', views.analysis_view, name='analysis'),
]
