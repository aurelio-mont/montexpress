from rest_framework import serializers
from post.models import Post

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']