from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import Post
from .serializers import UserSerializer, PostSerializer
from .permissions import IsAuthorOrReadOnly


# Authentication Helper Function
def create_auth_response(user):
    token = AuthToken.objects.create(user)[1]  
    return {
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
        'token': token 
    }


# User Registration API
@api_view(['POST'])
def register_api(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(create_auth_response(user), status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login API
@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        return Response(create_auth_response(user)) 
    return Response({'error': "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# Get Authenticated User Data
@api_view(['GET'])
def get_user_data(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    return Response({'error': 'Not Authenticated'}, status=status.HTTP_401_UNAUTHORIZED)



class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
