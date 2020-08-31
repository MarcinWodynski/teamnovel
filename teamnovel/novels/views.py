from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from novels.models import Team, Novel, PublishedNovel, UserCommentNovels
from .forms import *
import random
# Create your views here.


class HomepageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            current_novels = Novel.objects.filter(current_turn=request.user)
            ctx = {'current_novels': current_novels}
            return render(request, "base.html", ctx)
        else:
            return render(request, "base.html")



def SignupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class CreateTeamView(View):
    def get(self, request):
        form = CreateTeamForm
        ctx = {'form': form}
        return render(request, 'create_team.html', ctx)

    def post(self, request):
        form = CreateTeamForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                new_team = Team()
                new_team.team_name = form.cleaned_data['team_name']
                new_team.group_leader = request.user
                new_team.save()
                return redirect('/moje_zespoly')
            else:
                ctx = {'form': form}
                return render(request, 'create_team.html', ctx)
        else:
            return redirect('/login')


class UserTeamsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            team_owned_list = Team.objects.filter(group_leader_id = request.user.id)
            user_included_in = Team.objects.filter(team_users=request.user)
            ctx = {'team_owned_list': team_owned_list, 'user_teams': user_included_in}
            return render(request, 'user_teams.html', ctx)


class TeamView(View):
    def get(self, request, team_id):
        if request.user.is_authenticated:
            team_id = team_id
            team = Team.objects.get(id= team_id)
            members = team.team_users.all()
            novels = Novel.objects.filter(team=team)
            ctx = {'team': team, 'members': members, 'novels': novels}
            if request.user == team.group_leader:
                form = MemberSearchForm()
                ctx['form'] = form
        return render(request, 'team_view.html', ctx)

    def post(self, request, team_id):
        form = MemberSearchForm(request.POST)
        team_id = team_id
        team = Team.objects.get(id=team_id)
        if form.is_valid():
            users = User.objects.filter(username__icontains=form.cleaned_data['team_users'])
            print(users)
            ctx = {'users': users, 'form': form, 'team': team}
            return render(request, 'team_view.html', ctx)


class AddMemberView(View):
    def get(self, request, team_id, user_id):
        team = Team.objects.get(id=team_id)
        if request.user.is_authenticated:
            if request.user == team.group_leader:
                user = User.objects.get(id=user_id)
                if user != team.group_leader:
                    team.team_users.add(user)
                else:
                    raise Http404
                return redirect('/moje_zespoly/{}'.format(team_id))
            else:
                raise Http404
        else:
            return redirect('/login')


class DeleteMemberView(View):
    def get(self,request, team_id, user_id):
        team = Team.objects.get(id=team_id)
        deleted_user = User.objects.get(id=user_id)
        novels = Novel.objects.filter(team_id=team.id)
        for novel in novels:
            if novel.current_turn == deleted_user:
                message = "Nie możesz usunąć użytkownika, który jest w turze dopisywania fragmentu opowiadania"
                team_id = team_id
                team = Team.objects.get(id=team_id)
                members = team.team_users.all()
                novels = Novel.objects.filter(team=team)
                ctx = {'team': team, 'members': members, 'novels': novels, 'message': message}
                if request.user == team.group_leader:
                    form = MemberSearchForm()
                    ctx['form'] = form
                return render(request, 'team_view.html', ctx)
            else:
                if request.user.is_authenticated:
                    if request.user == team.group_leader:
                        team.team_users.remove(deleted_user)
                        return redirect('/moje_zespoly/{}'.format(team_id))
                    else:
                        raise Http404
                else:
                    return redirect('/login')


class CreateNovel(View):
    def get(self, request, team_id, user_id):
        user = User.objects.get(pk=user_id)
        if user.is_authenticated:
            team = Team.objects.get(pk=team_id)
            if user == team.group_leader:
                form = CreateNovelForm()
                ctx = {'form': form}
                return render(request, 'create_novel.html', ctx)
            else:
                raise Http404
        else:
            redirect('/login')
    def post(self, request, team_id, user_id):
        form = CreateNovelForm(request.POST)
        if form.is_valid():
            team = Team.objects.get(pk=team_id)
            teammates = team.team_users.all()
            number_of_members = len(teammates) + 1
            if number_of_members > 2:
                new_novel = Novel()
                new_novel.team = team
                new_novel.team_leader = team.group_leader
                new_novel.title = form.cleaned_data['title']
                new_novel.content = form.cleaned_data['content']
                new_novel.last_turn = team.group_leader
                members = team.team_users.all()
                team_member_list = []
                for member in members:
                    team_member_list.append(member)
                new_novel.current_turn = team_member_list[0]
                new_novel.save()
                return redirect('/opowiadanie/{}'.format(new_novel.pk))
            else:
                user = User.objects.get(pk=user_id)
                if user.is_authenticated:
                    team = Team.objects.get(pk=team_id)
                    if user == team.group_leader:
                        form = CreateNovelForm()
                        message = "Za mało osób w zespole, by stworzyć opowiadanie"
                        ctx = {'form': form, 'message': message}
                        return render(request, 'create_novel.html', ctx)
class NovelView(View):
    def get(self, request, novel_id):
        novel = Novel.objects.get(pk=novel_id)
        form = UpdateNovelForm
        ctx = {'novel': novel, 'form': form}
        return render(request, 'novel_view.html', ctx)
    def post(self, request, novel_id):
        novel = Novel.objects.get(pk=novel_id)                             # pobieram obiekt opowiadania
        last_user = novel.last_turn
        novel.previous_turn = last_user
        form = UpdateNovelForm(request.POST)
        def random_user(team_size):                                        # funkcja, która losuje kolejnego usera
            next_turn = random.randint(0, team_size)
            return next_turn
        if form.is_valid():
            team = novel.team
            members = team.team_users.all()
            team_member_list = []
            for member in members:
                team_member_list.append(member)
            team_member_list.append(team.group_leader)
            team_size = len(team_member_list) - 1
            if team_size > 3:
                added_content = form.cleaned_data['added_content']             # nowy fragment przesłany przez formularz
                current_content = novel.content                                # obecna część opowiadania
                new_content = str(current_content) + " " + str(added_content)  # połączenie obecnego opowiadania z dodanym fragmentem
                novel.content = new_content                                    # przekazanie do obiektu
                novel.last_turn = request.user
                                      # zmienna z liczbą członków grupy do losowania
                next_user = team_member_list[random_user(team_size)]
                while novel.current_turn == next_user or novel.last_turn == next_user or novel.previous_turn == next_user: # sprawdzenie, czy użytkownik, który własnie dopisał fragment nie został wybrany ponownie
                    next_user = team_member_list[random_user(team_size)]
                else:
                    novel.current_turn = next_user                         # przekazanie kolejki kolejnemu userowi
                    novel.save()
                    return redirect('/opowiadanie/{}'.format(novel.pk))
            else:
                added_content = form.cleaned_data['added_content']  # nowy fragment przesłany przez formularz
                current_content = novel.content  # obecna część opowiadania
                new_content = str(current_content) + " " + str(
                    added_content)  # połączenie obecnego opowiadania z dodanym fragmentem
                novel.content = new_content  # przekazanie do obiektu
                novel.last_turn = request.user
                members = team.team_users.all()
                team_member_list = []
                for member in members:
                    team_member_list.append(member)
                team_member_list.append(team.group_leader)
                team_size = len(team_member_list) - 1  # zmienna z liczbą członków grupy do losowania
                next_user = team_member_list[random_user(team_size)]
                while novel.current_turn == next_user or novel.last_turn == next_user: # sprawdzenie, czy użytkownik, który własnie dopisał fragment nie został wybrany ponownie
                    next_user = team_member_list[random_user(team_size)]
                else:
                    novel.current_turn = next_user
                    novel.save()
                    return redirect('/opowiadanie/{}'.format(novel.pk))


class SkipTurnView(View):
    def get(self, request, novel_id):
        novel = Novel.objects.get(pk=novel_id)
        all_members = []
        team = novel.team
        regular_members = team.team_users.all()
        leader = novel.team_leader
        for member in regular_members:
            all_members.append(member)
        all_members.append(leader)
        if request.user != novel.team_leader:
            all_members.remove(request.user)
        form = SkipTurnForm(all_members)
        if request.user.is_authenticated:
            if request.user == novel.current_turn or novel.team_leader:
                ctx = {'form': form}
                return render(request, "skip_turn.html", ctx)
            else:
                raise Http404
        else:
            redirect('/login')

    def post(self, request, novel_id):
        novel = Novel.objects.get(pk=novel_id)
        all_members = []
        team = novel.team
        regular_members = team.team_users.all()
        leader = novel.team_leader
        for member in regular_members:
            all_members.append(member)
        all_members.append(leader)
        if request.user != novel.team_leader:
            all_members.remove(request.user)
        form = SkipTurnForm(all_members, request.POST)
        if form.is_valid():
            form_user = form.cleaned_data['current_user']
            print(form_user)
            new_user = User.objects.get(id=form_user)
            novel.current_turn = new_user
            novel.save()
            return redirect('/opowiadanie/{}'.format(novel_id))
        else:
            ctx = {'form': form}
            return render(request, "skip_turn.html", ctx)


class EditNovel(View):
    def get(self, request, novel_id):
        novel = Novel.objects.get(id=novel_id)
        form = EditNovelForm()
        form.fields['content'].initial = novel.content
        ctx = {'novel': novel, 'form': form}
        return render(request, 'edit_novel.html', ctx)
    def post(self, request, novel_id):
        novel = Novel.objects.get(id=novel_id)
        if request.user.is_authenticated:
            if request.user == novel.team_leader:
                new_content = request.POST.get('content')
                novel.content = new_content
                novel.save()
                return redirect('/opowiadanie/{}'.format(novel_id))
            else:
                return Http404
        else:
            return redirect('/login')



class PublishNovelView(View):
    def get(self, request, novel_id):
        if request.user.is_authenticated:
            novel = Novel.objects.get(id=novel_id)
            if request.user == novel.team_leader:
                form = PublishNovelForm()
                form.fields['content'].initial = novel.content
                ctx = {'form': form}
                return render(request, 'publish_form.html', ctx)
            else:
                return redirect('/opowiadanie/{}'.format(novel_id))
        else:
            return redirect('/login')

    def post(self, request, novel_id):
            novel = Novel.objects.get(id=novel_id)
            if request.user == novel.team_leader:
                to_publish = PublishedNovel()
                to_publish.team_name = novel.team.team_name
                print(to_publish.team_name)
                to_publish.title = novel.title
                to_publish.content = novel.content
                to_publish.save()
                novel.delete()
                return redirect('/opublikowane_opowiadania/{}'.format(to_publish.id))


class PublishedNovelsListView(View):
    def get(self, request):
        published_novels = PublishedNovel.objects.all()
        ctx = {'published_novels': published_novels }
        return render(request, 'published_novels_list.html', ctx)


class PublishedNovelView(View):
    def get(self, request, published_novel_id):
        published_novel = PublishedNovel.objects.get(id=published_novel_id)
        comments = UserCommentNovels.objects.filter(PublishedNovel=published_novel)
        ratings = published_novel.user_ratings.all()
        likes = len(ratings)
        if request.user.is_authenticated:
            comment_form = CommentPublishedNovelForm()
        else:
            comment_form = None
        ctx = {'published_novel': published_novel, 'likes': likes, 'comment_form': comment_form, 'comments': comments}
        return render(request, 'published_novel_view.html', ctx)
    def post(self,request,published_novel_id):
        published_novel = PublishedNovel.objects.get(id=published_novel_id)
        comment_form = CommentPublishedNovelForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.cleaned_data['comment']
            novel_comment = UserCommentNovels.objects.create(User=request.user, PublishedNovel=published_novel, Comment=new_comment)
            novel_comment.save()
            return redirect ('/opublikowane_opowiadania/{}'.format(published_novel.id))
        else:
            return redirect ('/opublikowane_opowiadania/{}'.format(published_novel.id))


class RateNovelView(View):
    def get(self, request, published_novel_id):
        published_novel = PublishedNovel.objects.get(id=published_novel_id)
        if published_novel.user_ratings.filter(id=request.user.id).exists():
            published_novel.user_ratings.remove(request.user)
        else:
            published_novel.user_ratings.add(request.user)
        return redirect('/opublikowane_opowiadania/{}'.format(published_novel.id))



class InfoView(View):
    def get(self, request):
        return render(request, 'info_view.html')


