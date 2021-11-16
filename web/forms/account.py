from django.shortcuts import render
from django import forms
from web import models
from django.core.validators import RegexValidator


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