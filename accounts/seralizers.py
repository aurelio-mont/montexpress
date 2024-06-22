from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from accounts.models import User

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(max_length=8, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        
    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        username_exists = User.objects.filter(username=attrs['username']).exists()

        if email_exists:
            raise ValidationError('Email already exists')
        
        if username_exists:
            raise ValidationError('Username already exists')

        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        
        Token.objects.create(user=user)

        return user
    

class CurrentUserPostsSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True, view_name="post_detail", queryset=User.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "posts"]

