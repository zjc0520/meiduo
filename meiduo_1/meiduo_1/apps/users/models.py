from django.db import models
from django.contrib.auth.models import AbstractUser
from utils import tjws

from rest_framework import settings
from settings import dev
from utils.models import BaseModel

from . import constants
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer

class User(AbstractUser):
    #默认拥有用户名密码,邮箱等属性
    #扩展属性
    email_active = models.BooleanField(default=False)
    mobile = models.CharField(max_length=11,unique=True)
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')
    class Mate:
        db_table = 'tb_users'

    def generate_verify_email_url(self):
        """
        生成验证邮箱的url
        """
        serializer =TJWSSerializer(dev.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
        data = {'user_id': self.id, 'email': self.email}
        token = serializer.dumps(data).decode()
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token
        return verify_url

class Address(BaseModel):
    """用户地址模型类"""
    # 所属用户
    user = models.ForeignKey(User,related_name='addresses')
    # 名称，如‘家’、‘公司’
    title = models.CharField(max_length=20)
    # 收件人
    receiver = models.CharField(max_length=10)
    # 省
    province = models.ForeignKey('areas.Area', related_name='province_addr')
    # 市
    city = models.ForeignKey('areas.Area', related_name='city_addr')
    # 区县
    district = models.ForeignKey('areas.Area', related_name='district_addr')
    # 详细地址
    place = models.CharField(max_length=100)
    # 手机号
    mobile = models.CharField(max_length=11)
    # 固定电话
    tel = models.CharField(max_length=20, null=True, blank=True)
    # 邮箱
    email = models.CharField(max_length=50, null=True, blank=True)
    # 逻辑删除
    is_delete = models.BooleanField(default=False)