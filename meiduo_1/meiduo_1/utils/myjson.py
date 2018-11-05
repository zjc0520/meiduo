import pickle
import base64

""" 
    字典-字节-加密字节-字符串
    字符串-字节-解密字节-字典
"""

def dumps(mydict):
    """
    将字典转换成加密字符串
    :param mydict:
    :return:
    """
    # 将字典转字节b'\x**\x**..'
    bytes_hex = pickle.dumps(mydict)
    #加密b'a-zA-Z0-9='
    bytes_64 = base64.b64encode(bytes_hex)
    # 转字符串
    return bytes_64.decode()

def loads(mystr):
    """
    将字符串转换成字典
    :param mystr:
    :return:
    """
    # 将字符串转字节
    bytes_64 = mystr.encode()
    #解密
    bytes_hex = base64.b64decode(bytes_64)
    #转字典
    return pickle.loads(bytes_hex)

