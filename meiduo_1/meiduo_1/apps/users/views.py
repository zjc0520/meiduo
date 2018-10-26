from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import View,APIView
from users.models import User
from users.serializers import UserCreateSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from rest_framework_jwt.utils import jwt_response_payload_handler


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