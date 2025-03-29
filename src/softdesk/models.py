import uuid
from django.db import models
from django.conf import settings
from rest_framework.exceptions import ValidationError


class Project(models.Model):
    """
    Model representing a project.
    """
    class ProjectType(models.TextChoices):
        BACKEND = 'BACKEND', 'Back-end'
        FRONTEND = 'FRONTEND', 'Front-end'
        IOS = 'IOS', 'iOS'
        ANDROID = 'ANDROID', 'Android'

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=100
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    type = models.TextField(
        choices=ProjectType.choices
    )
    time_created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        """
        Constraint to avoid double posting.
        """
        constraints = [models.UniqueConstraint(
            fields=['author', 'title'],
            name='unique_project'
        )]

    def __str__(self):
        return f"{self.id} - {self.title}"


class Contributor(models.Model):
    """
    Model representing a contributor of a project.
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='contributors'
    )
    time_created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        """
        Constraint to avoid adding a user as a contributor's project
        twice.
        """
        constraints = [models.UniqueConstraint(
            fields=['user', 'project'],
            name='unique_contributor'
        )]

    def delete(self, *args, **kwargs):
        """
        Block the deletion of a Contributor if the contributor is also
        the author of the project.
        """
        if self.user == self.project.author:
            raise ValidationError(
                "The author cannot be deleted from the contributors!"
            )
        super().delete(*args, **kwargs)

    def __str__(self):
        return (f"{self.id} : user-{self.user_id} - "
                f"project-{self.project_id}")


class Issue(models.Model):
    """
    Model representing an issue of a project.
    """
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

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_issue'
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=100
    )
    description = models.TextField(
        blank=True,
        null=True
    )

    assigned_to = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='affected_issue'
    )

    priority = models.TextField(
        choices=IssuePriority.choices,
        blank=True,
        null=True
    )
    type = models.TextField(
        choices=IssueType.choices,
        blank=True,
        null=True
    )
    status = models.TextField(
        choices=IssueStatus.choices,
        default='TO_DO'
    )

    time_created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        """
        Constraint to avoid double posting.
        """
        constraints = [models.UniqueConstraint(
            fields=['author', 'project', 'title'],
            name='unique_issue'
        )]

    def __str__(self):
        return f"{self.id} - {self.title}"


class Comment(models.Model):
    """
    Model representing a comment of an issue.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    time_created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.id}"
