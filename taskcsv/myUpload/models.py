from django.db import models


class MyModel(models.Model):
    product_range = models.CharField(max_length=255)
    product_group = models.CharField(max_length=255)
    style = models.CharField(max_length=255)
    item_code = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item_code
