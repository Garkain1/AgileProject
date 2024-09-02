from django.db import models
from ..dependencies import Project, User
from ..choices import Statuses, Priority
from ..utils import calculate_end_of_month


class Task(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    status = models.CharField(
        max_length=15,
        choices=Statuses.choices(),
        default=Statuses.NEW
    )
    priority = models.SmallIntegerField(
        choices=Priority.choices(),
        default=Priority.MEDIUM[0]
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    tags = models.ManyToManyField('Tag', related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(default=calculate_end_of_month)
    assignee = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-deadline']
        unique_together = ('name', 'project')

    def __str__(self):
        return f"{self.name}, status: {self.status}"
