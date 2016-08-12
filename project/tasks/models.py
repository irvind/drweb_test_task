from datetime import datetime
from django.db import models


class Task(models.Model):
    STATUS_PENDING = 0
    STATUS_RUNNING = 1
    STATUS_FINISHED = 2

    STATUS_CHOICES = (
        (STATUS_PENDING, 'В очереди'),
        (STATUS_RUNNING, 'Выполняется'),
        (STATUS_FINISHED, 'Выполнено'),
    )

    timestamp = models.DateTimeField(default=datetime.now)
    status = models.IntegerField(choices=STATUS_CHOICES)


class TaskResult(models.Model):
    create_time = models.DateTimeField()
    finish_time = models.DateTimeField()
