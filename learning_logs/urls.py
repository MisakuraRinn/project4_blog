"""定义learning_logs的URL模式"""
from django.urls import path
from . import views
app_name='learning_logs'
urlpatterns=[
  # 主页
  path('',views.index,name='index'),
  path('topics/',views.topics,name='topics'),
  #特定主体的详细页面
  path('topics/<int:topic_id>/',views.topic,name='topic'),
  # 用于添加新主题的网页
  path('new_topic/',views.new_topic,name='new_topic'),
  # 给网址取别称，方便修改
  # 是不是用这个别称的时候就会调用view里面的new_entry函数？
  path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),
  path('edit_entry/<int:entry_id>/',views.edit_entry,name='edit_entry')
]