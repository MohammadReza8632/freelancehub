from django.db import models
from projects.models import Project


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'

    project = models.ForeignKey(Project, related_name='applications', on_delete=models.CASCADE)
    freelancer_id = models.IntegerField()
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project', 'freelancer_id'], name='unique_application_per_freelancer')
        ]

    def __str__(self):
        return f'Freelancer {self.freelancer_id} -> {self.project.title} ({self.status})'