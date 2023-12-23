from django.db import connection

class UserFavoritesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
         
    
    def __call__(self, request):
            log_checker = False
            if 'username' in request.session:
                print(True)
                log_checker = True
                request.login_checker = True
                request.username = request.session.get('username')
            else:
                print(False)
                request.login_checker = False
                request.username = ""

            user = request.user
            if log_checker:
                user_id = user.id
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM favorite_matches WHERE user_id = %s",   [user_id])
                    user_favorites = cursor.fetchall()
                    request.user_favorites = user_favorites
                    print(user_favorites)
            return self.get_response(request)