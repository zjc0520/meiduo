from rest_framework import serializers
from django_redis import get_redis_connection
import re
from rest_framework_jwt.settings import api_settings

from celery_tasks.email.tasks import send_verify_email
from goods.models import SKU
from users.models import User, Address
from . import constants

#创建序列化器类
from utils import tjws


class UserCreateSerializer(serializers.Serializer):
    #定义属性
    token = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    # 不接收客户端的数据，只向客户端输出
    username = serializers.CharField(
        min_length=5,
        max_length=20,
        error_messages={
            'min_length': '用户名包含5-20个字符',
            'max_length': '用户名包含5-20个字符',
        }
    )
    password = serializers.CharField(
        min_length=8,
        max_length=20,
        error_messages={
            'min_length': '密码包含8-20个字符',
            'max_length': '密码包含8-20个字符',
        },
        write_only=True
    )
    password2 = serializers.CharField(
        min_length=8,
        max_length=20,
        error_messages={
            'min_length': '密码包含8-20个字符',
            'max_length': '密码包含8-20个字符',
        },
        write_only=True
    )
    sms_code = serializers.IntegerField(write_only=True)
    mobile = serializers.CharField()
    allow = serializers.BooleanField(write_only=True)
    #验证
    def validate_username(self,value):
        # 验证用户名是否重复
        count = User.objects.filter(username = value).count()
        if count > 0:
            raise serializers.ValidationError("用户名已存在")
        return value


    def validate_mobile(self,value):
        #验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$',value):
            raise serializers.ValidationError("手机号格式错误")
        # 验证手机号是否重复
        count = User.objects.filter(mobile=value).count()
        if count >0:
            raise serializers.ValidationError("手机号已经存在")
        return value
    def validate_allow(self,value):
        #是否同意协议
        if not value:
            raise serializers.ValidationError("请先阅读协议并同意")
        return value
    #2.多属性判断
    def validate(self, attrs):
        # 判断两个密码是否一致
        password = attrs.get("password")
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("两个密码不一致")

        # 短信验证码是否正确
        # 1.获取请求报文中的短信验证码、手机号
        sms_code_request = attrs.get("sms_code")
        mobile = attrs.get("mobile")
        #2.获取redis中的短信验证码
        redis_cli = get_redis_connection('sms_code')
        sms_code_redis = redis_cli.get('sms_code_' + mobile)
        # 3判断是否过期
        if sms_code_redis is None:
            raise serializers.ValidationError('短信验证码已经过期')
        # 4.强制立即过期
        redis_cli.delete('sms_code_'+mobile)
        #5.判断两个验证码是否相等
        if int(sms_code_request) != int(sms_code_redis):
            raise serializers.ValidationError('短信验证码错误')
        return attrs
    # 保存
    def create(self,validated_data):
        user = User()
        user.username = validated_data.get("username")
        user.set_password(validated_data.get("password"))
        user.mobile = validated_data.get("mobile")
        user.save()

        #需要生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)  # header.payload.signature

        # 将token输出到客户端
        user.token = token

        return user
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email', 'email_active']

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ['email']
    def update(self, instance, validated_data):
        email = validated_data['email']
        instance.email = email
        instance.save()
        # 生成验证链接
        verify_url = instance.generate_verify_email_url()
        # 发送验证邮件
        send_verify_email.delay(email, verify_url)
        return instance


class EmailActiveSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=200)

    def validate(self, attrs):
        #获取加密字符串中
        token = attrs.get('token')
        #解密
        data_dict = tjws.loads(token,constants.VERIFY_EMAIL_TOKEN_EXPIRES)
        #判断是否过期
        if data_dict is None:
            raise serializers.ValidationError("激活链接已经过期")
        # 将获取到的user_id加入验证后的数据字典中
        attrs['user_id'] = data_dict.get('user_id')

        return attrs
# class AddressSerializer(serializers.ModelSerializer):
#     #关系属性,使用id接收
#     province_id =

class AddressSerializer(serializers.ModelSerializer):
    # 关系属性，使用id接收
    province_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    district_id = serializers.IntegerField()
    # 关系属性，改成非必须
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Address
        # fields=[]
        # 指定不需要的属性
        # 说明：user不需要传递，而是获取当前登录的用户
        exclude = ['is_delete', 'create_time', 'update_time', 'user']

    # create()
    def create(self, validated_data):
        # 判断当前是否达到上限
        user = self.context['request'].user
        if user.addresses.filter(is_delete=False).count() >= constants.ADDRESS_LIMIT:
            raise serializers.ValidationError('已经达到收货地址上限')
            # 默认实现中，未指定属性user，则添加时必然报错，所以在添加前需要指定user属性
        validated_data['user'] = user
        print(validated_data)

        address = super().create(validated_data)
        # address = Address.objects.create(**validated_data)
        return address
            # update()


class BrowseHistorySerializer(serializers.Serializer):
    sku_id = serializers.IntegerField(min_value=1)

    def validate_sku_id(self, value):
        # 查询商品编号是否存在
        count = SKU.objects.filter(pk=value).count()
        if count <= 0:
            raise serializers.ValidationError('商品编号无效')
        return value

    def create(self, validated_data):
        sku_id = validated_data['sku_id']
        # 连接redis
        redis_cli = get_redis_connection('history')
        # 根据不同的用户构造键
        key = 'history_%d' % self.context['request'].user.id
        # 1.删除sku_id
        redis_cli.lrem(key, 0, sku_id)
        # 2.添加
        redis_cli.lpush(key, sku_id)
        # 3.判断长度
        if redis_cli.llen(key) > constants.BROWSE_HISTORY_LIMIT:
            # 4.如果超过长度则删除最后一个
            redis_cli.rpop(key)

        return {'sku_id': sku_id}

