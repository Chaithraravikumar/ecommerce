from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from django.db.models import Q 

from catalogapp.models import Categorie, Product, Cart, Review, OrderPlaced
from catalogapp.api.serializers import ProductSerializer, CatagorieSerializer, CartSerializer, ReviewSerializer

class CatagorieList(APIView):
    def get(self, request):
        categories = Categorie.objects.all()
        serializer = CatagorieSerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CatagorieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CatagorieDetail(APIView):
    def get(self, request,pk):
        try:
            categories = Categorie.objects.get(pk=pk)
            serializer = CatagorieSerializer(categories)
            return Response(serializer.data)
        except Categorie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    def put(self, request, pk):
        try:
            category = Categorie.objects.get(pk=pk)
            serializer = CatagorieSerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Categorie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            category = Categorie.objects.get(pk=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Categorie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)    
        
class ProductList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer       

class CartList(generics.ListAPIView):
    serializer_class = CartSerializer
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Cart.objects.filter(added_by__username=username)   
    
class Checkout(APIView):
    def get(self, request):
        total_item=0
        user=request.user
        cart_items=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=75.0
        total_amount=0.0
        cart_product=[pro for pro in Cart.objects.all() if pro.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
        totalamount=amount + shipping_amount
        if request.user.is_authenticated:
                total_item=len(Cart.objects.filter(user=request.user))
        return Response({'totalamount':totalamount,'cart_items':cart_items,'total_item':total_item})
            
class AddCart(APIView):
    def get(self, request):
      prod_id=request.GET['prod_id']
      cart=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      cart.quantity+=1
      cart.save()
      amount=0.0
      shipping_amount=75.0
      total_amount=0.0
      cart_product=[p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
      totalamount=amount + shipping_amount

      data={
            'quantity':cart.quantity,
            'amount':amount,
            'totalamount':totalamount
      }
      return Response(data)
  
class RemoveCart(APIView):
    def get(self, request):
        total_item=0
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=75.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
                tempamount=(p.quantity * p.product.discounted_price)
                amount+=tempamount
        totalamount=amount + shipping_amount
        if request.user.is_authenticated:
            total_item=len(Cart.objects.filter(user=request.user))
        data={
                'amount':amount,
                'totalamount':totalamount,
                'total_item':total_item
        }
        return Response(data)

class PlaceOrder(APIView):
    def post(request):
        total_item=0
        order_placed=OrderPlaced.objects.filter(user=request.user)
        if request.user.is_authenticated:
                total_item=len(Cart.objects.filter(user=request.user))
        return Response({'order_placed':order_placed,'total_item':total_item})

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        pro = Product.objects.get(pk=pk)
        
        user = self.request.user
        product_queryset = Review.objects.filter(product=pro,review_user=user)
        
        if product_queryset.exists():
            raise ValidationError("You have already reviewed this product!")
        
        if pro.number_rating == 0:
            pro.avg_rating = serializer.validated_data['rating']
        else:
            pro.avg_rating = (pro.avg_rating + serializer.validated_data['rating'])/2

        pro.number_rating = pro.number_rating + 1
        pro.save()
        serializer.save(watchlist=pro, review_user=user)

class ReviewParticular(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(product=pk)

class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
