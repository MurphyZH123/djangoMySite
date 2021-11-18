from django.shortcuts import render
import random
from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from utils.tencent.sms import send_sms_single
from django_redis import get_redis_connection


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


class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile_phone(self):
        """ 手机号校验的钩子 """
        mobile_phone = self.cleaned_data['mobile_phone']

        # 判断短信模板是否有问题
        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            # self.add_error('mobile_phone','短信模板错误')
            raise ValidationError('短信模板错误')

        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl == 'login':
            if not exists:
                raise ValidationError('手机号不存在')
        else:
            # 校验数据库中是否已有手机号
            if exists:
                raise ValidationError('手机号已存在')

        # 生成随即验证码
        code = 1234

        # 发送短信
        sms = send_sms_single(mobile_phone, template_id, [code, ])
        if sms is not None:
            raise ValidationError("短信发送失败，{}".format(sms['errmsg']))

        # 验证码 写入redis（django-redis）
        conn = get_redis_connection()
        conn.set(mobile_phone, code, ex=60) # ex为超时时间

        return mobile_phone

