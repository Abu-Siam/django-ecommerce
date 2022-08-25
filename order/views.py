from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.models import MyUser
from order.serializers import ProductSerializer,BlogSerializer,OrderSerializer,CategorySerializer,ProductCreateSerializer
from order.models import Order,Product,Blog
from rest_framework.permissions import IsAuthenticated

# Create your views here.

def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class ProductListView(APIView):
    def get(self, request, category_title,format=None):
        if category_title is None:
            product = Product.objects.all()
        else:
            product = Product.objects.filter(category__title=category_title)
        serializer = ProductSerializer(product,many=True)
        try:
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request,category, format=None):
        for item in request.data:

            serializer = ProductCreateSerializer(data = item)
            if serializer.is_valid():
                serializer.save()

        return Response({"data": serializer.data})


class HomePageView(APIView):
    def get(self, request, format=None):
        top_products = Product.objects.all().order_by('-rating')[:1]
        top_product_serializer = ProductSerializer(top_products,many=True)
        recent_products = Product.objects.all().order_by('-date_added')[:2]
        recent_product_serializer = ProductSerializer(recent_products,many=True)
        blog = Blog.objects.all().order_by('-pub_date')[:1]
        blog_serializer = BlogSerializer(blog,many=True)

        try:
            return Response({"top_products":top_product_serializer.data,"recent_products":recent_product_serializer.data,"blog":blog_serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"msg":"invalid request"}, status=status.HTTP_400_BAD_REQUEST)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        past_order = Order.objects.filter(user__phone= request.user.phone).filter(order_status='delivered').order_by('-order_date')[:2]
        past_order_serializer = OrderSerializer(past_order,many=True)
        current_order = Order.objects.filter(user__phone= request.user.phone).filter(order_status='process').order_by('-order_date')[:2]
        current_order_serializer = OrderSerializer(current_order,many=True)
        try:
            return Response({"past_order":past_order_serializer.data, "current_order":current_order_serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response(past_order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

