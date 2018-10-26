from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserCreateSerializer

from users.models import User


class UsernameCountView(APIView):
    """判断用户是否存在"""
    def get(self,request,username):
        #查询用户数量
        count = User.objects.filter(username=username).count()
        data = {
            "username":username,
            "count":count
        }
        return Response(data=data)
class MobileCountView(APIView):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()

        data = {
            "mobile":mobile,
            'count':count
        }
        return Response(data=data)
class UserCreateView(CreateAPIView):
    """注册用户,创建用户"""
    serializer_class = UserCreateSerializer
