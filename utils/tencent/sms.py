#!/usr/bin/env python
# -*- coding:utf-8 -*-
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from qcloudsms_py import SmsMultiSender, SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from django.conf import settings


def send_sms_single(phone_num, template_id, template_param_list):
    """
    单条发送短信
    :param phone_num: 手机号
    :param template_id: 腾讯云短信模板ID
    :param template_param_list: 短信模板所需参数列表，例如:【验证码：{1}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
    :return:
    """
    # appid = settings.TENCENT_SMS_APP_ID  # 自己应用ID
    # appkey = settings.TENCENT_SMS_APP_KEY  # 自己应用Key
    # sms_sign = settings.TENCENT_SMS_SIGN  # 自己腾讯云创建签名时填写的签名内容（使用公众号的话这个值一般是公众号全称或简称）
    appid = 1400588388  # 腾讯云短信的appid
    appkey = "7c7c569e866c179fbf18a17d6a75d00c"  # 腾讯云短信的appkey
    sms_sign = "激进的点工"  # 腾讯云短信的签名，跟公众号名称一致
    sender = SmsSingleSender(appid, appkey)
    try:
        response = sender.send_with_param(86, phone_num, template_id, template_param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result': 1000, 'errmsg': "网络异常发送失败"}
    return response


def send_sms_multi(phone_num_list, template_id, param_list):
    """
    批量发送短信
    :param phone_num_list:手机号列表
    :param template_id:腾讯云短信模板ID
    :param param_list:短信模板所需参数列表，例如:【验证码：{1}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
    :return:
    """
    appid = 1400588388  # 腾讯云短信的appid
    appkey = "7c7c569e866c179fbf18a17d6a75d00c"  # 腾讯云短信的appkey
    sms_sign = "进击的测试猿"  # 腾讯云短信的签名，跟公众号名称一致
    sender = SmsMultiSender(appid, appkey)
    try:
        response = sender.send_with_param(86, phone_num_list, template_id, param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result': 1000, 'errmsg': "网络异常发送失败"}
    return response


if __name__ == '__main__':
    result1 = send_sms_single("18854823673", 1176778, [666])
    print(result1)
result2 = send_sms_single( ["15131255089", "15131255089", "15131255089", ],548760, [999, ])
print(result2)

# from qcloudsms_py import SmsSingleSender
# from qcloudsms_py.httpclient import HTTPError
# import random
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
#
#
# # 使用腾讯云发送手机6位随机验证码
# class TestQCloudSMS(object):
#     def __init__(self, phone_num):
#         self.appid = 1400588388  # 准备工作中的SDK AppID，类型：int
#         self.appkey = '7c7c569e866c179fbf18a17d6a75d00c'   # 准备工作中的App Key，类型：str
#         self.phone_num = phone_num
#         self.sign = '进击的测试猿'  # 准备工作中的应用签名，类型：str
#
#     def make_code(self):
#         """
#         :return: code 6位随机数
#         """
#         code = ''
#         for item in range(6):
#             code += str(random.randint(0, 9))
#         return code
#
#     def send_msg(self):
#         ssender = SmsSingleSender(self.appid, self.appkey)
#         try:
#             # parms参数类型为list
#             rzb = ssender.send_with_param(86, self.phone_num, 1176778, [self.make_code()],
#                                           sign=self.sign, extend='', ext='')
#             print(rzb)
#         except HTTPError as http:
#             print("HTTPError", http)
#         except Exception as e:
#             print(e)
#
#
# if __name__ == '__main__':
#     phone_num = ['18854823673', '18736971383']
#     sendmsg = TestQCloudSMS(random.choices(phone_num)[0])   # 需传入发送短信的手机号，单发
#     sendmsg.send_msg()


