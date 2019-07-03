from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("<int:pk>/comment", views.blog_comment, name="blog_comment"),
    path("<category>/", views.blog_category, name="blog_category"),
]
