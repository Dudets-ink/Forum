from django.shortcuts import render, redirect
from .models import Topic, Discuss, Messages
from .forms import MessageForm, EditForm, TopicAddForm, NewDiscussionForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Secondary functions

def check_user_ownership(request, place):
    """Comparas user and place owner, if it different, raises a 404 error"""

    if place.owner != request.user.id:
        raise Http404

# Create your views here.

def index(request):
    """Создает главную страницу"""

    topics = Topic.objects.all()
    context = {'topics':topics}

    return render(request, 'forum_body/index.html', context)

def topic(request, topic_name):
    """Создает страницу выбора обсуждения"""
    
    topic = Topic.objects.get(name=topic_name)
    discussions = topic.discuss_set.all()
    discussion = Discuss.objects.all()
    context = {
            'topic':topic, 'topic_name':topic.name, 'discussions':discussions,
            'discussion':discussion, 
            }

    return render(request, 'forum_body/topic.html', context)


def discussion(request, topic_name, discussion_id):
    """Создает страницу обсуждения темы"""

    topic = Topic.objects.get(name=topic_name)
    discussion = Discuss.objects.get(id=discussion_id) 
    messages = discussion.messages_set.all()
    
    if request.method != 'POST':
        message_form = MessageForm()
    else:
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.topic = topic
            new_message.discuss = discussion
            new_message.save()
            return redirect('forum_body:discussion', topic_name=topic_name, discussion_id=discussion_id)

    context = {'topic':topic, 'discussion':discussion, 'messages':messages,
                'form':message_form}

    return render(request, 'forum_body/discussion.html', context)
    
@login_required
def message_edit(request, topic_name, discussion_id, message_id):
    """Редактирование сообщений темы"""

    topic = Topic.objects.get(name=topic_name)
    discussion = Discuss.objects.get(id=discussion_id)
    message = Messages.objects.get(id=message_id)
    check_user_ownership(request, message)

    if request.method != 'POST':
        edit_form = EditForm(instance=message)
    else:
        redacted_mark = 'redacted'
        edit_form = EditForm(instance=message, data=request.POST)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('forum_body:discussion',
                    topic_name=topic.name, discussion_id=discussion.id)
        
    context = {'discussion': discussion, 'message': message, 'form':edit_form, 'topic':topic}
    return render(request, 'forum_body/edit_message.html', context)

@login_required
def new_topic(request):
    """Добавлеяет тему"""
    
    if request.method != 'POST':
        topic_add_form = TopicAddForm()
    else:
        topic_add_form = TopicAddForm(data=request.POST)
        if topic_add_form.is_valid():
            topic_add_form.save()
            return redirect('forum_body:index')
    context = {'form': topic_add_form}
    return render(request, 'forum_body/add_topic.html', context)

@login_required
def new_discussion(request, topic_name):
    """Создает новое обсуждение темы"""

    topic = Topic.objects.get(name=topic_name)

    if request.method != 'POST':
        new_discussion_form = NewDiscussionForm()
    else:
        new_discussion_form = NewDiscussionForm(data=request.POST)
        if new_discussion_form.is_valid():
            new_form = new_discussion_form.save(commit=False)
            new_form.topic = topic
            new_form.save()
            return redirect('forum_body:topic', topic_name = topic_name)
    context = {'form':new_discussion_form, 'topic': topic}
    return render(request, 'forum_body/new_discussion.html', context)

def delete_message(request,topic_id, discussion_id, message_id):
    """Удаляет из базы данных запись"""

    topic = Topic.objects.get(id=topic_id)
    discussion = Discuss.objects.get(id=discussion_id)
    message = Messages.objects.get(id=message_id)
    check_user_ownership(request, message)
    
    message.delete()
    return redirect('forum_body:discussion', topic_name=topic.name, discussion_id=discussion.id)
