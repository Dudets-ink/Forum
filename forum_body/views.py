from django.shortcuts import render, redirect
from .models import Topic, Discuss, Messages
from .forms import MessageForm, EditForm, TopicAddForm, NewDiscussionForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Help functions

def check_user_ownership(request, place):
    """Compares user and place owner ids, if it different, raises a 404 error"""

    if place.owner.id != request.user.id:
        raise Http404

# Create your views here.

def index(request):
    """Renders homepage"""

    topics = Topic.objects.all()
    context = {'topics':topics}

    return render(request, 'forum_body/index.html', context)

def topic(request, topic_name):
    """Renders topic page"""
    
    topic = get_object_or_404(Topic, name=topic_name)
    discussions = topic.discuss_set.all()
    discussion = Discuss.objects.all()
    context = {
            'topic':topic, 'topic_name':topic.name, 'discussions':discussions,
            'discussion':discussion, 
            }

    return render(request, 'forum_body/topic.html', context)


def discussion(request, topic_name, discussion_id):
    """Renders discussion page and implements message creation form"""

    topic = get_object_or_404(Topic, name=topic_name)
    discussion = get_object_or_404(Discuss, id=discussion_id) 
    messages = discussion.messages_set.all()
    
    # message creation form
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
    """Renders message edit page"""

    topic = get_object_or_404(Topic, name=topic_name)
    discussion = get_object_or_404(Discuss, id=discussion_id)
    message = get_object_or_404(Messages, id=message_id)
    check_user_ownership(request, message)

    if request.method != 'POST':
        edit_form = EditForm(instance=message)
    else:
        edit_form = EditForm(instance=message, data=request.POST)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('forum_body:discussion',
                    topic_name=topic.name, discussion_id=discussion.id)
        
    context = {'discussion': discussion, 'message': message, 'form':edit_form, 'topic':topic}
    return render(request, 'forum_body/edit_message.html', context)

@login_required
def new_topic(request):
    """Renders message creation page"""
    
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
    """Renders discussion creation page"""

    topic = get_object_or_404(Topic, name=topic_name)

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
    """Deletes message from discussion page and db"""

    topic = get_object_or_404(Topic, id=topic_id)
    discussion = get_object_or_404(Discuss, id=discussion_id)
    message = get_object_or_404(Messages, id=message_id)
    check_user_ownership(request, message)
    
    message.delete()
    return redirect('forum_body:discussion', topic_name=topic.name, discussion_id=discussion.id)
