from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,IsAdminUser
)
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model

from .models import (
    Category, Product, Cart, CartItem,
    Coupon, Order, OrderItem, Wallet, Wishlist,Stock
)

from .serializers import (
    CategorySerializer, ProductSerializer, CartSerializer,
    CartItemSerializer, CouponSerializer, OrderSerializer,
    OrderItemSerializer, WalletSerializer, WishlistSerializer,
    UserSerializer,StockSerializer
)

User = get_user_model()


# ==========================
# CATEGORY
# ==========================
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]   # sab GET kar sakte hain
        return [IsAdminUser()]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ==========================
# PRODUCT
# ==========================
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]   # sab GET kar sakte hain
        return [IsAdminUser()]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ==========================
# CART
# ==========================
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    


# ==========================
# CART ITEM
# ==========================


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
        serializer.save(user=self.request.user)

# ==========================
# COUPON
# ==========================
class CouponViewSet(viewsets.ModelViewSet):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()   

    def get_queryset(self):
        # Admin sab dekh sakta hai
        if self.request.user.is_staff:
            return Coupon.objects.all()

        # Customer sirf active coupons dekhega
        return Coupon.objects.filter(active=True)

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]   
        return [IsAdminUser()]    
# ==========================
# ORDER
# ==========================
class OrderViewSet(viewsets.ModelViewSet):
    queryset =Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Admin sab orders dekh sakta hai
        if user.is_staff:
            return Order.objects.all()

        # User sirf apne orders dekh sakta hai
        return Order.objects.filter(user=user)


# ==========================
# ORDER ITEM
# ==========================
class OrderItemViewSet(viewsets.ModelViewSet):
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaa")
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ==========================
# WISHLIST
# ==========================
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ==========================
# WALLET
# ==========================
class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
# ==========================
# USER + LOGIN / LOGOUT
# ==========================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    # LOGIN
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "id": user.id,
            "username": user.username
        })

    # LOGOUT
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"})
    
    
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def create(self, request, *args, **kwargs):

        product_id = request.data.get("product")
        quantity = request.data.get("quantity")

        stock = Stock.objects.filter(product_id=product_id).first()
        quantity = int(quantity)


        # अगर stock already exist है → update
        if stock:
            stock.quantity += quantity
            stock.save()

            serializer = self.get_serializer(stock)
            return Response(serializer.data)

        # अगर exist नहीं करता → create
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)