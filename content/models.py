from django.db import models
from auth_manager.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver

    
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    title = models.CharField(max_length= 200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)
    tags = models.ManyToManyField(Tag, related_name='questions', blank= True)
    categories = models.ManyToManyField(Category, related_name= 'questions', blank= True)

    def __str__(self):
        return self.title
    

class Answer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    content = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    accepted = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add= True)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete= models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)

@receiver(post_save, sender=Answer)
def update_reputation(sender, instance, **kwargs):
    user = instance.user
    reputation = 0
    reputation += 10 * Answer.objects.filter(user = user).aggregate(models.Sum('upvotes'))['upvotes__sum'] or 0
    reputation -= 5 * Answer.objects.filter(user = user).aggregate(models.Sum('downvotes'))['downvotes__sum'] or 0
    reputation += 15 * Answer.objects.filter(user=user, accepted=True).count()
    user.reputation = reputation
    user.save()