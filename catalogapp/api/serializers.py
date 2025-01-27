from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from catalogapp.models import Product, Categorie, Cart, Review

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class CatagorieSerializer(ModelSerializer):
    product_list = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Categorie
        fields = '__all__'
        
class CartSerializer(ModelSerializer):
    added_by = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Cart
        fields = '__all__'
        # exclude = ['product']
        
class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Review
        exclude = ('watchlist',)