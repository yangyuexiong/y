from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from bbs import models
from bbs import comment_hander
import json
#django内置验证模块
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

#排序（-）
#动态-全局-返回同一导航页面
category_list = models.Category.objects.filter(set_as_top_menu=True).order_by('position_index')

#注册
def register(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        user.save()
        profile = models.UserProfile()
        profile.User = user
        profile.save()
        # return HttpResponseRedirect(redirect_to="/bbs")
        return HttpResponseRedirect(redirect_to='status/注册成功/login')
    else:
        return render(request,'bbs/register.html')


#登陆验证
def acc_login(request):
    if request.method == 'POST':
        print(request.POST.get('username'))
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(request.GET.get('next')or'/bbs')
        else:
            login_err = '账号或密码错误'
            return render(request,'bbs/login.html',{'login_err':login_err})
    return render(request,'bbs/login.html')
#注销
def acc_logout(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next')or'/bbs')


#主页
def index(request):
    #排序（-）
    # category_list = models.Category.objects.filter(set_as_top_menu=True).order_by('position_index')
    #板块(全部) 显示高亮
    category_obj = models.Category.objects.get(position_index=0)
    article_list = models.Article.objects.filter(status='published')
    return render(request,'bbs/index.html',{'category_list':category_list,
                                            'article_list': article_list,
                                            'category_obj': category_obj})

#板块
def category(request,id):
    #获取：category
    category_obj = models.Category.objects.get(id=id)
    if category_obj.name == "全部":
        article_list = models.Article.objects.filter(status='published')
        #print(article_list)
    else:
        #筛选出article中category_id对应的id,过滤状态显示
        article_list = models.Article.objects.filter(category_id=category_obj.id,status='published')
    return render(request,'bbs/index.html',{'category_list':category_list,
                                            'category_obj':category_obj,
                                            'article_list':article_list,})

#文章内页
def article_detail(request,article_id):
    article_obj = models.Article.objects.get(id=article_id)
    comment_tree = comment_hander.build_tree(article_obj.comment_set.select_related())
    commentList = article_obj.comment_set.select_related()
    return render(request,'bbs/article_detail.html',{
        'article_obj':article_obj,
        'category_list': category_list,
        'commentList': commentList
    })


#评论
def comment(request):
    print(request.POST)
    if request.method == 'POST':
        new_comment_obj = models.Comment(
            article_id = request.POST.get('article_id'),
            parent_comment_id = request.POST.get('parent_comment_id')or None,
            comment_type = request.POST.get('comment_type'),
            user_id = request.user.userprofile.id,
            comment = request.POST.get('comment'),
        )
        new_comment_obj.save()
    return HttpResponse('success')

#获取评论
def get_comments(request,article_id):
    article_obj = models.Article.objects.get(id=article_id)
    comment_tree = comment_hander.build_tree(article_obj.comment_set.select_related())
    tree_html = comment_hander.render_comment_tree(comment_tree)
    return HttpResponse(tree_html)

#操作结果显示
def show_status_page(request, msg, url):
    return render(request, 'bbs/status_page.html', {
        'msg': msg,
        'url': url
    })
