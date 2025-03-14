import uuid
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError


class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACKEND = 'BACKEND', 'Back-end'
        FRONTEND = 'FRONTEND', 'Front-end'
        IOS = 'IOS', 'iOS'
        ANDROID = 'ANDROID', 'Android'

    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type = models.TextField(choices=ProjectType.choices)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Constraint to avoid double posting
        constraints = [models.UniqueConstraint(fields=['author', 'title'], name='unique_project')]

    def __str__(self):
        return f"{self.id} - {self.title}"


@receiver(post_save, sender=Project)
def assign_contributor(instance, **kwargs):
    contributor = Contributor(user=instance.author, project=instance)
    contributor.save()


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='contributors')
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'project'], name='unique_contributor')]

    def delete(self, *args, **kwargs):
        if self.user == self.project.author:
            raise ValidationError("The author cannot be deleted from the contributors!")
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.id} : user-{self.user_id} - project-{self.project_id}"


class Issue(models.Model):
    class IssuePriority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    class IssueType(models.TextChoices):
        BUG = 'BUG', 'Bug'
        FEATURE = 'FEATURE', 'Feature'
        TASK = 'TASK', 'Task'

    class IssueStatus(models.TextChoices):
        TO_DO = 'TO_DO', 'To Do'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        FINISHED = 'FINISHED', 'Finished'

    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='created_issue')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    to_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                related_name='affected_issue')

    priority = models.TextField(choices=IssuePriority.choices, blank=True, null=True)
    type = models.TextField(choices=IssueType.choices, blank=True, null=True)
    status = models.TextField(choices=IssueStatus.choices, default='TO_DO')

    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Constraint to avoid double posting
        constraints = [models.UniqueConstraint(fields=['author', 'project', 'title'], name='unique_issue')]

    def __str__(self):
        return f"{self.id} - {self.title}"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
