import os

from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin


# Create your models here.

# =============================================================================================
class AppUserManager(BaseUserManager):
    """ custom manager for AppUser model"""
    def create_user(self, email, password=None, **extra_fields):
        """" create standard users, expects an email & password  & additional fields """
        if not email:
            raise ValueError('An email is required.')
        if not password:
            raise ValueError('A password is required.')

        # ================================== password validations ==============================
        # if len(password) < 8:
        #     raise ValueError("Password must be at least 8 characters long.")
        # if not any(char.isdigit() for char in password):
        #     raise ValueError('Password must contain at least one numeric character.')
        # if not any(char.isalpha() for char in password):
        #     raise ValueError('password must contain at least one alphabetic character.')

        email = self.normalize_email(email)                  # normalize email, converts the domain part of the email to lowercase
        user = self.model(email=email, **extra_fields)       # create a user instance
        user.set_password(password)                          # set its ps (hashed)
        user.save()                                          # save to database
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """" create superusers """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        superuser = self.create_user(email, password, **extra_fields)
        return superuser


class AppUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)

    # use the email as the unique identifier for authentication, instead of the default "username"
    USERNAME_FIELD = 'email'
    # list of fields that will be prompted for when creating
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = AppUserManager()

    # is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email} - {self.last_name}"

    # def delete(self, *args, **kwargs):
    #     # Instead of deleting the record, we just set the is_active flag to False
    #     self.is_active = False
    #     self.save()


# ==========================  User Profile  ==================================================
# class CustomerProfile(models.Model):
#     # cus
#     customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # delete user will delete user profile, not vice verse
#     address = models.TextField(null=True, blank=True)
#     phone = models.CharField(null=True, blank=True, max_length=20)
#
#     def __str__(self):
#         return self.customer.email


class Address(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    # add fields in admin.py
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    address_line_1 = models.CharField(max_length=500)
    address_line_2 = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name}, {self.city}, {self.phone}"

    def save(self, *args, **kwargs):
        # if this address is set to be the default
        if self.is_default:
            # Reset the `is_default` field of all other addresses for this user to `False`
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)

        # Now save (or update) the current instance
        super(Address, self).save(*args, **kwargs)


# ================================= Contact ==================================================
class ContactRequest(models.Model):
    SUBJECT_CHOICES = (
        ('Order issues', 'Order status'),
        ('Product question', 'Product question'),
        ('General Inquiry', 'General Inquiry'),
        ('Report an issue', 'Report an issue'),
        ('Request refund or discount', 'Request refund or discount'),
        ('Feedback', 'Feedback'),
        ('Other', 'Other'),
        # Add more options as needed
    )

    sender = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='sent_contact_requests',
        null=True,
        default=None
    )
    full_name = models.CharField(max_length=255, null=True)
    sender_email = models.EmailField(null=True)
    # related_name:  can access a user's sent requests using user.sent_contact_requests.all()
    # Add a field to specify the receiver's email
    subject = models.CharField(max_length=255, choices=SUBJECT_CHOICES)
    message = models.TextField()
    # attachments = models.ManyToManyField('Attachment', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Contact Request form {self.sender}'


# def user_attachment_path(instance, filename):
#     # Define the upload path for attachment files
#     # The filename will be user_<user_id>_attachment.ext
#     return f'contact_request_attachments/user_{instance.user.id}/{os.path.splitext(filename)[1]}'
#
#
# def validate_file_size(value):
#     # Set the maximum file size (in bytes) you want to allow
#     max_file_size = 5 * 1024 * 1024  # 5 MB
#
#
# class Attachment(models.Model):
#     user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='attachments')
#     file = models.FileField(upload_to='contact_request_attachments/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.file.name
# =============================================================================================


# =============================================================================================


class Material(models.Model):
    material_name = models.CharField(max_length=255)

    def __str__(self):
        return self.material_name


class Collection(models.Model):
    """ A collection can have many Products """
    collection_name = models.CharField(max_length=120)
    cover_image = models.ImageField(null=True, blank=True, upload_to='collections/')

    def __str__(self):
        return self.collection_name


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.FloatField()
    # stock = models.PositiveIntegerField()
    # is_active = models.BooleanField(default=True)
    # create_at = models.DateTimeField(auto_now_add=True)
    # cover image
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    materials = models.ManyToManyField(Material, related_name="products")

    collection = models.ForeignKey(Collection, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """ A product has many images- ForeignKey """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image_name = models.CharField(max_length=120)
    product_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.image_name


class Carousel(models.Model):
    """ Image Sliders in home page """
    theme = models.CharField(max_length=120)
    caption = models.CharField(max_length=120)
    image = models.ImageField(null=True, blank=True, upload_to="carousel/")

    def __str__(self):
        return self.theme


# ============================== Cart ========================================================
class Cart(models.Model):
    """ each user has their own cart, it can contain multiple CartItems instances """
    user = models.OneToOneField(AppUser, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        username = f'{self.user.first_name} {self.user.last_name}' if self.user else "Guest"
        if self.user:
            return f'User ID: {self.user.user_id} - {username}'
        else:
            return f'Session Key: {self.session_key}'

    def empty_cart(self):
        self.cart_items.all().delete()

    def total_price(self):
        # cart_items is defined as reverse relation to CartItem model
        return sum(item.product.price * item.quantity for item in self.cart_items.all())

    def total_quantity(self):
        return sum(item.quantity for item in self.cart_items.all())


class CartItem(models.Model):
    """ items within a shopping cart - a cart contains multiple cartitems; a cartitem belongs to only one cart """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_product")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product} - {self.cart.user} {self.cart.user.last_name}'

    def get_product_details(self):
        # Access the associated product and extract product details
        product = self.product
        product_details = {
            "cart_item_id": self.id,
            "product_image": product.image.url,
            # without "url" -> UnicodeDecodeError -> <ImageFieldFile: images/2_c3vyDIH.jpeg>
            "product_title": product.title,
            "product_price": product.price,
        }

        return product_details


# ============================== order ========================================================
# class Order(models.Model):
#     """ a user can place multiple orders over time, but each order is linked to only 1 user """
#     user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='cart_items')
#     # address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
#     # on_delete=models.SET_NULL ensures that if the associated address is deleted, the reference in the order will be set to NULL instead of deleting the order itself.
#     # null=True allows the address field to be empty, which could represent scenarios where an order has not yet been assigned a shipping address
#     total = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(
#         choices=[
#             ('processing', 'Processing'),
#             ('shipped', 'Shipped'),
#             ('cancelled', 'Cancelled')
#         ],
#         default='processing',
#         max_length=10
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'Order {self.id} for {self.user.first_name} {self.user.last_name}'
#
#
# class OrderItem(models.Model):
#     """ an individual item within an order """
#     order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)  # related_name, create reverse relationship, allow access from 'order' model to its items with 'order_items' property
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#
#     def __str__(self):
#         return f"{self.order.id} - {self.quantity} x {self.product.name}"
