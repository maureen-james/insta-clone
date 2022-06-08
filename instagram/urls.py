# from . import views
# from django.urls import path



# urlpatterns=[
#     path('',views.welcome,name = 'welcome'),
# ]

from django.urls import path, re_path as url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    path('',views.welcome,name = 'welcome'),
    path('accounts/profile/',views.profile,name = 'profile'),
    path('profile/',views.other_profile,name = 'visitprofile'),
    path('search/profile', views.search, name='profileresults'),
    path('timeline', views.timeline, name='timeline'),
    path('user/', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit'),
    path('post/<post_id>/like',views.like_post,name='likepost'),
    path('post/<post_id>/comment',views.single_comment,name='comment'),
    path('profile/<str:username>/followers/', views.
        FollowerListView.as_view(), name='follower-list'),
    path('profile/<str:username>/following/', views.
        FollowerListView.as_view(), name='following-list'),


    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    