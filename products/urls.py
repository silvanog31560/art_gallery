from django.urls import path

from . import views

app_name='products'
urlpatterns = [
    path('add/', views.ProductCreate.as_view(), name='add-product'),
    path('<str:filter_val>/<str:orderby>/', views.ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('update/<int:pk>', views.ProductUpdate.as_view(), name='product-update'),
    path('delete/<int:pk>', views.ProductDelete.as_view(), name='product-delete'),
]
