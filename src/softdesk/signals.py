from django.db.models.signals import post_save
from django.dispatch import receiver
from softdesk.models import Project, Contributor


@receiver(post_save, sender=Project)
def assign_contributor(instance, created, **kwargs):
    """
    Signal to automatically create a Contributor link between a Project
    and its Author after a Project is saved in the Database.
    """
    if created:
        contributor = Contributor(
            user=instance.author,
            project=instance
        )
        contributor.save()
