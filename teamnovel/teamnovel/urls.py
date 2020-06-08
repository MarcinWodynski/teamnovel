"""teamnovel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from novels import views as core_views
from django.contrib.auth import views as auth_views
from novels.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'novels/login.html'}, name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    path('', HomepageView.as_view()),
    path('info/', InfoView.as_view(), name='info'),
    path('rejestracja/', core_views.SignupView, name='signup'),
    path('nowy_team/', CreateTeamView.as_view(), name='new_team'),
    path('moje_zespoly/', UserTeamsView.as_view(), name='user_teams'),
    path('moje_zespoly/<int:team_id>', TeamView.as_view(), name='team_view'),
    path('dodaj_czlonka_zespolu/<int:team_id>/<int:user_id>', AddMemberView.as_view(), name='add_member'),
    path('usun_z_zespolu/<int:team_id>/<int:user_id>', DeleteMemberView.as_view(), name='delete_member'),
    path('nowe_opowiadanie/<int:team_id>/<int:user_id>', CreateNovel.as_view(), name='new_novel'),
    path('opowiadanie/<int:novel_id>', NovelView.as_view(), name='novel'),
    path('opuszczenie_kolejki/<int:novel_id>', SkipTurnView.as_view(), name='skip_turn'),
    path('edycja_opowiadania/<int:novel_id>', EditNovel.as_view(), name='edit_novel'),
    path('publikacja_opowiadania/<int:novel_id>', PublishNovelView.as_view(), name='publish_novel'),
    path('opublikowane_opowiadania/', PublishedNovelsListView.as_view(), name='published_novels'),
    path('opublikowane_opowiadania/<int:published_novel_id>', PublishedNovelView.as_view(), name='published'),
    path('opublikowane_opowiadania/polub/<int:published_novel_id>', RateNovelView.as_view(), name='rate_novel')
]
