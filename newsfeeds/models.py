"""
Deprecated
use newsfeeds.hbase_models.HBaseNewsFeed instead
"""
from django.db import models
from django.contrib.auth.models import User
from tweets.models import Tweet


class NewsFeed(models.Model):
    # users who can see this tweet
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('user', 'created_at'),)
        unique_together = (('user', 'tweet'),)
        ordering = ('user','-created_at',)

    def __str__(self):
        return f'{self.created_at} inbox of {self.user}: {self.tweet}'

#     @property
#     def cached_tweet(self):
#         return MemcachedHelper.get_object_through_cache(Tweet, self.tweet_id)
#
#
# post_save.connect(push_newsfeed_to_cache, sender=NewsFeed)