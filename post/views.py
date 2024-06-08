from accounts.seralizers import CurrentUserPostsSerializer

from django.shortcuts import get_object_or_404

from rest_framework import status, generics, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser


from post.models import Post
from post.serializers import PostSerializer
from post.permitions import AuthorOrReadOnly
from post.pagination import PostPagination

@api_view(http_method_names=['GET', 'POST'])
@permission_classes([])
def homepage(request: Request):
    if request.method == 'POST':
        data = request.data
        return Response(data=data, status=status.HTTP_200_OK)

    response = {'message': 'Hello World'}
    return Response(data=response, status=status.HTTP_200_OK)

@api_view(http_method_names=['GET', 'POST'])
def list_create_posts(request: Request):
    
    if request.method == 'POST':
        data = request.data
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Post created successfully',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        response = {
            'message': 'Validation error',
            'data': serializer.errors
        }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    

    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    response = {
        'message': 'List of posts',
        'data': serializer.data
    }
    return Response(data=response, status=status.HTTP_200_OK)

@api_view(http_method_names=['GET','PUT','DELETE'])
def post_detail(request: Request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        response = {
            'message': 'Post detail',
            'data': serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        data = request.data
        serializer = PostSerializer(post, data=data)

        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Post updated successfully',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        
        response = {
            'message': 'Validation error',
            'data': serializer.errors
        }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PostListCreateAPIView(APIView):

    serializer_class = PostSerializer

    def get(self, request: Request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Post created successfully',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostRetrieveUpdateDestroyAPIView(APIView):

    serializer_class = PostSerializer

    def get(self, request: Request, id, *args, **kwargs):
        post = get_object_or_404(Post, pk=id)
        serializer = self.serializer_class(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request: Request, id, *args, **kwargs):
        post = get_object_or_404(Post, pk=id)
        data = request.data
        serializer = self.serializer_class(post, data=data)

        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Post updated successfully',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request: Request, id, *args, **kwargs):
        post = get_object_or_404(Post, pk=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostListCreateViewGenerics(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination

    queryset = Post.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

list_create_posts_view = PostListCreateViewGenerics.as_view()

class PostRetrieveUpdateDestroyViewGenerics(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

retrieve_update_destroy_posts_view = PostRetrieveUpdateDestroyViewGenerics.as_view()

    
    
@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request: Request):
    user = request.user

    serializer = CurrentUserPostsSerializer(instance=user, context={"request": request})

    return Response(data=serializer.data, status=status.HTTP_200_OK)

class ListPostsForAuthorView(generics.GenericAPIView, mixins.ListModelMixin):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.request.query_params.get("username") or None
        queryset = self.queryset
        print(username)
        if username is not None:
            return Post.objects.filter(author__username=username)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    


list_posts_for_author_view = ListPostsForAuthorView.as_view()