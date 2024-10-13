from django.urls import path
from . import views


urlpatterns = [
    path('', views.postwall, name='postwall'),
    path('post/', views.post, name='post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/delete/confirm/', views.delete_post_confirmation, name='delete_post_confirmation'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('search/', views.search, name='search'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
]
