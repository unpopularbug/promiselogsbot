from celery import shared_task
from .management.commands.post import reddit_post_direct

@shared_task
def run_reddit_bot():
    reddit_post_direct()
