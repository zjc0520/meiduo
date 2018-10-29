from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    #默认拥有用户名密码,邮箱等属性
    #扩展属性
    email_active = models.BooleanField(default=False)
    mobile = models.CharField(max_length=11,unique=True)
    class Mate:
        db_table = 'tb_users'