"""Код обьявлений urls для forum_body"""

from django.urls import path
from . import views

app_name = 'forum_body'
urlpatterns = [
        path('', views.index, name='index'), #главная страница
        path('<str:topic_name>/', views.topic, name='topic'), #страница обсуждения темы
        path('<str:topic_name>/<int:discussion_id>/', views.discussion, name='discussion'),
        path('<str:topic_name>/<int:discussion_id>/<int:message_id>/edit/', views.message_edit, name='message_edit'),
        path('new_topic/>', views.new_topic, name='new_topic'),
        path('<str:topic_name>/new_discussion/', views.new_discussion, name='new_discussion'),
        path('delete_message/<int:topic_id>/<int:discussion_id>/<int:message_id>', views.delete_message, name='delete_message'),
        ]
