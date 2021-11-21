from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from utils.time_helpers import utc_now


class Tweet(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Who posts this tweet",
    )
    content = models.CharField(max_length=255)
    # Creat at which time
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            ('user', 'created_at'),
        )
        ordering = ('user', '-created_at')

    @property
    def hours_to_now(self):
        # return (datetime.now() - self.created_at).seconds//3600
        return (utc_now() - self.created_at).seconds // 3600
        # make sure UTC 0

    def __str__(self):
        # 执行print 显示的内容
        return f'{self.created_at} {self.user}:{self.content}'