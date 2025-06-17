from django.db import models
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    title = models.CharField(
        max_length=100
    )
    description = models.TextField(
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )
    due_date = models.DateField(
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_tasks"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def is_overdue(self):
        return self.due_date and self.due_date < date.today() and self.status != "done"

    def __str__(self):
        return self.title

