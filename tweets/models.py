from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from utils.time_helpers import utc_now


class Tweet(models.Model):
    #设置3个属性
    # user的属性就是记录这篇帖子是谁发的（who post this tweet）
    # 如果你是一个ForeignKey, 你一定要用 SET_NULL， 然后null就必须是True
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # 实际上是256，2的幂次方，最后会有一个默认的\0,'abcde'看上去存储的是5个字符，实际上是6个：'abcde\0'
    # 不是字符串的0，是ascci码的0. 表示一个字符串的结尾，不可见
    content = models.CharField(max_length=255)
    # 这个帖子是什么时候创建的，
    # auto_now_add：我们希望这个帖子在创建的时候，这个时间戳是自动填上的，当创建的时候，自动去计算当前的时间
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def hours_to_now(self):
        # datetime.now 不带时区信息，需要增加上 utc 的时区信息
        # 计算当前时间和发帖的时间隔了多少个小时
        # from utils.time_helpers import utc_now
        # created_at自带当前vagrant所在的时区
        return (utc_now() - self.created_at).seconds // 3600

    # 这个方法类似于java里面的 toString函数
    def __str__(self):
        # 这里是你执行 print(tweet instance) 的时候会显示的内容
        # f 是format的缩写
        return f'{self.created_at} {self.user}: {self.content}'
