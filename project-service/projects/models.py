from django.db import models

class Project(models.Model):
    client_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=7, decimal_places=2)
    duration_days = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    freelancer_id = models.IntegerField(null=True, blank=True)

    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In Progress'
        CLOSED = 'closed', 'Closed'

    status = models.CharField(max_length=11, choices=Status.choices, default=Status.OPEN)


    def __str__(self):
        return self.title
