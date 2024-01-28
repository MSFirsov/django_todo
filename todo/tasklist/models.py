from django.contrib.auth import get_user_model
from django.db import models


class Task(models.Model):
    text = models.CharField(max_length=255)
    task_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts', null=True)

    def __str__(self):
        return self.text

