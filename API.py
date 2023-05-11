from flask import Flask, jsonify, render_template
from mysql import connector
from films import getFilms, get_fav_films, get_user_info
from gameCenter import getGames

# * Default flask project (don't change)
app = Flask(__name__)
app.secret_key = "secret_key"


# * Database connection details
connection = connector.connect(
    host= "localhost",
    port=3306,
    user= "root",
    password = "root",
    database="Project" #was "testingFlask", change if shit fucks up
)

# * Creating the cursor
cursor = connection.cursor()

# * Pages the user is gonna visit

@app.route("/", methods=['GET'])  # ENDPOINT / Accepting the methods ['GET'], ['POST', 'GET']
#@cross_origin(origin='*', headers=['Content-Type']) # * Needs to stay commented unless you have problems.. then you're fucked. GL
def home():
    result = getGames(connection,cursor)
    return jsonify(result)
    #return render_template("front.html") # * Renders the HTML page

# * API Pages -- User should usually not go on these sites

@app.route("/api/films", methods=['GET'])
def films():
    result = getFilms(connection, cursor)
    return jsonify(result) # * Returns the result is JSON, easier to work with

@app.route("/api/<user>/infos", methods=['GET'])
def user_infos(user):
    result = get_user_info(connection, cursor, user)
    return jsonify(result)

@app.route("/api/<user>/favourite_films", methods=['GET'])
def fav_film(user):
    result = get_fav_films(connection, cursor, user)
    return jsonify(result)


# * Si le port 5000 ne marche pas, lancer sur port 8000
#if __name__ == "__main__":
#    app.run(port=8000, debug=True)


# * Running the app
app.run(debug=True)


