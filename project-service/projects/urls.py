from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView
from applications.views import ApplicationListCreateView



urlpatterns = [

    path('', ProjectListCreateView.as_view(), name='project-list-create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='single-project-retrieve'),
    path('<int:pk>/applications/', ApplicationListCreateView.as_view(), name='project-applications-list-create'),
]
