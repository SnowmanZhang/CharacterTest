#-*-coding:utf-8-*-
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

def index(request):
	response_content = '''<p>hello world! this is the Django web service connectted with Apache.</p>
<h1>气质测试临时站点</h1>
<code>author: SnowmanZhang</code>
<h4>点击下方链接进入测试页面</h4>
<a href="./tmt/">进入</a>
'''
	
	return render(request,"index.html")
