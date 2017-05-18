from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

# Create your models here.

#帖子表-存放帖子文章
class Article(models.Model):
    #标题
    title = models.CharField(verbose_name="标题" ,max_length=255)
    #描述简介
    brief = models.CharField(null=True,blank=True,max_length=255)
    #分类/板块-关联
    category = models.ForeignKey(to='Category', verbose_name="分类")
    #内容
    content = models.TextField(verbose_name="文章内容")
    #作者
    author = models.ForeignKey('UserProfile')
    #发布时间
    #自动创建的时候的时间,默认不能更改。
    pub_date = models.DateTimeField(blank=True,null=True)
    #最后更新时间
    last_modify = models.DateTimeField(auto_now=True)
    #优先级
    priority = models.IntegerField(u'优先级',default=0, null=True)

    #图片
    head_img = models.ImageField(u'文章标题图片',upload_to='tupian')


    #附件
    atfile = models.ImageField(verbose_name="图片附件", null=True,blank=True)

    #状态
    status_choices = (('draft',u'草稿'),
                      ('published',u'已发布'),
                      ('hidden',u'隐藏'),)

    status = models.CharField(choices=status_choices,default='published',max_length=255)

    def __str__(self):
        return self.title

    #判断
    def clean(self):
        if self.status == 'draft' and self.pub_date is not None:
            raise ValidationError('error')
        if self.status == 'published' and self.pub_date is None:
            self.pub_date = datetime.date.today()

    

#贴-内容(评论)
class Comment(models.Model):
    article = models.ForeignKey(Article,verbose_name=u'所属文章')
    #父级评论
    parent_comment = models.ForeignKey('self',related_name='my_children',blank=True,null=True)
    #评论点赞-同一个表-默认为评论
    comment_choices = (('1',u'评论'),
                       ('2',u'点赞'))
    comment_type = models.ImageField(choices=comment_choices,default=1)
    #评论人
    user = models.ForeignKey('UserProfile')
    #评论时间
    date = models.DateTimeField(auto_now_add=True)
    #评论内容
    comment = models.TextField(blank=True,null=True)


    def clean(self):
        if self.comment_type == 1 and self.comment is None:
            raise ValidationError(u'内容不能为空')

    def __str__(self):
        # return '%s,P:%s,%s' % (self.article, self.parent_comment.id, self.comment)
         return self.comment


#帖子属于的板块
class Category(models.Model):
    #板块名字_唯一
    name = models.CharField(max_length=64,unique=True)
    #简介
    brief = models.CharField(null=True,blank=True,max_length=255)
    #
    set_as_top_menu = models.BooleanField(default=False)
    #展示位置
    position_index = models.SmallIntegerField()
    #版主-可以以为空
    admins = models.ManyToManyField('UserProfile',blank=True)

    def __str__(self):
        return self.name



#用户
class UserProfile(models.Model):
    #
    User = models.OneToOneField(User)
    #昵称
    name = models.CharField(max_length=32)
    #个人简介
    signature =models.CharField(max_length=255,blank=True,null=True)
    #头像-宽高设定-裁剪
    head_img = models.ImageField(height_field=150,width_field=150,blank=True,null=True)

    def __str__(self):
        return self.name
