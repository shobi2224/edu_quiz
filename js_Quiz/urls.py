from django.urls import path
from . import views

urlpatterns = [
    path('quiz/<str:topic_name>/', views.quiz_view, name='quiz'),
]
