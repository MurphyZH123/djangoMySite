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


