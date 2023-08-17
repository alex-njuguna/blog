from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
         views.post_detail, name='post_detail'),

    # share a post
    path('<int:post_id>/share/', views.post_share, name='post_share')
]