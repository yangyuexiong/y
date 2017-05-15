from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from bbs import models

#django内置验证模块
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

#排序（-）
#动态-全局-返回同一页面
category_list = models.Category.objects.filter(set_as_top_menu=True).order_by('position_index')

#登陆验证
def acc_login(request):
    if request.method == 'POST':
        print(request.POST)
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/bbs')
        else:
            login_err = '账号或密码错误'
            return render(request,'bbs/login.html',{'login_err':login_err})
    return render(request,'bbs/login.html')
#退出
def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/bbs')



def index(request):
    #排序（-）
    # category_list = models.Category.objects.filter(set_as_top_menu=True).order_by('position_index')
    return render(request,'bbs/index.html',{'category_list':category_list})

def category(request,id):
    #获取：category
    category_obj = models.Category.objects.get(id=id)
    return render(request,'bbs/index.html',{'category_list':category_list,
                                            'category_obj':category_obj})