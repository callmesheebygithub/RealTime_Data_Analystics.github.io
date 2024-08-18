# project_name/models.py

from django.db import models

class Product(models.Model):
    ProductID = models.IntegerField(primary_key=True)
    ProductName = models.CharField(max_length=255)
    ProductCategory = models.CharField(max_length=255)
    SalesAmount = models.FloatField()
    UnitSold = models.FloatField()
    Region = models.CharField(max_length=255)
    Age = models.IntegerField()
    
    def __str__(self):
        return self.ProductName