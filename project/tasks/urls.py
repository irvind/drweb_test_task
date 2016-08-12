from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^tasks$', views.TasksViewCreateView.as_view()),
    url(r'^reset$', views.ResetTasksView.as_view()),
]
