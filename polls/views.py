from django.shortcuts import render, HttpResponse
from utils.tencent.sms import send_sms_single
from django.conf import settings
import random


def send_sms(request):
    """
    发送短信
    ?tpl=login  -> 登录模版ID
    ?tpl=register -> 注册模版ID
    """
    tpl = request.GET.get('tpl')
    tpl_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    print(tpl_id)
    if tpl_id is None:
        return HttpResponse('模版不存在')
    code = random.randrange(1000, 9999)
    res = send_sms_single('18854823673', tpl_id, [code, ])
    print(res)
    if res is None:
        return HttpResponse("成功")
    else:
        return HttpResponse("失败")


from django import forms
from polls import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])   # 将model中的mobile_phone进行重写,validators接受两个参数，一个是正则校验，一个是报错信息
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请确认你的密码'}))
    confirm_password = forms.CharField(label='重复密码',
                                       widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再次确认你的密码'}))   # 新增form字段，数据库没有
    code = forms.CharField(label='验证码',
                           required=True, min_length=4, max_length=4,
                           widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入你的验证码'}))

    class Meta:
        model = models.UserInfo
        # fields = '__all__'  # 默认获取model中的字段顺序
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']

# 重写__init__方法，添加统一的样式
    def __init__(self,*args,**kwargs):
        super().__init__()
        for name,field in self.fields.items():
            # name=字段名称 field=后面的规则
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)


def register(request):
    form = RegisterModelForm()
    return render(request, 'polls/register.html', {'form':form})


if __name__ == '__main__':
    send_sms('http://127.0.0.1:8000/send/sms?tpl=login')
