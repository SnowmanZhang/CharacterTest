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

def index(request):
	request.session['dict_choice'] = {}
	request.session['pagenumber'] = 1
	return render(request,'tmt/tmtindex.html')


# Create your views here.
