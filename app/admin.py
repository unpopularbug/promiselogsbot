from django.contrib import admin

from .models import RedditAccounts, SubReddit

admin.site.register(RedditAccounts)
admin.site.register(SubReddit)