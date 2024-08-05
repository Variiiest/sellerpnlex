# parserapp/models.py

from django.db import models

class Store(models.Model):
    store_id = models.CharField(max_length=10, unique=True)
    store_name = models.CharField(max_length=100)

    def __str__(self):
        return self.store_name

class DataFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('orderdata', 'Order Data'),
        ('productdata', 'Product Data'),
        ('logistic', 'Logistic'),
        ('marketing', 'Marketing'),
    ]
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    file = models.FileField(upload_to='data_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.store.store_name} - {self.get_file_type_display()}"
