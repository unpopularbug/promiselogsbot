import time
import requests
import praw
import django
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from celery import shared_task

from app.models import RedditAccounts, SubReddit

django.setup()

api_url = f"{settings.BASE_URL}/national_assembly/members/"

@shared_task
def reddit_post():
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from the promiselogs API: {e}")
        return
    
    members = data.get("members", [])

    accounts = RedditAccounts.objects.all()
    subreddits = SubReddit.objects.all()

    for account in accounts:
        for subreddit_obj in subreddits:
            for member in members:
                name = member.get("name")
                constituency = member.get("represents")
                phone_number = member.get("tel")

                if name and constituency:
                    title = f"{name} - {constituency}"
                    message = f"Phone Number: {phone_number}"

                    print(f"Title: {title}")
                    print(f"Message: {message}")


def post_on_reddit(account, subreddit_obj, title, message):
    try:
        reddit_instance = get_reddit_instance(account)

        flair_name = subreddit_obj.flair
        flair_id = get_flair_id(reddit_instance, subreddit_obj.sub_name, flair_name)

        submission = reddit_instance.subreddit(subreddit_obj.sub_name).submit(
            title=title,
            selftext=message,
            flair_id=flair_id,
        )
        print(f"Posted to r/{subreddit_obj.sub_name} with flair ID {flair_id} using account {account.acc_username}")
        time.sleep(10)

    except Exception as e:
        print(f"Failed to post in r/{subreddit_obj.sub_name} using account {account.acc_username}: {e}")


def get_reddit_instance(account):
    return praw.Reddit(
        client_id=account.client_id,
        client_secret=account.client_secret,
        username=account.acc_username,
        password=account.acc_password,
        user_agent=account.user_agent,
    )


def get_flair_id(reddit_instance, subreddit_name, flair_name):
    subreddit = reddit_instance.subreddit(subreddit_name)
    flairs = {flair['text']: flair['id'] for flair in subreddit.flair.link_templates}
    flair_id = flairs.get(flair_name)
    if flair_id is None:
        raise ValueError(f"Flair '{flair_name}' not found in subreddit {subreddit_name}")
    return flair_id


class Command(BaseCommand):
    help = 'Post to Reddit'

    def handle(self, *args, **options):
        reddit_post.delay()