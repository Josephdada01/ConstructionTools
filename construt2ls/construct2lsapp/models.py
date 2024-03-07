from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    description = models.TextField(max_length=1000)
    phone_num = models.IntegerField()

    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    #price = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desc = models.CharField(max_length=300)

    image = models.ImageField(upload_to='images/images', default="")

    def __str__(self):
        return self.product_name

