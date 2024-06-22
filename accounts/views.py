from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.seralizers import SignUpSerializer
from accounts.tokens import create_jwt_pair_for_user, delete_jwt_pair_for_user

class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                'message': 'Account created successfully',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            delete_jwt_pair_for_user(refresh_token)

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = []
    def post(self, request: Request):
        
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        
        if user is not None:
            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Successfull", "tokens": tokens}

            return Response(data=response   , status=status.HTTP_200_OK)
        
        response = {
            'message': 'Invalid credentials'
        }
        return Response(data=response, status=status.HTTP_401_UNAUTHORIZED)


    def get(self, request: Request):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }

        return Response(data=content, status=status.HTTP_200_OK)
    

class UsersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SignUpSerializer
    queryset = SignUpSerializer.Meta.model.objects.all()
    
    def get_queryset(self):
        return self.queryset
