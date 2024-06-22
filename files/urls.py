from django.urls import path
from .views import (
    ListFilesView, 
    DownloadFileView, 
    DownloadWithTokenView
)

urlpatterns = [
    path('list-files/', ListFilesView.as_view(), name='list-files'),
    path('download-file/<int:file_id>/', DownloadFileView.as_view(), name='download-file'),
    path('download-file/<str:token>/<int:file_id>/', DownloadWithTokenView.as_view(), name='download-with-token'),
]

