from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token # <--- The table for Keys

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')

    if User.objects.filter(username=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user (We use email as the username for simplicity)
    user = User.objects.create_user(username=email, email=email, password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    # Create the Key (Token) immediately
    token = Token.objects.create(user=user)

    return Response({
        'key': token.key, 
        'user_id': user.id,
        'email': user.email
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email, password=password)

    if user is not None:
        # Get or Create the token
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'key': token.key,
            'user_id': user.id,
            'email': user.email
        })
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # <--- Protects this view
def user_profile(request):
    # This view requires the Key in headers to work
    user = request.user
    return Response({
        'username': user.get_full_name() or user.username,
        'bio': "This is a bio from the server!",
        'post_count': 12, # Dummy data
        'email': user.email
    })
