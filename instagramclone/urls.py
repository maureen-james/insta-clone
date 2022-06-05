"""instagramclone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import include, path

# from instagram import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',include('instagram.urls')),
#     path('accounts/profile/',views.profile,name = 'profile'),
#     # url(r'^profile/(\d+)',views.other_profile,name = 'visitprofile'),
#     # url(r'^search/profile$', views.search, name='profileresults'),
#     # url(r'^timeline$', views.timeline, name='timeline'),
#     # url(r'^edit_profile$', views.edit_profile, name='edit'),

# ]


from django.urls import re_path as url,include
from django.contrib.auth import views 
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'',include('instagram.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    # url(r'^logout/$', views.logout, {"next_page": '/'}),
    url( r'^login/$',auth_views.LoginView.as_view(template_name="useraccounts/login.html"), name="login"),
    
]


