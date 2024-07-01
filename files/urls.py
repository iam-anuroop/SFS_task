from django.urls import path
from .views import (
    FileuploadView,
    ListFilesView, 
    DownloadFileView, 
    DownloadWithTokenView
)

urlpatterns = [
    path('upload-file/', FileuploadView.as_view(), name='upload-file'),
    path('list-files/', ListFilesView.as_view(), name='list-files'),
    path('download-file/<int:file_id>/', DownloadFileView.as_view(), name='download-file'),
    path('download-file/<str:token>/<int:file_id>/', DownloadWithTokenView.as_view(), name='download-with-token'),
]

