from django.shortcuts import render
from django.db import connection
from collections import defaultdict

class MatchData:
    def __init__(self, match_id, date, season, stage,home_team_goal,away_team_goal, home_team_name, away_team_name,league_name=None,home_id=None,away_id=None,):
        self.match_id = match_id
        self.date = date
        self.season = season
        self.stage = stage
        self.home_team_goal = home_team_goal
        self.away_team_goal = away_team_goal
        self.home_team_name = home_team_name
        self.away_team_name = away_team_name
        self.league_name = league_name
        self.home_id = home_id
        self.away_id = away_id


class LeagueData:
    def __init__(self,sid,name):
        self.id = sid
        self.name = name

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
    matches_query = '''SELECT m.id , m.date , m. season , m.stage ,m.home_team_goal,m.away_team_goal, t1.team_long_name , t2.team_long_name ,l.name, t1.team_api_id, t2.team_api_id, m.league_id FROM matches m join team t1 on m.home_team_api_id = t1.team_api_id JOIN team t2 on m.away_team_api_id = t2.team_api_id 
    JOIN league l on l.id = m.league_id
    WHERE day(current_date) = day(m.date) AND month(current_date) = month(m.date);'''


    with connection.cursor() as cursor:
        cursor.execute("SELECT id,name FROM league")
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
            league_name=row[8],
            home_id=row[9],
            away_id=row[10]
        )
        if row[8] not in matches_by_league:
            matches_by_league[row[8]] = []
        matches_by_league[row[8]].append(match) 

    leagues = [LeagueData(row[0],row[1]) for row in rows]
    return render(request,'football_website/main.html',{ 'matches_data':matches_by_league})



class MatchDetails:
    def __init__(self, data):
        self.id = data.get('id')
        self.country_name = data.get('country_name')
        self.league_name = data.get('league_name')
        self.season = data.get('season')
        self.stage = data.get('stage')
        self.date = data.get('date')
        self.match_api_id = data.get('match_api_id')
        self.home_name = data.get('home_name')
        self.away_name = data.get('away_name')
        self.home_team_goal = data.get('home_team_goal')
        self.away_team_goal = data.get('away_team_goal')

        self.home_team_players = [
            data.get(f'home_player_{i}_name') for i in range(1, 12)
        ]
        self.away_team_players = [
            data.get(f'away_player_{i}_name') for i in range(1, 12)
        ]

        self.b365h = data.get('B365H')
        self.b365d = data.get('B365D')
        self.b365a = data.get('B365A')
        self.bwh = data.get('BWH')
        self.bwd = data.get('BWD')
        self.bwa = data.get('BWA')
        self.iwh = data.get('IWH')
        self.iwd = data.get('IWD')
        self.iwa = data.get('IWA')
        self.lbh = data.get('LBH')
        self.lbd = data.get('LBD')
        self.lba = data.get('LBA')
        self.psh = data.get('PSH')
        self.psd = data.get('PSD')
        self.psa = data.get('PSA')
        self.whh = data.get('WHH')
        self.whd = data.get('WHD')
        self.wha = data.get('WHA')
        self.sjh = data.get('SJH')
        self.sjd = data.get('SJD')
        self.sja = data.get('SJA')
        self.vch = data.get('VCH')
        self.vcd = data.get('VCD')
        self.vca = data.get('VCA')
        self.gbh = data.get('GBH')
        self.gbd = data.get('GBD')
        self.gba = data.get('GBA')
        self.bsh = data.get('BSH')
        self.bsd = data.get('BSD')
        self.bsa = data.get('BSA')  
        



def match_page(request,match_id):
    player_columns_home = [f'home_player_{i}' for i in range(1, 12)]
    player_columns_away = [f'away_player_{i}' for i in range(1, 12)]

    player_joins_home = ' '.join([f'LEFT JOIN player h_p_{i} ON h_p_{i}.player_api_id = matches.{col}' for i,col in enumerate(player_columns_home,1)])
    player_joins_away = ' '.join([f'LEFT JOIN player a_p_{i} ON a_p_{i}.player_api_id = matches.{col}' for i,col in enumerate(player_columns_away,1)])
    
    # this query sucks ???? optimization ????
    match_query = f'SELECT matches.id, matches.country_id, matches.league_id, matches.season, matches.stage,matches.date,matches.home_team_api_id, matches.away_team_api_id, matches.home_team_goal, matches.away_team_goal,matches.B365H, matches.B365D, matches.B365A,matches.BWH, matches.BWD, matches.BWA,matches.IWH, matches.IWD, matches.IWA,matches.LBH, matches.LBD, matches.LBA,matches.PSH, matches.PSD, matches.PSA,matches.WHH, matches.WHD,matches.WHA,matches.SJH, matches.SJD, matches.SJA,matches.VCH, matches.VCD, matches.VCA,matches.GBH, matches.GBD, matches.GBA,matches.BSH, matches.BSD, matches.BSA,country.name as country_name, league.name as league_name, ' \
    f't.team_long_name as home_name, t2.team_long_name as away_name, ' \
    f'{", ".join([f"h_p_{i}.player_name as {col}_name" for i, col in enumerate(player_columns_home, 1)])}, ' \
    f'{", ".join([f"a_p_{i}.player_name as {col}_name" for i, col in enumerate(player_columns_away, 1)])} ' \
    f'FROM matches ' \
    f'INNER JOIN country ON matches.country_id = country.id ' \
    f'INNER JOIN league ON matches.league_id = league.id ' \
    f'INNER JOIN team t ON matches.home_team_api_id = t.team_api_id ' \
    f'INNER JOIN team t2 ON matches.away_team_api_id = t2.team_api_id ' \
    f'{player_joins_home} ' \
    f'{player_joins_away} ' \
    f'WHERE matches.id = {match_id}'


    with connection.cursor() as cursor:
        cursor.execute(match_query)
        match_data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

    match_dict = dict(zip(column_names, match_data[0]))
    match_details = MatchDetails(match_dict)

    return render(request,'football_website/match.html',{'match_details':match_details})


class Team:
    def __init__(self,sid,name,wins,draws,losses,points,avg_points,goals_scored,goals_conceded):
        self.id = sid
        self.name = name
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.points = points
        self.avg_points = avg_points
        self.goals_scored = goals_scored
        self.goals_conceded = goals_conceded
        


# Get all teams in that league and also show their participation date also get some statistics for that league
def league_page(request,league_id):
    query = 'SELECT home.team_api_id , home.team_long_name , COALESCE(home.wins, 0) + COALESCE(away.wins, 0) AS total_wins, ' \
    'COALESCE (home.draws, 0) + COALESCE(away.draws, 0) AS total_draws ,' \
    'COALESCE(home.losses, 0) + COALESCE(away.losses, 0) AS total_losses ,  '\
    '(COALESCE(home.wins, 0)+COALESCE(away.wins, 0))*3+COALESCE(home.draws,0)+COALESCE(away.draws, 0) AS total_points, ' \
    '((COALESCE(home.wins, 0)+COALESCE(away.wins, 0))*3+COALESCE(home.draws,0)+COALESCE(away.draws, 0)) /  ' \
    '(COALESCE(home.wins, 0) + COALESCE(away.wins, 0) + COALESCE(home.draws, 0) + COALESCE(away.draws, 0) + '\
    'COALESCE(home.losses, 0) + COALESCE(away.losses, 0)) AS avg_points, ' \
    'COALESCE(home.goals_scored, 0) + COALESCE(away.goals_scored, 0) AS goals_scored, ' \
    'COALESCE(home.goals_conceded, 0) + COALESCE(away.goals_conceded, 0) AS goals_conceded ' \
    'FROM ( SELECT DISTINCT t.team_long_name , t.team_api_id, '\
    'Count( CASE WHEN matches.home_team_goal > matches.away_team_goal THEN 1 ELSE NULL END ) AS wins,' \
    'Count( CASE WHEN matches.home_team_goal = matches.away_team_goal THEN 1 ELSE NULL END) AS draws, '\
    'Count( CASE WHEN matches.home_team_goal < matches.away_team_goal THEN 1 ELSE NULL END) AS losses, '\
    'SUM(matches.home_team_goal) AS goals_scored, ' \
    'SUM(matches.away_team_goal) AS goals_conceded ' \
    'FROM matches LEFT JOIN team t ON t.team_api_id = matches.home_team_api_id  '\
    f'WHERE matches.league_id = {league_id} GROUP BY team_api_id) AS home ' \
    'LEFT JOIN (SELECT DISTINCT t2.team_long_name ,t2.team_api_id , ' \
    'COUNT( CASE WHEN matches.home_team_goal < matches.away_team_goal THEN 1 ELSE NULL END ) AS wins, ' \
    'COUNT( CASE WHEN matches.home_team_goal = matches.away_team_goal THEN 1 ELSE NULL END ) AS draws, ' \
    'COUNT( CASE WHEN matches.home_team_goal > matches.away_team_goal THEN 1 ELSE NULL END ) AS losses, ' \
    'SUM(matches.away_team_goal) AS goals_scored, ' \
    'SUM(matches.home_team_goal) AS goals_conceded ' \
    'FROM matches LEFT JOIN team t2 ON t2.team_api_id  = matches.away_team_api_id  ' \
    f'WHERE matches.league_id = {league_id} GROUP BY team_api_id ) AS away ON home.team_api_id = away.team_api_id  ORDER BY avg_points DESC;'


    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.execute(f'SELECT league.id,league.name,country.name FROM league JOIN country on country.id = league.country_id WHERE league.id={league_id} ')
        rows2 = cursor.fetchall()


    teams = [Team(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])for row in rows]
    return render(request,'football_website/league.html',{'teams':teams, 'league':LeagueData(rows2[0][0],rows2[0][1]) , 'country_name':rows2[0][2]})



def team_page(request,team_id):
    # Get all matches and extract some stats for the current team
    query = f'''SELECT m.id , m.date , m. season , m.stage ,m.home_team_goal, m.away_team_goal, t1.team_long_name , t2.team_long_name FROM matches m JOIN team t1 ON m.home_team_api_id = t1.team_api_id JOIN team t2 ON m.away_team_api_id = t2.team_api_id  WHERE m.home_team_api_id = {team_id} OR m.away_team_api_id = {team_id};'''
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    print(rows)
    matches = []
    for row in rows:
        match = MatchData(
            match_id=row[0],
            date=row[1],
            season=row[2],
            stage=row[3],
            home_team_goal=row[4],
            away_team_goal=row[5],
            home_team_name=row[6],
            away_team_name=row[7],)
        matches.append(match)    
    return render(request,'football_website/team.html',{'matches':matches})

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