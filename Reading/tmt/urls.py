from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$',views.index,name='index'),
url(r'^testing/$',views.deal,name='testing'),
url(r'^submit/$',views.calculate,name='submit'),
url(r'^(?P<question_id>[0-9]+)/$',views.deal,name='deal'),
]
