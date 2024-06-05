from rest_framework.routers import DefaultRouter
from post.viewsets import PostViewSet

router = DefaultRouter()
router.register(r'', PostViewSet)