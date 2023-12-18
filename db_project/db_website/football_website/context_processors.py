from django.db import connection

class LeagueData:
    def __init__(self,sid,name):
        self.id = sid
        self.name = name

def leagues(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id,name FROM league")
        rows = cursor.fetchall()
    leagues = [LeagueData(row[0],row[1]) for row in rows]
    return {'leagues': leagues}
