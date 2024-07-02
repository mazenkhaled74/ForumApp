from django.db.models.signals import post_save
from django.dispatch import receiver
from content.models import Comment
from auth_manager.models import CustomUser, Badge
from django.db import models
from django.utils.timezone import now, timedelta

@receiver(post_save, sender=Comment)
def AwardActiveUserBadge(sender, instance, **kwargs):
    user = instance.user
    todayStart = now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrowStart = todayStart + timedelta(days=1)

    numCommentsToday = Comment.objects.filter(user= user, created_at__gte=todayStart, created_at__lt=tomorrowStart).count()
    if numCommentsToday >= 5:
        activeUserBadge = Badge.objects.get(name="Active User")
        user.badges.add(activeUserBadge)
        user.save()