from mysql import connector
# * Database connection details
connection = connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="bd_proj"  # was "testingFlask", change if shit fucks up
)

# * sql query wrapper
def dbquery(q, action="select"):
        result = []
        with connection.cursor() as cursor:
                cursor.execute(q)
                if action != "select":
                        connection.commit() # either update or insert
                else:
                        rows = cursor.fetchall()
                        if rows:
                                for r in rows:
                                        result.append(r)
                                return result[0][0]

def getGames(gameid, option="", getall=False):
	if getall:
		query = f"SELECT {option} from Game"
	else:
		query = f"SELECT {option} FROM Game WHERE IdGame=\'{gameid}\'"
	return dbquery(query)

def getUsers(userid, option="", getall=False):
	if getall:
		query = f"SELECT {option} from User"
	else:
		query = f"SELECT {option} FROM User WHERE IdUser = \'{userid}\'"
	
	return dbquery(query)

def getUserid(email):
	return dbquery(f"SELECT IdUser FROM User WHERE email = \'{email}\'")[0]

def setSession(session, userid):
	session['userid'] = userid

def authenticate(session):
	if not session.get('userid'):
		return False
	return True

def error(message):
	return f"<script>alert(\'{message}\');window.location.assign(\'http://localhost:5000/\')</script>"
