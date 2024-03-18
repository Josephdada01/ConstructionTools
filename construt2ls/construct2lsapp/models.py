"""
This file defines Django models for a web application. It includes models for 
contacts, products, orders, and order updates.
"""

from django.db import models
from django.contrib.auth.models import User

# Contact model represents contact information for users
class Contact(models.Model):
    name = models.CharField(max_length=30)  # Name of the contact
    email = models.EmailField()  # Email of the contact
    description = models.TextField(max_length=1000)  # Description or message
    phone_num = models.IntegerField()  # Phone number of the contact

    # String representation of the contact object, returns the name
    def __str__(self):
        return self.name

# Product model represents the products available in the store
class Product(models.Model):
    product_name = models.CharField(max_length=50)  # Name of the product
    category = models.CharField(max_length=50, default="")  # Category of the product
    subcategory = models.CharField(max_length=50, default="")  # Subcategory of the product
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Price of the product
    desc = models.CharField(max_length=300)  # Description of the product
    image = models.ImageField(upload_to='images/images', default="")  # Image of the product

    # String representation of the product object, returns the product name
    def __str__(self):
        return self.product_name

# Orders model represents the orders placed by users
class Orders(models.Model):
    """
    This model represents orders placed by users.
    """
    order_id = models.AutoField(primary_key=True)  # Unique identifier for the order
    items_json = models.CharField(max_length=5000)  # JSON string representing ordered items
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total amount of the order
    name = models.CharField(max_length=90)  # Name of the customer
    email = models.CharField(max_length=90)  # Email of the customer
    address1 = models.CharField(max_length=200)  # Address line 1 of the customer
    address2 = models.CharField(max_length=200)  # Address line 2 of the customer
    city = models.CharField(max_length=100)  # City of the customer
    state = models.CharField(max_length=100)  # State of the customer
    zip_code = models.CharField(max_length=100)  # ZIP code of the customer
    oid = models.CharField(max_length=150, blank=True)  # Order ID (optional)
    amountpaid = models.CharField(max_length=500, blank=True, null=True)  # Amount paid (optional)
    paymentstatus = models.CharField(max_length=20, blank=True)  # Payment status (optional)
    phone = models.CharField(max_length=100, default="")  # Phone number of the customer

    # String representation of the order object, returns the customer's name
    def __str__(self):
        return self.name

# OrderUpdate model represents updates for orders
class OrderUpdate(models.Model):
    """
    This model represents updates for orders.
    """
    update_id = models.AutoField(primary_key=True)  # Unique identifier for the update
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)  # Order associated with the update
    update_desc = models.CharField(max_length=5000)  # Description of the update
    delivered = models.BooleanField(default=False)  # Indicates whether the order is delivered
    timestamp = models.DateField(auto_now_add=True)  # Timestamp of the update

    # String representation of the order update object, returns a truncated version of the update description
    def __str__(self):
        return self.update_desc[0:7] + "..."

