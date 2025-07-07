# views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from .serializers import UserLoginSerializer, ProductSerializer, BlogSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Blog, Cart, Wishlist
from .serializers import ProductSerializer, CartSerializer, WishlistSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Registration Successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserloginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {
                        "token": token,
                        "name": user.name,  # Add name (username) here
                        "msg": "Login Successfully",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["Email or Password is not Valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )


class MenProductAPIView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, id=None):
        if id is not None:
            try:
                product = Product.objects.get(id=id, category="Men")
                serializer = ProductSerializer(product, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )

        men_products = Product.objects.filter(category="Men")
        serializer = ProductSerializer(
            men_products, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data["category"] = "Men"
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Product added successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            product = Product.objects.get(id=id, category="Men")
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Product updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            product = Product.objects.get(id=id, category="Men")
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Product updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id, category="Men")
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        product.delete()
        return Response(
            {"msg": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class WomenProductAPIView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, id=None):
        if id is not None:
            try:
                product = Product.objects.get(id=id, category="Women")
                serializer = ProductSerializer(product, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )

        women_products = Product.objects.filter(category="Women")
        serializer = ProductSerializer(
            women_products, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data["category"] = "Women"
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Product added successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            product = Product.objects.get(id=id, category="Women")
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product, data=request.data, partial=False, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Product updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            product = Product.objects.get(id=id, category="Women")
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Product updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id, category="Women")
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        product.delete()
        return Response(
            {"msg": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class ChildrenProductAPIView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, id=None):
        if id is not None:
            try:
                product = Product.objects.get(id=id, category="Children")
                serializer = ProductSerializer(product, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )

        children_products = Product.objects.filter(category="Children")
        serializer = ProductSerializer(
            children_products, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data["category"] = "Children"
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Product added successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            product = Product.objects.get(id=id, category="Children")
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product, data=request.data, partial=False, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Product updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            product = Product.objects.get(id=id, category="Children")
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Product updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id, category="Children")
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        product.delete()
        return Response(
            {"msg": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class BlogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id is not None:
            try:
                blog = Blog.objects.get(id=id)
                serializer = BlogSerializer(blog)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Blog.DoesNotExist:
                return Response(
                    {"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND
                )

        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data["author"] = request.user.id
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(
                {"msg": "Blog created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            blog = Blog.objects.get(id=id, author=request.user)
        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog not found or you are not the author"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BlogSerializer(blog, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Blog updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            blog = Blog.objects.get(id=id, author=request.user)
        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog not found or you are not the author"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Blog updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            blog = Blog.objects.get(id=id, author=request.user)
        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog not found or you are not the author"},
                status=status.HTTP_404_NOT_FOUND,
            )

        blog.delete()
        return Response(
            {"msg": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class CartListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDeleteView(generics.DestroyAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class WishlistListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishlistDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class EmailTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
