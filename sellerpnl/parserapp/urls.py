# parserapp/urls.py

# parserapp/urls.py

from django.urls import path
from parserapp.views import DataFileUploadView, PnlView, OrderDataView

urlpatterns = [
    path('upload-data/', DataFileUploadView.as_view(), name='upload-data'),
    path('pnl/<str:store_id>/', PnlView.as_view(), name='pnl'),
    path('orderdata/<str:store_id>/', OrderDataView.as_view(), name='orderdata'),
]
