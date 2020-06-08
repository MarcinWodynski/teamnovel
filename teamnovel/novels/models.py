from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Novel(models.Model):
    title = models.CharField(max_length=200)
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leading_novel')
    content = models.TextField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='novels')
    last_turn = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='last_user')
    current_turn = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='current_turn_user')
    previous_turn = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_before_last')

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    group_leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leading_team')
    team_users = models.ManyToManyField(User)

    def __str__(self):
        return self.team_name

class PublishedNovel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    team_name = models.CharField(max_length=300)
    publish_date = models.DateField(auto_now_add=True)
    user_ratings = models.ManyToManyField(User, related_name='rated')
    user_comments = models.ManyToManyField(User, related_name='commented', through='UserCommentNovels')


class UserCommentNovels(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    PublishedNovel = models.ForeignKey(PublishedNovel,on_delete=models.CASCADE)
    Comment = models.CharField(max_length=200)
