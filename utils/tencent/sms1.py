# -*- coding: utf-8 -*-

"""
@author: rzb
@software: PyCharm
@file: sms_qcloud.py
@time: 2019/8/21 11:54
"""

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import random
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# 使用腾讯云发送手机6位随机验证码
class TestQCloudSMS(object):
    def __init__(self, phone_num):
        self.appid = 1400588388  # 准备工作中的SDK AppID，类型：int
        self.appkey = '7c7c569e866c179fbf18a17d6a75d00c'   # 准备工作中的App Key，类型：str
        self.phone_num = phone_num
        self.sign = '进击的测试猿'  # 准备工作中的应用签名，类型：str

    def make_code(self):
        """
        :return: code 6位随机数
        """
        code = ''
        for item in range(6):
            code += str(random.randint(0, 9))
        return code

    def send_msg(self):
        ssender = SmsSingleSender(self.appid, self.appkey)
        try:
            # parms参数类型为list
            rzb = ssender.send_with_param(86, self.phone_num, 1176778, [self.make_code()],
                                          sign=self.sign, extend='', ext='')
            print(rzb)
        except HTTPError as http:
            print("HTTPError", http)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    phone_num = ['18854823673', '18736971383']
    sendmsg = TestQCloudSMS(random.choices(phone_num)[0])   # 需传入发送短信的手机号，单发
    sendmsg.send_msg()

