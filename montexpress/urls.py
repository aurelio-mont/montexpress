from django.contrib import admin
from django.urls import path, include

#from post.routers import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
    path('accounts/', include('accounts.urls')),
]
