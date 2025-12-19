from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.http import Http404
# Create your views here.
# from django.shortcuts import render

def index(request):
  """学习笔记的主页"""
  return render(request,'learning_logs/index.html')
@login_required
def topics(request):
  """显示所有主题"""
  # topics=Topic.objects.filter(owner=request.user).order_by('date_added')
  # 只显示自己创建的主题
  topics=Topic.objects.order_by('date_added')
  # 显示所有主题
  context={'topics':topics}
  return render(request,'learning_logs/topics.html',context)
@login_required
def topic(request,topic_id):
  """显示单个主题及其所有的条目"""
  topic=Topic.objects.get(id=topic_id)
  # if topic.owner != request.user:
  #   raise Http404
  entries=topic.entry_set.order_by('-date_added')
  context={'topic':topic,'entries':entries}
  return render(request,'learning_logs/topic.html',context)
@login_required
def new_topic(request):
  # print("add new_topic")
  """添加新主题"""
  if request.method!='POST':
    # 未提交数据：创建一个新表单
    form=TopicForm()
  else:
    # POST提交的数据：对数据进行处理
    form=TopicForm(data=request.POST)
    if form.is_valid():
      new_topic=form.save(commit=False)
      new_topic.owner=request.user
      new_topic.save()
      # form.save()
      return redirect('learning_logs:topics')
  context={'form':form}
  return render(request,'learning_logs/new_topic.html',context)
@login_required
def new_entry(request,topic_id):
  print("ckp")
  """在特定主题中添加新条目"""
  topic=Topic.objects.get(id=topic_id)
  if request.method !='POST':
    form=EntryForm()
  else:
    form=EntryForm(data=request.POST)
    if form.is_valid():
      new_entry=form.save(commit=False)
      new_entry.topic=topic
      new_entry.save()
      # 提交后进行重定向并传一个topic_id参数
      return redirect('learning_logs:topic',topic_id=topic_id)
  context={'topic':topic,'form':form}
  # 返回对应的html页面
  return render(request,'learning_logs/new_entry.html',context)
@login_required
def edit_entry(request,entry_id):
  """编辑既有的条目"""
  entry=Entry.objects.get(id=entry_id)
  topic=entry.topic
  if topic.owner != request.user:
    raise Http404
  if request.method!='POST':
    form=EntryForm(instance=entry)
  else:
    form=EntryForm(instance=entry,data=request.POST)
    if form.is_valid():
      form.save()
      return redirect('learning_logs:topic',topic_id=topic.id)
  context={'entry':entry,'topic':topic,'form':form}
  return render(request,'learning_logs/edit_entry.html',context)
