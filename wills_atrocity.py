#!/usr/bin/env python3


from flask import Flask, render_template, request, redirect, url_for, session
from mysql.connector import connect, Error
import time

app = Flask(__name__, template_folder='./')

# mysql connection config
mysql_user = 'root'
mysql_passwd = ''
mysql_db = 'bd_proj'

# mysql connection wrapper, assuming select query by default

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
				return result[0]

def getBalance(userid):
	query = f"SELECT balance FROM User WHERE IdUser = {userid}"
	balance = dbquery(query)[0]
	return balance

def getmaxid(table):
	query = f"SELECT MAX(Id{table}) FROM {table}"
	return dbquery(query)[0]

def createSession(gameid):
	query = f"SELECT COUNT(IdSession) from Session where IdGame = {gameid}"
	session_count = dbquery(query)[0]
	session_id = getmaxid('Session')[0]	

	if session_count != 0:
		return dbquery(f'select IdSession from Session where IdGame = {gameid}')[0] # if session already exists, return the corresponding sessionid
	
	if not getmaxid('Session'): # if no session is present, start with sessid = 1
		sessionid = 1
	else:
		sessionid += 1
	
	query = f"INSERT INTO Session (Session.IdSession, Session.IdRoom, Session.IdGame, Session.date) VALUES ({sessionid}, {roomid}, {gameid}, )"	

@app.route('/')
def index():
	if not session.get('userid'):
		return render_template('login.html')
	username = session.get('name')
	userid = session.get('userid')
	
	return f"""<h1>Welcome, {username}</h1>
		 <p>Your current balance: {getBalance(userid)} CHF</p>
		 <form action = "http://localhost:5000/addBalance" method = "GET">
		 	<p>Add balance</p>
	         	<p><input type="text" name="amount"/></p>
		 	<p><input type="submit" value="submit"/></p>
		 </form>
		 <form action = "http://localhost:5000/logout" method = "GET">
			<p><input type="submit" value="Log out"/></p>
		 </form>
                """

@app.route('/login', methods=['POST', 'GET'])
def login():
	email = request.form.get('email')
	query = f"select name,IdUser FROM User WHERE email = \'{email}\'"
	result = dbquery(query)
	
	if not result:
		return f'<h1>User not found</h1>'
	
	userid = result[1]
	username = result[0]
	session['userid'] = userid # setting session
	session['name'] = username	

	return redirect('/')

@app.route('/logout')
def logout():
	session['userid'] = None
	return redirect('/')

@app.route('/signup.html')
def signupage():
	return render_template('./signup.html')
		
@app.route('/addUser', methods=['GET'])
def addUser():
	email = request.args['email']
	name = request.args['name']
	userid = getmaxid('User') 
	
	if dbquery(f'select count(email) from User where email = \'{email}\'')[0] > 0: # user cannot signup with already existing email
		err = f"User with {email} exists!"
		return f'<script>alert(\"{err}\");window.location.assign(\'http://localhost:5000/\')</script>'

	if not userid: # this means that there's no user in the db
		userid = 1
	else:
		userid += 1

	query = f'INSERT INTO User(User.IdUser, User.name, User.email, User.balance) VALUES({userid}, \'{name}\', \'{email}\', 0)'
	dbquery(query, "insert") # add new user into db

	return redirect('/')


@app.route('/addBalance', methods=['GET'])
def addBalance():
	if not session.get('userid'):
		return redirect('/')

	amount = int(request.args['amount'])
	userid = session.get('userid')

	if amount < 0:
		return f'<script>alert(\"Amount can\'t be negative!\");window.location.assign(\'http://localhost:5000/\')</script>'
	
	newbalance = amount + getBalance(userid)
	query = f'UPDATE User SET balance={newbalance} WHERE IdUser = {userid}' # update balance
	dbquery(query, "update")

	return redirect('/')

if __name__ == '__main__':
	try:
		connection = connect(host='localhost', user=mysql_user, password=mysql_passwd,database=mysql_db,)
	except Error as e:
		print(e)
	gamename = "Valorant"
	query = f"SELECT IdGame from Game where game_title = \'{gamename}\'"
	print(dbquery(query)[0])
	app.secret_key = 'base_donne_project'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run()
