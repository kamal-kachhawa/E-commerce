# admin.py
from django.contrib import admin
from api.models import User, Product, Blog
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Custom User Admin
class UserModelAdmin(BaseUserAdmin):
    list_display = ["id", "email", "name", "is_admin"]
    list_filter = ["is_admin"]

    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal Info", {"fields": ["name"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["name", "email", "password1", "password2"],
            },
        ),
    ]

    search_fields = ["email", "name"]
    ordering = ["id", "email"]
    filter_horizontal = []


# Product Admin
class ProductModelAdmin(admin.ModelAdmin):

    # Django admin me jaha product list show hoti hai (table format)
    list_display = [
        "name",
        "category",
        "subcategory",
        "brand",
        "sku",
        "price",
        "discount",
        "final_price",
        "main_image",
        "stock",
    ]

    # Sidebar filter ke liye
    list_filter = ["category", "brand", "size", "color"]

    # Django admin ke andar product detail view (read/edit)
    fieldsets = [
        (
            "Basic Info",
            {
                "fields": [
                    "name",
                    "description",
                    "category",
                    "subcategory",
                    "brand",
                    "sku",
                ]
            },
        ),
        ("Pricing", {"fields": ["price", "discount", "final_price"]}),
        ("Other Details", {"fields": ["main_image", "size", "color", "stock"]}),
    ]

    # Jab product add karte hain admin me, to input form ke liye
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "name",
                    "description",
                    "category",
                    "subcategory",
                    "brand",
                    "sku",
                    "price",
                    "discount",
                    "main_image",
                    "size",
                    "color",
                    "stock",
                ],
            },
        ),
    ]

    # Search bar ke liye fields
    search_fields = ["name", "sku", "brand"]

    # Sorting
    ordering = ["id", "name"]

    # Read-only field, jo auto calculate hota hai
    readonly_fields = ["final_price"]


class BlogModelAdmin(admin.ModelAdmin):
    list_display = ["product_title", "author", "created_at"]
    list_filter = ["author"]
    search_fields = ["product_title", "description"]


# Product model register karo admin me
admin.site.register(Product, ProductModelAdmin)
# Registering Models
admin.site.register(User, UserModelAdmin)
admin.site.register(Blog, BlogModelAdmin)
