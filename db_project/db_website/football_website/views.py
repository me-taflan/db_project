from django.shortcuts import render
from django.db import connection
from collections import defaultdict
#from django.contrib.auth import login
#from django.contrib.auth import views as auth_views
from .forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .forms import LoginForm,SignUpForm
from django.contrib.auth import views as auth_views
#from django.contrib.auth.decorators import login_required
from django.urls import reverse


class MatchData:
    def __init__(self, match_id, date, season, stage,home_team_goal,away_team_goal, home_team_name, away_team_name,league_name):
        self.match_id = match_id
        self.date = date
        self.season = season
        self.stage = stage
        self.home_team_goal = home_team_goal
        self.away_team_goal = away_team_goal
        self.home_team_name = home_team_name
        self.away_team_name = away_team_name
        self.league_name = league_name

class PlayerData:
    def __init__(self,id,player_api_id,player_name,player_fifa_api_id,birthday,height,weight):
        self.id=id
        self.player_api_id=player_api_id
        self.player_name=player_name
        self.player_fifa_api_id=player_fifa_api_id
        self.birthday=birthday
        self.height=height
        self.weight=weight
class Player_info:
    def __init__(self,id,player_fifa_api_id,player_api_id,date,overall_rating,potential,preferred_foot,attacking_work_rate,defensive_work_rate,crossing,finishing,heading_accuracy,short_passing,volleys,dribbling,curve,free_kick_accuracy,long_passing,ball_control,acceleration,sprint_speed,agility,reactions,balance,shot_power,jumping,stamina,strength,long_shots,aggression,interceptions,positioning,vision,penalties,marking,standing_tackle,sliding_tackle,gk_diving,gk_handling,gk_kicking,gk_positioning,gk_reflexes):
        self.id=id
        self.player_fifa_api_id=player_fifa_api_id
        self.player_api_id=player_api_id
        self.date=date
        self.overall_rating=overall_rating
        self.potential=potential
        self.preferred_foot=preferred_foot
        self.attacking_work_rate=attacking_work_rate
        self.defensive_work_rate=defensive_work_rate
        self.crossing=crossing
        self.finishing=finishing
        self.heading_accuracy=heading_accuracy
        self.short_passing=short_passing
        self.volleys=volleys
        self.dribbling=dribbling
        self.curve=curve
        self.free_kick_accuracy=free_kick_accuracy
        self.long_passing=long_passing
        self.ball_control=ball_control
        self.acceleration=acceleration
        self.sprint_speed=sprint_speed
        self.agility=agility
        self.reactions=reactions
        self.balance=balance
        self.shot_power=shot_power
        self.jumping=jumping
        self.stamina=stamina
        self.strength=strength
        self.long_shots=long_shots
        self.aggression=aggression
        self.interceptions=interceptions
        self.positioning=positioning
        self.vision=vision
        self.penalties=penalties
        self.marking=marking
        self.standing_tackle=standing_tackle
        self.sliding_tackle=sliding_tackle
        self.gk_diving=gk_diving
        self.gk_handling=gk_handling
        self.gk_kicking=gk_kicking
        self.gk_positioning=gk_positioning
        self.gk_reflexes=gk_reflexes
        
        


def LoginView(request):
    matches_query = '''select m.id , m.date , m. season , m.stage ,m.home_team_goal,m.away_team_goal, t1.team_long_name , t2.team_long_name ,l.name
    from matches m join team t1 on m.home_team_api_id = t1.team_api_id 
    join team t2 on m.away_team_api_id = t2.team_api_id 
    join league l on l.id = m.league_id
    where day(current_date) = day(m.date) and month(current_date) = month(m.date);'''


    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM league")
        rows = cursor.fetchall()
        cursor.execute(matches_query)
        match_rows = cursor.fetchall()

    matches_by_league = {}
    for row in match_rows:
        match = MatchData(
            match_id=row[0],
            date=row[1],
            season=row[2],
            stage=row[3],
            home_team_goal=row[4],
            away_team_goal=row[5],
            home_team_name=row[6],
            away_team_name=row[7],
            league_name=row[8]
        )
        if row[8] not in matches_by_league:
            matches_by_league[row[8]] = []
        matches_by_league[row[8]].append(match) 
    print(type(matches_by_league))

    leagues = [row[0] for row in rows]
    login_checker=False
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            auth_query='''SELECT * FROM auth_user WHERE username = %s AND password =%s'''
            with connection.cursor() as cursor:
                cursor.execute(auth_query,([username],[password]))
                user=cursor.fetchone()
            if user is not None:
                login_checker=True
                return render(request,'football_website/main.html',{'leagues':leagues, 'matches_data':matches_by_league,'login_checker':login_checker, 'username':username})
            else:
                return redirect('football_website:login')
    else:
       # GET request or form is invalid
       form = LoginForm()
       return render(request, 'registration/login.html', {'form': form})
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password1']
            user_creation_query='''INSERT INTO auth_user (username, email, password,is_superuser,first_name,last_name,is_staff,is_active,date_joined)
            VALUES (%s, %s, %s,%s,'null','null',0,1,CURRENT_TIMESTAMP);
             '''
            with connection.cursor() as cursor:
                cursor.execute(user_creation_query,([username],[email],[password],[0]))
            
            return redirect('football_website:main_page')  # Replace 'home' with the desired redirect path after signup
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

#@login_required
def main_page(request):
    matches_query = '''select m.id , m.date , m. season , m.stage ,m.home_team_goal,m.away_team_goal, t1.team_long_name , t2.team_long_name ,l.name
    from matches m join team t1 on m.home_team_api_id = t1.team_api_id 
    join team t2 on m.away_team_api_id = t2.team_api_id 
    join league l on l.id = m.league_id
    where day(current_date) = day(m.date) and month(current_date) = month(m.date);'''


    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM league")
        rows = cursor.fetchall()
        cursor.execute(matches_query)
        match_rows = cursor.fetchall()

    matches_by_league = {}
    for row in match_rows:
        match = MatchData(
            match_id=row[0],
            date=row[1],
            season=row[2],
            stage=row[3],
            home_team_goal=row[4],
            away_team_goal=row[5],
            home_team_name=row[6],
            away_team_name=row[7],
            league_name=row[8]
        )
        if row[8] not in matches_by_league:
            matches_by_league[row[8]] = []
        matches_by_league[row[8]].append(match) 
    print(type(matches_by_league))

    leagues = [row[0] for row in rows]
    return render(request,'football_website/main.html',{'leagues':leagues, 'matches_data':matches_by_league})


#@login_required
def today_born_players():
    player_query='''select id,player_name,player_fifa_api_id,date(player.birthday) as birthday from player where
    day(current_date) = day(player.birthday) and month(current_date) = month(player.birthday); '''
    
    with connection.cursor() as cursor:
        cursor.execute(player_query)
        player_rows=cursor.fetchall()
    
    player_data=[]
    for row in player_rows:
        player = PlayerData(
            id=row[0],
            player_api_id=0,
            player_name=row[1],
            player_fifa_api_id=row[2],
            birthday=row[3],
            height=0,
            weight=0
        )
        player_data.append(player)
    return player_data
    
#@login_required
def search_players_by_name(name):
    with connection.cursor() as cursor:
        query = "SELECT * FROM player WHERE player_name LIKE %s"
        cursor.execute(query, ['%' + name + '%'])
        player_rows = cursor.fetchall()
        player_data=[]
    for row in player_rows:
        player = PlayerData(
            id=0,
            player_api_id=0,
            player_name=row[0],
            player_fifa_api_id=row[1],
            birthday=row[2],
            height=0,
            weight=0
        )
        player_data.append(player)
    return player_data

#@login_required
def player_page(request):
    if 'search' in request.GET:
        search_query = request.GET['search']
        players = search_players_by_name(search_query)
        return render(request, 'football_website/player_page.html', {'players': players, 'search_query': search_query})
    else:
        players = today_born_players()
        return render(request, 'football_website/player_page.html', {'players': players})
    
#@login_required
def player_info_page(request,player_id):
    with connection.cursor() as cursor:
        player_query='''SELECT pa.*
        FROM player_attributes pa
        JOIN player p ON pa.player_api_id = p.player_api_id
        WHERE p.id = %s;
         '''
        cursor.execute(player_query,[player_id])
        player_data=cursor.fetchall()
        new_query='''select upper(player_name) from player where id=%s;'''
        cursor.execute(new_query,[ player_id ])
        player_name=cursor.fetchone()
        
    player_info=[]
    for row in player_data:
        player_attr=Player_info(id=row[0],
                                player_fifa_api_id=row[1],
                                player_api_id=row[2],
                                date=row[3],
                                overall_rating=row[4],
                                potential=row[5],
                                preferred_foot=row[6],
                                attacking_work_rate=row[7],
                                defensive_work_rate=row[8],
                                crossing=row[9],
                                finishing=row[10],
                                heading_accuracy=row[11],
                                short_passing=row[12],
                                volleys=row[13],
                                dribbling=row[14],
                                curve=row[15],
                                free_kick_accuracy=row[16],
                                long_passing=row[17],
                                ball_control=row[18],
                                acceleration=row[19],
                                sprint_speed=row[20],
                                agility=row[21],
                                reactions=row[22],
                                balance=row[23],
                                shot_power=row[24],
                                jumping=row[25],
                                stamina=row[26],
                                strength=row[27],
                                long_shots=row[28],
                                aggression=row[29],
                                interceptions=row[30],
                                positioning=row[31],
                                vision=row[32],
                                penalties=row[33],
                                marking=row[34],
                                standing_tackle=row[35],
                                sliding_tackle=row[36],
                                gk_diving=row[37],
                                gk_handling=row[38],
                                gk_kicking=row[39],
                                gk_positioning=row[40],
                                gk_reflexes=row[41])
        player_info.append(player_attr)
    
    return render(request,'football_website/player_info.html',{'player_info':player_info,'player_name':player_name})

#@login_required
#def league_page(request,league_id):
    