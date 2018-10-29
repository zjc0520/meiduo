from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.jwt_token import generate
from . import constants
from oauth.qq_sdk import OAuthQQ
from utils import tjws
from oauth.models import OAuthQQUser
from oauth.serializers import QQBindSerializer

#  url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),


class QQURLView(APIView):
    """
    获取QQ登录的url
    """
    def get(self,request):
        # 提供用于qq登录的url
        next = request.query_params.get("next")
        #用户QQ登录成功后进入美多商城的哪个网址
        oauth = OAuthQQ(state=next)
        login_url = oauth.get_qq_login_url()
        return Response({'login_url':login_url})
class QQloginView(APIView):
    def get(self,request):
        #获取code
        code = request.query_params.get('code')
        #根据code获取token
        oauthqq = OAuthQQ()
        token = oauthqq.get_access_token(code)
        #根据token获取openid
        openid = oauthqq.get_openid(token)

        #查询openid是否存在

        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except:
            #如果不存在,则通知用户绑定页面
            #将openid加密进行输出
            data = tjws.dumps({'openid':openid},
                        constants.BIND_TOKEN_EXPIRES)
            # 响应
            return Response({
                'access_token': data
            })
        else:
            # 如果存在则状态保持，登录成功
            return Response({
                "user_id":qquser.user_id,
                "username":qquser.user.username,
                "token":generate(qquser.user)
                })
    def post(self,request):
        #接收
        serializer = QQBindSerializer(data=request.data)
        #验证
        if not serializer.is_valid():
            return Response({
                "message":
                    serializer.errors
            })
        # 绑定：在qquser表中创建一条数据
        qquser = serializer.save()
        # 响应：绑定完成，登录成功，状态保持
        return Response({
         "user_id":qquser.user.id,
            "username":qquser.user.username,
            "token":generate(qquser.user)
        })

