from django.urls import path
from api.views import (
    UserRegistrationView,
    UserloginView,
    MenProductAPIView,
    WomenProductAPIView,
    ChildrenProductAPIView,
    BlogAPIView,
    CartListCreateView,
    CartDeleteView,
    WishlistListCreateView,
    WishlistDeleteView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserloginView.as_view(), name="login"),
    path("products/men/", MenProductAPIView.as_view(), name="men-products"),
    path(
        "products/men/<int:id>/", MenProductAPIView.as_view(), name="men-product-detail"
    ),
    path("products/women/", WomenProductAPIView.as_view(), name="women-products"),
    path(
        "products/women/<int:id>/",
        WomenProductAPIView.as_view(),
        name="women-product-detail",
    ),
    path(
        "products/children/", ChildrenProductAPIView.as_view(), name="children-products"
    ),
    path(
        "products/children/<int:id>/",
        ChildrenProductAPIView.as_view(),
        name="children-product-detail",
    ),
    path("blogs/", BlogAPIView.as_view(), name="blogs"),
    path("blogs/<int:id>/", BlogAPIView.as_view(), name="blog-detail"),
    path("cart/", CartListCreateView.as_view(), name="cart-list-create"),
    path("cart/<int:pk>/", CartDeleteView.as_view(), name="cart-delete"),
    path("wishlist/", WishlistListCreateView.as_view(), name="wishlist-list-create"),
    path("wishlist/<int:pk>/", WishlistDeleteView.as_view(), name="wishlist-delete"),
]
