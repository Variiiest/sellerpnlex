from rest_framework import serializers
from .models import Store, DataFile

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['store_id', 'store_name']

class DataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFile
        fields = ['store', 'file_type', 'file']


class PnlSerializer(serializers.Serializer):
    order_date = serializers.DateField()  # Date field only
    selling_price = serializers.FloatField()
    cost_price = serializers.FloatField()
    logistic_charges = serializers.FloatField()
    profit = serializers.FloatField()
    order_count = serializers.IntegerField()  # Total number of orders
    cancelled_count = serializers.IntegerField()  # Count of cancelled orders
    delivered_count = serializers.IntegerField()  # Count of delivered orders
    rto_count = serializers.IntegerField()  # Count of RTO orders
    cancelled_percentage = serializers.FloatField()  # Percentage of cancelled orders
    delivered_percentage = serializers.FloatField()  # Percentage of delivered orders
    rto_percentage = serializers.FloatField()  # Percentage of RTO orders


class OrderDataSerializer(serializers.Serializer):
    order_date = serializers.DateField()
    order_id = serializers.CharField(max_length=100)
    sku_id = serializers.CharField(max_length=100)
    selling_price = serializers.FloatField()
    cost_price = serializers.FloatField()
    order_status = serializers.CharField(max_length=100)
    logistic_charges = serializers.FloatField()