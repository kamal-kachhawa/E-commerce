# model.py
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from django.utils import timezone
from datetime import timedelta


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )

    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app app_label?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Men", "Men"),
        ("Women", "Women"),
        ("Children", "Children"),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    main_image = models.ImageField(upload_to="products", null=True, blank=True)
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        price = self.price if self.price is not None else 0
        discount = self.discount if self.discount is not None else 0
        self.final_price = price - (price * discount / 100)
        super().save(*args, **kwargs)

    def _str_(self):
        return f"{self.name} ({self.category})"


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    product_title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # image = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)

    def __str__(self):
        return f"{self.product_title} by {self.author.username}"

    @property
    def time_ago(self):
        """
        Returns a human-readable string like 'min ago', 'hour ago', 'days ago', etc.
        """
        now = timezone.now()
        diff = now - self.created_at

        if diff < timezone.timedelta(minutes=1):
            return "just now"
        elif diff < timezone.timedelta(hours=1):
            minutes = diff.seconds // 60
            return f"{minutes} min ago" if minutes != 1 else "1 min ago"
        elif diff < timezone.timedelta(days=1):
            hours = diff.seconds // 3600
            return f"{hours} hour ago" if hours != 1 else "1 hour ago"
        elif diff < timezone.timedelta(days=7):
            days = diff.days
            return f"{days} days ago" if days != 1 else "1 day ago"
        elif diff < timezone.timedelta(days=30):
            weeks = diff.days // 7
            return f"{weeks} weeks ago" if weeks != 1 else "1 week ago"
        else:
            months = diff.days // 30
            return f"{months} months ago" if months != 1 else "1 month ago"


##############Changes made below
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username}'s cart: {self.product.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username}'s wishlist: {self.product.name}"
