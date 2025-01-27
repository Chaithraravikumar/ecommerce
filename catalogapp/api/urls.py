from django.urls import path
from catalogapp.api.views import ProductList, ProductDetail, CatagorieList, CatagorieDetail, CartList, Checkout, AddCart, RemoveCart, ReviewCreate, ReviewParticular, ReviewList, PlaceOrder

urlpatterns = [
    path('products-list/', ProductList.as_view(), name='products-list'),
    path('products-detail/<int:pk>/', ProductDetail.as_view(), name='products-detail'),
    path('categorie-list/', CatagorieList.as_view(), name='categorie-list'),
    path('categorie-detail/<int:pk>/', CatagorieDetail.as_view(), name='categorie-detail'),
    path('cart/', CartList.as_view(), name='cart-view'),
    path('cart-checkout/', Checkout.as_view(), name='cart-checkout'),
    path('cart-add/<int:pk>/', AddCart.as_view(), name='cart-add-items'),
    path('cart-remove/<int:pk>/', RemoveCart.as_view(), name='cart-remove-items'),
    path('place-order/',PlaceOrder.as_view(),name = 'review-username'),
    path('review_details/<int:pk>/reviewcreate/',ReviewCreate.as_view(), name = 'review-detailcv'), 
    path('review_details/<int:pk>/',ReviewParticular.as_view(), name = 'review-details'), 
    path('review-details/',ReviewList.as_view(),name = 'review-username'),
]
