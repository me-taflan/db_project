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
        matches_by_league[row[8]].append(match)
    for league_name, matches in matches_by_league.items():
        print(league_name)
        for match in matches:
            print(match)


    leagues = [row[0] for row in rows]
    return render(request,'football_website/main.html',{'leagues':leagues, 'matches_data':matches_by_league})
