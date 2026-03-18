from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Category,Product,Cart,CartItem,Coupon,Order,OrderItem,Wallet,Wishlist,Stock
User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
        
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Category
        fields="__all__"


class ProductSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = "__all__"
        
class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Cart
        fields="__all__"

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    

    class Meta:
        model = CartItem
        fields = "__all__"  
        read_only_fields = ['cart']

class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_percent', 'active']
        

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['user'] 

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context['request']

        # 👇 Sirf admin status change kar sakta hai
        if 'status' in validated_data:
            if not request.user.is_staff:
                validated_data.pop('status')

        return super().update(instance, validated_data)
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields="__all__"

class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model=Wishlist
        fields="__all__"
        
class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ['id','user', 'balance']   # ❗ user field hata diya

class StockSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    category_name = serializers.CharField(
        source="product.category.name",
        read_only=True
    )

    class Meta:
        model = Stock
        fields = ["id", "product", "product_name", "category_name", "quantity"]