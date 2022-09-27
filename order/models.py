from datetime import datetime

from django.db import models
from account.models import MyUser
# Create your models here.


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    title=models.CharField(max_length=100)

    def __str__(self):
        return self.title

status_choice=(
        ('process','In Process'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
    )
class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    order_date = models.DateTimeField(default = datetime.now)
    order_status=models.CharField(choices=status_choice,default='process',max_length=150)
    paid_status=models.BooleanField(default=False)
    total_amt=models.FloatField(default = 0.0)

    def __str__(self):
        return str(self.id)

RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class Product(models.Model):
    title=models.CharField(max_length=200)
    detail=models.TextField()
    specs=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True, blank=True)
    status=models.BooleanField(default=True)
    rating = models.IntegerField(choices=RATING,max_length=150)
    date_added=models.DateTimeField(default = datetime.now)
    price=models.PositiveIntegerField(default=0)
    is_featured=models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def category_title(self):
        return self.category.title


class OrderItems(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)
    qty = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return str(self.order.id)


class Blog(models.Model):
    title=models.CharField(max_length=200)
    detail=models.TextField()
    pub_date=models.DateField(auto_now_add=True)
    is_featured=models.BooleanField(default=False)

    def __str__(self):
        return self.title

class BlogDetail(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    details=models.TextField()

    def __str__(self):
        return self.blog.title






