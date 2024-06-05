from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostListCreateViewGenerics.as_view(), name='post_list'),
    path('<int:pk>/', views.PostRetrieveUpdateDestroyViewGenerics.as_view(), name='post_detail'),
    path('homepage/', views.homepage, name='post_homepage'),

]