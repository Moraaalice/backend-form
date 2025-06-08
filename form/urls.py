# form/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_form, name='submit_form'),
    path('submit/<int:submission_id>/', views.get_submission_by_id, name='get_submission_by_id'),
    path('submissions/', views.get_submissions, name='get_submissions'),
    path('submit/<int:submission_id>/update/', views.update_submission, name='update_submission'),
]
