from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("subpage/<int:book_id>/", views.subpage, name="subpage"),
]
