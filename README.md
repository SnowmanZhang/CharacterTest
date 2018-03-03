# CharacterTest

This is a tiny project of Django to test which character you are.

## 简介

这是一个练手做的Django小项目，它旨在使用一套已经成熟的气质类型测试题对测试者进行测试。在测试者提交了他们的答案后(不需要全部提交，只需答满足够的题目数量)，系统自动计算出来测试结果。


- [网站入口](123.207.5.36)
- [测试题出处](https://www.wjx.cn/jq/183158.aspx)


## 项目详解

现在让我们开始从头分析完成这个小项目需要做些什么。

最核心的需求就是

1. 从数据库中提取出题目，生成一个测试页面
2. 每当测试者点击完答案，则返回下一道题的页面
3. 为了防止有人跳页，上述逻辑不能使用静态页面生成

### 模型构建

那么现在首先需要建立一个关于问题的数据模型。这个模型包括以下几个字段

- 问题内容
- 问题类别(这是因为本套测试题将问题本身分为四类，并在对四个气质分别相加，故在输入问题时就要界定该问题是对哪一种气质的计算)
- 问题归属(为了服务的可拓展性，例如以后再增设新的测试题，则可以继续使用该模型，但两套测试题不能混在一起，故设置一个问题归属，本次60题全部属于一个名叫`tmt`的类别)
- 问题id(这是该套题的第几个题)

在总项目下，新建一个服务并命名为tmt，接着在其中的models.py中建立模型

```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    attribute = models.CharField(max_length=12) 
    project = models.CharField(max_length=32,default ="")
    project_id = models.CharField(max_length=12,default="")
    def __unicode__(self):
        return self.question_text

```

### 路由设置

模型建立好了以后，我们来思考一下页面的设置是怎样的。它应该有如下逻辑

1. 点击测试题页面，首先是一篇简介，点击简介里的开始答题方开始输出问题，这个简介的页面可以设置为tmt的首页，即url为 `ip_address/tmt/`
2. 开始答题了以后，为了防止有人跳页回答，产生无效答卷，url只使用一个，即是`ip_address/tmt/testing`，用户向这个页面提交表单，服务器收到表单之后一边记录，一边生成新的单页返回。
3. 所有前面已经答过的题及答案，可以使用session保存，在交互中不断增加，当点击提交按钮后，服务器提取session中的所有问题，进行计算并返回结果

因此主页urls.py及tmt服务的urls.py设置如下

```python
from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^tmt/',include('tmt.urls',namespace='tmt')),
]



from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$',views.index,name='index'),
url(r'^testing/$',views.deal,name='testing'),
url(r'^submit/$',views.calculate,name='submit'),
]

```

### 首页设置与静态资源调取

我们首先解决index首页的问题，在urls.py中，我们已经将`ip_address/tmt/`的页面交由views.index函数来处理，因此只需要在views.py文件中设置好index函数即可。在这个函数中，我们套用了一个静态模板，tmtindex.html是一个静态页面，Django一般规定放置于该服务下的templates/目录下。

```python


def index(request):
    request.session['dict_choice'] = {}
    request.session['pagenumber'] = 1
    return render(request,'tmt/tmtindex.html')

```

以下是tmtindex.html模板页面，需要注意的是，Django有自身的静态资源引用方式，不可以直接使用相对路径表示CSS资源或JS资源，静态资源一般需要放置在该服务下的static目录下，而引用方式为`href="{% static 'dist/image/icon_snowman.ico' %}"`

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
{% load static %}
    <link rel="icon" href="{% static 'dist/image/icon_snowman.ico' %}">
    <title>气质测试|首页</title>
    <!-- Bootstrap core CSS -->
    <link href="{% static 'dist/css/bootstrap.min.css' %}" rel="stylesheet">
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <link href="{% static 'dist/css/ie10-viewport-bug-workaround.css' %}" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="{% static 'dist/css/navbar-static-top.css' %}" rel="stylesheet">
    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="{% static 'dist/js/ie-emulation-modes-warning.js' %}"></script>
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="container">
      <!-- Main component for a primary marketing message or call to action -->
      <div class="jumbotron">
        <h1>气质测试简介</h1>
        <p>根据希波克拉底的四液说，人的气质类型分为：多血质、粘液质、抑郁质和胆汁质。分别对应着人们气质行为的四种类别，随着生活变化，人的气质类型也会发生变化。测试题共60题整，本站经过前期数据优化，可以以尽可能少的题目数量得知您的气质类型，但我们更加推荐您做完这60道题获得最准确的判断。</p>
        <p>
          <a class="btn btn-lg btn-primary" href="./testing/" role="button">开始答题</a>
        </p>
      </div>
    </div> <!-- /container -->
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="{% static 'dist/js/jquery.min.js' %}"></script>
    <script src="{% static 'dist/js/bootstrap.min.js' %}"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="{% static 'dist/js/ie10-viewport-bug-workaround.js' %}"></script>
  </body>
</html>

```

### views处理函数

现在我们就来到了最关键的views.py部分，在这个文件中，主要是deal函数，用于接收用户传来的答案，并存入session中，并且依据问题id返回下一个问题渲染的单页，将session附回去。而calculate函数用于计算session中提交的问题。


```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.template import RequestContext,loader
from .models import Question
from django.http import HttpResponse

def deal(request):
    question_id = request.session['pagenumber']
    p = get_object_or_404(Question,project_id=question_id)
    request.session['pagenumber'] = request.session['pagenumber'] + 1
    if request.POST and request.POST.has_key('choice'):
        if request.POST['choice'] == "":
            pass
        else:
            request.session['dict_choice'][question_id] = request.POST['choice']
    else:
        request.session['pagenumber'] = request.session['pagenumber'] - 1 
        return render(request,'tmt/ss_input.html',{'s_question':p,'pagenumber':request.session['pagenumber'],})
    if question_id < 60:
        pnext = get_object_or_404(Question,project_id=str(int(question_id)+1))
    else:
        pnext = p
    return render(request,'tmt/ss_input.html',{'s_question':pnext,'pagenumber':request.session['pagenumber'],})


def calculate(request):
    dict_choice = request.session['dict_choice']
    score_tree = {'1':0,'2':0,'3':0,'4':0}
    for unit in dict_choice:
        attr = get_object_or_404(Question,project_id = unit).attribute
        score_tree[attr] = score_tree[attr] - int(dict_choice[unit]) + 3
    scorelist = [score_tree['1'],score_tree['2'],score_tree['3'],score_tree['4']]
    temp = scorelist[:]
    temp.sort()
    enddict = {'胆汁质':score_tree['1'],'多血质':score_tree['2'],'黏液质':score_tree['3'],'抑郁质':score_tree['4'],}
    res_dict = ['胆汁质','多血质','黏液质','抑郁质']
    if temp[-1] - temp[-2] > 4:
        result = res_dict[scorelist.index(temp[-1])]
    elif temp[-2] - temp[-3] > 4:
        result = res_dict[scorelist.index(temp[-1])]
        scorelist[scorelist.index(temp[-1])] = -50
        result = result + '+' + res_dict[scorelist.index(temp[-2])] 
    elif temp[-3] - temp[-4] > 4:
        result = res_dict[scorelist.index(temp[-1])]
        scorelist[scorelist.index(temp[-1])] = -50
        result = result + '+' + res_dict[scorelist.index(temp[-2])] 
        scorelist[scorelist.index(temp[-2])]
        result = result + '+' + res_dict[scorelist.index(temp[-3])]
    else:
        result = "混合气质"
    if len(dict_choice) > 10:
        with open("/home/tmtlog.txt",'a') as f:
            for key,value in dict_choice.items():
                f.write(key+','+value+'\t')
            f.write('\n')
    return render(request,'tmt/result.html',{'score_tree':enddict,'result':result,})


```

当然，细心的同学会发现，我在calculate的最后部分加入了点奇怪的东西，当表单长度大于10，即答完了10道题以上，我会在后台将此次问卷记录下来，视为有效问卷。

这个部分如果有什么值得说的，就是关于表单提交的问题。

### 细节：表单提交

首先我们可以看一下deal函数最后返回的渲染页面是`return render(request,'tmt/ss_input.html',{'s_question':pnext,'pagenumber':request.session['pagenumber'],})`

在这里，模板是ss_input.html，传参为当前需要渲染的新问题pnext，以及当前已经答了多少题pagenumber。那么之前答卷的session呢？它们已经包含在了request里了，会一并转发回来。deal函数里如果判定本次回答有效，则会给request.session加入新的内容。现在我们来看ss_input.html内容

```html

    {% load static %}

    <link rel="icon" href="{% static 'dist/image/icon_snowman.ico' %}">
    <title>第 {{ pagenumber }} 题</title>

...

{% if s_question %}
<form action="{% url 'tmt:testing' %}" method="post">   
...

{% ifnotequal pagenumber 61 %}
      <div class="jumbotron">
        <h3>{{ s_question.question_text }}</h3>
      </div>
      <div class="row">
        <div class="col-lg-8">
            <p><button type="submit" name="choice" class="btn btn-lg btn-success"  id="choice1" value="1"/>非常符合</button></p>
        </div><!-- /.col-lg-6 -->
        <div class="col-lg-8">
            <p><button type="submit" name="choice" class="btn btn-lg btn-success"  id="choice2" value="2"/>比较符合</button></p>
        </div><!-- /.col-lg-6 -->
        <div class="col-lg-8">
            <p><button type="submit" name="choice" class="btn btn-lg btn-success"  id="choice3" value="3"/>不能确定</button></p>
        </div><!-- /.col-lg-6 -->
        <div class="col-lg-8">
            <p><button type="submit" name="choice" class="btn btn-lg btn-success"  id="choice4" value="4"/>较不符合</button></p>
        </div><!-- /.col-lg-6 -->
        <div class="col-lg-8">
            <p><button type="submit" name="choice" class="btn btn-lg btn-success"  id="choice5" value="5"/>完全不符</button></p>
        </div><!-- /.col-lg-6 -->
      </div><!-- /.row -->
{% else %}
    <div class="row">
        <div class="col-lg-3">
            <p><a name="choice" class="btn btn-lg btn-success" href="{% url 'tmt:submit' %}">提交</a></p>
        </div>
    </div>
{% endifnotequal %}


</form>
{% endif %}
```


可以看到，模板页面的主体就是一个form表单，五个值代表从完全相符到完全不符的五个按钮，点击后直接提交，返回给服务器的deal函数，这时提交的回答被保存在了`request.POST['choice']`里面。

## 联系我

一个小小的练习作品，帮助自己了解了Django的基础应用和想象空间，非常有趣。如果您对该项目有什么兴趣或者疑问，欢迎联系我。

- E-mail: zhijunzhang_hi@163.com
- Github: https://github.com/SnowmanZhang
- 测试网站(域名snowman1995.cn正在申请中): 123.207.5.36
- Wechat: renxdu