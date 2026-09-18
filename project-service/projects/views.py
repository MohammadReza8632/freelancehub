from common.celery_client import celery_app
from rest_framework import generics, permissions
from .serializers import ProjectSerializer
from .models import Project
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


    def perform_create(self, serializer):
        if self.request.user.role != 'client':
            raise PermissionDenied()
        serializer.save(client_id=self.request.user.id)

        celery_app.send_task(
            'notifications.tasks.send_notification_email',
            args=[self.request.user.email, 'Project Created', 'Your project was posted successfully!']

        )


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_object(self):
        project = super().get_object()
        if self.request.method != 'GET':
            if project.client_id != int(self.request.user.id):
                raise PermissionDenied('You can only modify your own projects')
        return project
