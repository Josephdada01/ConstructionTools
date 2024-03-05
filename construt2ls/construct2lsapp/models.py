from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    description = models.TextField(max_length=1000)
    phone_num = models.IntegerField()

    def __str__(self):
        return self.name

