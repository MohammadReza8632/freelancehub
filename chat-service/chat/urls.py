from django.urls import path
from .views import MessageListView

urlpatterns = [
    path('<int:user_id_1>/<int:user_id_2>/', MessageListView.as_view(), name='retrieve-messages'),
]