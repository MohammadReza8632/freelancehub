from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from projects.models import Project
from .models import Application
from .serializers import ApplicationSerializer


class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        if int(self.request.user.id) != project.client_id:
            raise PermissionDenied('Only the project owner can view its applications')
        return Application.objects.filter(project=project)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])

        if self.request.user.role != 'freelancer':
            raise PermissionDenied('Only freelancers can apply to projects')

        if project.status != Project.Status.OPEN:
            raise ValidationError('This project is not open for applications')

        try:
            serializer.save(project=project, freelancer_id=self.request.user.id)
        except IntegrityError:
            raise ValidationError('You have already applied to this project')


class ApplicationAcceptView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        project = application.project

        if int(request.user.id) != project.client_id:
            raise PermissionDenied('Only the project owner can accept applications')

        if project.status != Project.Status.OPEN:
            raise ValidationError('This project is no longer open')

        application.status = Application.Status.ACCEPTED
        application.save()

        project.freelancer_id = application.freelancer_id
        project.status = Project.Status.IN_PROGRESS
        project.save()

        # every other still-pending applicant on this project gets auto-rejected
        Application.objects.filter(
            project=project, status=Application.Status.PENDING
        ).exclude(pk=application.pk).update(status=Application.Status.REJECTED)

        return Response(ApplicationSerializer(application).data)


class ApplicationRejectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        project = application.project

        if int(request.user.id) != project.client_id:
            raise PermissionDenied('Only the project owner can reject applications')

        application.status = Application.Status.REJECTED
        application.save()

        return Response(ApplicationSerializer(application).data)