from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from tweets.models import Tweet
from datetime import timedelta
from utils.time_helpers import utc_now


class TweetTests(TestCase):

    # 测试 hours to now是否正确
    def test_hours_to_now(self):
        # 创建了一个user
        linghu = User.objects.create_user(username='linghu')
        # 创建了一个tweet
        tweet = Tweet.objects.create(user=linghu, content='Jiuzhang Dafa Good!')
        tweet.created_at = utc_now() - timedelta(hours=10)
        tweet.save()
        self.assertEqual(tweet.hours_to_now, 10)

