from django.contrib import admin
from django.urls import path,include
from SearchAPP import views

urlpatterns = [
    path('Search/', views.SearchView.as_view()),
    path('DL/', views.DLView.as_view()),
    path('progress/', views.ProgressView.as_view()),    
]
