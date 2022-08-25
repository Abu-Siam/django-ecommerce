from django.urls import path
from order.views import ProductListView,HomePageView,DashboardView

urlpatterns =[
    path('products/<category_title>', ProductListView.as_view(), name='product-list-categorised'),
    path('home/', HomePageView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('products/', ProductListView.as_view(), name='product-list'),

]