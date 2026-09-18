from django.urls import path
from .views import ApplicationAcceptView, ApplicationRejectView

urlpatterns = [
    path('<int:pk>/accept/', ApplicationAcceptView.as_view(), name='application-accept'),
    path('<int:pk>/reject/', ApplicationRejectView.as_view(), name='application-reject'),
]