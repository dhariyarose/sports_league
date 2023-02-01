import imp
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView, TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Game
from django.contrib import messages
from django.urls import reverse
from .forms import GameForm, GameUpdateForm
import csv
import codecs 
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime

class Error404View(TemplateView):
    template_name = "404.html"

class Error500View(TemplateView):
    template_name = "500.html"

class Home(View):
    """ 
    Redirects to dashboard if user is logged in.
    Or redirect to login page
    """
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/sports_league/dashboard/')


@method_decorator(login_required, name='dispatch')
class Dashboard(View):
    """
    Dashboard view
    """
    template_name = 'dashboard.html'

    def get(self,request):
        game_count = Game.objects.all().count() # To show the total number of games on the dashboard
        return render(request, self.template_name, {'game_count':game_count})


@method_decorator(login_required, name='dispatch')
class GamesList(ListView):
    """
    Lists all games
    """
    model = Game
    template_name = 'games_list.html'
    context_object_name = 'games'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(GamesList, self).get_context_data(**kwargs)
        games = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(games, self.paginate_by)
        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            games = paginator.page(1)
        except EmptyPage:
            games = paginator.page(paginator.num_pages)
        context['games'] = games
        return context


@method_decorator(login_required, name='dispatch')
class GameNew(View):
    """
    To add new game
    """
    def post(self,request):
        form = GameForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            messages.success(request,"Game {0} added successfully".format(obj.name))
        return HttpResponseRedirect('/sports_league/games-list/') 


@method_decorator(login_required, name='dispatch')
class GameDelete(DeleteView):
    """
    To delete a game using its ID.
    """
    def post(self, request, *args, **kwargs):
        id = self.request.POST['game_id']
        obj = Game.objects.get(pk=id)
        name = obj.name
        obj.delete()
        messages.success(request,"Game {0} deleted successfully".format(name))
        return HttpResponseRedirect('/sports_league/games-list/') 


@method_decorator(login_required, name='dispatch')
class GameEdit(View):
    """
    To delete a game using its slug.
    """
    template_name = 'game_edit.html'

    def get(self, request, slug):
        game = Game.objects.get(slug=slug)
        return render(request, self.template_name, {'game':game})
    
    def post(self, request, slug):
        game = Game.objects.get(slug=slug)
        form = GameUpdateForm(request.POST, instance = game)
        if form.is_valid():
            obj = form.save()
            obj.updated_by = request.user
            obj.save()
            messages.success(request,"Game {0} updated successfully".format(obj.name))
            return HttpResponseRedirect('/sports_league/games-list/') 
        return render(request, self.template_name, {'game':game})

    
@method_decorator(login_required, name='dispatch')
class RankingTable(View):
    """
    Redirects to ranking table form
    """
    template_name = 'ranking_table.html'

    def get(self,request):
        return render(request, self.template_name, {})
        
    
@method_decorator(login_required, name='dispatch')
class CSVFileUpload(View):
    """
    Prepare ranking list based on uploaded data.
    """
    template_name = 'ranking_table.html'

    def get(self,request):
        return render(request, self.template_name, {})
        
    def post(self,request):
        try:
            csv_file = request.FILES["file"]

            if not csv_file.name.endswith('.csv'): # Checks whether the uploaded file is in csv format or not
                messages.error(request,'File is not CSV type')
                return render(request, self.template_name, {})

            if csv_file.multiple_chunks():#if file is too large, return
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return render(request, self.template_name, {})
            
            #codecs: to push the error away from your system, will decode your required file while allowing you to specify its encoding type
            read = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
            team_and_score = {}
            for row in read:
                row[1] = int(row[1]) # as per sample document, team_1 name row[0], team_1 score row[1], team_2 name row[2], team_2 score  row[3]
                row[3] = int(row[3])

                if row[0] not in team_and_score.keys(): #Checks whether team 1 is in the team_and_score or not
                    team_and_score[row[0]] = 0 
                if row[2] not in team_and_score.keys(): #Checks whether team 2 is in the team_and_score or not
                    team_and_score[row[2]] = 0

                if row[1] > row[3]: #Checks if team1's score is greater than team2's score
                    team = row[0]
                    score = 3
                    team_and_score[team] += score

                elif row[1] == row[3]: #Check if both teams are tied
                    team1 = row[0]
                    team2 = row[2]
                    score = 1

                    for team in [team1, team2]:
                        team_and_score[team] += score
                
                elif row[1] < row[3]: #Checks if team2's score is greater than team1's score
                    team = row[2]
                    score = 3
                    team_and_score[team] += score
                

            team_and_score = dict(sorted(team_and_score.items(), key=lambda x:x[0])) # sorting by alphabetical order
            team_and_score = dict(sorted(team_and_score.items(), key=lambda x:x[1], reverse=True))# sorting by points order

            # Create csv file to view ranking table
            current_datetime=datetime.datetime.now()
            str_date = current_datetime.strftime("%d-%m-%Y:%H:%M:%S")
            ranking_table_csv_file = settings.MEDIA_ROOT +'ranking_table-'+str(str_date)+'.csv'
            with open(ranking_table_csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Ranking", "Team", "Points"])
                count = 1
                for team in team_and_score:
                    writer.writerow([count, team, team_and_score[team]])
                    count += 1

            # Create pdf file to view ranking table
            template_path = 'generate_pdf.html'
            context = {'team_and_score':team_and_score}
            file = open(settings.MEDIA_ROOT  + 'ranking_table-'+str(str_date)+'.pdf', "w+b")

            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)

            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=file)

            # if error then show some funy view
            if pisa_status.err:
                pass
                
            return render(request, self.template_name, {'team_and_score':team_and_score,'csv_file':settings.MEDIA_URL+'ranking_table-'+str(str_date)+'.csv',\
                'pdf_file':settings.MEDIA_URL+'ranking_table-'+str(str_date)+'.pdf'})


        except Exception as e:
            print(e)
            messages.error(request,"Something went wrong!")
        return render(request, self.template_name, {})
        