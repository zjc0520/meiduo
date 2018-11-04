from collections import OrderedDict

from django.conf import settings

from goods.models import GoodsChannel

def get_goods_category():
    """
    categories =

    {
        组1编号(即频道编号):
        {
            一级分类channels:[]
            二级分类sub_cats:[]
        },
         组2编号(即频道编号):
         {
            一级分类channels:[]
            二级分类sub_cats:[]
         }
    }
    如:
    {
        1:{
            channels:[
                {手机},{相机},{数码}
            ],
            sub_cats:[二级分类]
        },
        2:{
            channels:[
                {电脑},{办公},{家用电器}
            ],
            sub_cats:[二级分类]
        },
        ....
    }
    :return:
    """
    # 1.查询分类数据、广告数据
    # 1.1查询分类数据
    categories = OrderedDict()#定义有序字典,代表整个页面的数据
    channels = GoodsChannel.objects.order_by('group_id','sequence')
    #channels:所有的频道
    for channel in channels:
        # channel.group_id===>组编号
        # channel.category====>一级分类
        # channel.url=========>一级分类的链接
        if channel.group_id not in categories:
            categories[channel.group_id] = {'channels':[],'sub_cats':[]}
            #表示为第几组添加数据hannel.group_id:组编号
        #添加一级分类
        categories[channel.group_id]['channels'].append({
            # categories[channel.group_id]['channels']:表示某一组的一级分类
            'id':channel.id,
            'name':channel.category.name,
            'url':channel.url
        })
        #添加二级分类
        sub_cats = channel.category.goodscategory_set.all()
        # goodscategory_set该关系字段是建表时自动生成的,
        # 可以通过一级分类查看所有的二级分类
        # 添加三级分类
        for cat2 in sub_cats:
            # sub_cats:所有的二级类别
            # cat2:某一个二级类别
            cat2.sub_cats=[]
            for cat3 in cat2.goodscategory_set.all():
                cat2.sub_cats.append(cat3)
            categories[channel.group_id]['sub_cats'].append(cat2)
    # print(categories)
    return categories