from django.db import models

class Message(models.Model):
    sender_id = models.IntegerField()
    content = models.TextField()
    room_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.sender_id}: {self.content}'