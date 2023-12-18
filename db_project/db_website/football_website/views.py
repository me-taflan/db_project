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
