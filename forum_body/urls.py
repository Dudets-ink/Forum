"""Код обьявлений urls для forum_body"""

from django.urls import path
from . import views

app_name = 'forum_body'
urlpatterns = [
        path('', views.index, name='index'), # homepage
        path('<str:topic_name>/', views.topic, name='topic'), # topic page
        path('<str:topic_name>/<int:discussion_id>/', views.discussion, name='discussion'), # topic discussion page
        path('edit/<str:topic_name>/<int:discussion_id>/<int:message_id>/', views.message_edit, name='message_edit'), # message edit page
        path('new_topic/>', views.new_topic, name='new_topic'), # topic creation page
        path('<str:topic_name>/new_discussion/', views.new_discussion, name='new_discussion'), # discussion creation page
        path('delete_message/<int:topic_id>/<int:discussion_id>/<int:message_id>', views.delete_message, name='delete_message'), # message delete function
        ]
