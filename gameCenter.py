# Get all the games
def getGames(conn, curs):
    mysql_query = """
                SELECT * 
                FROM GAME
    """

    curs.execute(mysql_query)  # execution de la requete
    games = curs.fetchall()  # renvoie des resulats

    result = {} #TODO Change json data (vr yes or no)

    result["data"] = []  # creation de la clé et de la liste qui va contenur chaque film. Il faut creer cette liste, car il y a plusieurs films

    for game in games:
        dico = {}  # dictionnaire
        dico["id"] = game[0]
        dico["game_title"] = game[1]
        dico["user_rating"] = game[2]
        dico["copyright"] = game[3]

        result["data"].append(dico)

    return result