import io

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, \
    UserChangePasswordSerializer, UserPasswordResetEnterPhoneSerializer,EditUserProfileSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.models import MyUser
from rest_framework.parsers import JSONParser



# Create your views here.
def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_token(user)
            return Response({"token": token, "msg": "registration successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.data.get('phone')
            password = serializer.data.get('password')
            user = authenticate(phone=phone, password=password)

            if user is not None:
                token = get_token(user)
                return Response({"token": token, "msg": "login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": "email or password incorrect"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, uid, token, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "change password successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetEnterPhoneView(APIView):
    def post(self, request, format=None):
        serializer = UserPasswordResetEnterPhoneSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "passwrod otp link sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        # json_data = request.user
        # stream = io.BytesIO(json_data)
        # python_data = JSONParser().parse(stream)
        user_phone = request.user.phone
        # print(user_phone)
        user = MyUser.objects.get(phone=user_phone)
        serializer = EditUserProfileSerializer(user, data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg": "updated profile"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # serializer = EditUserProfileSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     return Response(serializer.data, status=status.HTTP_200_OK
        return Response( status=status.HTTP_400_BAD_REQUEST)
