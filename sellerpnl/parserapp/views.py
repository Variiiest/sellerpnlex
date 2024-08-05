# parserapp/views.py

import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from parserapp.models import Store, DataFile
from parserapp.serializers import StoreSerializer, DataFileSerializer, PnlSerializer, OrderDataSerializer
import pandas as pd
from io import StringIO


class DataFileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        store_id = request.data.get('store_id')
        store = get_object_or_404(Store, store_id=store_id)

        files = request.FILES.getlist('file')
        file_types = ['orderdata', 'productdata', 'logistic', 'marketing']
        
        for file in files:
            file_type = file.content_type
            if file_type in file_types:
                data_file = DataFile(store=store, file_type=file_type, file=file)
                data_file.save()
            else:
                return Response({'error': f'Invalid file type: {file_type}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Files uploaded successfully'}, status=status.HTTP_201_CREATED)



# views.py

from datetime import datetime

from datetime import datetime

class PnlView(APIView):
    def get(self, request, store_id, format=None):
        store = get_object_or_404(Store, store_id=store_id)

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({'error': 'start_date and end_date query parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError as e:
            return Response({'error': f'Invalid date format: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        data_files = DataFile.objects.filter(store=store)
        data_dict = {df.file_type: df.file for df in data_files}

        try:
            order_df = pd.read_csv(StringIO(data_dict.get('orderdata', '').read().decode('utf-8')))
            product_df = pd.read_csv(StringIO(data_dict.get('productdata', '').read().decode('utf-8')))
            logistic_df = pd.read_csv(StringIO(data_dict.get('logistic', '').read().decode('utf-8')))
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Convert 'Order date' column to datetime
        order_df['Order date'] = pd.to_datetime(order_df['Order date'], format='%d-%m-%y')
        logistic_df['Order date'] = pd.to_datetime(logistic_df['Order date'], format='%d-%m-%y')

        # Merge data
        merged_df = pd.merge(order_df, product_df, how='left', on='Sku id')
        merged_df = pd.merge(merged_df, logistic_df, how='left', on=['Order date', 'Order id', 'Sku id'])

        # Filter by date range
        merged_df = merged_df[(merged_df['Order date'].dt.date >= start_date) & (merged_df['Order date'].dt.date <= end_date)]

        # Select required columns and include "Logistic Charges"
        merged_df = merged_df[['Order date', 'Order id', 'Sku id', 'Selling price', 'Cost price', 'Order Status', 'Logistic Charges']]

        # Rename columns for clarity
        merged_df = merged_df.rename(columns={
            'Selling price': 'selling_price',
            'Cost price': 'cost_price',
            'Order Status': 'order_status',
            'Logistic Charges': 'logistic_charges'
        })

        # Calculate daily P&L
        merged_df['Profit'] = merged_df.apply(
            lambda row: row['selling_price'] - row['cost_price'] - row['logistic_charges']
            if row['order_status'] == 'delivered' else 
            0 if row['order_status'] == 'cancelled' else
            -row['logistic_charges'],
            axis=1
        )

        # Calculate daily metrics
        daily_pnl = merged_df.groupby(merged_df['Order date'].dt.date).agg({
            'selling_price': 'sum',
            'cost_price': 'sum',
            'logistic_charges': 'sum',
            'Profit': 'sum',
            'Order id': 'count'
        }).reset_index()

        # Calculate percentage metrics
        status_counts = merged_df.groupby([merged_df['Order date'].dt.date, 'order_status']).size().unstack(fill_value=0)
        status_counts = status_counts.rename(columns={
            'cancelled': 'cancelled_count',
            'delivered': 'delivered_count',
            'rto': 'rto_count'
        })

        # Ensure all expected columns are present
        for col in ['cancelled_count', 'delivered_count', 'rto_count']:
            if col not in status_counts.columns:
                status_counts[col] = 0

        daily_pnl = daily_pnl.merge(status_counts, left_on='Order date', right_index=True)

        # Calculate percentages
        daily_pnl['total_orders'] = daily_pnl[['cancelled_count', 'delivered_count', 'rto_count']].sum(axis=1)
        daily_pnl['cancelled_percentage'] = (daily_pnl['cancelled_count'] / daily_pnl['total_orders']) * 100
        daily_pnl['delivered_percentage'] = (daily_pnl['delivered_count'] / daily_pnl['total_orders']) * 100
        daily_pnl['rto_percentage'] = (daily_pnl['rto_count'] / daily_pnl['total_orders']) * 100

        # Rename columns to match the serializer
        daily_pnl = daily_pnl.rename(columns={
            'Order date': 'order_date',
            'selling_price': 'selling_price',
            'cost_price': 'cost_price',
            'logistic_charges': 'logistic_charges',
            'Profit': 'profit',
            'Order id': 'order_count',
            'cancelled_count': 'cancelled_count',
            'delivered_count': 'delivered_count',
            'rto_count': 'rto_count',
            'cancelled_percentage': 'cancelled_percentage',
            'delivered_percentage': 'delivered_percentage',
            'rto_percentage': 'rto_percentage'
        })

        # Serialize and return data
        serializer = PnlSerializer(daily_pnl.to_dict(orient='records'), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDataView(APIView):
    def get(self, request, store_id, format=None):
        store = get_object_or_404(Store, store_id=store_id)

        data_files = DataFile.objects.filter(store=store)
        data_dict = {df.file_type: df.file for df in data_files}

        try:
            order_df = pd.read_csv(StringIO(data_dict.get('orderdata', '').read().decode('utf-8')))
            product_df = pd.read_csv(StringIO(data_dict.get('productdata', '').read().decode('utf-8')))
            logistic_df = pd.read_csv(StringIO(data_dict.get('logistic', '').read().decode('utf-8')))
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Merge data
        merged_df = pd.merge(order_df, product_df, how='left', on='Sku id')
        merged_df = pd.merge(merged_df, logistic_df, how='left', on=['Order date', 'Order id', 'Sku id'])

        # Select required columns
        merged_df = merged_df[['Order date', 'Order id', 'Sku id', 'Selling price', 'Cost price', 'Order Status', 'Logistic Charges']]

        # Rename columns for clarity
        merged_df = merged_df.rename(columns={
            'Selling price': 'selling_price',
            'Cost price': 'cost_price',
            'Order Status': 'order_status',
            "Order date": 'order_date',
            "Order id": 'order_id',
            "Sku id": "sku_id",
            "Logistic Charges" :"logistic_charges"
        })

        # Serialize and return data
        serializer = OrderDataSerializer(merged_df.to_dict(orient='records'), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)