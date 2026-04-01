from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Halls
    path('halls/', views.hall_list, name='hall_list'),
    path('halls/create/', views.hall_create, name='hall_create'),
    path('halls/<int:pk>/delete/', views.hall_delete, name='hall_delete'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Exams
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/create/', views.exam_create, name='exam_create'),
    path('exams/<int:pk>/delete/', views.exam_delete, name='exam_delete'),

    # Seating
    path('exams/<int:exam_id>/seating/', views.seating_view, name='seating_view'),
    path('exams/<int:exam_id>/seating/auto/', views.auto_assign, name='auto_assign'),
    path('exams/<int:exam_id>/seating/assign/', views.assign_seat, name='assign_seat'),
    path('exams/<int:exam_id>/seating/clear/', views.clear_seating, name='clear_seating'),

    # API
    path('api/exams/<int:exam_id>/seating/', views.api_seating, name='api_seating'),
]
