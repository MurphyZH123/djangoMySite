from django.shortcuts import render,HttpResponse

# Create your views here.
import random
from utils.tencent.sms import send_sms_single


def send_sms(request):
    """发送短信"""
    code = random.randrange(1000, 9999)
    res = send_sms_single('18854823673', 1176778, [code, ])
    print(res)
    if res is None:
        return HttpResponse("成功")
    else:
        return HttpResponse("失败")
