from django.db.models.signals import post_save
from django.dispatch import receiver
from content.models import Answer
from django.db import models

@receiver(post_save, sender=Answer)
def update_reputation(sender, instance, **kwargs):
    user = instance.user
    reputation = 0
    reputation += 10 * Answer.objects.filter(user = user).aggregate(models.Sum('upvotes'))['upvotes__sum'] or 0
    reputation -= 5 * Answer.objects.filter(user = user).aggregate(models.Sum('downvotes'))['downvotes__sum'] or 0
    reputation += 15 * Answer.objects.filter(user=user, accepted=True).count()
    user.reputation = reputation
    user.save()