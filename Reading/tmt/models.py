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
# Create your models here.
