from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('verifySchedule', views.verifySchedule, name='verifySchedule'),
    path('generateSchedule', views.generateSchedule, name='generateSchedule'),
]
