# parserapp/admin.py

from django.contrib import admin
from .models import Store, DataFile

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_id', 'store_name']
    search_fields = ['store_id', 'store_name']
    list_filter = ['store_id']

@admin.register(DataFile)
class DataFileAdmin(admin.ModelAdmin):
    list_display = ['store', 'file_type', 'file', 'uploaded_at']
    search_fields = ['store__store_id', 'file_type']
    list_filter = ['file_type', 'uploaded_at', 'store']
