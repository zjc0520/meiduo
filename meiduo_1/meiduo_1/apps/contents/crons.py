import os
from collections import OrderedDict

from crispy_forms.tests.test_settings import BASE_DIR
from django.conf import settings
from meiduo_1.settings import dev

from .models import ContentCategory,Content
from goods.models import GoodsCategory,GoodsChannel
from django.shortcuts import render



from utils.goods_category import get_goods_category

#网页静态化
def generate_index_html():
    categories = get_goods_category()
    # 1.2查询广告数据
    contents = {}
    content_categories = ContentCategory.objects.all()
    for category in content_categories:
        contents[category.key] = category.content_set.filter(status=True).order_by('sequence')
    # 2.生成html标签，写到html文件中
    # 2.1生成html字符串

    response = render(None,'index.html',{'categories':categories,'contents':contents})
    html_str = response.content.decode()
    #2.2写文件
    filename = os.path.join(dev.GENERATE_STATIC_HTML_PATH,'index.html')
    # filename = settings.GENERATE_STATIC_HTML_PATH + '/index.html'
    # print(filename)
    with open(filename,'w',encoding='utf-8') as f:
        f.write(html_str)
    print('ok')
