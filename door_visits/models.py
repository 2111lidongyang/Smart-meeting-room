from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=20)
    userphone = models.CharField(verbose_name='用户手机', max_length=20)

    class Meta:
        db_table = 'visits_info'
