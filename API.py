from flask import Flask, jsonify, render_template
from mysql import connector
from films import getFilms, get_fav_films, get_user_info

app = Flask(__name__)
app.secret_key = "secret_key"

connection = connector.connect(
    host= "localhost",
    port=3306,
    user= "root",
    password = "root",
    database="testingFlask" #C'est le nom du schema, changer plus tardddd
)

#creation du cursor
cursor = connection.cursor()


@app.route("/", methods=['GET'])  # endpoint / acceptant tant la méthode GET
#@cross_origin(origin='*', headers=['Content-Type'])
def home():
    return render_template("front.html") # Retourner le message en json. Le front s'attend en principe J du Json


@app.route("/api/films", methods=['GET'])
def films():
    result = getFilms(connection, cursor)
    return jsonify(result)

@app.route("/api/<user>/infos", methods=['GET'])
def user_infos(user):
    result = get_user_info(connection, cursor, user)
    return jsonify(result)

@app.route("/api/<user>/favourite_films", methods=['GET'])
def fav_film(user):
    result = get_fav_films(connection, cursor, user)
    return jsonify(result)


#Si le port 5000 ne marche pas, lancer sur port 8000

#if __name__ == "__main__":
#    app.run(port=8000, debug=True)

app.run(debug=True)  # lanncement du serveur Flask


