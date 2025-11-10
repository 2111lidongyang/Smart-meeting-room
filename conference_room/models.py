from django.db import models


# Create your models here.
class UserManager(models.Model):
    # 会议室管理员表
    useraccount = models.CharField(verbose_name='账号', max_length=20)
    userpwd = models.CharField(verbose_name='密码', max_length=20)

    class meta:
        db_table = 'manager_info'


class UserCompere(models.Model):
    # 会议主持人表
    useraccount = models.CharField(verbose_name='账号', max_length=20, primary_key=True)
    userpwd = models.CharField(verbose_name='密码', max_length=20)
    username = models.CharField(verbose_name='用户名', max_length=20)
    conferenceid = models.CharField(verbose_name='会议编号', max_length=20)
    face = models.BinaryField(verbose_name='人脸数据', null=True, blank=True)

    class meta:
        db_table = 'compere_info'


class Conference(models.Model):
    # 会议表
    conferenceroom = models.CharField(verbose_name='会议室', max_length=20)
    compereaccount = models.CharField(verbose_name='主持人账号', max_length=20)
    conferencenums = models.CharField(verbose_name='会议人数', max_length=20)
    conferencetitle = models.CharField(verbose_name='会议标题', max_length=20)
    conferenceid = models.CharField(verbose_name='会议编号', max_length=20)
    conferencestatus = models.CharField(verbose_name='会议状态', max_length=20)
    conferencetime = models.DateTimeField(verbose_name='会议时间', null=True)  # 待修改

    class meta:
        db_table = 'conference'
