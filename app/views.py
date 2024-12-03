from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser, Book, Transaction, Exchange, Wishlist
from .serializers import CustomUserSerializer, BookSerializer, TransactionSerializer, ExchangeSerializer, WishlistSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# ViewSet for User
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# ViewSet for Book
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# ViewSet for Transaction
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
#ds
# ViewSet for Exchange
class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer

# ViewSet for Wishlist
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer


#7765674523

'''
{
"username": "Edward",
"email": "edward@gmail.com",
"password": "edwardo",
"name": "edward"
}
'''

# Registration View
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")  # Add name to the payload

        if not username or not email or not password or not name:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(username=username, email=email, password=password, name=name)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "message": "User registered successfully"})

# Login View
class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the user's refresh token
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            # Blacklist the token
            token.blacklist()
            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

#new variant

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .serializers import UserRegisterSerializer, UserSerializer

from datetime import datetime, timedelta


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.error)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data

            access_token = tokens['access']
            refresh_token = tokens['refresh']

            seriliazer = UserSerializer(request.user, many=False)

            res = Response()

            res.data = {'success': True}

            res.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            res.set_cookie(
                key='refresh_token',
                value=str(refresh_token),
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            res.data.update(tokens)
            return res

        except Exception as e:
            print(e)
            return Response({'success': False})


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            request.data['refresh'] = refresh_token

            response = super().post(request, *args, **kwargs)

            tokens = response.data
            access_token = tokens['access']

            res = Response()

            res.data = {'refreshed': True}

            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='None',
                path='/'
            )
            return res

        except Exception as e:
            print(e)
            return Response({'refreshed': False})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:

        res = Response()
        res.data = {'success': True}
        res.delete_cookie('access_token', path='/', samesite='None')
        res.delete_cookie('response_token', path='/', samesite='None')

        return res

    except Exception as e:
        print(e)
        return Response({'success': False})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    return Response(User.objects.all())



import jwt,datetime


class register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class loginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email = email).first()


        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data ={
            'jwt':token
        }

        return response


class userget(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('unauthenticated')

        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class logoutView(APIView):
    def post(self,request):
        respnse = Response()
        respnse.delete_cookie('jwt')
        respnse.data = {
            "message":"success"
        }
        return respnse
