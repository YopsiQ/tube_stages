from django.urls import path

from tube.views import VideoView, watch
from tube.views import uploaded_stream_detail, main


urlpatterns = [
    path('', main, name='main'),
    path('upload/', VideoView.as_view(), name='upload_video'),
    path('watch/<int:video_id>/', watch, name='video_stream_detail'),
    path('<str:name>/', uploaded_stream_detail, name='video_stream'),
]
