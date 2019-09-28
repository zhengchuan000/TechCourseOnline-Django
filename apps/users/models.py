from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


GENDER_CHOICE = (
    ("male","男"),
    ("female", "女")
)


class BaseModel(models.Model):
    added_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        abstract = True


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, default="", verbose_name='昵称')
    birthday = models.DateField(blank=True, null=True, verbose_name="生日")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICE, verbose_name="性别")
    address = models.CharField(max_length=100, default="", verbose_name="地址")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    image = models.ImageField(upload_to="head_image/%Y/%m", default="default.jpg", verbose_name="用户头像")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def unread_nums(self):
        #未读的消息
        return self.usercourse_set.filter(has_read=False).count()

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username