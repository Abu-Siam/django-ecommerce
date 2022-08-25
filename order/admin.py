from django.contrib import admin

# Register your models here.
from order.models import Order,OrderItems,Product,Category,Blog,BlogDetail


admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(BlogDetail)
