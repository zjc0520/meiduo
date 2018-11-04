from rest_framework.generics import ListAPIView
from goods.models import SKU
from goods.serializers import SKUSerializer
from rest_framework.filters import OrderingFilter
from utils.pagination import SKUListPagination

from drf_haystack.viewsets import HaystackViewSet
from goods.serializers import SKUIndexSerializer

class SKUListView(ListAPIView):
    # queryset = SKU.objects.all()
    def get_queryset(self):
        # 查询多个时，获取路径中的参数：self.kwargs===>字典
        return SKU.objects.filter(category_id=self.kwargs['category_id'])

    serializer_class = SKUSerializer

    # 分页
    pagination_class = SKUListPagination

    # 排序
    filter_backends = [OrderingFilter]
    ordering_fields = ['create_time', 'price', 'sales']

class SKUSearchViewSet(HaystackViewSet):
    """
    SKU搜索
    """
    # 模型类可改
    index_models = [SKU]
    # 序列化器
    serializer_class = SKUIndexSerializer
    # 分页
    pagination_class = SKUListPagination
