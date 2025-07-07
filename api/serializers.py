from rest_framework import serializers
from api.models import User
from .models import Product, Blog, Cart, Wishlist


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match"
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]


class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(allow_null=True, required=False, default=None)
    description = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    subcategory = serializers.CharField(required=False)
    brand = serializers.CharField(required=False)
    sku = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    size = serializers.CharField(required=False)
    color = serializers.CharField(required=False)
    stock = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "subcategory",
            "brand",
            "sku",
            "price",
            "discount",
            "final_price",
            "main_image",
            "size",
            "color",
            "stock",
        ]


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    time_ago = serializers.CharField(read_only=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "author",
            "product_title",
            "description",
            "created_at",
            "time_ago",
            "image",
        ]
        read_only_fields = ["created_at"]


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = Cart
        fields = ["id", "user", "product", "product_id", "quantity", "created_at"]
        read_only_fields = ["user", "created_at"]


class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = Wishlist
        fields = ["id", "user", "product", "product_id", "created_at"]
        read_only_fields = ["user", "created_at"]
