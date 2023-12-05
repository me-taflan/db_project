from django.shortcuts import render
from django.db import connection
from collections import defaultdict

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

    matches_by_league_2 = {
    'Premier League': "jksadhfjklsa",
    'La Liga': "kjasdfhadjsk",
    'La Liga': "kjasdfhadjsk",
    'La Liga': "kjasdfhadjsk",

}

    leagues = [row[0] for row in rows]
    return render(request,'football_website/main.html',{'leagues':leagues, 'matches_data':matches_by_league})


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


def player_page(request):
    if 'search' in request.GET:
        search_query = request.GET['search']
        players = search_players_by_name(search_query)
        return render(request, 'football_website/player_page.html', {'players': players, 'search_query': search_query})
    else:
        players = today_born_players()
        return render(request, 'football_website/player_page.html', {'players': players})
    
    
def player_info_page(request,player_id):
    with connection.cursor() as cursor:
        player_query='''SELECT pa.*
        FROM player_attributes pa
        JOIN player p ON pa.player_api_id = p.player_api_id
        WHERE p.id = %s;
         '''
        cursor.execute(player_query,[player_id])
        player_data=cursor.fetchall()
        
    
    player_info=Player_info(id=player_data[0][0],
                            player_fifa_api_id=player_data[0][1],
                            player_api_id=player_data[0][2],
                            date=player_data[0][3],
                            overall_rating=player_data[0][4],
                            potential=player_data[0][5],
                            preferred_foot=player_data[0][6],
                            attacking_work_rate=player_data[0][7],
                            defensive_work_rate=player_data[0][8],
                            crossing=player_data[0][9],
                            finishing=player_data[0][10],
                            heading_accuracy=player_data[0][11],
                            short_passing=player_data[0][12],
                            volleys=player_data[0][13],
                            dribbling=player_data[0][14],
                            curve=player_data[0][15],
                            free_kick_accuracy=player_data[0][16],
                            long_passing=player_data[0][17],
                            ball_control=player_data[0][18],
                            acceleration=player_data[0][19],
                            sprint_speed=player_data[0][20],
                            agility=player_data[0][21],
                            reactions=player_data[0][22],
                            balance=player_data[0][23],
                            shot_power=player_data[0][24],
                            jumping=player_data[0][25],
                            stamina=player_data[0][26],
                            strength=player_data[0][27],
                            long_shots=player_data[0][28],
                            aggression=player_data[0][29],
                            interceptions=player_data[0][30],
                            positioning=player_data[0][31],
                            vision=player_data[0][32],
                            penalties=player_data[0][33],
                            marking=player_data[0][34],
                            standing_tackle=player_data[0][35],
                            sliding_tackle=player_data[0][36],
                            gk_diving=player_data[0][37],
                            gk_handling=player_data[0][38],
                            gk_kicking=player_data[0][39],
                            gk_positioning=player_data[0][40],
                            gk_reflexes=player_data[0][41])
    print (player_info)
    return render(request,'football_website/player_info.html',{'player_info':player_info})