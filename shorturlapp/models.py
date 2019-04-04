from django.db import models
from ShortUrl.settings import LONG_URL_MAX_LENGTH, SHORT_URL_MAX_LENGTH
# Create your models here.


class Info(models.Model):
    """
    数据表
    """
    id = models.AutoField(primary_key=True)  # id
    long_url = models.CharField(null=False, max_length=LONG_URL_MAX_LENGTH)  # 长链接
    short_url = models.CharField(null=False, max_length=SHORT_URL_MAX_LENGTH)  # 短链接
