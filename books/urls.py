from django.contrib import admin
from django.urls import path,include
from . import views


app_name = 'books'

urlpatterns = [

    path('add-book/', views.AddBookCreateView.as_view(),name='add_books'),
    path('edit-book/<int:id>/', views.EditBookUpdateView.as_view(),name='edit_books'),
    path('delete-book/<int:id>/', views.BookDeleteView.as_view(),name='delete_books'),
    path('details-book/<int:id>/', views.DetailBookView.as_view(),name='details_books'),
    path('review-book/<int:id>/', views.ReviewBookView.as_view(),name='review_books'),
]

