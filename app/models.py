import uuid
from django.db import models
from django.contrib.auth.models import User


class RedditAccounts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_id = models.CharField(max_length=255, null=False)
    client_secret = models.CharField(max_length=255, null=False)
    acc_username = models.CharField(unique=True, max_length=255, null=False)
    acc_password = models.CharField(max_length=255, null=False)
    user_agent = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name_plural = 'Reddit Accounts'

    def __str__(self):
        return self.acc_username


class SubReddit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sub_name = models.CharField(max_length=255, null=False)
    flair = models.CharField(max_length=255, null=True, blank=True)
    last_posted_at = models.DateTimeField(null=True, blank=True)
    last_posted_by = models.ForeignKey('RedditAccounts', on_delete=models.SET_NULL, null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.sub_name


# class TwitterAccounts(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


# class FacebookAccounts(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


# class FacebookForums(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)