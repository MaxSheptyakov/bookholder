from django.urls import path
from . import views

app_name = 'book_receiver'

urlpatterns = [ # post views
    path('', views.main, name='main'),
    path('catalog/', views.catalog, name='catalog'),
    path('add_book/', views.upload_book, name='add_book'),
    path('donations/', views.donations, name='donations'),
    path('book/<slug:book_slug>/', views.book_info, name='book_info'),
    ]