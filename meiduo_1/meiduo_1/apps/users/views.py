from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import View,APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User, Address
from users.serializers import UserCreateSerializer, UserDetailSerializer, EmailSerializer,EmailActiveSerializer,AddressSerializer
from . import constants
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from rest_framework_jwt.utils import jwt_response_payload_handler
from rest_framework import generics

class UsernameCountView(APIView):
    """
        用户名数量
    """
    def get(self,request,username):
        #查询用户的个数
        count = User.objects.filter(username=username).count()
        #响应
        #组织响应数据
        data ={
            "username":username,
            "count":count
        }
        return Response(data=data)
class MobileCountView(APIView):
    def get(self,request,mobile):
        #查询手机号的个数
        count = User.objects.filter(mobile=mobile).count()
        #响应
        data = {
            "mobile":mobile,
            'count':count
        }
        return Response(data=data)
class UserCreateView(CreateAPIView):
    # def post(self,request):
    # 注册用户==>创建用户
    # queryset = 当前进行创建操作，不需要查询
    serializer_class = UserCreateSerializer
class UserDetailView(generics.RetrieveAPIView):
    # queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    #要求登录
    permission_classes = [IsAuthenticated]
    # 视图中封装好的代码，是根据主键查询得到的对象
    # 需求：不根据pk查，而是获取登录的用户
    # 解决：重写get_object()方法
    # request.user:获取登录的用户
    def get_object(self):
        return self.request.user

"""保存邮箱"""
class EmailView(generics.UpdateAPIView):
    #要求登录
    permission_classes = [IsAuthenticated]
    #指定序列化器
    serializer_class = EmailSerializer
    def get_object(self):
        return self.request.user
"""修改邮箱属性并保存"""
class EmailActiveView(APIView):
    def get(self,request):
        #接收数据并验证
        serializer = EmailActiveSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors)
        #查询当前用户并修改属性
        user = User.objects.get(pk=serializer.validated_data.get('user_id'))
        user.email_active = True
        user.save()
        #响应
        return Response({'message':'OK'})

class AddressViewSet(ModelViewSet):
    # 待实现
    # retrieve==》根据主键查询1个，不需要
    # update===》修改
    # destroy==》删除
    permission_classes = [IsAuthenticated]
    # create====》创建self.request.user
    serializer_class = AddressSerializer

    # 指定查询集
    queryset = Address.objects.filter(is_delete=False)
    def get_queryset(self):
        return self.request.user.addresses.filter(is_delete=False)

    # list======>查询多个[{},{},....]
    # 重写
    def list(self, request, *args, **kwargs):
        # 查询数据
        address_list = self.get_queryset()
        # 创建序列化器对象
        serializer = self.get_serializer(address_list, many=True)
        # 返回值的结构：
        '''
        {
            'user_id': 用户编号,
            'default_address_id': 默认收货地址编号,
            'limit': 每个用户的收货地址数量上限,
            'addresses': 地址数据，格式如[{地址的字典},{},...]
        }
        '''
        return Response({
            'user_id': self.request.user.id,
            'default_address_id': self.request.user.default_address_id,
            'limit': constants.ADDRESS_LIMIT,
            'addresses': serializer.data  # [{},{},...]
        })
    # destroy==》物理删除，重写，实现逻辑删除
    def destory(self,request,*args,**kwargs):
        #根据主键查询对象
        address = self.get_object()
        #逻辑删除
        address.is_delete = True
        #保存
        address.save()
        #响应
        return Response(status=204)
    # 修改标题===>****/pk/title/------put
    # 如果没有detail=False=====>*****/title/
    # ^ ^addresses/(?P<pk>[^/.]+)/title/$ [name='addresses-title']
    @action(methods=['put'],detail=True)
    def title(self,request,pk):
        #根据主键查询收货地址
        address = self.get_object()
        #接收数据,修改标题属性
        address.title = request.data.get('title')
        #保存
        address.save()
        #响应
        return Response({'title':address.title})
    # 设置默认收货地址===>^ ^addresses/(?P<pk>[^/.]+)/status/$ [name='addresses-status']
    @action(methods=['put'],detail=True)
    def status(self,request,pk):
        #查找当前登录用户
        user = request.user
        #修改属性
        user.default_address_id = pk
        #保存
        user.save()
        #响应
        return Response({'message':'ok'})






