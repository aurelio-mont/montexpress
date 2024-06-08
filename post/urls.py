from post.views import list_posts_for_author_view,list_create_posts_view, retrieve_update_destroy_posts_view, homepage, get_posts_for_current_user
from django.urls import path

urlpatterns = [
    path('', list_create_posts_view, name='post_list'),
    path('<int:pk>/', retrieve_update_destroy_posts_view, name='post_detail'),
    path('homepage/', homepage, name='post_homepage'),
    path('curent_user_posts/', get_posts_for_current_user, name='user_post_list'),
    path('author_posts/', list_posts_for_author_view, name='author_post_list'),

]