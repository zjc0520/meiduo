from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import View,APIView
from users.models import User
from users.serializers import UserCreateSerializer, UserDetailSerializer
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
    def get_object(self):
        return self.request.user

