from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.models import MyUser
from order.models import Order,Product,Blog,Category

# class HomeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('title','specs','rating','price','status')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__',)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','order_date','total_amt','order_status')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title','specs','rating','price','status','category_title',)

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('title','author')




